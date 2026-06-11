import { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import {
  purple60,
  cyan40,
  teal60,
  magenta40,
  red50,
  green30,
  blue50,
} from "@carbon/colors";
import type { CyElements } from "../types";

cytoscape.use(dagre);

// Carbon data-viz categorical palette (dark theme order); consistent across t0/t1
// thanks to backend cluster indexing.
export const CLUSTER_PALETTE = [purple60, cyan40, teal60, magenta40, red50, green30, blue50];

export function clusterColor(clusterId: string | undefined): string {
  if (!clusterId) return "#a8a8a8"; // gray-40
  const n = parseInt(clusterId.replace(/\D/g, ""), 10) || 0;
  return CLUSTER_PALETTE[n % CLUSTER_PALETTE.length];
}

interface Props {
  elements: CyElements;
  height?: number;
}

/** Cytoscape wrapper: dagre layout for directed graphs, cluster-colored nodes.
 *
 * Cytoscape cannot read CSS custom properties, so colors below are hex literals
 * mirroring the g100 tokens (text-primary #f4f4f4, gray-50 #8d8d8d).
 */
export function GraphView({ elements, height = 480 }: Props) {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const cy = cytoscape({
      container: ref.current,
      elements: [...elements.nodes, ...elements.edges],
      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            "background-color": (ele: cytoscape.NodeSingular) =>
              clusterColor(ele.data("cluster") as string | undefined),
            "font-size": 10,
            // Label below the node: white-on-fill fails contrast for light palette colors.
            "text-valign": "bottom",
            "text-margin-y": 4,
            color: "#f4f4f4",
          },
        },
        {
          selector: "edge",
          style: {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            width: 1.5,
            "line-color": "#8d8d8d",
            "target-arrow-color": "#8d8d8d",
          },
        },
      ],
      // nodeSep keeps long function-name labels from overlapping horizontally.
      layout: { name: "dagre", rankDir: "TB", nodeSep: 60, rankSep: 50 } as cytoscape.LayoutOptions,
    });
    return () => cy.destroy();
  }, [elements]);

  return <div className="graph-canvas" style={{ height }} ref={ref} />;
}
