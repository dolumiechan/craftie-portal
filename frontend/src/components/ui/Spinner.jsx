export default function Spinner({ label = 'Загрузка…', className = '' }) {
  return (
    <div
      className={`flex flex-col items-center justify-center gap-3 py-12 ${className}`}
      role="status"
      aria-live="polite"
    >
      <span
        className="h-9 w-9 animate-spin rounded-full border-2 border-craft-brown/20 border-t-craft-brown"
        aria-hidden="true"
      />
      <span className="text-sm text-craft-brown/70">{label}</span>
    </div>
  );
}
