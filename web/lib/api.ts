// -------- BASE URL --------
export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5000";


// -------- NORMAL CHAT --------
export async function sendMessage(message: string) {
  try {
    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) {
      throw new Error("Failed to fetch response");
    }

    return await res.json();
  } catch (error) {
    console.error("API Error:", error);
    return { reply: "⚠️ Error connecting to server." };
  }
}


// -------- STREAM CHAT (🔥 IMPORTANT) --------
export async function streamChat(message: string) {
  try {
    const res = await fetch(`${API_URL}/chat-stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!res.body) {
      throw new Error("No response body");
    }

    return res;
  } catch (error) {
    console.error("Stream Error:", error);
    throw error;
  }
}