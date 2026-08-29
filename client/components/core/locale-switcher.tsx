"use client";

import { useTranslation } from "react-i18next";

import { cn } from "@/lib/utils";

const LOCALES = ["en", "my"] as const;

export function LocaleSwitcher() {
  const { i18n, t } = useTranslation("common");
  const activeLanguage = i18n.language.startsWith("my") ? "my" : "en";

  return (
    <div
      role="group"
      aria-label={t("locale.label")}
      className="flex rounded-full bg-primary-foreground/10 p-0.5 ring-1 ring-primary-foreground/15"
    >
      {LOCALES.map((locale) => {
        const isActive = activeLanguage === locale;

        return (
          <button
            key={locale}
            type="button"
            aria-pressed={isActive}
            className={cn(
              "h-7 min-w-8 rounded-full px-2 text-xs font-medium transition-colors",
              isActive
                ? "bg-horizon text-indigo"
                : "text-primary-foreground/75 hover:text-primary-foreground",
            )}
            onClick={() => {
              void i18n.changeLanguage(locale);
              window.localStorage.setItem("lng", locale);
              document.documentElement.lang = locale;
            }}
          >
            {t(`locale.${locale}`)}
          </button>
        );
      })}
    </div>
  );
}
