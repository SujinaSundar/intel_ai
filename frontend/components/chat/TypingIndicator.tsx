export default function TypingIndicator() {
  return (
    <div className="flex justify-start mb-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900 px-5 py-4">
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400"></span>
          <span
            className="h-2 w-2 animate-bounce rounded-full bg-slate-400"
            style={{ animationDelay: "0.15s" }}
          ></span>
          <span
            className="h-2 w-2 animate-bounce rounded-full bg-slate-400"
            style={{ animationDelay: "0.3s" }}
          ></span>
        </div>
      </div>
    </div>
  );
}