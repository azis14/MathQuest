
export default function ErrorBanner({ message }) {
  if (!message) return null
  return (
    <div className="rounded-md bg-red-50 border border-red-200 text-red-700 px-3 py-2 text-sm">
      {message}
    </div>
  )
}
