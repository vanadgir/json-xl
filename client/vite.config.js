import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      "/convert": "http://localhost:8000",
    },
  },
});
