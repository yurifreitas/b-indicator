import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const ChatBox: React.FC = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<
    { type: "user" | "bot"; text: string; full?: any; steps?: any[] }[]
  >([]);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [history, loading]);

  const extractSteps = (full: any): any[] => {
    if (!full?.steps || !Array.isArray(full.steps)) return [];
    return full.steps;
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    const cleaned = message.trim();
    setLoading(true);
    setMessage("");
    setResponse(null);
    setHistory((prev) => [...prev, { type: "user", text: cleaned }]);

    try {
      const res = await axios.post(
        "http://localhost:8000/runs",
        {
          agent_name: "finance_agent",
          input: [
            {
              parts: [{ content: cleaned }],
            },
          ],
          mode: "sync",
        },
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      );

      const content =
        res.data?.output?.parts?.[0]?.content || "Resposta vazia do agente.";
      const steps = extractSteps(res.data);

      setResponse(res.data);
      setHistory((prev) => [
        ...prev,
        { type: "bot", text: content, full: res.data, steps },
      ]);
    } catch (err) {
      const errorMsg = "Erro ao conectar com o agente.";
      setResponse({ error: errorMsg });
      setHistory((prev) => [...prev, { type: "bot", text: errorMsg }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow h-[75vh] flex flex-col">
      <h2 className="text-xl font-semibold mb-4">Chat com IA Financeira</h2>

      {/* Área de mensagens */}
      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {history.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded max-w-[90%] whitespace-pre-wrap ${
              msg.type === "user"
                ? "bg-blue-100 self-end text-right"
                : "bg-green-50 border border-green-200 self-start text-left"
            }`}
          >
            <strong>{msg.type === "user" ? "Você:" : "IA:"}</strong>
            <p className="mt-1">{msg.text}</p>

            {/* Mostra imagem se for resposta base64 */}
            {msg.text.startsWith("data:image") && (
              <img
                src={msg.text}
                alt="Gráfico técnico"
                className="mt-2 rounded max-w-full"
              />
            )}

            {/* Exibir steps do agente (se houver) */}
            {msg.steps && msg.steps.length > 0 && (
              <div className="mt-3 space-y-2 text-sm">
                <strong>📚 Etapas da execução:</strong>
                {msg.steps.map((step, stepIdx) => (
                  <div key={stepIdx} className="bg-gray-100 p-2 rounded">
                    <p className="text-gray-700 font-medium mb-1">
                      Step {stepIdx + 1}{" "}
                      {step.tool_name && `→ Tool: ${step.tool_name}`}
                    </p>

                    {step.arguments && (
                      <pre className="text-xs text-gray-600 overflow-x-auto">
                        {JSON.stringify(step.arguments, null, 2)}
                      </pre>
                    )}

                    {step.observation && (
                      <div className="mt-1">
                        <span className="font-semibold">🔍 Observação:</span>
                        <pre className="text-xs text-gray-700 bg-white p-1 mt-1 rounded border">
                          {typeof step.observation === "string"
                            ? step.observation
                            : JSON.stringify(step.observation, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* JSON completo (opcional) */}
            {msg.type === "bot" && msg.full && (
              <details className="mt-2">
                <summary className="text-sm text-gray-600 cursor-pointer">
                  📦 Ver JSON completo
                </summary>
                <pre className="bg-gray-100 p-2 rounded text-sm mt-2 overflow-x-auto">
                  {JSON.stringify(msg.full, null, 2)}
                </pre>
              </details>
            )}
          </div>
        ))}

        {loading && (
          <div className="italic text-gray-500">
            ⏳ Aguardando resposta do agente...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Caixa de entrada */}
      <div className="mt-4 flex gap-2">
        <textarea
          className="flex-1 p-2 border rounded"
          rows={2}
          placeholder="Digite sua pergunta..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? "Enviando..." : "Enviar"}
        </button>

        <button
          onClick={() => {
            setMessage(
              "Analise técnica do BTCUSDT semanal com todos os indicadores"
            );
            setTimeout(sendMessage, 0);
          }}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded"
        >
          📊 BTC Weekly
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
