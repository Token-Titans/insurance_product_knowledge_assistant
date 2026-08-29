"use client";

import { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";

import { AppShell } from "@/components/layouts/app-shell";
import { AskComposer } from "@/features/assistant/components/ask-composer";
import { ChatTurnItem } from "@/features/assistant/components/chat-turn";
import { ConversationHistory } from "@/features/assistant/components/conversation-history";
import { useAskScreen } from "@/features/assistant/hooks/use-ask-screen";

export function AskScreen() {
  const { t } = useTranslation("assistant");
  const { turns, isPending, isEmpty, submitAsk } = useAskScreen();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [turns]);

  function scrollToTurn(id: string) {
    document.getElementById(`ask-turn-${id}`)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }

  return (
    <AppShell
      historyAction={
        <ConversationHistory items={turns} onSelect={scrollToTurn} />
      }
    >
      {isEmpty ? (
        <div className="mx-auto flex min-h-0 w-full max-w-3xl flex-1 flex-col overflow-y-auto px-4 py-8 sm:px-6">
          <div className="flex flex-1 flex-col justify-center gap-8">
            <div className="space-y-2 text-center">
              <h1 className="font-heading text-3xl font-medium">
                {t("ask.greeting")}
              </h1>
              <p className="text-sm text-muted-foreground">{t("ask.subtitle")}</p>
            </div>
            <AskComposer
              isPending={isPending}
              showSuggestions
              onSubmitAsk={submitAsk}
            />
          </div>
        </div>
      ) : (
        <div className="mx-auto flex min-h-0 w-full max-w-3xl flex-1 flex-col">
          <div
            className="min-h-0 flex-1 overflow-y-auto px-4 py-6 sm:px-6"
            role="log"
            aria-label={t("ask.thread_label")}
            aria-live="polite"
          >
            <div className="space-y-8">
              {turns.map((turn) => (
                <ChatTurnItem key={turn.id} turn={turn} />
              ))}
              <div ref={bottomRef} />
            </div>
          </div>
          <div className="shrink-0 border-t border-border bg-background/80 px-4 py-4 sm:px-6">
            <AskComposer
              isPending={isPending}
              showSuggestions={false}
              onSubmitAsk={submitAsk}
            />
          </div>
        </div>
      )}
    </AppShell>
  );
}
