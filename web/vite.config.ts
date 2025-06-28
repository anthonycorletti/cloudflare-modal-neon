import basicSsl from "@vitejs/plugin-basic-ssl";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig(({ mode }) => {
  let pluginArr = [];
  if (mode === "development") {
    pluginArr = [react(), basicSsl()];
  } else {
    pluginArr = [react()];
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
