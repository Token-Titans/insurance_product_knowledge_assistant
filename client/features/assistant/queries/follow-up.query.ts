"use client";

import { useMutation } from "@tanstack/react-query";

import { scheduleFollowUp } from "@/features/assistant/services/follow-up.service";
import { isApiError } from "@/shared/types/api-error";

import type { FollowUpRequest } from "@/features/assistant/types/follow-up.types";

function shouldRetryFollowUp(failureCount: number, error: unknown) {
  if (isApiError(error) && error.status >= 400 && error.status < 500) {
    return false;
  }

  return failureCount < 1;
}

export function useScheduleFollowUp() {
  return useMutation({
    mutationFn: (request: FollowUpRequest) => scheduleFollowUp(request),
    retry: shouldRetryFollowUp,
  });
}
