import { Metadata } from 'next';
import { Hero } from '@/components/landing/Hero';
import { Features } from '@/components/landing/Features';

// SEO Metadata - title < 60 chars, description < 160 chars
export const metadata: Metadata = {
  title: 'Todo App - Organize Your Tasks Efficiently',
  description: 'A simple and powerful todo application to help you manage tasks, set due dates, and stay productive. Get started for free today.',
  openGraph: {
    title: 'Todo App - Organize Your Tasks Efficiently',
    description: 'A simple and powerful todo application to help you manage tasks, set due dates, and stay productive.',
    type: 'website',
  },
};

// Public Landing Page - Server Component (no 'use client')
// Renders without authentication checks or redirects (FR-005, FR-008)
export default function LandingPage() {
  return (
    <main>
      {/* Hero section with value proposition and CTAs */}
      <Hero />

      {/* Features section highlighting core benefits */}
      <Features />

      {/* Footer with minimal info */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm">
            &copy; {new Date().getFullYear()} Todo App. All rights reserved.
          </p>
        </div>
      </footer>
    </main>
  );
}
