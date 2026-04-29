"use client";

import { useState, KeyboardEvent } from "react";

type Props = {
  onSend: (message: string) => void;
};

export default function InputBar({ onSend }: Props) {
  const [input, setInput] = useState("");

  // -------- SEND --------
  const handleSend = () => {
    const text = input.trim();
    if (!text) return;

    onSend(text);
    setInput("");
  };

  // -------- KEY HANDLER --------
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Enter = send, Shift+Enter = new line
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={styles.container}>
      <textarea
        style={styles.input}
        rows={1}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask BrahmX anything..."
      />

      <button
        style={{
          ...styles.button,
          opacity: input.trim() ? 1 : 0.5,
          cursor: input.trim() ? "pointer" : "not-allowed",
        }}
        onClick={handleSend}
        disabled={!input.trim()}
      >
        ➤
      </button>
    </div>
  );
}

// -------- STYLES --------
const styles = {
  container: {
    display: "flex",
    gap: "10px",
    padding: "12px",
    borderTop: "1px solid #1e293b",
    background: "#020617",
  },
  input: {
    flex: 1,
    resize: "none" as const,
    padding: "12px 16px",   // 🔥 UPDATED
    borderRadius: "20px",   // 🔥 UPDATED
    border: "none",
    outline: "none",
    fontSize: "14px",
    background: "#1e293b",
    color: "white",
    lineHeight: "1.4",
  },
  button: {
    padding: "10px 14px",
    borderRadius: "10px",
    border: "none",
    background: "#22c55e",
    color: "black",
    fontWeight: "bold",
    fontSize: "16px",
  },
};