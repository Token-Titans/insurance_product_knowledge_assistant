"use client";

import { useState } from "react";

import { useAskProductQuestion } from "@/shared/queries/ask.query";
import { isApiError, isCanceledError } from "@/shared/types/api-error";

import type { AskRequest, AskResponse } from "@/features/assistant/types/ask.types";
import type {
  AskHistoryItem,
  AskOutcome,
  AskScreenResult,
  AskViewState,
} from "@/features/assistant/types/ask-screen.types";

function createHistoryId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

function outcomeFromResponse(response: AskResponse): AskOutcome {
  return response.confidence === "grounded" ? "answered" : "unavailable";
}

export function useAskScreen() {
  const askMutation = useAskProductQuestion();
  const [viewState, setViewState] = useState<AskViewState>("idle");
  const [result, setResult] = useState<AskScreenResult | null>(null);
  const [history, setHistory] = useState<AskHistoryItem[]>([]);
  const [errorCode, setErrorCode] = useState<string | null>(null);

  const isPending = askMutation.isPending;
  const isLoading = isPending && result === null;

  async function submitAsk(request: AskRequest) {
    const productIds = request.product_ids ?? [];
    const isRepeat =
      result !== null &&
      result.question === request.question &&
      result.productIds.join() === productIds.join();

    setErrorCode(null);
    setViewState(isRepeat ? "pending" : "loading");

    if (!isRepeat) {
      setResult(null);
    }

    try {
      const response = await askMutation.mutateAsync(request);
      const outcome = outcomeFromResponse(response);
      const nextResult: AskScreenResult = {
        question: request.question,
        productIds,
        outcome,
        response,
      };

      setResult(nextResult);
      setViewState(outcome);
      setHistory((items) => [
        {
          id: createHistoryId(),
          question: request.question,
          productIds,
          outcome,
          response,
        },
        ...items,
      ]);
    } catch (error) {
      if (isCanceledError(error)) {
        return;
      }

      setErrorCode(isApiError(error) ? error.code : "HTTP_ERROR");
      setViewState(isRepeat && result ? result.outcome : "idle");
    }
  }

  function restoreHistoryItem(item: AskHistoryItem) {
    askMutation.reset();
    setErrorCode(null);
    setResult({
      question: item.question,
      productIds: item.productIds,
      outcome: item.outcome,
      response: item.response,
    });
    setViewState(item.outcome);
  }

  return {
    viewState,
    result,
    history,
    errorCode,
    isPending,
    isLoading,
    submitAsk,
    restoreHistoryItem,
  };
}
