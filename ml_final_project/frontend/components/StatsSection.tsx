import React from 'react';

interface Stat {
    label: string;
    value: string;
    color: string;
}

interface StatsSectionProps {
    stats: Stat[];
    className?: string;
}

const StatsSection: React.FC<StatsSectionProps> = ({ stats, className = '' }) => {
    return (
        <section className={`bg-white rounded-2xl shadow-sm border p-8 ${className}`}>
            <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">
                Platform Statistics
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <div key={index} className="text-center">
                        <div className={`text-3xl font-bold ${stat.color} mb-2`}>
                            {stat.value}
                        </div>
                        <div className="text-gray-600 font-medium">
                            {stat.label}
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default StatsSection; 