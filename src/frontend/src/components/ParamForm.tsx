import { useState } from "react";
import { useRunStore } from "../state/runStore";
import type { BehaviourFeature, EmbeddingMode } from "../types";

const MODES: EmbeddingMode[] = ["node2vec_only", "behaviour_only", "fused"];
const FEATURES: BehaviourFeature[] = ["EPL", "indeg", "outdeg", "depth", "pagerank"];

/**
 * Simple controls + collapsible Advanced/OFAT panel.
 * Embedding mode drives which params are enabled (see design §4):
 *  - node2vec_only -> node2vec params on, behaviour off
 *  - behaviour_only -> behaviour on, node2vec off
 *  - fused -> both + alpha/beta on
 */
export function ParamForm() {
  const { config, setConfig } = useRunStore();
  const [advanced, setAdvanced] = useState(false);

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

  return (
    <section>
      <h3>Parameters</h3>

      <label>
        Embedding mode:{" "}
        <select
          value={config.embedding_mode}
          onChange={(e) => setConfig({ embedding_mode: e.target.value as EmbeddingMode })}
        >
          {MODES.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </label>

      <fieldset disabled={!behaviourActive}>
        <legend>Behaviour features</legend>
        {FEATURES.map((f) => (
          <label key={f} style={{ display: "block" }}>
            <input
              type="checkbox"
              checked={config.behaviour_features.includes(f)}
              onChange={() => toggleFeature(f)}
            />
            {f}
          </label>
        ))}
      </fieldset>

      <label>
        K clusters:{" "}
        <input
          type="number"
          min={1}
          value={config.k_clusters}
          onChange={(e) => setConfig({ k_clusters: Number(e.target.value) })}
        />
      </label>

      <details open={advanced} onToggle={(e) => setAdvanced((e.target as HTMLDetailsElement).open)}>
        <summary>Advanced / OFAT</summary>
        <fieldset disabled={!node2vecActive}>
          <legend>node2vec</legend>
          {(
            [
              ["embed_dim", "EMBED_DIM"],
              ["walk_length", "WALK_LENGTH"],
              ["num_walks", "NUM_WALKS"],
              ["p_return", "P_RETURN"],
              ["q_inout", "Q_INOUT"],
              ["seed", "SEED"],
            ] as const
          ).map(([key, label]) => (
            <label key={key} style={{ display: "block" }}>
              {label}:{" "}
              <input
                type="number"
                value={config[key] as number}
                onChange={(e) => setConfig({ [key]: Number(e.target.value) })}
              />
            </label>
          ))}
        </fieldset>
        <fieldset disabled={config.embedding_mode !== "fused"}>
          <legend>fusion</legend>
          <label>
            alpha:{" "}
            <input
              type="number"
              step={0.1}
              value={config.alpha}
              onChange={(e) => setConfig({ alpha: Number(e.target.value) })}
            />
          </label>
          <label>
            beta:{" "}
            <input
              type="number"
              step={0.1}
              value={config.beta}
              onChange={(e) => setConfig({ beta: Number(e.target.value) })}
            />
          </label>
        </fieldset>
      </details>
    </section>
  );
}
