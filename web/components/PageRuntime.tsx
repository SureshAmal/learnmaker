"use client";

import { useEffect } from "react";

/**
 * Everything the rendered article needs once it is in a browser:
 *
 *   - Mermaid diagrams, drawn from the <pre class="mermaid"> text the server left alone,
 *     and redrawn when the theme flips (Mermaid bakes its palette into the SVG).
 *   - A full-screen viewer for any figure — diagram, hand-drawn SVG or slide image.
 *   - Copy buttons on code blocks.
 *
 * Math is already static KaTeX HTML from the server, so nothing here touches it.
 */
export default function PageRuntime({ hasDiagrams }: { hasDiagrams: boolean }) {
  useEffect(() => {
    let cancelled = false;

    // ---- full-screen figure viewer -------------------------------------------------
    // An image is COPIED into the overlay: a copy is indistinguishable from the original
    // and the page keeps its picture no matter what happens to the overlay. Moving the
    // real node, as this used to, meant any interruption before the close handler ran
    // left the article with an empty figure.
    //
    // A Mermaid diagram still has to be moved, because Mermaid scopes its CSS and its
    // arrowhead markers to the svg's own id and a clone loses every fill and marker.
    let held: { node: Element; home: Element; css: string } | null = null;

    function closeFig() {
      const box = document.querySelector<HTMLElement>(".figbox");
      if (!box) return;
      if (held) {
        held.node.setAttribute("style", held.css);
        held.home.appendChild(held.node);
        held = null;
      }
      box.querySelector(".figbox-stage")?.replaceChildren();
      box.hidden = true;
      document.documentElement.classList.remove("figbox-open");
    }

    function lightbox() {
      let box = document.querySelector<HTMLElement>(".figbox");
      if (box) return box;
      box = document.createElement("div");
      box.className = "figbox";
      box.hidden = true;
      box.innerHTML =
        '<button class="figbox-exit" type="button">Exit</button><div class="figbox-stage"></div>';
      box.addEventListener("click", (e) => {
        const t = e.target as HTMLElement;
        if (t === box || t.closest(".figbox-exit")) closeFig();
      });
      document.body.appendChild(box);
      return box;
    }

    function openFig(host: Element) {
      const original = host.querySelector("svg, img");
      if (!original || held) return;
      const box = lightbox();
      const stage = box.querySelector(".figbox-stage")!;

      let node: Element;
      if (original.tagName.toLowerCase() === "img") {
        node = original.cloneNode(true) as Element;
        node.removeAttribute("style");
      } else {
        node = original;
        held = { node, home: host, css: node.getAttribute("style") ?? "" };
      }
      stage.replaceChildren(node);
      box.hidden = false;
      document.documentElement.classList.add("figbox-open");

      // One fit-scale so the whole figure sits inside the stage: no scrollbars, no panning.
      const el = node as HTMLElement;
      el.style.maxWidth = "none";
      el.style.maxHeight = "none";
      el.style.width = "auto";
      el.style.height = "auto";
      const figure = el.getBoundingClientRect();
      const room = stage.getBoundingClientRect();
      if (figure.width && figure.height) {
        const k = Math.min(room.width / figure.width, room.height / figure.height, 2.4);
        el.style.transformOrigin = "center center";
        el.style.transform = `scale(${k.toFixed(4)})`;
      }
    }

    function onEsc(e: KeyboardEvent) {
      if (e.key === "Escape") closeFig();
    }
    document.addEventListener("keydown", onEsc);

    function zoomable(root: ParentNode) {
      root
        .querySelectorAll<HTMLElement>(".figsvg:not([data-zoom]),.figimg:not([data-zoom])")
        .forEach((f) => {
          f.dataset.zoom = "1";
          f.addEventListener("click", () => openFig(f));
        });
    }

    // ---- copy buttons ----------------------------------------------------------------
    function onCopyClick(e: MouseEvent) {
      const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(".copy");
      if (!btn) return;
      navigator.clipboard.writeText(btn.dataset.code ?? "").then(() => {
        btn.classList.add("done");
        setTimeout(() => btn.classList.remove("done"), 1400);
      });
    }
    document.addEventListener("click", onCopyClick);

    // ---- diagrams ---------------------------------------------------------------------
    let redrawObserver: MutationObserver | null = null;

    if (hasDiagrams) {
      (async () => {
        const mermaid = (await import("mermaid")).default;
        if (cancelled) return;

        const dark = () => document.documentElement.getAttribute("data-theme") === "dark";
        // Mermaid's own light/dark themes, unmodified — they are known-good, and hand
        // overriding the palette only ever produced black-on-black.
        const config = () => ({
          startOnLoad: false,
          theme: (dark() ? "dark" : "neutral") as "dark" | "neutral",
          securityLevel: "loose" as const,
          flowchart: { curve: "basis" as const, useMaxWidth: true },
        });
        mermaid.initialize(config());

        async function draw() {
          const nodes = [
            ...document.querySelectorAll<HTMLElement>("pre.mermaid:not([data-done])"),
          ];
          nodes.forEach((n) => {
            if (!n.dataset.src) n.dataset.src = n.textContent ?? "";
          });
          if (!nodes.length) return;
          try {
            await mermaid.run({ nodes });
          } catch {
            /* a malformed diagram stays as its own source text, which is the useful fallback */
          }
          nodes.forEach((n) => {
            n.dataset.done = "1";
            n.title = "Click to view full screen";
            if (!n.dataset.zoom) {
              n.dataset.zoom = "1";
              n.addEventListener("click", () => openFig(n));
            }
          });
        }

        await draw();
        zoomable(document);

        // A theme switch means every diagram has to be drawn again from its source.
        redrawObserver = new MutationObserver(() => {
          closeFig();
          mermaid.initialize(config());
          document.querySelectorAll<HTMLElement>("pre.mermaid[data-done]").forEach((n) => {
            n.removeAttribute("data-done");
            n.removeAttribute("data-processed");
            n.innerHTML = "";
            n.textContent = n.dataset.src ?? "";
          });
          draw();
        });
        redrawObserver.observe(document.documentElement, {
          attributes: true,
          attributeFilter: ["data-theme"],
        });
      })();
    } else {
      zoomable(document);
    }

    return () => {
      cancelled = true;
      document.removeEventListener("keydown", onEsc);
      document.removeEventListener("click", onCopyClick);
      redrawObserver?.disconnect();
      closeFig();
    };
  }, [hasDiagrams]);

  return null;
}
