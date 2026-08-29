"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { compareRequestSchema } from "@/features/assistant/schemas/ask.schema";
import { isApiError } from "@/shared/types/api-error";
import { askProductQuestion } from "@/shared/services/ask.service";

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
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: [...assistantKeys.all, "compare"],
    mutationFn: async (request: CompareRequest) => {
      const body = compareRequestSchema.parse(request);

      const run = (productId: string) =>
        queryClient.fetchQuery({
          queryKey: assistantKeys.ask(body.question, productId),
          queryFn: ({ signal }) =>
            askProductQuestion(
              { product_id: productId, question: body.question },
              signal,
            ),
          staleTime: 2 * 60_000,
          gcTime: 10 * 60_000,
          retry: shouldRetryAsk,
        });

      const [left, right] = await Promise.allSettled([
        run(body.left_product_id),
        run(body.right_product_id),
      ]);

      return { left, right } as {
        left: PromiseSettledResult<AskResponse>;
        right: PromiseSettledResult<AskResponse>;
      };
    },
  });
}
