import path from "path";
import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";
import basicSsl from "@vitejs/plugin-basic-ssl";

export default defineConfig(({ mode }) => {
  let pluginArr = [];
  if (mode === 'development') {
    pluginArr = [react(), basicSsl()];
  } else {
    pluginArr = [react()];
  }
  const plugins = pluginArr;
  //
  return {
    plugins,
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
  };
});
