import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

export default function Dashboard() {
  const [panel, setPanel] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = "http://localhost:8000";

  async function fetchPanel() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/dashboard`);
      const data = await res.json();
      setPanel(data.panel || "Nenhum painel encontrado.");
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  async function updatePanel() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/update-dashboard?limit=3`, {
        method: "POST",
      });
      const data = await res.json();
      setPanel(data.panel);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  useEffect(() => {
    fetchPanel();
  }, []);

  return (
    <div className="h-screen bg-black text-blue-200 flex flex-col items-center p-6 font-mono">
      <div className="w-full max-w-4xl border border-blue-800 bg-black/70 shadow-lg rounded-xl p-6 overflow-hidden">
        <h1 className="text-center text-2xl mb-6 text-blue-400 tracking-widest">
          ✦ CAMPAIGN DASHBOARD ✦
        </h1>

        <div className="flex gap-4 mb-6 justify-center">
          <button
            onClick={updatePanel}
            className="px-4 py-2 bg-blue-900 hover:bg-blue-800 text-blue-100 rounded-lg border border-blue-700"
          >
            Update Dashboard
          </button>
          <button
            onClick={fetchPanel}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-blue-100 rounded-lg border border-blue-700"
          >
            Reload
          </button>
        </div>

        <div className="h-[65vh] overflow-y-auto p-4 bg-black/50 border border-blue-900 rounded-lg leading-relaxed">
          {loading ? (
            <p className="text-blue-400 animate-pulse">
              Atualizando o painel...
            </p>
          ) : (
            <div className="prose prose-invert max-w-none">
              <ReactMarkdown
                components={{
                  h1: ({node, ...props}) => (
                    <h1 className="text-blue-300 text-2xl font-bold mt-6 mb-3" {...props} />
                  ),
                  h2: ({node, ...props}) => (
                    <h2 className="text-blue-300 text-xl font-semibold mt-5 mb-2" {...props} />
                  ),
                  h3: ({node, ...props}) => (
                    <h3 className="text-blue-300 text-lg font-semibold mt-4 mb-2" {...props} />
                  ),
                  p: ({node, ...props}) => (
                    <p className="my-2 text-blue-100" {...props} />
                  ),
                  strong: ({node, ...props}) => (
                    <strong className="text-blue-200 font-bold" {...props} />
                  ),
                  ul: ({node, ...props}) => (
                    <ul className="list-disc list-inside space-y-1 ml-3 text-blue-100" {...props} />
                  ),
                  li: ({node, ...props}) => (
                    <li className="leading-relaxed" {...props} />
                  ),
                }}
              >
                {panel}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
