const DEFAULT_API_BASE_URL = "https://13.250.105.96/api/v1";

export function getApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;
}
