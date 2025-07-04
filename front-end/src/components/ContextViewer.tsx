import React, { useState } from "react";
import { get } from "../services/api";
const ContextViewer: React.FC = () => {
  const [userId, setUserId] = useState("");
  const [context, setContext] = useState<any>(null);

  const fetchContext = async () => {
    try {
      const res = await get(`/users/${userId}/context`);
      setContext(res.data);
    } catch {
      setContext(null);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Contexto da IA</h2>
      <input
        className="w-full p-2 border rounded mb-2"
        placeholder="ID do Usuário"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <button onClick={fetchContext} className="bg-yellow-600 text-white px-4 py-2 rounded">
        Ver Contexto
      </button>
      {context && (
        <pre className="mt-4 p-2 bg-gray-100 rounded whitespace-pre-wrap text-sm">
          {JSON.stringify(context, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default ContextViewer;
