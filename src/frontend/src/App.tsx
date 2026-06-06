import { UploadPanel } from "./components/UploadPanel";
import { ParamForm } from "./components/ParamForm";
import { DirectView } from "./components/views/DirectView";
import { SideBySideView } from "./components/views/SideBySideView";
import { StepByStepView } from "./components/views/StepByStepView";
import { createRun, pollRun } from "./api/client";
import { useRunStore, type ViewMode } from "./state/runStore";

const VIEWS: { id: ViewMode; label: string }[] = [
  { id: "direct", label: "Direct" },
  { id: "side-by-side", label: "Side-by-side" },
  { id: "step-by-step", label: "Step-by-Step" },
];

export default function App() {
  const { config, sourceT0, sourceT1, status, setStatus, setBundle, view, setView, bundle } =
    useRunStore();

  async function run() {
    if (!sourceT0 || !sourceT1) return;
    setStatus("pending");
    try {
      const jobId = await createRun(sourceT0, sourceT1, config);
      const result = await pollRun(jobId, { onStatus: setStatus });
      setBundle(result);
      setStatus("done");
    } catch (e) {
      console.error(e);
      setStatus("error");
    }
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <h2>Web HCSumm*</h2>
        <UploadPanel />
        <ParamForm />
        <button onClick={run} disabled={!sourceT0 || !sourceT1 || status === "running"}>
          Run pipeline
        </button>
        <p>Status: {status}</p>
      </aside>
      <main className="main">
        <nav>
          {VIEWS.map((v) => (
            <button
              key={v.id}
              onClick={() => setView(v.id)}
              disabled={!bundle}
              style={{ fontWeight: view === v.id ? "bold" : "normal" }}
            >
              {v.label}
            </button>
          ))}
        </nav>
        {!bundle && <p>Upload t0 &amp; t1, set parameters, then Run.</p>}
        {bundle && view === "direct" && <DirectView />}
        {bundle && view === "side-by-side" && <SideBySideView />}
        {bundle && view === "step-by-step" && <StepByStepView />}
      </main>
    </div>
  );
}
