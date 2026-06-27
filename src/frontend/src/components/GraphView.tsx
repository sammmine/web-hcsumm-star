import { useEffect, useRef, useState, useId } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import { Slider } from "@carbon/react";
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
  const cyRef = useRef<cytoscape.Core | null>(null);
  const [zoom, setZoom] = useState(100);
  const sliderId = useId();

  useEffect(() => {
    if (!ref.current) return;
    const cy = cytoscape({
      container: ref.current,
      userZoomingEnabled: false,
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
    
    cyRef.current = cy;
    cy.on("layoutstop", () => {
      setZoom(Math.round(cy.zoom() * 100));
    });

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [elements]);

  return (
    <div style={{ position: "relative", border: "1px solid #393939", borderRadius: 4 }}>
      <div className="graph-canvas" style={{ height }} ref={ref} />
      <div
        style={{
          position: "absolute",
          bottom: 16,
          left: 16,
          right: 16,
          background: "rgba(38, 38, 38, 0.9)",
          padding: "8px 16px",
          borderRadius: 4,
          display: "flex",
          alignItems: "center",
        }}
      >
        <div style={{ flex: 1 }}>
          <Slider
            id={sliderId}
            labelText="Zoom"
            value={zoom}
            min={10}
            max={300}
            step={10}
            hideTextInput
            onChange={(d: { value: number }) => {
              setZoom(d.value);
              if (cyRef.current) cyRef.current.zoom(d.value / 100);
            }}
          />
        </div>
        <div style={{ marginLeft: "1rem", color: "#f4f4f4", fontFamily: "sans-serif", fontSize: 12, minWidth: "40px", textAlign: "right" }}>
          {zoom}%
        </div>
      </div>
    </div>
  );
}
