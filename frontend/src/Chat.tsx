import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  text: string;
}

// AgentInputItem is opaque — we store it as unknown for history passthrough
type HistoryItem = unknown;

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setError(null);
    setMessages((m) => [...m, { role: "user", text }]);
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ history, userMessage: text }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Unknown error");
      setHistory(data.history);
      setMessages((m) => [...m, { role: "assistant", text: data.response }]);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>Craig</div>
      <div style={styles.messages}>
        {messages.length === 0 && (
          <div style={styles.empty}>Ask Craig anything about the graph-native architecture.</div>
        )}
        {messages.map((m, i) => (
          <div key={i} style={m.role === "user" ? styles.userBubble : styles.craigBubble}>
            <span style={styles.sender}>{m.role === "user" ? "You" : "Craig"}</span>
            <div style={styles.text}>{m.text}</div>
          </div>
        ))}
        {loading && (
          <div style={styles.craigBubble}>
            <span style={styles.sender}>Craig</span>
            <div style={{ ...styles.text, opacity: 0.5 }}>Thinking…</div>
          </div>
        )}
        {error && <div style={styles.error}>{error}</div>}
        <div ref={bottomRef} />
      </div>
      <div style={styles.inputRow}>
        <textarea
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKey}
          placeholder="Message Craig… (Enter to send, Shift+Enter for newline)"
          rows={2}
          disabled={loading}
        />
        <button style={styles.button} onClick={send} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    maxWidth: 760,
    margin: "0 auto",
    fontFamily: "system-ui, sans-serif",
    background: "#0f0f0f",
    color: "#e8e8e8",
  },
  header: {
    padding: "14px 20px",
    borderBottom: "1px solid #2a2a2a",
    fontSize: 16,
    fontWeight: 600,
    letterSpacing: 1,
    color: "#a0a0a0",
  },
  messages: {
    flex: 1,
    overflowY: "auto",
    padding: "20px 16px",
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  empty: {
    color: "#444",
    textAlign: "center",
    marginTop: 60,
    fontSize: 14,
  },
  userBubble: {
    alignSelf: "flex-end",
    maxWidth: "75%",
    background: "#1a1a2e",
    borderRadius: "12px 12px 2px 12px",
    padding: "10px 14px",
  },
  craigBubble: {
    alignSelf: "flex-start",
    maxWidth: "80%",
    background: "#1a1a1a",
    borderRadius: "12px 12px 12px 2px",
    padding: "10px 14px",
    border: "1px solid #2a2a2a",
  },
  sender: {
    display: "block",
    fontSize: 11,
    color: "#555",
    marginBottom: 4,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  text: {
    fontSize: 14,
    lineHeight: 1.6,
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
  },
  error: {
    color: "#ff6b6b",
    fontSize: 13,
    padding: "8px 12px",
    background: "#1a0000",
    borderRadius: 8,
    border: "1px solid #3a0000",
  },
  inputRow: {
    display: "flex",
    gap: 8,
    padding: "12px 16px",
    borderTop: "1px solid #2a2a2a",
    background: "#0f0f0f",
  },
  input: {
    flex: 1,
    background: "#1a1a1a",
    color: "#e8e8e8",
    border: "1px solid #2a2a2a",
    borderRadius: 8,
    padding: "10px 12px",
    fontSize: 14,
    resize: "none",
    outline: "none",
    fontFamily: "inherit",
  },
  button: {
    background: "#2a2a4a",
    color: "#a0a0e0",
    border: "none",
    borderRadius: 8,
    padding: "0 18px",
    cursor: "pointer",
    fontSize: 14,
    fontWeight: 500,
  },
};
