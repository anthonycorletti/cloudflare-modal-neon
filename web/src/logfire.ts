import { getWebAutoInstrumentations } from "@opentelemetry/auto-instrumentations-web";
import * as logfire from '@pydantic/logfire-browser';
import packageJson from '../package.json';
import { CONFIG } from "./lib/config";

logfire.configure({
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
