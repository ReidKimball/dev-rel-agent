const API_BASE = "http://localhost:8000";

export interface ChatResponse {
  response: string;
  thread_id: string;
  todos: { content: string; status: string }[] | null;
}

export async function sendMessage(
  message: string,
  threadId?: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, thread_id: threadId }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function checkHealth(): Promise<{
  status: string;
  target_repo: string;
  agent_ready: boolean;
}> {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error("Backend unavailable");
  return res.json();
}
