import { useState } from "react";

const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export default function PredictWidget() {
  const [preview, setPreview] = useState(null);
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState(null);
  const [loading, setLoading] = useState(false);
  const [latencyMs, setLatencyMs] = useState(null);

  async function onFileChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!/\.(jpg|jpeg|png|webp|bmp)$/i.test(file.name)) {
      setError("Unsupported file type"); setResult(null); setPreview(null); return;
    }
    if (file.size > 8 * 1024 * 1024) {
      setError("File too large (> 8MB)"); setResult(null); setPreview(null); return;
    }

    setPreview(URL.createObjectURL(file));
    setError(null); setResult(null); setLatencyMs(null);

    const form = new FormData();
    form.append("file", file);

    setLoading(true);
    const t0 = performance.now();
    try {
      const res  = await fetch(`${API}/predict`, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Request failed");
      setResult(data);
    } catch (err) {
      setError(err.message || "Request failed");
    } finally {
      setLatencyMs(Math.round(performance.now() - t0));
      setLoading(false);
    }
  }

  return (
    <section>
      {/* centered upload button */}
      <div className="btnRow">
        <label className="btn">
          <input type="file" accept="image/*" onChange={onFileChange} hidden disabled={loading} />
          {loading ? "Classifying…" : "Choose an image"}
        </label>
      </div>

      {/* preview */}
      {preview && <img src={preview} alt="preview" className="preview" />}

      {/* meta + errors */}
      {latencyMs != null && <p className="mono">Latency: {latencyMs} ms</p>}
      {error && <p className="error">{error}</p>}

      {/* result */}
      {result && (
        <div className="result">
          <h3 style={{ marginTop: 0 }}>Prediction</h3>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
            <strong>{result.label}</strong>
            {result.confidence != null && (
              <span style={{ fontWeight: 600 }}>{(result.confidence * 100).toFixed(1)}%</span>
            )}
          </div>

          {Array.isArray(result.top3) && (
            <ul className="list">
              {result.top3.map((t, i) => (
                <li key={i} className="list-item">
                  <span style={{ width: 110 }}>{t.label}</span>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${Math.max(2, t.p * 100)}%` }} />
                  </div>
                  <span className="mono" style={{ minWidth: 52, textAlign: "right" }}>
                    {(t.p * 100).toFixed(1)}%
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}
