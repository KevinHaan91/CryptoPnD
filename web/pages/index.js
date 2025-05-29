import React, { useState } from "react";

export default function Home() {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPumpScore = async () => {
    setLoading(true);
    setResult(null);

    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${baseUrl}/pump-score?symbol=${symbol}`);

      if (!res.ok) {
        throw new Error(`API returned ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    }

    setLoading(false);
  };

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Crypto Pump Score</h1>
      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="e.g., BTCUSDT"
        style={{ marginRight: "1rem", padding: "0.5rem" }}
      />
      <button onClick={fetchPumpScore} style={{ padding: "0.5rem 1rem" }}>
        Check
      </button>

      {loading && <p>Loading...</p>}

      {result && (
        <pre style={{ backgroundColor: "#f4f4f4", padding: "1rem", marginTop: "1rem" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  );
}
