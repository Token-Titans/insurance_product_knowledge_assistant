"use client";

import { useTranslation } from "react-i18next";

import { AppShell } from "@/components/layouts/app-shell";
import { AnswerPanel } from "@/features/assistant/components/answer-panel";
import { AskComposer } from "@/features/assistant/components/ask-composer";
import { AskErrorBanner } from "@/features/assistant/components/ask-error-banner";
import { AskPendingBar } from "@/features/assistant/components/ask-pending-bar";
import { ConversationHistory } from "@/features/assistant/components/conversation-history";
import { RetrieveLoading } from "@/features/assistant/components/retrieve-loading";
import { UnavailableState } from "@/features/assistant/components/unavailable-state";
import { useAskScreen } from "@/features/assistant/hooks/use-ask-screen";

export function AskScreen() {
  const { t } = useTranslation("assistant");
  const {
    viewState,
    result,
    history,
    errorCode,
    isPending,
    isLoading,
    submitAsk,
    restoreHistoryItem,
  } = useAskScreen();

  const isIdle = viewState === "idle" && !isPending;

  return (
    <AppShell
      historyAction={
        <ConversationHistory items={history} onSelect={restoreHistoryItem} />
      }
    >
      <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col gap-8 px-4 py-8 sm:px-6">
        {isIdle ? (
          <div className="flex flex-1 flex-col justify-center gap-8">
            <div className="space-y-2 text-center">
              <h1 className="font-heading text-3xl font-medium">
                {t("ask.greeting")}
              </h1>
              <p className="text-sm text-muted-foreground">{t("ask.subtitle")}</p>
            </div>
            {errorCode ? <AskErrorBanner code={errorCode} /> : null}
            <AskComposer
              isPending={isPending}
              showSuggestions
              onSubmitAsk={submitAsk}
            />
          </div>
        ) : (
          <>
            <div className="flex-1 space-y-6">
              {isLoading || viewState === "loading" ? <RetrieveLoading /> : null}
              <AskPendingBar isVisible={viewState === "pending"} />
              {errorCode ? <AskErrorBanner code={errorCode} /> : null}
              {(viewState === "answered" || viewState === "pending") &&
              result?.response?.confidence === "grounded" ? (
                <AnswerPanel
                  question={result.question}
                  response={result.response}
                />
              ) : null}
              {(viewState === "unavailable" || viewState === "pending") &&
              result?.outcome === "unavailable" ? (
                <UnavailableState
                  question={result.question}
                  message={result.response?.answer}
                />
              ) : null}
            </div>
            <AskComposer
              isPending={isPending}
              showSuggestions={false}
              onSubmitAsk={submitAsk}
            />
          </>
        )}
      </div>
    </AppShell>
  );
}
