import { Bot, User } from "lucide-react";
import Markdown from "react-markdown";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export default function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div className={`flex gap-3 px-4 py-4 ${isUser ? "bg-slate-800/40" : ""}`}>
      <div
        className={`shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
          isUser ? "bg-indigo-600" : "bg-emerald-600"
        }`}
      >
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>
      <div className="min-w-0 flex-1 prose prose-invert prose-sm max-w-none">
        <Markdown
          components={{
            code({ className, children, ...props }) {
              const isBlock = className?.startsWith("language-");
              if (isBlock) {
                return (
                  <pre className="bg-slate-900 rounded-lg p-3 overflow-x-auto text-sm">
                    <code className={className} {...props}>
                      {children}
                    </code>
                  </pre>
                );
              }
              return (
                <code
                  className="bg-slate-700 px-1.5 py-0.5 rounded text-emerald-300 text-sm"
                  {...props}
                >
                  {children}
                </code>
              );
            },
          }}
        >
          {content}
        </Markdown>
      </div>
    </div>
  );
}
