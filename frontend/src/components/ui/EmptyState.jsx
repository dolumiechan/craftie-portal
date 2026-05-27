export default function EmptyState({ title, description, action }) {
  return (
    <div className="rounded-2xl border-2 border-dashed border-craft-brown/25 bg-craft-cream/50 px-6 py-10 text-center">
      {title && <p className="font-medium text-craft-brown">{title}</p>}
      {description && (
        <p className="mt-2 text-sm text-craft-brown/70">{description}</p>
      )}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
