import Link from 'next/link';

export function Hero() {
  return (
    <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-20 lg:py-24">
        <div className="text-center">
          {/* Main headline - single h1 for SEO */}
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight mb-4 sm:mb-6">
            Organize Your Tasks, Simplify Your Life
          </h1>

          {/* Subheadline */}
          <p className="text-lg sm:text-xl lg:text-2xl text-blue-100 max-w-2xl mx-auto mb-8 sm:mb-10">
            A simple and powerful todo app that helps you stay on top of your tasks and achieve your goals.
          </p>

          {/* CTA Buttons - 44px min height for touch accessibility */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/register"
              className="w-full sm:w-auto min-h-[44px] px-8 py-3 text-lg font-semibold bg-white text-blue-600 rounded-lg shadow-lg hover:bg-blue-50 transition-colors flex items-center justify-center"
              aria-label="Get started by creating a new account"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="w-full sm:w-auto min-h-[44px] px-8 py-3 text-lg font-semibold border-2 border-white text-white rounded-lg hover:bg-white/10 transition-colors flex items-center justify-center"
              aria-label="Sign in to your existing account"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
