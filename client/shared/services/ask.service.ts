import {
  askRequestSchema,
  askResponseSchema,
} from "@/features/assistant/schemas/ask.schema";
import { api } from "@/shared/lib/api";

import type {
  AskRequest,
  AskResponse,
} from "@/features/assistant/types/ask.types";

export async function askProductQuestion(
  payload: AskRequest,
  signal?: AbortSignal,
): Promise<AskResponse> {
  const body = askRequestSchema.parse(payload);
  const response = await api.post<unknown>("/assistant/ask", body, { signal });

  return askResponseSchema.parse(response.data);
}
