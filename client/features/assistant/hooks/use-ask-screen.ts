"use client";

import { useState } from "react";

import { isGroundedResponse } from "@/features/assistant/schemas/ask.schema";
import {
  useAskProductQuestion,
  useCompareProducts,
} from "@/shared/queries/ask.query";
import { isApiError, isCanceledError } from "@/shared/types/api-error";

import type {
  AskRequest,
  AskResponse,
  CompareRequest,
} from "@/features/assistant/types/ask.types";
import type {
  ChatTurn,
  ChatTurnStatus,
  CompareColumnState,
} from "@/features/assistant/types/ask-screen.types";

function createTurnId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

function statusFromResponse(response: AskResponse): ChatTurnStatus {
  return isGroundedResponse(response.confidence) ? "answered" : "unavailable";
}

function columnFromSettled(
  productId: string,
  result: PromiseSettledResult<AskResponse>,
): CompareColumnState {
  if (result.status === "fulfilled") {
    return {
      productId,
      status: statusFromResponse(result.value),
      response: result.value,
      errorCode: null,
    };
  }

  return {
    productId,
    status: "error",
    response: null,
    errorCode: isApiError(result.reason) ? result.reason.code : "HTTP_ERROR",
  };
}

function compareStatus(
  left: CompareColumnState,
  right: CompareColumnState,
): ChatTurnStatus {
  if (left.status === "error" && right.status === "error") {
    return "error";
  }

  if (left.status === "answered" || right.status === "answered") {
    return "answered";
  }

  return "unavailable";
}

export function useAskScreen() {
  const askMutation = useAskProductQuestion();
  const compareMutation = useCompareProducts();
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [isCompare, setIsCompare] = useState(false);

  const isPending = askMutation.isPending || compareMutation.isPending;
  const isEmpty = turns.length === 0;

  async function submitAsk(request: AskRequest) {
    const id = createTurnId();

    setTurns((items) => [
      ...items,
      {
        id,
        kind: "ask",
        question: request.question,
        productId: request.product_id,
        status: "pending",
        response: null,
        errorCode: null,
        shouldType: false,
      },
    ]);

    try {
      const response = await askMutation.mutateAsync(request);

      setTurns((items) =>
        items.map((item) =>
          item.id === id && item.kind === "ask"
            ? {
                ...item,
                status: statusFromResponse(response),
                response,
                errorCode: null,
                shouldType: true,
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
          item.id === id && item.kind === "ask"
            ? {
                ...item,
                status: "error",
                errorCode: isApiError(error) ? error.code : "HTTP_ERROR",
                shouldType: false,
              }
            : item,
        ),
      );
    }
  }

  async function submitCompare(request: CompareRequest) {
    const id = createTurnId();
    const pendingColumn = (productId: string): CompareColumnState => ({
      productId,
      status: "pending",
      response: null,
      errorCode: null,
    });

    setTurns((items) => [
      ...items,
      {
        id,
        kind: "compare",
        question: request.question,
        status: "pending",
        shouldType: false,
        left: pendingColumn(request.left_product_id),
        right: pendingColumn(request.right_product_id),
      },
    ]);

    try {
      const result = await compareMutation.mutateAsync(request);
      const left = columnFromSettled(request.left_product_id, result.left);
      const right = columnFromSettled(request.right_product_id, result.right);

      if (
        result.left.status === "rejected" &&
        result.right.status === "rejected" &&
        isCanceledError(result.left.reason) &&
        isCanceledError(result.right.reason)
      ) {
        setTurns((items) => items.filter((item) => item.id !== id));
        return;
      }

      setTurns((items) =>
        items.map((item) =>
          item.id === id && item.kind === "compare"
            ? {
                ...item,
                status: compareStatus(left, right),
                left,
                right,
              }
            : item,
        ),
      );
    } catch (error) {
      if (isCanceledError(error)) {
        setTurns((items) => items.filter((item) => item.id !== id));
        return;
      }

      const errorCode = isApiError(error) ? error.code : "HTTP_ERROR";

      setTurns((items) =>
        items.map((item) =>
          item.id === id && item.kind === "compare"
            ? {
                ...item,
                status: "error",
                left: { ...item.left, status: "error", errorCode },
                right: { ...item.right, status: "error", errorCode },
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
    isCompare,
    setIsCompare,
    submitAsk,
    submitCompare,
  };
}
