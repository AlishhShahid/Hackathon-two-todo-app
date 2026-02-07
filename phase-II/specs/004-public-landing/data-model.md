# Data Model: Public Landing Page

**Feature**: 004-public-landing
**Date**: 2026-02-07

## Overview

The Public Landing Page is a **static, content-only feature** with no database entities or API endpoints. All content is hardcoded in React components.

## Content Entities (Static)

### 1. Hero Content

| Field | Type | Description |
|-------|------|-------------|
| headline | string | Main value proposition headline |
| subheadline | string | Supporting description text |
| primaryCTA | object | Primary call-to-action button |
| secondaryCTA | object | Secondary call-to-action button |

**Example**:
```
headline: "Organize Your Tasks, Simplify Your Life"
subheadline: "A simple and powerful todo app that helps you stay on top of your tasks"
primaryCTA: { text: "Get Started", href: "/register" }
secondaryCTA: { text: "Sign In", href: "/login" }
```

### 2. Feature Item

| Field | Type | Description |
|-------|------|-------------|
| title | string | Feature name |
| description | string | Feature benefit description |
| icon | ReactNode | SVG icon representing the feature |

**Features to Highlight**:
1. Easy Task Management - Create, edit, and delete tasks effortlessly
2. Due Dates & Reminders - Never miss a deadline
3. Secure & Private - Your data is protected with secure authentication

### 3. Page Metadata

| Field | Type | Description |
|-------|------|-------------|
| title | string | Page title for browser tab (< 60 chars) |
| description | string | Meta description for SEO (< 160 chars) |
| ogTitle | string | OpenGraph title for social sharing |
| ogDescription | string | OpenGraph description |

## Component Structure

```
app/
├── page.tsx              # Landing page (Server Component)
└── layout.tsx            # Root layout (metadata defined here or in page)

components/
└── landing/
    ├── Hero.tsx          # Hero section component
    ├── Features.tsx      # Features grid component
    └── FeatureCard.tsx   # Individual feature card
```

## Data Flow

```
[Static Content] → [Server Component] → [HTML Response] → [Browser]
                   (No client JS needed for initial render)
```

## Notes

- No database tables created
- No API endpoints required
- All content is compile-time static
- Future enhancement: Content could be moved to CMS if marketing needs dynamic updates
