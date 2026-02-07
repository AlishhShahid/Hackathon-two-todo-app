# Quickstart: Public Landing Page

**Feature**: 004-public-landing
**Date**: 2026-02-07

## Prerequisites

- Node.js 18+
- Frontend dependencies installed (`cd frontend && npm install`)
- Frontend dev server running (`npm run dev`)

## Development

### 1. Start the Development Server

```bash
cd frontend
npm run dev
```

The app will be available at `http://localhost:3000` (or next available port).

### 2. View the Landing Page

Navigate to the root URL: `http://localhost:3000/`

### 3. File Locations

| Component | Path |
|-----------|------|
| Landing Page Route | `app/page.tsx` |
| Hero Component | `components/landing/Hero.tsx` |
| Features Component | `components/landing/Features.tsx` |
| Feature Card | `components/landing/FeatureCard.tsx` |

## Testing Checklist

### Visual Testing

- [ ] Hero section displays correctly with headline, subheadline, and buttons
- [ ] Features section shows 3 feature cards in a grid
- [ ] "Get Started" button navigates to `/register`
- [ ] "Sign In" button navigates to `/login`

### Responsive Testing

- [ ] Mobile (320px-767px): Stacked layout, readable text
- [ ] Tablet (768px-1023px): Adjusted grid layout
- [ ] Desktop (1024px+): Full horizontal layout

### SEO Testing

- [ ] Page title appears in browser tab
- [ ] View source shows meta description tag
- [ ] Semantic HTML (h1, h2, proper landmarks)

### Accessibility Testing

- [ ] All buttons have minimum 44px touch target
- [ ] Proper heading hierarchy (single h1)
- [ ] Color contrast meets WCAG standards

## Quick Verification Commands

```bash
# Check page loads without errors
curl -I http://localhost:3000/

# Run Lighthouse audit (requires Chrome)
npx lighthouse http://localhost:3000 --only-categories=accessibility,seo
```

## Troubleshooting

### Page shows loading spinner instead of landing page

The old `app/page.tsx` may still have auth redirect logic. Ensure it's replaced with the static landing page component.

### Hydration errors in console

Ensure `app/page.tsx` is a Server Component (no `'use client'` directive).

### Buttons not navigating

Check that `Link` components from `next/link` are used with correct `href` values.
