"use client";

import { useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import SuggestedQuestions from "./SuggestedQuestions";
import TypingIndicator from "./TypingIndicator";

import { Message } from "@/types/chat";

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading] = useState(false);

  const handleSend = (question: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
  };

  return (
    <div className="mx-auto flex h-[80vh] max-w-5xl flex-col">
      <div className="mb-8">
        <h1 className="text-4xl font-bold">
          🧠 Research Copilot
        </h1>

        <p className="mt-2 text-slate-400">
          AI-powered trading research for NIFTY 50 companies.
        </p>
      </div>

      {messages.length === 0 && (
        <SuggestedQuestions onSelect={handleSend} />
      )}

      <div className="flex-1 overflow-y-auto">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
          />
        ))}

        {loading && <TypingIndicator />}
      </div>

      <ChatInput
        onSend={handleSend}
        disabled={loading}
      />
    </div>
  );
}