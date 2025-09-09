import {useEffect, useState } from "react"
import PredictWidget from "./components/PredictWidget";

const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export default function App() {
  const [msg, setMsg] = useState("loading...");

  useEffect(() => {
    fetch(`${API}/ping`)
      .then((res) => res.json())
      .then((data) => setMsg(`${data.status} - ${data.service}`))
      .catch(() => setMsg("backend unreachable"));
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>EcoVision</h1>
      <p>Backend says: {msg}</p>
      <PredictWidget />
    </main>
  );
}
