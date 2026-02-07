---
name: build_public_landing_page
description: Build a complete public landing page for a web application. Use for unauthenticated homepage designs.
---

# Public Landing Page Design

## Instructions

1. **Page purpose**
   - Public (unauthenticated) entry point
   - First impression of the product
   - Clear explanation of what the app does

2. **Layout structure**
   - Hero section at the top
   - Feature highlights section
   - Call-to-action section (Sign In / Sign Up)
   - Clean footer (optional)

3. **Content elements**
   - Product name and short tagline
   - 3–5 key feature highlights
   - Clear call-to-action buttons
   - Navigation links to login and signup pages

4. **Routing behavior**
   - Accessible without authentication
   - Must not call protected APIs
   - Redirects only via user interaction (buttons/links)

5. **Styling**
   - Responsive, mobile-first layout
   - Consistent spacing and typography
   - Use Tailwind CSS utility classes
   - High contrast text for readability

## Best Practices
- Keep messaging simple and benefit-focused
- Avoid technical jargon on the landing page
- One primary CTA (Sign In or Get Started)
- Secondary CTA for Sign Up
- Ensure fast load time (no heavy assets)
- No authentication logic on initial render

## Example Structure
```tsx
<section className="min-h-screen flex flex-col items-center justify-center">
  <h1 className="text-4xl font-bold">Manage Your Tasks Effortlessly</h1>
  <p className="mt-4 text-gray-600 text-center max-w-md">
    A simple, secure todo app to organize your daily work.
  </p>

  <div className="mt-6 flex gap-4">
    <Link href="/login" className="px-6 py-2 bg-black text-white rounded">
      Sign In
    </Link>
    <Link href="/signup" className="px-6 py-2 border border-black rounded">
      Sign Up
    </Link>
  </div>
</section>
