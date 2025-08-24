import {useEffect, useState } from "react"


const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export default function App() {
  const [msg, setMsg] = useState("loading...");
  const [result, setResult] = useState(null);

  useEffect(() => {
    console.log("API =", API);

    fetch(`${API}/ping`)
      .then((res) => res.json())
      .then((data) => setMsg(`${data.status} - ${data.service}`))
      .catch((err) => {
        console.error("Fetch error:", err);
        setMsg("backend unreachable");
    });
  }, []);

  async function uploadFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API}/classify`, { method: "POST", body: form });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ ok: false, error: "request failed" });
    }
  
  }

  return (
    <main style={{ padding: 24, fontFamily: "system-ui"}}>
      <h1>EcoVision</h1>
      <p>Backend says: {msg}</p>
    </main>
  );

}
  