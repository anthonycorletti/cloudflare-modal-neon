const env = import.meta.env;

const defaults = {
    ENV: env.MODE,
    SERVER_BASE_URL: env.VITE_SERVER_BASE_URL || "https://127.0.0.1:8000",
    WEB_BASE_URL: env.VITE_WEB_BASE_URL || "https://127.0.0.1:5173",
};

console.log("CONFIG", defaults);

export const CONFIG = {
    ...defaults,
};
