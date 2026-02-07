import { ReactNode } from 'react';

interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
}

export function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 sm:p-8 text-center hover:shadow-lg transition-shadow">
      {/* Icon container */}
      <div className="w-14 h-14 sm:w-16 sm:h-16 mx-auto mb-4 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
        {icon}
      </div>

      {/* Feature title */}
      <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">
        {title}
      </h3>

      {/* Feature description */}
      <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
        {description}
      </p>
    </div>
  );
}
