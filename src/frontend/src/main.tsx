import React from "react";
import ReactDOM from "react-dom/client";
import { GlobalTheme, Theme } from "@carbon/react";
import App from "./App";

import "@fontsource/ibm-plex-sans/300.css";
import "@fontsource/ibm-plex-sans/400.css";
import "@fontsource/ibm-plex-sans/600.css";
import "@fontsource/ibm-plex-mono/400.css";
import "./index.scss";

// Carbon emits theme tokens only under zone classes (.cds--g100), not :root —
// the Theme wrapper provides the class; GlobalTheme aligns portal'd elements (tooltips).
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <GlobalTheme theme="g100">
      <Theme theme="g100" className="theme-root">
        <App />
      </Theme>
    </GlobalTheme>
  </React.StrictMode>,
);
