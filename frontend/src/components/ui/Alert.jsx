export default function Alert({ variant = 'error', children, onDismiss }) {
  const styles = {
    error: 'border-red-800/30 bg-red-50 text-red-900',
    success: 'border-green-800/30 bg-green-50 text-green-900',
    info: 'border-craft-brown/20 bg-craft-cream text-craft-brown',
  };

  return (
    <div
      className={`flex items-start justify-between gap-3 rounded-xl border-2 px-4 py-3 text-sm ${styles[variant]}`}
      role="alert"
    >
      <div className="min-w-0 flex-1">{children}</div>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          className="shrink-0 opacity-70 hover:opacity-100"
          aria-label="Закрыть"
        >
          ×
        </button>
      )}
    </div>
  );
}
