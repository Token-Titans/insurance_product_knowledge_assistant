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
  const parsed = askRequestSchema.parse(payload);
  const body =
    parsed.product_ids && parsed.product_ids.length > 0
      ? parsed
      : { question: parsed.question };

  const response = await api.post<unknown>("/assistant/ask", body, { signal });

  return askResponseSchema.parse(response.data);
}
