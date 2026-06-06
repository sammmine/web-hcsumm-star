import { useRunStore } from "../state/runStore";

/** Upload two .py files (t0, t1). TODO: add "load sample" using bundled tc1-tc4. */
export function UploadPanel() {
  const { setSources, sourceT0, sourceT1 } = useRunStore();

  async function onFile(which: "t0" | "t1", file: File | undefined) {
    if (!file) return;
    const text = await file.text();
    if (which === "t0") setSources(text, sourceT1);
    else setSources(sourceT0, text);
  }

  return (
    <section>
      <h3>Upload</h3>
      <label>
        t0: <input type="file" accept=".py" onChange={(e) => onFile("t0", e.target.files?.[0])} />
      </label>
      <br />
      <label>
        t1: <input type="file" accept=".py" onChange={(e) => onFile("t1", e.target.files?.[0])} />
      </label>
    </section>
  );
}
