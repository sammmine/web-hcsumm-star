import { create } from "zustand";
import type { ArtifactBundle, JobStatus, PipelineConfig } from "../types";
import { DEFAULT_CONFIG } from "../types";

export type ViewMode = "direct" | "side-by-side" | "step-by-step" | "iterations";

interface RunState {
  config: PipelineConfig;
  setConfig: (patch: Partial<PipelineConfig>) => void;

  sourceT0: string;
  sourceT1: string;
  setSources: (t0: string, t1: string) => void;

  status: JobStatus | "idle";
  setStatus: (s: JobStatus | "idle") => void;

  bundle: ArtifactBundle | null;
  setBundle: (b: ArtifactBundle | null) => void;

  view: ViewMode;
  setView: (v: ViewMode) => void;
}

export const useRunStore = create<RunState>((set) => ({
  config: DEFAULT_CONFIG,
  setConfig: (patch) => set((s) => ({ config: { ...s.config, ...patch } })),

  sourceT0: "",
  sourceT1: "",
  setSources: (sourceT0, sourceT1) => set({ sourceT0, sourceT1 }),

  status: "idle",
  setStatus: (status) => set({ status }),

  bundle: null,
  setBundle: (bundle) => set({ bundle }),

  view: "direct",
  setView: (view) => set({ view }),
}));
