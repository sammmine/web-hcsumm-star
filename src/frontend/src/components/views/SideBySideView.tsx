import { useState } from "react";
import { ContentSwitcher, Switch, Stack } from "@carbon/react";
import { useRunStore } from "../../state/runStore";
import { GraphView } from "../GraphView";

/** MVP: summary and callgraph graphs t0 vs t1 side by side; cluster colors consistent via backend indexing. */
export function SideBySideView() {
  const bundle = useRunStore((s) => s.bundle);
  const [mode, setMode] = useState<"cluster" | "non-cluster">("cluster");

  if (!bundle) return null;

  const elementsT0 = mode === "cluster" ? bundle.t0.summary : bundle.t0.callgraph;
  const elementsT1 = mode === "cluster" ? bundle.t1.summary : bundle.t1.callgraph;

  return (
    <Stack gap={5}>
      <ContentSwitcher
        selectedIndex={mode === "cluster" ? 0 : 1}
        onChange={(d) => setMode(d.index === 0 ? "cluster" : "non-cluster")}
        size="sm"
      >
        <Switch name="cluster" text="Clustered (Summary)" />
        <Switch name="non-cluster" text="Non-Clustered (Callgraph)" />
      </ContentSwitcher>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
        <div>
          <h3 className="cds--type-heading-02">t0 (before)</h3>
          <GraphView elements={elementsT0} title={`${mode === "cluster" ? "summary" : "callgraph"}_t0_before`} />
        </div>
        <div>
          <h3 className="cds--type-heading-02">t1 (after)</h3>
          <GraphView elements={elementsT1} title={`${mode === "cluster" ? "summary" : "callgraph"}_t1_after`} />
        </div>
      </div>
    </Stack>
  );
}
