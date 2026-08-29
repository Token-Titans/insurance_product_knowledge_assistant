"use client";

import { useState } from "react";

import { useAskProductQuestion } from "@/shared/queries/ask.query";
import { isApiError, isCanceledError } from "@/shared/types/api-error";

import type { AskRequest, AskResponse } from "@/features/assistant/types/ask.types";
import type { ChatTurn } from "@/features/assistant/types/ask-screen.types";

function createTurnId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

function statusFromResponse(response: AskResponse): ChatTurn["status"] {
  return response.confidence === "grounded" ? "answered" : "unavailable";
}

export function useAskScreen() {
  const askMutation = useAskProductQuestion();
  const [turns, setTurns] = useState<ChatTurn[]>([]);

  const isPending = askMutation.isPending;
  const isEmpty = turns.length === 0;

  async function submitAsk(request: AskRequest) {
    const id = createTurnId();

    setTurns((items) => [
      ...items,
      {
        id,
        question: request.question,
        productId: request.product_id,
        status: "pending",
        response: null,
        errorCode: null,
      },
    ]);

    try {
      const response = await askMutation.mutateAsync(request);

      setTurns((items) =>
        items.map((item) =>
          item.id === id
            ? {
                ...item,
                status: statusFromResponse(response),
                response,
                errorCode: null,
              }
            : item,
        ),
      );
    } catch (error) {
      if (isCanceledError(error)) {
        setTurns((items) => items.filter((item) => item.id !== id));
        return;
      }

      setTurns((items) =>
        items.map((item) =>
          item.id === id
            ? {
                ...item,
                status: "error",
                errorCode: isApiError(error) ? error.code : "HTTP_ERROR",
              }
            : item,
        ),
      );
    }
  }

  return {
    turns,
    isPending,
    isEmpty,
    submitAsk,
  };
}
