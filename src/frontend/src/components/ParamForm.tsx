import {
  Accordion,
  AccordionItem,
  Checkbox,
  FormGroup,
  NumberInput,
  Select,
  SelectItem,
  Stack,
} from "@carbon/react";
import { useRunStore } from "../state/runStore";
import type { BehaviourFeature, EmbeddingMode, PipelineConfig } from "../types";

const MODES: { value: EmbeddingMode; label: string }[] = [
  { value: "fused", label: "Fused (node2vec + behaviour)" },
  { value: "node2vec_only", label: "Node2vec only" },
  { value: "behaviour_only", label: "Behaviour only" },
];
const FEATURES: BehaviourFeature[] = ["EPL", "indeg", "outdeg", "depth", "pagerank"];

/** Carbon NumberInput reports `number | string`; only commit finite numbers. */
function num(value: number | string): number | null {
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
}

/**
 * Simple controls + collapsible Advanced/OFAT panel.
 * Embedding mode drives which params are enabled (see design §4):
 *  - node2vec_only -> node2vec params on, behaviour off
 *  - behaviour_only -> behaviour on, node2vec off
 *  - fused -> both + alpha/beta on
 */
export function ParamForm() {
  const { config, setConfig } = useRunStore();

  const node2vecActive = config.embedding_mode !== "behaviour_only";
  const behaviourActive = config.embedding_mode !== "node2vec_only";

  function toggleFeature(f: BehaviourFeature) {
    const has = config.behaviour_features.includes(f);
    setConfig({
      behaviour_features: has
        ? config.behaviour_features.filter((x) => x !== f)
        : [...config.behaviour_features, f],
    });
  }

  function numberField(key: keyof PipelineConfig, label: string, opts?: { step?: number; min?: number; disabled?: boolean }) {
    return (
      <NumberInput
        key={key}
        id={`param-${key}`}
        label={label}
        size="sm"
        min={opts?.min}
        step={opts?.step ?? 1}
        disabled={opts?.disabled}
        value={config[key] as number}
        onChange={(_e, { value }) => {
          const n = num(value);
          if (n !== null) setConfig({ [key]: n });
        }}
      />
    );
  }

  return (
    <section>
      <Stack gap={5}>
        <h2 className="cds--type-heading-compact-01">Parameters</h2>

        <Select
          id="embedding-mode"
          labelText="Embedding mode"
          value={config.embedding_mode}
          onChange={(e) => setConfig({ embedding_mode: e.target.value as EmbeddingMode })}
        >
          {MODES.map((m) => (
            <SelectItem key={m.value} value={m.value} text={m.label} />
          ))}
        </Select>

        <FormGroup legendText="Behaviour features">
          {FEATURES.map((f) => (
            <Checkbox
              key={f}
              id={`feature-${f}`}
              labelText={f}
              checked={config.behaviour_features.includes(f)}
              disabled={!behaviourActive}
              onChange={() => toggleFeature(f)}
            />
          ))}
        </FormGroup>

        {numberField("k_clusters", "K clusters", { min: 1 })}

        <Accordion>
          <AccordionItem title="Advanced / OFAT">
            <Stack gap={5}>
              <FormGroup legendText="node2vec">
                <Stack gap={4}>
                  {numberField("embed_dim", "EMBED_DIM", { min: 1, disabled: !node2vecActive })}
                  {numberField("walk_length", "WALK_LENGTH", { min: 1, disabled: !node2vecActive })}
                  {numberField("num_walks", "NUM_WALKS", { min: 1, disabled: !node2vecActive })}
                  {numberField("p_return", "P_RETURN", { step: 0.1, disabled: !node2vecActive })}
                  {numberField("q_inout", "Q_INOUT", { step: 0.1, disabled: !node2vecActive })}
                  {numberField("seed", "SEED", { disabled: !node2vecActive })}
                </Stack>
              </FormGroup>
              <FormGroup legendText="fusion">
                <Stack gap={4}>
                  {numberField("alpha", "alpha", { step: 0.1, disabled: config.embedding_mode !== "fused" })}
                  {numberField("beta", "beta", { step: 0.1, disabled: config.embedding_mode !== "fused" })}
                </Stack>
              </FormGroup>
            </Stack>
          </AccordionItem>
        </Accordion>
      </Stack>
    </section>
  );
}
