import { clusterColor } from "./GraphView";

export function ClusterMembershipTable({ membership }: { membership: Record<string, string> }) {
  const entries = Object.entries(membership).sort((a, b) => a[1].localeCompare(b[1]));
  return (
    <table>
      <thead>
        <tr>
          <th>Node</th>
          <th>Cluster</th>
        </tr>
      </thead>
      <tbody>
        {entries.map(([node, cid]) => (
          <tr key={node}>
            <td>{node}</td>
            <td style={{ color: clusterColor(cid) }}>{cid}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
