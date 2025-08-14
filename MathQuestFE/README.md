
# MathQuest Frontend (React + Vite + Tailwind)

Mobile-first UI that talks to the FastAPI backend.

## Quick start
```bash
npm i
npm run dev
```

### API proxy (during dev)
Vite dev server proxies `/api` to `http://localhost:8000` by default.
Change target via env before `npm run dev`:

```bash
VITE_API_PROXY=http://localhost:8001 npm run dev
```

### Build
```bash
npm run build && npm run preview
```

### Config
- `VITE_API_URL` (optional) — to call a different origin (e.g., deployed backend).
  If unset, the app calls same-origin `/api` (good for reverse-proxy setups).
