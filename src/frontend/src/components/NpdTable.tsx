import type { NpdRow } from "../types";

export function NpdTable({ rows }: { rows: NpdRow[] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>When</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={i}>
            <td>{r.metric}</td>
            <td>{r.when}</td>
            <td>{r.value.toFixed(4)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
