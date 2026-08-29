"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { isApiError } from "@/shared/types/api-error";
import { askProductQuestion } from "@/shared/services/ask.service";

import type { AskRequest } from "@/features/assistant/types/ask.types";

export const assistantKeys = {
  all: ["assistant"] as const,
  ask: (question: string, productId: string) =>
    [...assistantKeys.all, "ask", question, productId] as const,
};

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
        retry: (failureCount, error) => {
          if (isApiError(error) && error.status >= 400 && error.status < 500) {
            return false;
          }

          return failureCount < 1;
        },
      });
    },
  });
}
