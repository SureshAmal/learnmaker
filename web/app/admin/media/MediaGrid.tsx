"use client";

import { useEffect, useState } from "react";
import { Trash2, X } from "lucide-react";
import { deleteAsset } from "../actions";

export type Asset = {
  id: number;
  url: string;
  pathname: string;
  size: number;
  tag: string;
};

/**
 * The library is for looking and for housekeeping. Images are put into a page from the
 * editor itself — dropped onto it, or picked with the image block — so there is nothing
 * here to copy and paste: clicking a thumbnail opens it full size instead.
 */
export default function MediaGrid({ assets }: { assets: Asset[] }) {
  const [open, setOpen] = useState<Asset | null>(null);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(null);
    }
    document.addEventListener("keydown", onKey);
    document.documentElement.classList.add("figbox-open");
    return () => {
      document.removeEventListener("keydown", onKey);
      document.documentElement.classList.remove("figbox-open");
    };
  }, [open]);

  return (
    <>
      <div className="grid-media">
        {assets.map((asset) => (
          <figure className="media-card" key={asset.id}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={asset.url}
              alt={asset.pathname}
              loading="lazy"
              onClick={() => setOpen(asset)}
              title="Click to view full size"
            />
            <figcaption className="name">{asset.pathname}</figcaption>
            <div className="media-actions">
              <span className="media-size">{Math.round(asset.size / 1024)} KB</span>
              <form action={deleteAsset}>
                <input type="hidden" name="id" value={asset.id} />
                <button className="btn danger" type="submit" aria-label="Delete image">
                  <Trash2 size={12} strokeWidth={1.7} />
                </button>
              </form>
            </div>
          </figure>
        ))}
      </div>

      {open ? (
        <div className="figbox" onClick={() => setOpen(null)}>
          <button className="figbox-exit" type="button" onClick={() => setOpen(null)}>
            <X size={13} strokeWidth={2} /> Close
          </button>
          <div className="figbox-stage" onClick={(e) => e.stopPropagation()}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={open.url} alt={open.pathname} />
          </div>
        </div>
      ) : null}
    </>
  );
}
