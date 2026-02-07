# Research: Public Landing Page

**Feature**: 004-public-landing
**Date**: 2026-02-07

## Technical Context Analysis

### Current State

The existing `app/page.tsx` (root route) is a client component that:
- Uses authentication context (`useAuth`)
- Redirects authenticated users to `/tasks`
- Redirects unauthenticated users to `/login`
- Shows a loading spinner during auth check

**Problem**: This conflicts with FR-005 and FR-008 which require the landing page to render without authentication checks or redirects.

### Research Findings

#### 1. Server Components vs Client Components for Landing Page

**Decision**: Use Server Component for the landing page

**Rationale**:
- Server components render on the server without JavaScript hydration overhead
- No client-side auth checks means faster initial paint
- Better SEO as content is immediately available to crawlers
- Satisfies SC-007 (no hydration errors or layout shifts)

**Alternatives Considered**:
- Client component with `use client` - rejected due to hydration concerns and auth dependency
- Static HTML export - not needed as Next.js App Router handles SSR well

#### 2. Component Architecture

**Decision**: Create reusable landing page components in `components/landing/`

**Rationale**:
- Separation of concerns (landing vs authenticated UI)
- Reusable components for potential future marketing pages
- Clean organization following existing patterns

**Components to Create**:
- `Hero.tsx` - Main hero section with headline, subheadline, CTAs
- `Features.tsx` - Feature highlights grid
- `Footer.tsx` - Public footer (optional, can be simple)

#### 3. Routing Strategy

**Decision**: Replace existing `app/page.tsx` with static landing page

**Rationale**:
- Root URL (/) is the most valuable for SEO
- Authenticated users can still see landing page (no forced redirect per edge case requirement)
- Dashboard link can be added to header for authenticated users in future

**Migration Path**:
1. Create new landing page components
2. Replace `app/page.tsx` with server component that renders landing page
3. Remove auth-based redirect logic

#### 4. SEO Implementation

**Decision**: Use Next.js Metadata API in `app/page.tsx` or `app/layout.tsx`

**Rationale**:
- Built-in Next.js feature, no external dependencies
- Supports title, description, OpenGraph tags
- Type-safe with TypeScript

**Implementation**:
```typescript
export const metadata = {
  title: 'Todo App - Organize Your Tasks Efficiently',
  description: 'A simple and powerful todo application...',
}
```

#### 5. Responsive Design Strategy

**Decision**: Mobile-first with Tailwind CSS breakpoints

**Rationale**:
- Consistent with existing codebase patterns
- Tailwind already configured
- Standard breakpoints: sm (640px), md (768px), lg (1024px)

**Key Patterns**:
- Stack layout on mobile, horizontal on desktop
- Font sizes scale with screen size
- Touch targets minimum 44px (min-h-[44px] pattern already used)

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `/login` route | EXISTS | Functional login page |
| `/register` route | EXISTS | Functional registration page |
| Tailwind CSS | EXISTS | Already configured |
| Next.js App Router | EXISTS | Using App Router |

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Existing auth redirect breaks users | Medium | High | Clear navigation to /tasks for authenticated users |
| Layout shift on hydration | Low | Medium | Use Server Component, avoid client-side state |
| SEO not indexed properly | Low | Medium | Test with Google Search Console after deploy |

## Conclusion

All NEEDS CLARIFICATION items resolved. No blockers identified. Ready for Phase 1 design.
