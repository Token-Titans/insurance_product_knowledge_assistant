import type { z } from "zod";

import type {
  askRequestSchema,
  askResponseSchema,
  askSourceSchema,
} from "@/features/assistant/schemas/ask.schema";

export type AskRequest = z.infer<typeof askRequestSchema>;
export type AskResponse = z.infer<typeof askResponseSchema>;
export type AskSource = z.infer<typeof askSourceSchema>;
