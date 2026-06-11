import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy /api to the FastAPI backend during development.
export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      scss: {
        // Carbon's SCSS triggers dart-sass deprecation warnings; keep the terminal usable.
        quietDeps: true,
        silenceDeprecations: ["mixed-decls", "global-builtin", "legacy-js-api"],
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
