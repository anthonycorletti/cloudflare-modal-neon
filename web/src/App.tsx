import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { ThemeProvider } from "@/components/theme-provider";
import { cn } from "@/lib/utils";
import { CONFIG } from "@/lib/config";

export default function App() {
  const [count, setCount] = useState(0);
  const baseUrl = CONFIG.WEB_BASE_URL;

  const [status, setStatus] = useState({
    message: "Checking system health...",
    version: "",
  });

  useEffect(() => {
    async function fetchStatus() {
      try {
        const response = await fetch(`${baseUrl}/readyz`);
        const data = await response.json();
        if (data.version) {
          data.version = `v${data.version}`;
        }
        setStatus({
          message: data.message || "Error fetching status",
          version: data.version || "unknown",
        });
      } catch (error) {
        console.error("Error fetching status", error);
        setStatus({
          message: "Error fetching status",
          version: "unknown",
        });
      }
    }

    fetchStatus();
  }, [baseUrl]);

  const { message, version } = status;

  return (
    <ThemeProvider>
      <div
        className={cn("flex flex-row items-center justify-center space-x-2")}
      >
        <img src="/vite.svg" alt="it's react" />
        <div className={cn("flex items-center justify-center min-h-screen")}>
          <Button onClick={() => setCount(count + 1)}>Click me {count}</Button>
        </div>
        <div className={cn("flex items-center justify-center min-h-screen")}>
          <Button variant={"destructive"} onClick={() => { throw new Error("Sentry Test Error"); }}>Oh 💩</Button>
        </div>
      </div>

      <footer
        className={cn(
          "absolute text-xs opacity-50 flex flex-col sm:flex-col w-full items-left bottom-0 p-5 space-y-2",
        )}
      >
        <div
          className={cn(
            "relative text-left flex flex-row space-x-2 items-center",
          )}
        >
          <div>{baseUrl}</div>
          <div>
            {version.length > 0
              ? `${message} @ ${version}`
              : "Checking system health..."}
          </div>
        </div>
        <div className={cn("text-left")}>
          © {new Date().getFullYear()} acme inc.
        </div>
      </footer>
    </ThemeProvider>
  );
}
