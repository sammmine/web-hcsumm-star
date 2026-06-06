import { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import type { CyElements } from "../types";

cytoscape.use(dagre);

// Palette for cluster coloring; consistent across t0/t1 thanks to backend cluster indexing.
const PALETTE = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1"];

export function clusterColor(clusterId: string | undefined): string {
  if (!clusterId) return "#999";
  const n = parseInt(clusterId.replace(/\D/g, ""), 10) || 0;
  return PALETTE[n % PALETTE.length];
}

interface Props {
  elements: CyElements;
  height?: number;
}

/** Cytoscape wrapper: dagre layout for directed graphs, cluster-colored nodes. */
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
            "text-valign": "center",
            color: "#fff",
          },
        },
        {
          selector: "edge",
          style: {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            width: 1.5,
            "line-color": "#aaa",
            "target-arrow-color": "#aaa",
          },
        },
      ],
      layout: { name: "dagre", rankDir: "TB" } as cytoscape.LayoutOptions,
    });
    return () => cy.destroy();
  }, [elements]);

  return <div className="graph-canvas" style={{ height }} ref={ref} />;
}
