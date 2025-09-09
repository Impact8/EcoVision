import { useState } from "react";

const API =
  process.env.REACT_APP_API_URL ||
  "http://127.0.0.1:8000"; // fallback for dev

export default function PredictWidget() {
  const [preview, setPreview] = useState(null);
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState(null);
  const [loading, setLoading] = useState(false);
  const [latencyMs, setLatencyMs] = useState(null);

  async function onFileChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    // quick client-side guards to match backend
    if (!/\.(jpg|jpeg|png|webp|bmp)$/i.test(file.name)) {
      setError("Unsupported file type"); setResult(null); setPreview(null);
      return;
    }
    if (file.size > 8 * 1024 * 1024) {
      setError("File too large (> 8MB)"); setResult(null); setPreview(null);
      return;
    }

    setPreview(URL.createObjectURL(file));
    setError(null); setResult(null); setLatencyMs(null);

    const form = new FormData();
    form.append("file", file); // backend expects 'file'

    setLoading(true);
    const t0 = performance.now();
    try {
      const res = await fetch(`${API}/predict`, { method: "POST", body: form });
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
    <div style={styles.wrap}>
      <label style={styles.uploader}>
        <input type="file" accept="image/*" onChange={onFileChange} disabled={loading} style={{ display: "none" }} />
        <span>{loading ? "Classifying…" : "Choose an image"}</span>
      </label>

      {preview && (
        <div style={styles.previewBox}>
          <img src={preview} alt="preview" style={styles.img} />
        </div>
      )}

      {latencyMs != null && <p style={styles.mono}>Latency: {latencyMs} ms</p>}
      {error && <p style={styles.err}>{error}</p>}

      {result && (
        <div style={styles.card}>
          <h3 style={{ marginTop: 0 }}>Prediction</h3>
          <p>
            <strong>{result.label}</strong>{" "}
            {result.confidence != null && `(${(result.confidence * 100).toFixed(1)}%)`}
          </p>

          {Array.isArray(result.top3) && (
            <>
              <h4 style={{ marginBottom: 8 }}>Top 3</h4>
              <ul style={styles.list}>
                {result.top3.map((t, i) => (
                  <li key={i} style={styles.listItem}>
                    <span style={{ width: 120 }}>{t.label}</span>
                    <div style={styles.barTrack}>
                      <div style={{ ...styles.barFill, width: `${Math.max(2, t.p * 100)}%` }} />
                    </div>
                    <span style={styles.mono}>{(t.p * 100).toFixed(1)}%</span>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

const styles = {
  wrap: { maxWidth: 560, margin: "24px auto", padding: "0 16px", fontFamily: "system-ui, sans-serif" },
  uploader: { display: "inline-block", padding: "10px 14px", border: "1px solid #ddd", borderRadius: 8, cursor: "pointer", background: "#fafafa" },
  previewBox: { marginTop: 16, border: "1px solid #eee", borderRadius: 8, overflow: "hidden" },
  img: { width: "100%", height: "auto", display: "block" },
  card: { marginTop: 16, border: "1px solid #eee", borderRadius: 8, padding: 16, background: "#fff" },
  list: { listStyle: "none", padding: 0, margin: 0 },
  listItem: { display: "flex", alignItems: "center", gap: 8, marginBottom: 6 },
  barTrack: { flex: 1, height: 8, background: "#eee", borderRadius: 999 },
  barFill: { height: 8, background: "#4a8", borderRadius: 999 },
  err: { color: "crimson", marginTop: 12 },
  mono: { fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace", color: "#666" },
};
