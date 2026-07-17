/**
 * API Client.
 *
 * Shared HTTP client
 * for Agent Service.
 */

const BASE_URL =
  process.env.NEXT_PUBLIC_AGENT_API ??
  "http://localhost:8000";

export async function apiClient(
  endpoint: string,
  options?: RequestInit
) {
  const response = await fetch(
    `${BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    }
  );

  if (!response.ok) {

    const error = await response.text();

    console.error("Status:", response.status);

    console.error("Response:", error);

    throw new Error(
        `API request failed (${response.status})`
    );

}

  return response.json();
}