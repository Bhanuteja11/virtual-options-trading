import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [nifty, setNifty] = useState(null);
  const [mtm, setMtm] = useState(null);
  const [wallet, setWallet] = useState(null);
  const [status, setStatus] = useState("");

  const [priceSeries, setPriceSeries] = useState([]);
  const [pnlSeries, setPnlSeries] = useState([]);

  const [optionType, setOptionType] = useState("CE");
  const [strike, setStrike] = useState("");
  const [qty, setQty] = useState("");
  const [openTrades, setOpenTrades] = useState([]);

  /* ---------------- API LOADERS ---------------- */

  const loadWallet = () => {
    fetch("http://127.0.0.1:8000/wallet/1")
      .then((res) => res.json())
      .then((data) => setWallet(data));
  };

  const loadOpenTrades = () => {
    fetch("http://127.0.0.1:8000/intraday/open-trades")
      .then((res) => res.json())
      .then((data) => setOpenTrades(data));
  };

  /* ---------------- TRADING ACTIONS ---------------- */

  const placeIntradayTrade = () => {
    if (!strike || !qty) {
      setStatus("Enter strike & quantity");
      return;
    }

    setStatus("Placing intraday trade...");
    fetch(
      `http://127.0.0.1:8000/intraday/trade?option_type=${optionType}&strike_price=${strike}&quantity=${parseInt(
        qty
      )}`,
      { method: "POST" }
    )
      .then((res) => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(() => {
        loadWallet();
        loadOpenTrades();
        setStatus("Intraday trade placed");
      })
      .catch(() => setStatus("Trade failed"));
  };

  const squareOff = (tradeId) => {
    fetch(`http://127.0.0.1:8000/intraday/square-off/${tradeId}`, {
      method: "POST",
    }).then(() => {
      loadWallet();
      loadOpenTrades();
    });
  };

  /* ---------------- LIVE MTM + CHART UPDATES ---------------- */

  useEffect(() => {
    loadWallet();
    loadOpenTrades();

    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/intraday/mtm")
        .then((res) => res.json())
        .then((data) => {
          setMtm(data);
          setNifty(data.spot);

          setPriceSeries((prev) => [
            ...prev.slice(-30),
            {
              time: new Date().toLocaleTimeString(),
              price: data.spot,
            },
          ]);

          setPnlSeries((prev) => [
            ...prev.slice(-30),
            {
              time: new Date().toLocaleTimeString(),
              pnl: data.total_mtm,
            },
          ]);
        });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  /* ---------------- UI ---------------- */

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", maxWidth: "900px" }}>
      <h1>Virtual Options Trading Dashboard</h1>
      <p>Paper trading | Intraday options practice</p>

      <h2>Market</h2>
      <p>NIFTY Index: {nifty ?? "Loading..."}</p>

      <h2>Wallet</h2>
      {wallet ? (
        <>
          <p>Balance: ₹{wallet.balance}</p>
          <p>Realized P&L: ₹{wallet.realized_pnl}</p>
        </>
      ) : (
        <p>Loading wallet...</p>
      )}

      <h2>Intraday Options Trade</h2>

      <select value={optionType} onChange={(e) => setOptionType(e.target.value)}>
        <option value="CE">CE</option>
        <option value="PE">PE</option>
      </select>

      <input
        type="number"
        placeholder="Strike Price"
        value={strike}
        onChange={(e) => setStrike(e.target.value)}
        style={{ marginLeft: "10px" }}
      />

      <input
        type="number"
        placeholder="Quantity"
        value={qty}
        onChange={(e) => setQty(e.target.value)}
        style={{ marginLeft: "10px" }}
      />

      <button style={{ marginLeft: "10px" }} onClick={placeIntradayTrade}>
        Place Intraday Trade
      </button>

      <p>{status}</p>

      <h2>Open Positions</h2>
      {openTrades.length === 0 && <p>No open positions</p>}

      {openTrades.map((t) => (
        <div key={t.trade_id} style={{ marginBottom: "8px" }}>
          {t.option_type} {t.strike_price} | Qty: {t.quantity}
          <button
            style={{ marginLeft: "10px" }}
            onClick={() => squareOff(t.trade_id)}
          >
            Square Off
          </button>
        </div>
      ))}

      <h2>Live MTM P&L</h2>

      {mtm ? (
        <>
          <p>
            <strong>Total MTM:</strong> ₹{mtm.total_mtm}
          </p>
          {mtm.positions.map((p) => (
            <div key={p.trade_id}>
              {p.option_type} {p.strike_price} | Entry: {p.entry_premium} | Now:{" "}
              {p.current_premium} |{" "}
              <strong>P&L: ₹{p.pnl}</strong>
            </div>
          ))}
        </>
      ) : (
        <p>Loading MTM...</p>
      )}

      <h2>NIFTY Intraday Chart</h2>

      {priceSeries.length < 2 ? (
        <p>Collecting price data...</p>
      ) : (
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={priceSeries}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="price" stroke="#2563eb" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      )}

      <h2>MTM P&L Chart</h2>

      {pnlSeries.length < 2 ? (
        <p>Collecting P&L data...</p>
      ) : (
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={pnlSeries}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="pnl" stroke="#16a34a" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default App;
