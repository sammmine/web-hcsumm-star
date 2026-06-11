// Bundled sample inputs (copies of research/testing/t2-12-20-mei test cases),
// inlined as strings via Vite's ?raw imports.
import tc1T0 from "./tc1_t0.py?raw";
import tc1T1 from "./tc1_t1.py?raw";
import tc2T0 from "./tc2_t0.py?raw";
import tc2T1 from "./tc2_t1.py?raw";
import tc3T0 from "./tc3_t0.py?raw";
import tc3T1 from "./tc3_t1.py?raw";
import tc4T0 from "./tc4_t0.py?raw";
import tc4T1 from "./tc4_t1.py?raw";

export interface SamplePair {
  t0: string;
  t1: string;
}

export const SAMPLES: Record<string, SamplePair> = {
  tc1: { t0: tc1T0, t1: tc1T1 },
  tc2: { t0: tc2T0, t1: tc2T1 },
  tc3: { t0: tc3T0, t1: tc3T1 },
  tc4: { t0: tc4T0, t1: tc4T1 },
};

export const SAMPLE_IDS = Object.keys(SAMPLES);
