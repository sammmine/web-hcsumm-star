import { useRunStore } from "../../state/runStore";
import { GraphView } from "../GraphView";
import { NpdTable } from "../NpdTable";
import { ClusterMembershipTable } from "../ClusterMembershipTable";

/** MVP: summary graphs t0 & t1 + cluster membership + NPD table. */
export function DirectView() {
  const bundle = useRunStore((s) => s.bundle);
  if (!bundle) return null;
  return (
    <div>
      {bundle.warnings.length > 0 && (
        <p style={{ color: "#b07000" }}>⚠ {bundle.warnings.join("; ")}</p>
      )}
      <h3>Summary graph t0</h3>
      <GraphView elements={bundle.t0.summary} />
      <h3>Summary graph t1</h3>
      <GraphView elements={bundle.t1.summary} />
      <h3>NPD metrics</h3>
      <NpdTable rows={bundle.npd} />
      <div style={{ display: "flex", gap: 32 }}>
        <div>
          <h4>Cluster membership t0</h4>
          <ClusterMembershipTable membership={bundle.t0.membership} />
        </div>
        <div>
          <h4>Cluster membership t1</h4>
          <ClusterMembershipTable membership={bundle.t1.membership} />
        </div>
      </div>
    </div>
  );
}
