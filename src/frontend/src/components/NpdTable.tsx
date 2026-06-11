import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@carbon/react";
import type { NpdRow } from "../types";

export function NpdTable({ rows }: { rows: NpdRow[] }) {
  return (
    <Table size="sm" useZebraStyles>
      <TableHead>
        <TableRow>
          <TableHeader>Metric</TableHeader>
          <TableHeader>When</TableHeader>
          <TableHeader>Value</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.map((r, i) => (
          <TableRow key={i}>
            <TableCell>{r.metric}</TableCell>
            <TableCell>{r.when}</TableCell>
            <TableCell>{r.value.toFixed(4)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
