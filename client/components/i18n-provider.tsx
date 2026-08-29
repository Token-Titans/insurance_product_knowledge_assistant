"use client";

import { useEffect } from "react";
import { I18nextProvider } from "react-i18next";

import { i18n } from "@/shared/lib/i18n";

import type { ReactNode } from "react";

interface I18nProviderProps {
  children: ReactNode;
}

export function I18nProvider({ children }: I18nProviderProps) {
  useEffect(() => {
    const storedLanguage = window.localStorage.getItem("lng");

    if (storedLanguage === "en" || storedLanguage === "my") {
      void i18n.changeLanguage(storedLanguage);
      document.documentElement.lang = storedLanguage;
      return;
    }

    document.documentElement.lang = "my";
  }, []);

  return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>;
}
