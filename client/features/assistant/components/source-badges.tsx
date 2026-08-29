"use client";

import { useTranslation } from "react-i18next";

import { Badge } from "@/components/ui/badge";

import type { AskSource } from "@/features/assistant/types/ask.types";

interface SourceBadgesProps {
  source: AskSource;
}

export function hasSourceCitation(source: AskSource) {
  return Boolean(
    source.document.trim() ||
      source.section.trim() ||
      source.file.trim() ||
      source.page != null,
  );
}

export function SourceBadges({ source }: SourceBadgesProps) {
  const { t } = useTranslation("assistant");

  if (!hasSourceCitation(source)) {
    return null;
  }

  return (
    <div className="flex min-w-0 flex-1 flex-wrap gap-1.5">
      <span className="sr-only">{t("answered.sources")}</span>
      {source.document.trim() ? (
        <Badge
          variant="outline"
          className="h-auto max-w-full whitespace-normal py-1"
        >
          {source.document}
        </Badge>
      ) : null}
      {source.section.trim() ? (
        <Badge
          variant="secondary"
          className="h-auto max-w-full whitespace-normal py-1"
        >
          {source.section}
        </Badge>
      ) : null}
      {source.page != null ? (
        <Badge
          variant="secondary"
          className="h-auto max-w-full whitespace-normal py-1"
        >
          {t("answered.page", { page: source.page })}
        </Badge>
      ) : null}
    </div>
  );
}
