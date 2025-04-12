import path from "path";
import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";
import basicSsl from "@vitejs/plugin-basic-ssl";

export default defineConfig(({ mode }) => {
  const plugins = [react()];

  if (mode === 'development') {
    plugins.push(basicSsl());
  }

  return {
    plugins,
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
  };
});
