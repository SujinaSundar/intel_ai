"use client";

import { useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import SuggestedQuestions from "./SuggestedQuestions";
import TypingIndicator from "./TypingIndicator";

import { Message } from "@/types/chat";

import {
  askQuestion
} from "@/services/agent.service";


export default function ChatWindow() {

  const [messages, setMessages] = useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  // ---------------------------------------------------------
  // Send Question
  // ---------------------------------------------------------

  const handleSend = async (
    question: string
  ) => {

    const userMessage: Message = {

      id: crypto.randomUUID(),

      role: "user",

      content: question,

      createdAt: new Date()

    };

    setMessages(

      (previous) => [

        ...previous,

        userMessage

      ]

    );

    setLoading(true);

    try {

      const answer = await askQuestion(

        question

      );

      const assistantMessage: Message = {

        id: crypto.randomUUID(),

        role: "assistant",

        content: answer,

        createdAt: new Date()

      };

      setMessages(

        (previous) => [

          ...previous,

          assistantMessage

        ]

      );

    }

    catch {

      const errorMessage: Message = {

        id: crypto.randomUUID(),

        role: "assistant",

        content:
          "Unable to connect to the Agent Service.",

        createdAt: new Date(),

        error: true

      };

      setMessages(

        (previous) => [

          ...previous,

          errorMessage

        ]

      );

    }

    finally {

      setLoading(false);

    }

  };

  // ---------------------------------------------------------
  // UI
  // ---------------------------------------------------------

  return (

    <div className="mx-auto flex h-[80vh] max-w-5xl flex-col">

      {/* -------------------------------------------------- */}
      {/* Header */}
      {/* -------------------------------------------------- */}

      <div className="mb-8">

        <h1 className="text-4xl font-bold">

          🧠 Research Copilot

        </h1>

        <p className="mt-2 text-slate-400">

          AI-powered trading research for
          NIFTY 50 companies.

        </p>

      </div>

      {/* -------------------------------------------------- */}
      {/* Suggested Questions */}
      {/* -------------------------------------------------- */}

      {

        messages.length === 0 && (

          <SuggestedQuestions

            onSelect={handleSend}

          />

        )

      }

      {/* -------------------------------------------------- */}
      {/* Messages */}
      {/* -------------------------------------------------- */}

      <div className="flex-1 overflow-y-auto">

        {

          messages.map(

            (message) => (

              <ChatMessage

                key={message.id}

                message={message}

              />

            )

          )

        }

        {

          loading && (

            <TypingIndicator />

          )

        }

      </div>

      {/* -------------------------------------------------- */}
      {/* Chat Input */}
      {/* -------------------------------------------------- */}

      <ChatInput

        onSend={handleSend}

        disabled={loading}

      />

    </div>

  );

}