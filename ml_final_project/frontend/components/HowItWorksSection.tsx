import React from 'react';

interface Step {
    number: number;
    title: string;
    description: string;
}

interface HowItWorksSectionProps {
    steps: Step[];
    className?: string;
}

const HowItWorksSection: React.FC<HowItWorksSectionProps> = ({ steps, className = '' }) => {
    return (
        <section className={className}>
            <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">
                How It Works
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {steps.map((step, index) => (
                    <div key={index} className="text-center">
                        <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                            {step.number}
                        </div>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">
                            {step.title}
                        </h4>
                        <p className="text-gray-600">
                            {step.description}
                        </p>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default HowItWorksSection; 