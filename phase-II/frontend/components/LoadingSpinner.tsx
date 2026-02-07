'use client';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  className?: string;
}

export function LoadingSpinner({ size = 'medium', className = '' }: LoadingSpinnerProps) {
  // Sizes ensure minimum 44px touch target (SC-006)
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-11 h-11', // 44px minimum
    large: 'w-16 h-16',
  };

  return (
    <div
      className={`flex items-center justify-center ${className}`}
      role="status"
      aria-label="Loading"
    >
      <div
        className={`${sizeClasses[size]} border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin`}
      />
      <span className="sr-only">Loading...</span>
    </div>
  );
}
