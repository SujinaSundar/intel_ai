const BASE_URL =
  process.env.NEXT_PUBLIC_AGENT_API ??
  "http://localhost:8000";

interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export async function register(
  request: RegisterRequest
) {
  const response = await fetch(
    `${BASE_URL}/auth/register`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const text = await response.text();

  if (!response.ok) {
    throw new Error(text);
  }

  return JSON.parse(text);
}