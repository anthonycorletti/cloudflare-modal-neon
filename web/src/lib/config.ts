const env = import.meta.env;

const defaults = {
  ENV: env.MODE,
  WEB_BASE_URL: env.VITE_WEB_BASE_URL || "https://127.0.0.1:5173",
  SERVER_BASE_URL: env.VITE_SERVER_BASE_URL || "https://127.0.0.1:8000",
  SERVER_CLIENT_TRACE_ROUTE: env.VITE_SERVER_CLIENT_TRACE_ROUTE || "/client-traces",
};

export const CONFIG = {
  ...defaults,
};
