"use client";

import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";

const LOCALES = ["en", "my"] as const;

export function LocaleSwitcher() {
  const { i18n, t } = useTranslation("common");

  return (
    <div className="flex items-center gap-1">
      {LOCALES.map((locale) => (
        <Button
          key={locale}
          type="button"
          size="xs"
          variant={i18n.language === locale ? "secondary" : "ghost"}
          onClick={() => {
            void i18n.changeLanguage(locale);
            window.localStorage.setItem("lng", locale);
            document.documentElement.lang = locale;
          }}
        >
          {t(`locale.${locale}`)}
        </Button>
      ))}
    </div>
  );
}
