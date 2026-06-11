import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@carbon/react";

const MONO: React.CSSProperties = { fontFamily: "'IBM Plex Mono', monospace" };

/** Per-node vector table (behaviour features, embedding, fusion). */
export function VectorTable({
  headers,
  data,
}: {
  headers: string[];
  data: Record<string, number[]>;
}) {
  const nodes = Object.keys(data).sort();
  return (
    <Table size="sm" useZebraStyles>
      <TableHead>
        <TableRow>
          {headers.map((h) => (
            <TableHeader key={h}>{h}</TableHeader>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {nodes.map((node) => (
          <TableRow key={node}>
            <TableCell style={MONO}>{node}</TableCell>
            {data[node].map((v, i) => (
              <TableCell key={i}>{v.toFixed(4)}</TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

/** Pairwise euclidean distance matrix; labels must follow the backend's sorted-node order. */
export function DistanceMatrixTable({
  matrix,
  labels,
}: {
  matrix: number[][];
  labels: string[];
}) {
  // Defensive: backend orders rows by Python sorted(nodes); fall back to indices on mismatch.
  const axis = labels.length === matrix.length ? labels : matrix.map((_, i) => String(i));
  return (
    <div className="matrix-scroll">
      <Table size="sm" useZebraStyles>
        <TableHead>
          <TableRow>
            <TableHeader />
            {axis.map((l) => (
              <TableHeader key={l} style={MONO}>
                {l}
              </TableHeader>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {matrix.map((row, i) => (
            <TableRow key={axis[i]}>
              <TableCell style={MONO}>{axis[i]}</TableCell>
              {row.map((v, j) => (
                <TableCell key={j}>{v.toFixed(4)}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
