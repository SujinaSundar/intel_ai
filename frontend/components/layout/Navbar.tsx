export default function Navbar() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-800 bg-slate-950 px-8">
      <div>
        <h2 className="text-lg font-semibold text-white">
          Intel AI Trading Research Assistant
        </h2>

        <p className="text-sm text-slate-400">
          Multi-Agent AI Platform
        </p>
      </div>

      <div className="rounded-full bg-blue-600 px-4 py-2 text-sm text-white">
        Online
      </div>
    </header>
  );
}