"use client";

import { useTranslation } from "react-i18next";

import { AppShell } from "@/components/layouts/app-shell";
import { ConditionsBlock } from "@/features/assistant/components/conditions-block";
import { ImportantPoints } from "@/features/assistant/components/important-points";
import { SourceCard } from "@/features/assistant/components/source-card";

function EmptyCompareColumn({ title }: { title: string }) {
  const { t } = useTranslation("assistant");

  return (
    <section className="space-y-4 rounded-2xl bg-card p-5 ring-1 ring-border">
      <h2 className="font-heading text-lg font-medium">{title}</h2>
      <p className="text-sm text-muted-foreground">{t("compare.empty")}</p>
      <ImportantPoints points={[]} />
      <ConditionsBlock conditions={[]} />
      <SourceCard
        source={{
          document: t("compare.empty"),
          section: t("compare.empty"),
        }}
      />
    </section>
  );
}

export function CompareShell() {
  const { t } = useTranslation("assistant");

  return (
    <AppShell>
      <div className="mx-auto flex min-h-0 w-full max-w-6xl flex-1 flex-col gap-6 overflow-y-auto px-4 py-8 sm:px-6">
        <div>
          <h1 className="font-heading text-3xl font-medium">{t("compare.title")}</h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            {t("compare.body")}
          </p>
        </div>
        <div className="grid gap-4 lg:grid-cols-2">
          <EmptyCompareColumn title={t("compare.column_a")} />
          <EmptyCompareColumn title={t("compare.column_b")} />
        </div>
      </div>
    </AppShell>
  );
}
