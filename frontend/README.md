# JanSaathi Frontend

The presentation layer for JanSaathi is built to be lighting fast, fully responsive, and incredibly accessible.

## Tech Stack
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **State Management:** React Hooks + Context API
- **Deployment Ready:** Vercel

## Architecture
- **`/app`**: Contains all routes (Dashboard, Login, Chat).
- **`/components`**: Reusable UI components.
- **`/lib`**: Utility functions and Authentication contexts.

## Setup Instructions
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Ensure the backend is running at `http://127.0.0.1:8000` (or configure `.env.local` with `NEXT_PUBLIC_API_URL`).

## Design Philosophy
We utilized **Glassmorphism**, dark modes, and subtle ambient glows to provide a premium, enterprise-grade feel without relying on heavy frontend assets. The UI is completely responsive and optimized for mobile users across India.
