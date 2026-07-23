import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Intel AI Trading Research Assistant",
  description: "Multi-Agent AI Trading Research Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}