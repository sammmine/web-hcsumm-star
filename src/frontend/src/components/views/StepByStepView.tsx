import { useRunStore } from "../../state/runStore";
import { GraphView } from "../GraphView";

/**
 * MVP: render each pipeline stage from bundle.t*.stages.
 * TODO: render features/embedding/fusion tables + distance matrix; this stub shows the
 * call graph and summary graph endpoints for each time point.
 */
export function StepByStepView() {
  const bundle = useRunStore((s) => s.bundle);
  if (!bundle) return null;
  return (
    <div>
      {(["t0", "t1"] as const).map((t) => (
        <section key={t}>
          <h3>{t} — call graph</h3>
          <GraphView elements={bundle[t].callgraph} height={360} />
          <h3>{t} — summary graph</h3>
          <GraphView elements={bundle[t].summary} height={360} />
          {/* TODO: behaviour features table, embedding, fusion, distance matrix */}
        </section>
      ))}
    </div>
  );
}
