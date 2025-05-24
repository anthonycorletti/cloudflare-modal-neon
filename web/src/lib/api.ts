import { CONFIG } from "./config";

export type apiRequest = {
  method: string;
  path: string;
  params?: URLSearchParams;
  body?: unknown;
};

export async function makeApiRequest(request: apiRequest): Promise<unknown> {
  const response = await fetch(`${CONFIG.WEB_BASE_URL}${request.path}`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    method: request.method,
    body: JSON.stringify(request.body),
  });

  if (response.ok) {
    return await response.json();
  } else if (response.status === 401) {
    return { error: "Unauthorized" };
  } else {
    // check if there is a response body
    const errorJson = await response.json();
    if (errorJson) {
      console.error(errorJson);
    } else {
      console.error(response.statusText);
    }
  }
}
