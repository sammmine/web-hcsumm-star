import { useRunStore } from "../../state/runStore";
import { GraphView } from "../GraphView";

/** MVP: summary graphs t0 vs t1 side by side; cluster colors consistent via backend indexing. */
export function SideBySideView() {
  const bundle = useRunStore((s) => s.bundle);
  if (!bundle) return null;
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
      <div>
        <h3>t0</h3>
        <GraphView elements={bundle.t0.summary} />
      </div>
      <div>
        <h3>t1</h3>
        <GraphView elements={bundle.t1.summary} />
      </div>
    </div>
  );
}
