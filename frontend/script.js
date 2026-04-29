// -------- ADD MESSAGE --------
function addMessage(sender, text = "") {
    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.className = sender;
    div.innerText = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;

    return div; // important for streaming update
}


// -------- SEND MESSAGE (STREAMING) --------
async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    // user message show
    addMessage("user", message);
    input.value = "";

    // bot message bubble (empty initially)
    const botDiv = addMessage("bot", "");

    const chatBox = document.getElementById("chat-box");

    try {
        const response = await fetch("http://127.0.0.1:5000/chat-stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        // stream reader
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let done = false;

        while (!done) {
            const { value, done: doneReading } = await reader.read();
            done = doneReading;

            const chunk = decoder.decode(value || new Uint8Array(), { stream: true });

            // 🔥 LIVE APPEND (ChatGPT style)
            botDiv.innerText += chunk;

            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (error) {
        botDiv.innerText = "⚠️ Error streaming response";
        console.error(error);
    }
}