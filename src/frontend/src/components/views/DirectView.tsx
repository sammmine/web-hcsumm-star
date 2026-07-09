import { InlineNotification, Stack } from "@carbon/react";
import { useRunStore } from "../../state/runStore";
import { GraphView } from "../GraphView";
import { NpdTable } from "../NpdTable";
import { ClusterMembershipTable } from "../ClusterMembershipTable";

/** MVP: summary graphs t0 & t1 + cluster membership + NPD table. */
export function DirectView() {
  const bundle = useRunStore((s) => s.bundle);
  if (!bundle) return null;
  return (
    <Stack gap={6}>
      {bundle.warnings.length > 0 && (
        <Stack gap={3}>
          {bundle.warnings.map((w, i) => (
            <InlineNotification
              key={i}
              kind="warning"
              lowContrast
              hideCloseButton
              title="Pipeline warning"
              subtitle={w}
            />
          ))}
        </Stack>
      )}
      <div>
        <h3 className="cds--type-heading-02">Summary graph t0</h3>
        <GraphView elements={bundle.t0.summary} title="summary_t0_before" />
      </div>
      <div>
        <h3 className="cds--type-heading-02">Summary graph t1</h3>
        <GraphView elements={bundle.t1.summary} title="summary_t1_after" />
      </div>
      <div>
        <h3 className="cds--type-heading-02">NPD metrics</h3>
        <NpdTable rows={bundle.npd} />
      </div>
      <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
        <div>
          <h4 className="cds--type-heading-01">Cluster membership t0</h4>
          <ClusterMembershipTable membership={bundle.t0.membership} />
        </div>
        <div>
          <h4 className="cds--type-heading-01">Cluster membership t1</h4>
          <ClusterMembershipTable membership={bundle.t1.membership} />
        </div>
      </div>
    </Stack>
  );
}
