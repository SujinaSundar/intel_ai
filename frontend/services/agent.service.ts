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

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export async function askQuestion(
  question: string,
  history: ChatMessage[]
): Promise<string> {

  const response = await apiClient(
    "/ask",
    {
      method: "POST",
      body: JSON.stringify({
        question,
        history,
      }),
    }
  );

  return (response as AskResponse).answer;
}