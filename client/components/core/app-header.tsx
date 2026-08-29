"use client";

import Link from "next/link";
import { useTranslation } from "react-i18next";

import { BrandMark } from "@/components/core/brand-mark";
import { HeaderNavLink } from "@/components/core/header-nav-link";
import { LocaleSwitcher } from "@/components/core/locale-switcher";

import type { ReactNode } from "react";

interface AppHeaderProps {
  historyAction?: ReactNode;
}

export function AppHeader({ historyAction }: AppHeaderProps) {
  const { t } = useTranslation("common");

  return (
    <header className="sticky top-0 z-40 overflow-hidden bg-horizon-band text-primary-foreground shadow-sm">
      <div
        aria-hidden
        className="absolute inset-y-0 right-0 w-1/3 origin-top-right -skew-x-16 bg-primary-foreground/10"
      />
      <div
        aria-hidden
        className="absolute inset-x-0 bottom-0 h-px bg-primary-foreground/15"
      />
      <div className="relative mx-auto flex h-16 max-w-6xl items-center justify-between gap-3 px-4 sm:px-6">
        <Link href="/" className="flex min-w-0 items-center gap-3">
          <BrandMark className="size-9 shrink-0" />
          <span className="min-w-0">
            <span className="block font-heading text-sm font-semibold tracking-tight">
              {t("app.name")}
            </span>
            <span className="hidden text-xs text-horizon sm:block">
              {t("app.tagline")}
            </span>
          </span>
        </Link>
        <div className="flex items-center gap-1 sm:gap-2">
          <nav
            aria-label={t("app.nav_label")}
            className="flex items-center md:absolute md:left-1/2 md:-translate-x-1/2"
          >
            <HeaderNavLink href="/">{t("app.ask")}</HeaderNavLink>
            <HeaderNavLink href="/compare">{t("app.compare")}</HeaderNavLink>
          </nav>
          {historyAction}
          <LocaleSwitcher />
        </div>
      </div>
    </header>
  );
}
