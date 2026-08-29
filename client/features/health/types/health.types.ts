import type { z } from "zod";

import type { healthResponseSchema } from "@/features/health/schemas/health.schema";

export type HealthResponse = z.infer<typeof healthResponseSchema>;
