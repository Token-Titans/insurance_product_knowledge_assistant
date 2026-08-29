"use client";

import Link from "next/link";
import { useTranslation } from "react-i18next";

import { LocaleSwitcher } from "@/components/core/locale-switcher";
import { Button } from "@/components/ui/button";

import type { ReactNode } from "react";

interface AppHeaderProps {
  historyAction?: ReactNode;
}

export function AppHeader({ historyAction }: AppHeaderProps) {
  const { t } = useTranslation("common");

  return (
    <header className="relative overflow-hidden bg-horizon-band text-primary-foreground">
      <div
        aria-hidden
        className="absolute inset-y-0 right-0 w-2/5 origin-top-right -skew-x-16 bg-horizon/25"
      />
      <div className="relative flex items-center justify-between gap-4 px-4 py-4 sm:px-6">
        <div>
          <p className="font-heading text-sm font-medium">{t("app.name")}</p>
          <p className="text-xs text-horizon">{t("app.tagline")}</p>
        </div>
        <div className="flex items-center gap-2">
          <Button asChild size="sm" variant="secondary">
            <Link href="/">{t("app.ask")}</Link>
          </Button>
          <Button
            asChild
            size="sm"
            variant="secondary"
            className="bg-primary-foreground/10 text-primary-foreground hover:bg-primary-foreground/20"
          >
            <Link href="/compare">{t("app.compare")}</Link>
          </Button>
          {historyAction}
          <LocaleSwitcher />
        </div>
      </div>
    </header>
  );
}
