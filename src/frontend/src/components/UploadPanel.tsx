import { useState } from "react";
import {
  Dropdown,
  FileUploaderDropContainer,
  FileUploaderItem,
  FormItem,
  Stack,
} from "@carbon/react";
import { useRunStore } from "../state/runStore";
import { SAMPLE_IDS, SAMPLES } from "../samples";

interface SlotProps {
  label: string;
  fileName: string | null;
  onFile: (file: File) => void;
  onClear: () => void;
}

function UploadSlot({ label, fileName, onFile, onClear }: SlotProps) {
  return (
    <FormItem>
      <p className="cds--label">{label}</p>
      {fileName ? (
        <FileUploaderItem name={fileName} status="edit" onDelete={onClear} />
      ) : (
        <FileUploaderDropContainer
          labelText="Drag and drop a .py file or click to upload"
          accept={[".py"]}
          onAddFiles={(_e, { addedFiles }: { addedFiles: File[] }) => {
            if (addedFiles[0]) onFile(addedFiles[0]);
          }}
        />
      )}
    </FormItem>
  );
}

/** Upload two .py files (t0, t1), or load a bundled sample pair (tc1-tc4). */
export function UploadPanel() {
  const { setSources, sourceT0, sourceT1 } = useRunStore();
  const [fileNameT0, setFileNameT0] = useState<string | null>(null);
  const [fileNameT1, setFileNameT1] = useState<string | null>(null);

  async function onFile(which: "t0" | "t1", file: File) {
    const text = await file.text();
    if (which === "t0") {
      setSources(text, sourceT1);
      setFileNameT0(file.name);
    } else {
      setSources(sourceT0, text);
      setFileNameT1(file.name);
    }
  }

  function loadSample(id: string | null) {
    if (!id || !SAMPLES[id]) return;
    setSources(SAMPLES[id].t0, SAMPLES[id].t1);
    setFileNameT0(`${id}_t0.py`);
    setFileNameT1(`${id}_t1.py`);
  }

  return (
    <section>
      <Stack gap={5}>
        <h2 className="cds--type-heading-compact-01">Input</h2>
        <UploadSlot
          label="t0 (before)"
          fileName={fileNameT0}
          onFile={(f) => onFile("t0", f)}
          onClear={() => {
            setSources("", sourceT1);
            setFileNameT0(null);
          }}
        />
        <UploadSlot
          label="t1 (after)"
          fileName={fileNameT1}
          onFile={(f) => onFile("t1", f)}
          onClear={() => {
            setSources(sourceT0, "");
            setFileNameT1(null);
          }}
        />
        <Dropdown
          id="load-sample"
          titleText="Load sample"
          label="Choose a test case"
          items={SAMPLE_IDS}
          onChange={({ selectedItem }) => loadSample(selectedItem ?? null)}
        />
      </Stack>
    </section>
  );
}
