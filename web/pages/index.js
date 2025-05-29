// FRONTEND: pages/index.js
import React, { useEffect, useState } from "react";

const COINS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT", "SOLUSDT"];
const REFRESH_INTERVAL = 10000; // every 10 seconds

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${baseUrl}/pump-scores`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ symbols: COINS }),
      });

      const result = await res.json();
      if (Array.isArray(result)) {
        setData(result.sort((a, b) => b.score - a.score));
      } else {
        setData([]);
      }
    } catch (err) {
      console.error("Error fetching pump scores:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Live Pump & Dump Leaderboard</h1>
      {loading && <p>Loading...</p>}
      {!loading && (
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Score</th>
              <th>Flags</th>
            </tr>
          </thead>
          <tbody>
            {data.map((coin, idx) => (
              <tr key={idx}>
                <td>{coin.symbol}</td>
                <td>{coin.score.toFixed(2)}</td>
                <td>{JSON.stringify(coin.flags)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
