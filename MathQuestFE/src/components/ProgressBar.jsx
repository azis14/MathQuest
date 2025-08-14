
export default function ProgressBar({ value = 0 }) {
  const pct = Math.round(Math.max(0, Math.min(1, value)) * 100)
  return (
    <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
      <div
        className="h-full bg-indigo-500 transition-[width] duration-700 ease-out"
        style={{ width: pct + '%' }}
      />
    </div>
  )
}
