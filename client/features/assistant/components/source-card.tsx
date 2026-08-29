import { BookOpen } from "lucide-react";

import type { AskSource } from "@/features/assistant/types/ask.types";

interface SourceCardProps {
  source: AskSource;
}

export function SourceCard({ source }: SourceCardProps) {
  return (
    <article className="flex items-start gap-3 rounded-xl bg-secondary p-4 text-secondary-foreground">
      <BookOpen className="mt-0.5 size-4 text-brand" />
      <div>
        <p className="font-medium">{source.document}</p>
        <p className="font-mono text-xs text-muted-foreground">{source.section}</p>
      </div>
    </article>
  );
}
