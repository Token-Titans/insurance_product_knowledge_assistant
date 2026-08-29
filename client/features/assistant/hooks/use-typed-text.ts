"use client";

import { useEffect, useState } from "react";

function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(() =>
    typeof window !== "undefined"
      ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
      : false,
  );

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(media.matches);

    function onChange() {
      setPrefersReducedMotion(media.matches);
    }

    media.addEventListener("change", onChange);

    return () => media.removeEventListener("change", onChange);
  }, []);

  return prefersReducedMotion;
}

export function useTypedText(content: string, enabled: boolean) {
  const prefersReducedMotion = usePrefersReducedMotion();
  const shouldType = enabled && !prefersReducedMotion && content.length > 0;
  const [count, setCount] = useState(shouldType ? 0 : content.length);

  useEffect(() => {
    if (!shouldType) {
      setCount(content.length);
      return;
    }

    setCount(0);
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
    shown: content.slice(0, count),
    isTyping: shouldType && count < content.length,
  };
}
