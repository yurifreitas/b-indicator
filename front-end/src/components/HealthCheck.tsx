import React, { useEffect, useState } from "react";
import { get } from "../services/api";

const HealthCheck: React.FC = () => {
  const [status, setStatus] = useState<"online" | "offline" | "loading">("loading");

  useEffect(() => {
    get("/health")
      .then(() => setStatus("online"))
      .catch(() => setStatus("offline"));
  }, []);

  const getColor = () => {
    switch (status) {
      case "online":
        return "bg-green-500";
      case "offline":
        return "bg-red-500";
      default:
        return "bg-yellow-400";
    }
  };

  return (
    <div
      className={`w-3 h-3 rounded-full ${getColor()}`}
      title={`API ${status}`}
    ></div>
  );
};

export default HealthCheck;
