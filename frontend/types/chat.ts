/**
 * Chat Types.
 *
 * Defines frontend
 * chat interfaces.
 */

export interface Message {
  id: string;

  role: "user" | "assistant";

  content: string;

  createdAt: Date;

  loading?: boolean;

  error?: boolean;
}