import React, { useEffect, useState } from 'react';

export default function Home() {
  const [data, setData] = useState(null);
  const [symbol, setSymbol] = useState('BTCUSDT');

  const fetchPumpScore = async () => {
    const res = await fetch(`/api/pump-score?symbol=${symbol}`);
    const result = await res.json();
    setData(result);
  };

  useEffect(() => {
    fetchPumpScore();
  }, [symbol]);

  return (
    <div className='p-8 font-sans text-white bg-gray-900 min-h-screen'>
      <h1 className='text-4xl mb-4 font-bold'>Pump & Dump Detector</h1>
      <input
        type='text'
        className='p-2 rounded text-black'
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
      />
      <button
        onClick={fetchPumpScore}
        className='ml-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded'
      >
        Refresh
      </button>
      {data && (
        <div className='mt-6 bg-gray-800 p-4 rounded shadow-lg'>
          <h2 className='text-2xl font-semibold mb-2'>Symbol: {data.symbol}</h2>
          <p><strong>Pump Score:</strong> {data.score}</p>
          <p><strong>Flags:</strong> {data.flags.join(', ')}</p>
          <h3 className='mt-4 font-semibold'>Exchange Data:</h3>
          <ul className='list-disc pl-5'>
            {data.data.map((entry, i) => (
              <li key={i}>
                {entry.exchange}: Price = ${entry.price}, Volume = {entry.volume}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
