/**
 * Agent Service.
 *
 * Communicates with the
 * LangGraph Agent Service.
 */

import { apiClient } from "@/lib/api-client";

interface AskResponse {
  answer: string;
}

export async function askQuestion(
  question: string
): Promise<string> {

  const response = await apiClient(
    "/ask",
    {
      method: "POST",

      body: JSON.stringify({
        question,
      }),
    }
  );

  return (response as AskResponse).answer;
}