import { CheckCircle2, Circle, Loader2 } from "lucide-react";

interface Todo {
  content: string;
  status: string;
}

interface TodoPanelProps {
  todos: Todo[];
}

function StatusIcon({ status }: { status: string }) {
  switch (status) {
    case "completed":
      return <CheckCircle2 size={14} className="text-emerald-400" />;
    case "in_progress":
      return <Loader2 size={14} className="text-amber-400 animate-spin" />;
    default:
      return <Circle size={14} className="text-slate-500" />;
  }
}

export default function TodoPanel({ todos }: TodoPanelProps) {
  if (todos.length === 0) return null;

  return (
    <div className="border-l border-slate-700 w-72 shrink-0 bg-slate-800/50 p-4 overflow-y-auto">
      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
        Agent Plan
      </h3>
      <ul className="space-y-2">
        {todos.map((todo, i) => (
          <li key={i} className="flex items-start gap-2 text-sm">
            <span className="mt-0.5">
              <StatusIcon status={todo.status} />
            </span>
            <span
              className={
                todo.status === "completed"
                  ? "text-slate-500 line-through"
                  : "text-slate-300"
              }
            >
              {todo.content}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
