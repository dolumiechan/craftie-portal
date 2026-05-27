export default function InfoPage({ title, children }) {
  return (
    <article className="mx-auto max-w-2xl rounded-2xl border-2 border-craft-brown bg-craft-beige p-6 sm:p-10">
      <h1 className="text-2xl font-bold text-craft-brown">{title}</h1>
      <div className="mt-4 space-y-3 text-sm leading-relaxed text-craft-brown/90">{children}</div>
    </article>
  );
}
