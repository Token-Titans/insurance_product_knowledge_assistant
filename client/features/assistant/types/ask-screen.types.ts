import type { AskResponse } from "@/features/assistant/types/ask.types";

export type ChatTurnStatus = "pending" | "answered" | "unavailable" | "error";

export interface ChatTurn {
  id: string;
  question: string;
  productId: string;
  status: ChatTurnStatus;
  response: AskResponse | null;
  errorCode: string | null;
}
