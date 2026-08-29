"use client";

import { useEffect, useState, useSyncExternalStore } from "react";

function subscribeReducedMotion(onStoreChange: () => void) {
  const media = window.matchMedia("(prefers-reduced-motion: reduce)");
  media.addEventListener("change", onStoreChange);

  return () => media.removeEventListener("change", onStoreChange);
}

function getReducedMotionSnapshot() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function getReducedMotionServerSnapshot() {
  return false;
}

function usePrefersReducedMotion() {
  return useSyncExternalStore(
    subscribeReducedMotion,
    getReducedMotionSnapshot,
    getReducedMotionServerSnapshot,
  );
}

export function useTypedText(content: string, enabled: boolean) {
  const prefersReducedMotion = usePrefersReducedMotion();
  const shouldType = enabled && !prefersReducedMotion && content.length > 0;
  const [count, setCount] = useState(0);
  const [typedContent, setTypedContent] = useState(content);

  if (content !== typedContent) {
    setTypedContent(content);
    setCount(0);
  }

  useEffect(() => {
    if (!shouldType) {
      return;
    }

    let index = 0;
    const step = Math.max(2, Math.ceil(content.length / 72));
    const timer = window.setInterval(() => {
      index = Math.min(content.length, index + step);
      setCount(index);

      if (index >= content.length) {
        window.clearInterval(timer);
      }
    }, 20);

    return () => window.clearInterval(timer);
  }, [content, shouldType]);

  return {
    shown: shouldType ? content.slice(0, count) : content,
    isTyping: shouldType && count < content.length,
  };
}
