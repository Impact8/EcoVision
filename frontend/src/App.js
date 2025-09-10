import "./App.css";
import PredictWidget from "./components/PredictWidget";

export default function App() {
  return (
    <main className="App">
      <header>
        <h1 className="App-title">EcoVision</h1>
      </header>

      <p className="App-descrptions">
        Upload a photo to classify recyclables vs landfill.
      </p>

      <PredictWidget />

      <footer style={{ marginTop: 100 }}>
        Demo only • FastAPI + PyTorch •{" "}
        <a href="http://127.0.0.1:8000/docs">API docs</a>
      </footer>
    </main>
  );
}
