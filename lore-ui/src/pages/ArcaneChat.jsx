import { useState } from "react";

export default function ArcaneChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask-oracle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input, top_k: 3 })
      });

      const data = await res.json();
      const oracleMsg = { role: "assistant", content: data.answer };

      setMessages(prev => [...prev, oracleMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: "⚠️ Erro ao consultar o Oráculo." }
      ]);
    }

    setInput("");
    setLoading(false);
  }

  return (
    <div className="h-screen bg-black text-blue-200 flex flex-col items-center p-6 font-mono">
      <div className="w-full max-w-3xl border border-blue-800 bg-black/70 shadow-lg rounded-xl p-4 overflow-hidden">
        <h1 className="text-center text-xl mb-4 text-blue-400 tracking-widest">
          ✦ ARCANE TERMINAL ✦
        </h1>

        <div className="h-[70vh] overflow-y-auto space-y-3 p-3 bg-black/50 border border-blue-900 rounded-lg">
          {messages.map((m, i) => (
            <div
              key={i}
              className={
                m.role === "user"
                  ? "text-white"
                  : "text-blue-300 whitespace-pre-wrap"
              }
            >
              <span className="text-blue-600">
                {m.role === "user" ? "> You:" : "> Zaheen:"}
              </span>{" "}
              {m.content}
            </div>
          ))}

          {loading && (
            <div className="text-blue-500">Zaheen está consultando os véus...</div>
          )}
        </div>

        <form onSubmit={sendMessage} className="mt-4 flex gap-2">
          <input
            className="flex-1 bg-black/60 border border-blue-700 text-blue-100 p-2 rounded-lg focus:outline-none focus:border-blue-400"
            placeholder="Faça sua pergunta ao Oráculo..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            className="px-4 py-2 bg-blue-900 hover:bg-blue-800 text-blue-100 rounded-lg border border-blue-700"
            disabled={loading}
          >
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}
