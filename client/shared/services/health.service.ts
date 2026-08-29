import { healthResponseSchema } from "@/features/health/schemas/health.schema";
import { api } from "@/shared/lib/api";

import type { HealthResponse } from "@/features/health/types/health.types";

export async function getHealth(): Promise<HealthResponse> {
  const response = await api.get<unknown>("/health");

  return healthResponseSchema.parse(response.data);
}
