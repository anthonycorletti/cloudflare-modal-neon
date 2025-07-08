import { getWebAutoInstrumentations } from "@opentelemetry/auto-instrumentations-web";
import * as logfire from '@pydantic/logfire-browser';
import packageJson from '../package.json';
import { CONFIG } from "./lib/config";

// if config.env is development pass
if (CONFIG.ENV === 'development') {
    console.warn("Logfire is not initialized in development mode. Set CONFIG.ENV to 'production' to enable logging.");
} else {

    logfire.configure({
        environment: CONFIG.ENV,
        traceUrl: CONFIG.SERVER_BASE_URL + CONFIG.SERVER_CLIENT_TRACE_ROUTE,
        serviceName: `web-${CONFIG.ENV}`,
        serviceVersion: packageJson.version,
        // The instrumentations to use
        // https://www.npmjs.com/package/@opentelemetry/auto-instrumentations-web - for more options and configuration
        instrumentations: [
            getWebAutoInstrumentations()
        ],
        // This outputs details about the generated spans in the browser console, use only in development and for troubleshooting.
        diagLogLevel: (CONFIG.ENV === 'development') ? logfire.DiagLogLevel.ALL : logfire.DiagLogLevel.WARN,
    })

    window.addEventListener("error", (event) => {
        logfire.error("Uncaught error", {
            message: event.message,
            stack: event.error?.stack,
            error: event.error,
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno,
        });
    });

    window.addEventListener("unhandledrejection", (event) => {
        logfire.error("Unhandled promise rejection", {
            reason: event.reason,
            stack: event.reason?.stack,
        });
    });

    logfire.error("Logfire initialized! 🔥");

}
