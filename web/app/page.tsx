"use client";

import { useState, useRef } from "react";
import ChatBox from "@/components/ChatBox";
import InputBar from "@/components/InputBar";
import { streamChat } from "@/lib/api";

type Message = {
  role: "user" | "bot";
  text: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const chatRef = useRef<HTMLDivElement | null>(null);

  // -------- HANDLE SEND --------
  const handleSend = async (input: string) => {
    if (!input.trim()) return;

    // user message
    const userMsg: Message = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    // bot placeholder
    const botMsg: Message = { role: "bot", text: "" };
    setMessages((prev) => [...prev, botMsg]);

    try {
      const res = await streamChat(input);

      if (!res.body) return;

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let done = false;
      let botText = "";

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;

        // 🔥 FIXED (smooth streaming)
        const chunk = decoder.decode(
          value || new Uint8Array(),
          { stream: true }
        );

        botText += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "bot",
            text: botText,
          };
          return updated;
        });

        // auto scroll
        setTimeout(() => {
          chatRef.current?.scrollTo({
            top: chatRef.current.scrollHeight,
            behavior: "smooth",
          });
        }, 0);
      }
    } catch (error) {
      console.error("Streaming error:", error);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🤖 BrahmX</h1>

      {/* CHAT */}
      <ChatBox messages={messages} chatRef={chatRef} />

      {/* INPUT */}
      <InputBar onSend={handleSend} />
    </div>
  );
}

// -------- STYLES --------
const styles = {
  container: {
    height: "100vh",
    display: "flex",
    flexDirection: "column" as const,
  },
  title: {
    textAlign: "center" as const,
    padding: "10px",
    borderBottom: "1px solid #1e293b",
  },
};