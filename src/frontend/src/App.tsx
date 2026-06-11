import {
  Button,
  ContentSwitcher,
  DataTableSkeleton,
  InlineLoading,
  SkeletonPlaceholder,
  Stack,
  Switch,
} from "@carbon/react";
import { UploadPanel } from "./components/UploadPanel";
import { ParamForm } from "./components/ParamForm";
import { DirectView } from "./components/views/DirectView";
import { SideBySideView } from "./components/views/SideBySideView";
import { StepByStepView } from "./components/views/StepByStepView";
import { createRun, pollRun } from "./api/client";
import { useRunStore, type ViewMode } from "./state/runStore";

const VIEWS: { id: ViewMode; label: string }[] = [
  { id: "direct", label: "Direct" },
  { id: "side-by-side", label: "Side-by-side" },
  { id: "step-by-step", label: "Step-by-step" },
];

function RunStatus({ status }: { status: ReturnType<typeof useRunStore.getState>["status"] }) {
  if (status === "idle") return null;
  if (status === "done") {
    return <InlineLoading status="finished" description="Done" />;
  }
  if (status === "error") {
    return <InlineLoading status="error" description="Run failed" />;
  }
  return <InlineLoading status="active" description="Running pipeline..." />;
}

export default function App() {
  const { config, sourceT0, sourceT1, status, setStatus, setBundle, view, setView, bundle } =
    useRunStore();

  const isRunning = status === "pending" || status === "running";

  async function run() {
    if (!sourceT0 || !sourceT1) return;
    setStatus("pending");
    try {
      const jobId = await createRun(sourceT0, sourceT1, config);
      const result = await pollRun(jobId, { onStatus: setStatus });
      setBundle(result);
      setStatus("done");
    } catch (e) {
      console.error(e);
      setStatus("error");
    }
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <Stack gap={6}>
          <h1 className="cds--type-heading-03">Web HCSumm*</h1>
          <UploadPanel />
          <ParamForm />
          <Stack gap={3}>
            <Button
              kind="primary"
              onClick={run}
              disabled={!sourceT0 || !sourceT1 || isRunning}
              style={{ width: "100%", maxWidth: "none" }}
            >
              Run pipeline
            </Button>
            <RunStatus status={status} />
          </Stack>
        </Stack>
      </aside>
      <main className="main">
        <Stack gap={5}>
          <ContentSwitcher
            selectedIndex={VIEWS.findIndex((v) => v.id === view)}
            onChange={(d) => {
              const idx = d.index as number;
              if (VIEWS[idx]) setView(VIEWS[idx].id);
            }}
            size="md"
          >
            {VIEWS.map((v) => (
              <Switch key={v.id} name={v.id} text={v.label} disabled={!bundle && !isRunning} />
            ))}
          </ContentSwitcher>
          {isRunning && (
            <Stack gap={5}>
              <SkeletonPlaceholder className="graph-skeleton" />
              <DataTableSkeleton columnCount={3} rowCount={5} showHeader={false} showToolbar={false} />
            </Stack>
          )}
          {!isRunning && !bundle && (
            <p className="cds--type-body-01">
              Upload t0 &amp; t1 (or load a sample), set parameters, then run the pipeline.
            </p>
          )}
          {!isRunning && bundle && view === "direct" && <DirectView />}
          {!isRunning && bundle && view === "side-by-side" && <SideBySideView />}
          {!isRunning && bundle && view === "step-by-step" && <StepByStepView />}
        </Stack>
      </main>
    </div>
  );
}
