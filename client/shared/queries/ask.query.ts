"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { compareRequestSchema } from "@/features/assistant/schemas/ask.schema";
import { isApiError, isCanceledError } from "@/shared/types/api-error";
import {
  askProductQuestion,
  compareProducts,
} from "@/shared/services/ask.service";

import type {
  AskRequest,
  AskResponse,
  CompareRequest,
} from "@/features/assistant/types/ask.types";

export const assistantKeys = {
  all: ["assistant"] as const,
  ask: (question: string, productId: string) =>
    [...assistantKeys.all, "ask", question, productId] as const,
};

function shouldRetryAsk(failureCount: number, error: unknown) {
  if (isApiError(error) && error.status >= 400 && error.status < 500) {
    return false;
  }

  return failureCount < 1;
}

export function useAskProductQuestion() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: assistantKeys.all,
    mutationFn: async (request: AskRequest) => {
      const queryKey = assistantKeys.ask(request.question, request.product_id);

      await queryClient.cancelQueries({ queryKey: assistantKeys.all });

      return queryClient.fetchQuery({
        queryKey,
        queryFn: ({ signal }) => askProductQuestion(request, signal),
        staleTime: 2 * 60_000,
        gcTime: 10 * 60_000,
        retry: shouldRetryAsk,
      });
    },
  });
}

export function useCompareProducts() {
  return useMutation({
    mutationKey: [...assistantKeys.all, "compare"],
    mutationFn: async (request: CompareRequest) => {
      const body = compareRequestSchema.parse(request);

      try {
        const data = await compareProducts(body);

        return {
          left: { status: "fulfilled" as const, value: data.left },
          right: { status: "fulfilled" as const, value: data.right },
        };
      } catch (error) {
        if (isCanceledError(error)) {
          throw error;
        }

        const rejected = {
          status: "rejected" as const,
          reason: error,
        };

        return {
          left: rejected,
          right: rejected,
        } as {
          left: PromiseSettledResult<AskResponse>;
          right: PromiseSettledResult<AskResponse>;
        };
      }
    },
  });
}
