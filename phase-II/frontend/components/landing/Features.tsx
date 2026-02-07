import { FeatureCard } from './FeatureCard';

// SVG Icons as components
const TaskIcon = () => (
  <svg className="w-7 h-7 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
  </svg>
);

const CalendarIcon = () => (
  <svg className="w-7 h-7 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const ShieldIcon = () => (
  <svg className="w-7 h-7 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
  </svg>
);

const features = [
  {
    icon: <TaskIcon />,
    title: 'Easy Task Management',
    description: 'Create, edit, and organize your tasks effortlessly. Mark tasks complete with a single click and stay focused on what matters.',
  },
  {
    icon: <CalendarIcon />,
    title: 'Due Dates & Tracking',
    description: 'Set due dates for your tasks and never miss a deadline. Track your progress and stay on top of your schedule.',
  },
  {
    icon: <ShieldIcon />,
    title: 'Secure & Private',
    description: 'Your data is protected with secure authentication. Access your tasks from anywhere with peace of mind.',
  },
];

export function Features() {
  return (
    <section className="bg-gray-50 py-16 sm:py-20 lg:py-24" aria-labelledby="features-heading">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section heading - h2 for proper hierarchy */}
        <div className="text-center mb-12 sm:mb-16">
          <h2 id="features-heading" className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Everything You Need to Stay Productive
          </h2>
          <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto">
            Simple yet powerful features designed to help you manage your tasks and achieve your goals.
          </p>
        </div>

        {/* Features grid - responsive: 1 col mobile, 2 col tablet, 3 col desktop */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
