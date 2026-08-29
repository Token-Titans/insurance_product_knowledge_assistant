"use client";

import { FileSearch, Link2, ShieldCheck } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Skeleton } from "@/components/ui/skeleton";

const STEPS = [
  { key: "loading.step_sources", icon: ShieldCheck },
  { key: "loading.step_match", icon: FileSearch },
  { key: "loading.step_cite", icon: Link2 },
] as const;

export function RetrieveLoading() {
  const { t } = useTranslation("assistant");

  return (
    <section className="space-y-4 rounded-2xl bg-card p-6 ring-1 ring-border">
      <div>
        <p className="font-heading text-base font-medium">{t("loading.title")}</p>
        <div className="mt-4 h-1 overflow-hidden rounded-full bg-muted">
          <div className="h-full w-2/3 animate-pulse bg-horizon-band" />
        </div>
      </div>
      <ul className="space-y-3">
        {STEPS.map(({ key, icon: Icon }) => (
          <li key={key} className="flex items-center gap-3 text-sm">
            <Icon className="size-4 text-brand" />
            <span>{t(key)}</span>
          </li>
        ))}
      </ul>
      <div className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-2/3" />
      </div>
    </section>
  );
}
