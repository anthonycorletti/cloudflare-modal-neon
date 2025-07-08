import tailwindcss from '@tailwindcss/vite';
import basicSsl from "@vitejs/plugin-basic-ssl";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { defineConfig } from "vite";


export default defineConfig(({ mode }) => {
  let pluginArr = [];
  if (mode === "development") {
    pluginArr = [react(), tailwindcss(), basicSsl()];
  } else {
    pluginArr = [react(), tailwindcss()];
  }
  const plugins = pluginArr;
  return {
    plugins,
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
  };
});
