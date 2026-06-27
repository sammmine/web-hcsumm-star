// Mirror of the backend ArtifactBundle (see doc/Desain Teknis Web HCSumm.md §4).

export type EmbeddingMode = "node2vec_only" | "behaviour_only" | "fused";
export type BehaviourFeature = "EPL" | "indeg" | "outdeg" | "depth" | "pagerank";

export interface PipelineConfig {
  embedding_mode: EmbeddingMode;
  behaviour_features: BehaviourFeature[];
  k_clusters: number;
  embed_dim: number;
  walk_length: number;
  num_walks: number;
  p_return: number;
  q_inout: number;
  seed: number;
  window: number;
  epochs: number;
  alpha: number;
  beta: number;
  max_paths: number;
  path_cutoff: number | null;
}

export const DEFAULT_CONFIG: PipelineConfig = {
  embedding_mode: "fused",
  behaviour_features: ["EPL", "indeg", "outdeg", "depth"],
  k_clusters: 2,
  embed_dim: 4,
  walk_length: 10,
  num_walks: 200,
  p_return: 1.0,
  q_inout: 1.0,
  seed: 42,
  window: 5,
  epochs: 100,
  alpha: 1.0,
  beta: 1.0,
  max_paths: 50000,
  path_cutoff: null,
};

// Cytoscape element collections.
export interface CyElements {
  nodes: { data: Record<string, unknown> }[];
  edges: { data: Record<string, unknown> }[];
}

export interface ClusterIterationStep {
  step: number;
  /** Two groups of node names that were merged in this step. */
  merged: string[][];
  distance: number;
  numClusters: number;
  graph: CyElements;
}

export interface SideBundle {
  callgraph: CyElements;
  summary: CyElements;
  membership: Record<string, string>;
  linkage: number[][];
  iterations: ClusterIterationStep[];
  stages: {
    features: Record<string, number[]>;
    embedding: Record<string, number[]>;
    fusion: Record<string, number[]>;
    distance_matrix: number[][];
  };
}

export interface NpdRow {
  metric: string;
  when: "before" | "after";
  value: number;
}

export interface ArtifactBundle {
  config: PipelineConfig;
  t0: SideBundle;
  t1: SideBundle;
  npd: NpdRow[];
  warnings: string[];
}

export type JobStatus = "pending" | "running" | "done" | "error";
