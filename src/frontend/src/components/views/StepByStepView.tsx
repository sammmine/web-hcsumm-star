import { useState } from "react";
import {
  Accordion,
  AccordionItem,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@carbon/react";
import { useRunStore } from "../../state/runStore";
import type { SideBundle } from "../../types";
import { GraphView } from "../GraphView";
import { DistanceMatrixTable, VectorTable } from "../StageTables";

const ALL_FEATURES = ["EPL", "indeg", "outdeg", "depth", "pagerank"];

function dimHeaders(data: Record<string, number[]>): string[] {
  const first = Object.values(data)[0] ?? [];
  return ["Node", ...first.map((_, i) => `dim${i}`)];
}

/** Cytoscape measures its container at mount; only mount the graph once the panel is open. */
function GraphAccordionItem({
  title,
  elements,
  defaultOpen = false,
}: {
  title: string;
  elements: SideBundle["callgraph"];
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <AccordionItem title={title} open={open} onHeadingClick={({ isOpen }) => setOpen(isOpen)}>
      {open && <GraphView elements={elements} height={360} title={title} />}
    </AccordionItem>
  );
}

function SideStages({ side, selectedFeatures }: { side: SideBundle; selectedFeatures: string[] }) {
  const { stages } = side;
  const hasEmbedding = Object.keys(stages.embedding).length > 0;
  const fusionNodes = Object.keys(stages.fusion).sort();

  const featureHeaders = ["Node", ...selectedFeatures];
  const filteredFeaturesData = Object.fromEntries(
    Object.entries(stages.features).map(([node, vals]) => {
      const filteredVals = selectedFeatures.map((f) => {
        const idx = ALL_FEATURES.indexOf(f);
        return vals[idx];
      });
      return [node, filteredVals];
    })
  );

  return (
    <Accordion>
      <GraphAccordionItem title="1 — Call graph" elements={side.callgraph} defaultOpen />
      <AccordionItem title="2 — Behaviour features f*(v)">
        <VectorTable headers={featureHeaders} data={filteredFeaturesData} />
      </AccordionItem>
      <AccordionItem title="3 — Node2vec embedding e'(v)">
        {hasEmbedding ? (
          <VectorTable headers={dimHeaders(stages.embedding)} data={stages.embedding} />
        ) : (
          <p className="cds--type-body-01">Not computed for this embedding mode.</p>
        )}
      </AccordionItem>
      <AccordionItem title="4 — Cluster vector x(v)">
        <VectorTable headers={dimHeaders(stages.fusion)} data={stages.fusion} />
      </AccordionItem>
      <AccordionItem title="5 — Distance matrix">
        <DistanceMatrixTable matrix={stages.distance_matrix} labels={fusionNodes} />
      </AccordionItem>
      <GraphAccordionItem title="6 — Summary graph" elements={side.summary} />
    </Accordion>
  );
}

/** Every pipeline stage per time point: graphs + the intermediate numeric artifacts. */
export function StepByStepView() {
  const bundle = useRunStore((s) => s.bundle);
  if (!bundle) return null;
  return (
    <Tabs>
      <TabList aria-label="Time points" contained>
        <Tab>t0 (before)</Tab>
        <Tab>t1 (after)</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>
          <SideStages side={bundle.t0} selectedFeatures={bundle.config.behaviour_features} />
        </TabPanel>
        <TabPanel>
          <SideStages side={bundle.t1} selectedFeatures={bundle.config.behaviour_features} />
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}
