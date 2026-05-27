export default function InterestPicker({ categories, selectedIds, onChange }) {
  if (!categories?.length) {
    return <p className="text-sm text-craft-brown/60">Категории пока не загружены.</p>;
  }

  const toggle = (id) => {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((x) => x !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  };

  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
      {categories.map((cat) => {
        const checked = selectedIds.includes(cat.id);
        return (
          <label
            key={cat.id}
            className={`flex cursor-pointer items-center gap-2 rounded-xl border-2 px-3 py-2 text-sm transition-colors ${
              checked
                ? 'border-craft-brown bg-craft-cream font-medium'
                : 'border-craft-brown/25 bg-white hover:border-craft-brown/50'
            }`}
          >
            <input
              type="checkbox"
              checked={checked}
              onChange={() => toggle(cat.id)}
              className="accent-craft-brown"
            />
            <span className="text-craft-brown">{cat.name}</span>
          </label>
        );
      })}
    </div>
  );
}
