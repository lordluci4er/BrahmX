"use client";

import { RefObject, useEffect } from "react";
import MessageBubble from "./MessageBubble";

type Message = {
  role: "user" | "bot";
  text: string;
};

type Props = {
  messages: Message[];
  chatRef: RefObject<HTMLDivElement | null>;
};

export default function ChatBox({ messages, chatRef }: Props) {
  // -------- AUTO SCROLL --------
  useEffect(() => {
    chatRef.current?.scrollTo({
      top: chatRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, chatRef]);

  return (
    <div ref={chatRef} style={styles.container}>
      {messages.length === 0 && (
        <div style={styles.empty}>
          👋 Start chatting with <b>BrahmX</b>
        </div>
      )}

      {messages.map((msg, index) => (
        <MessageBubble key={index} role={msg.role} text={msg.text} />
      ))}
    </div>
  );
}

// -------- STYLES --------
const styles = {
  container: {
    flex: 1,
    overflowY: "auto" as const,
    display: "flex",
    flexDirection: "column" as const,
    gap: "10px",
    padding: "12px",

    // 🔥 NEW (UI FIX)
    maxWidth: "800px",
    margin: "0 auto",
    width: "100%",
  },
  empty: {
    textAlign: "center" as const,
    opacity: 0.6,
    marginTop: "40px",
  },
};