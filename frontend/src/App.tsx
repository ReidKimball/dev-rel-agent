import { useState, useRef, useEffect } from "react";
import { Bot, AlertCircle } from "lucide-react";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import TodoPanel from "./components/TodoPanel";
import { sendMessage } from "./api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Todo {
  content: string;
  status: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [todos, setTodos] = useState<Todo[]>([]);
  const [threadId, setThreadId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (content: string) => {
    const userMsg: Message = { role: "user", content };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const res = await sendMessage(content, threadId);
      setThreadId(res.thread_id);
      if (res.todos) setTodos(res.todos);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.response },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900">
      {/* Header */}
      <header className="shrink-0 border-b border-slate-700 bg-slate-800/80 px-6 py-3 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-emerald-600 flex items-center justify-center">
          <Bot size={20} />
        </div>
        <div>
          <h1 className="text-base font-semibold text-slate-100">
            DevRel Agent
          </h1>
          <p className="text-xs text-slate-400">
            AI-powered developer education &amp; codebase teaching
          </p>
        </div>
      </header>

      {/* Main area */}
      <div className="flex flex-1 min-h-0">
        {/* Chat column */}
        <div className="flex flex-col flex-1 min-w-0">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-center px-6">
                <div className="w-16 h-16 rounded-2xl bg-emerald-600/20 flex items-center justify-center mb-4">
                  <Bot size={32} className="text-emerald-400" />
                </div>
                <h2 className="text-xl font-semibold text-slate-200 mb-2">
                  Welcome to DevRel Agent
                </h2>
                <p className="text-sm text-slate-400 max-w-md mb-6">
                  I can help you understand any codebase. Point me at a
                  repository and ask me to explain its architecture, show code
                  examples, or teach you how it works.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg w-full">
                  {[
                    "Explain the overall architecture of this project",
                    "What are the main modules and how do they connect?",
                    "Show me a code example for the API client",
                    "Walk me through the request lifecycle",
                  ].map((prompt) => (
                    <button
                      key={prompt}
                      onClick={() => handleSend(prompt)}
                      className="text-left text-sm px-4 py-3 rounded-xl border border-slate-700 hover:border-indigo-500 hover:bg-slate-800 text-slate-300 transition-colors"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="max-w-3xl mx-auto">
              {messages.map((msg, i) => (
                <ChatMessage key={i} role={msg.role} content={msg.content} />
              ))}

              {loading && (
                <div className="flex gap-3 px-4 py-4">
                  <div className="shrink-0 w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center">
                    <Bot size={16} />
                  </div>
                  <div className="flex items-center gap-1 pt-2">
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce [animation-delay:0ms]" />
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce [animation-delay:150ms]" />
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce [animation-delay:300ms]" />
                  </div>
                </div>
              )}

              {error && (
                <div className="mx-4 my-2 p-3 rounded-lg bg-red-900/30 border border-red-800 flex items-center gap-2 text-sm text-red-300">
                  <AlertCircle size={16} />
                  {error}
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input */}
          <ChatInput onSend={handleSend} disabled={loading} />
        </div>

        {/* Todo panel */}
        <TodoPanel todos={todos} />
      </div>
    </div>
  );
}

export default App
