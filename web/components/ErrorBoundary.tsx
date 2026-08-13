"use client";

import { Component, type ReactNode } from "react";

/**
 * A crash in the visual editor must never cost an author their page. Anything it throws
 * while rendering is caught here and reported to the parent, which drops back to the raw
 * Markdown pane — the text itself is held in the parent's state, so nothing is lost.
 */
export default class ErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode; onError?: (error: Error) => void },
  { failed: boolean }
> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error: Error) {
    this.props.onError?.(error);
  }

  render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}
