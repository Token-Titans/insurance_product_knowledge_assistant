import {
  followUpRequestSchema,
  followUpResponseSchema,
} from "@/features/assistant/schemas/follow-up.schema";
import { api } from "@/shared/lib/api";

import type {
  FollowUpRequest,
  FollowUpResponse,
} from "@/features/assistant/types/follow-up.types";

export async function scheduleFollowUp(
  payload: FollowUpRequest,
  signal?: AbortSignal,
): Promise<FollowUpResponse> {
  const body = followUpRequestSchema.parse(payload);
  const response = await api.post<unknown>("/assistant/follow-up", body, {
    signal,
  });

  return followUpResponseSchema.parse(response.data);
}
