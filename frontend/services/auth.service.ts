const BASE_URL =
  process.env.NEXT_PUBLIC_AGENT_API ??
  "http://localhost:8000";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const body = new URLSearchParams();

  body.append("username", email);
  body.append("password", password);

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  const text = await response.text();

  if (!response.ok) {
    throw new Error(text);
  }

  const data: LoginResponse = JSON.parse(text);

  // Save JWT token
  localStorage.setItem("access_token", data.access_token);

  return data;
}

export function getToken(): string | null {
  return localStorage.getItem("access_token");
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export function logout(): void {
  localStorage.removeItem("access_token");
}
export async function validateToken(): Promise<boolean> {
  const token = getToken();

  if (!token) {
    return false;
  }

  try {
    const response = await fetch(`${BASE_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      logout();
      return false;
    }

    return true;
  } catch (error) {
    console.error("Token validation failed:", error);
    logout();
    return false;
  }
}