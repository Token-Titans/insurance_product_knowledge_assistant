import axios, { isAxiosError } from "axios";

import { ApiError, isCanceledError } from "@/shared/types/api-error";

import { getApiBaseUrl } from "./env";

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function normalizeApiError(error: unknown): ApiError {
  if (error instanceof ApiError) {
    return error;
  }

  if (isAxiosError(error)) {
    const status = error.response?.status ?? 0;
    const data: unknown = error.response?.data;

    if (isRecord(data) && isRecord(data.detail)) {
      const code =
        typeof data.detail.code === "string" ? data.detail.code : "UNKNOWN";
      const message =
        typeof data.detail.message === "string"
          ? data.detail.message
          : error.message;

      return new ApiError(status, code, message);
    }

    if (isRecord(data) && typeof data.detail === "string") {
      return new ApiError(status, "HTTP_ERROR", data.detail);
    }

    return new ApiError(status, "HTTP_ERROR", error.message);
  }

  if (error instanceof Error) {
    return new ApiError(0, "UNKNOWN", error.message);
  }

  return new ApiError(0, "UNKNOWN", "Unknown error");
}

export const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 45_000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (isCanceledError(error)) {
      return Promise.reject(error);
    }

    return Promise.reject(normalizeApiError(error));
  },
);
