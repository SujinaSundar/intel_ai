"use client";

import { useState } from "react";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface Props {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({
  onSend,
  disabled,
}: Props) {
  const [message, setMessage] = useState("");

  const send = () => {
    if (!message.trim()) return;

    onSend(message);

    setMessage("");
  };

  return (
    <div className="border-t border-slate-800 pt-6">
      <div className="flex gap-4">
        <Textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask anything about NIFTY 50 companies..."
          className="min-h-[60px]"
          disabled={disabled}
        />

        <Button onClick={send} disabled={disabled}>
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}