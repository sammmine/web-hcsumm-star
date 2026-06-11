import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@carbon/react";
import { clusterColor } from "./GraphView";

export function ClusterMembershipTable({ membership }: { membership: Record<string, string> }) {
  const entries = Object.entries(membership).sort((a, b) => a[1].localeCompare(b[1]));
  return (
    <Table size="sm" useZebraStyles>
      <TableHead>
        <TableRow>
          <TableHeader>Node</TableHeader>
          <TableHeader>Cluster</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {entries.map(([node, cid]) => (
          <TableRow key={node}>
            <TableCell>{node}</TableCell>
            <TableCell>
              <span className="cluster-swatch" style={{ background: clusterColor(cid) }} />
              {cid}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
