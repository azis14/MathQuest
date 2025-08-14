
export default function Spinner({ className = '' }) {
  return (
    <div className={"animate-spin h-5 w-5 border-2 border-indigo-500 border-t-transparent rounded-full " + className} aria-label="loading" />
  )
}
