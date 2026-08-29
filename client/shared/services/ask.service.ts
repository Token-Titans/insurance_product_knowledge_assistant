import {
  askRequestSchema,
  askResponseSchema,
  compareRequestSchema,
  compareResponseSchema,
} from "@/features/assistant/schemas/ask.schema";
import { api } from "@/shared/lib/api";

import type {
  AskRequest,
  AskResponse,
  CompareRequest,
  CompareResponse,
} from "@/features/assistant/types/ask.types";

export async function askProductQuestion(
  payload: AskRequest,
  signal?: AbortSignal,
): Promise<AskResponse> {
  const body = askRequestSchema.parse(payload);
  const response = await api.post<unknown>("/assistant/ask", body, { signal });

  return askResponseSchema.parse(response.data);
}

export async function compareProducts(
  payload: CompareRequest,
  signal?: AbortSignal,
): Promise<CompareResponse> {
  const body = compareRequestSchema.parse(payload);
  const response = await api.post<unknown>("/assistant/compare", body, {
    signal,
  });

  return compareResponseSchema.parse(response.data);
}
