"use client";

import { Sun, Moon } from "lucide-react";

/**
 * The choice is written to localStorage and read back by the inline boot script in the
 * root layout, so it survives a reload without a flash of the wrong theme.
 */
export default function ThemeToggle() {
  function flip() {
    const root = document.documentElement;
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      localStorage.setItem("learn-theme", next);
    } catch {
      /* private mode: the theme just does not persist */
    }
  }

  return (
    <button className="theme" type="button" onClick={flip} aria-label="Switch theme">
      <Sun className="icon ico-light" size={15} strokeWidth={1.7} />
      <Moon className="icon ico-dark" size={15} strokeWidth={1.7} />
    </button>
  );
}
