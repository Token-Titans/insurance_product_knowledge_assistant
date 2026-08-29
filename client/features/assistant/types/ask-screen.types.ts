import type { AskResponse } from "@/features/assistant/types/ask.types";

export type ChatTurnStatus = "pending" | "answered" | "unavailable" | "error";

interface ChatTurnBase {
  id: string;
  question: string;
  status: ChatTurnStatus;
  shouldType: boolean;
}

export interface AskChatTurn extends ChatTurnBase {
  kind: "ask";
  productId: string;
  response: AskResponse | null;
  errorCode: string | null;
}

export interface CompareColumnState {
  productId: string;
  status: ChatTurnStatus;
  response: AskResponse | null;
  errorCode: string | null;
}

export interface CompareChatTurn extends ChatTurnBase {
  kind: "compare";
  left: CompareColumnState;
  right: CompareColumnState;
}

export type ChatTurn = AskChatTurn | CompareChatTurn;
