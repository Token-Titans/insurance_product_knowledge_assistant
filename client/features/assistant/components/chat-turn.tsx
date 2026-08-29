import { AnswerPanel } from "@/features/assistant/components/answer-panel";
import { AskErrorBanner } from "@/features/assistant/components/ask-error-banner";
import { RetrieveLoading } from "@/features/assistant/components/retrieve-loading";
import { UnavailableState } from "@/features/assistant/components/unavailable-state";

import type { ChatTurn } from "@/features/assistant/types/ask-screen.types";

interface ChatTurnItemProps {
  turn: ChatTurn;
}

export function ChatTurnItem({ turn }: ChatTurnItemProps) {
  return (
    <article id={`ask-turn-${turn.id}`} className="space-y-3">
      <div className="flex justify-end">
        <p className="max-w-md rounded-2xl bg-primary px-4 py-2 font-myanmar text-sm text-primary-foreground">
          {turn.question}
        </p>
      </div>
      {turn.status === "pending" ? <RetrieveLoading /> : null}
      {turn.status === "error" && turn.errorCode ? (
        <AskErrorBanner code={turn.errorCode} />
      ) : null}
      {turn.status === "answered" && turn.response ? (
        <AnswerPanel response={turn.response} />
      ) : null}
      {turn.status === "unavailable" ? (
        <UnavailableState message={turn.response?.answer} />
      ) : null}
    </article>
  );
}
