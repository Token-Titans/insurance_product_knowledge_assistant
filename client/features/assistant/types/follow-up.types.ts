import type { z } from "zod";

import type {
  followUpRequestSchema,
  followUpResponseSchema,
} from "@/features/assistant/schemas/follow-up.schema";

export type FollowUpRequest = z.infer<typeof followUpRequestSchema>;
export type FollowUpResponse = z.infer<typeof followUpResponseSchema>;
