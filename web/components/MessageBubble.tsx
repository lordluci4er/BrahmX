type Props = {
  role: "user" | "bot";
  text: string;
};

export default function MessageBubble({ role, text }: Props) {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
      }}
    >
      {/* Bot Avatar */}
      {!isUser && <div style={styles.avatar}>🤖</div>}

      <div
        style={{
          ...styles.bubble,
          backgroundColor: isUser ? "#2563eb" : "#334155",
          borderTopRightRadius: isUser ? "0px" : "12px",
          borderTopLeftRadius: isUser ? "12px" : "0px",
        }}
      >
        {/* 🔥 Typing fallback */}
        {text || "•••"}
      </div>

      {/* User Avatar */}
      {isUser && <div style={styles.avatar}>🧑</div>}
    </div>
  );
}

// -------- STYLES --------
const styles = {
  bubble: {
    maxWidth: "60%", // 🔥 UPDATED
    padding: "10px 14px",
    borderRadius: "12px",
    color: "white",
    fontSize: "14px",
    lineHeight: "1.5",
    whiteSpace: "pre-wrap" as const,
    wordBreak: "break-word" as const,
  },
  avatar: {
    margin: "0 6px",
    display: "flex",
    alignItems: "flex-end",
    fontSize: "18px",
  },
};