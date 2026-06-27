import { useState } from "react";
import {
  Slider,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Tag,
  Stack,
} from "@carbon/react";
import { useRunStore } from "../../state/runStore";
import type { SideBundle, ClusterIterationStep } from "../../types";
import { GraphView } from "../GraphView";

/** Render one side's clustering iterations with a step slider. */
function IterationPlayer({ side, label }: { side: SideBundle; label: string }) {
  const iterations = side.iterations;
  const maxStep = iterations.length - 1;
  const [step, setStep] = useState(maxStep);

  if (iterations.length === 0) {
    return <p className="cds--type-body-01">No iteration data available.</p>;
  }

  const current: ClusterIterationStep = iterations[step];

  return (
    <Stack gap={5}>
      <div style={{ padding: "0 1rem" }}>
        <Slider
          id={`iter-slider-${label}`}
          labelText={`Iteration step (${label})`}
          value={step}
          min={0}
          max={maxStep}
          step={1}
          onChange={({ value }: { value: number }) => setStep(value)}
        />
      </div>

      <div
        style={{
          display: "flex",
          gap: "0.75rem",
          flexWrap: "wrap",
          alignItems: "center",
          padding: "0 1rem",
        }}
      >
        <Tag type="blue" size="sm">
          Step {current.step} / {maxStep}
        </Tag>
        <Tag type="teal" size="sm">
          {current.numClusters} cluster{current.numClusters !== 1 ? "s" : ""}
        </Tag>
        {current.step > 0 && current.merged.length === 2 && (
          <>
            <Tag type="purple" size="sm">
              Merged: {current.merged[0].join(", ")} + {current.merged[1].join(", ")}
            </Tag>
            <Tag type="gray" size="sm">
              Distance: {current.distance.toFixed(4)}
            </Tag>
          </>
        )}
      </div>

      <GraphView elements={current.graph} height={480} totalClusters={current.numClusters} />
    </Stack>
  );
}

/** Tab view showing clustering iterations for t0 and t1. */
export function ClusterIterationsView() {
  const bundle = useRunStore((s) => s.bundle);
  if (!bundle) return null;

  return (
    <Tabs>
      <TabList aria-label="Time points – iterations" contained>
        <Tab>t0 (before)</Tab>
        <Tab>t1 (after)</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>
          <IterationPlayer side={bundle.t0} label="t0" />
        </TabPanel>
        <TabPanel>
          <IterationPlayer side={bundle.t1} label="t1" />
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}
