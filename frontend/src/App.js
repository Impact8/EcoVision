import {useEffect, useState } from "react"

export default function App() {
  const [msg, setMsg] = useState("loading...");

  useEffect(() => {
    fetch("/ping")
    .then((r) => r.json())
    .then((data) => setMsg(`${data.status} - ${data.service}`))
    .catch((err) => {
      console.error("Fetch error:", err);
      setMsg("backend unreachable");
    });
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui"}}>
      <h1>EcoVision</h1>
      <p>Backend says: {msg}</p>
    </main>
  );

}
  