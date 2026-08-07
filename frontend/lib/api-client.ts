/**
 * API Client.
 *
 * Shared HTTP client
 * for Agent Service.
 */

const BASE_URL =
  process.env.NEXT_PUBLIC_AGENT_API ??
  "https://agent-service-70305477964.asia-south1.run.app";

export async function apiClient(
  endpoint: string,
  options?: RequestInit
) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token && {
          Authorization: `Bearer ${token}`,
        }),
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
