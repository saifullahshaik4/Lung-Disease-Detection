import React from 'react';
import Link from 'next/link';
import { LucideIcon } from 'lucide-react';

interface DiseaseCardProps {
    disease: {
        id: string;
        name: string;
        description: string;
        icon: LucideIcon;
        color: string;
        bgColor: string;
        borderColor: string;
        severity: string;
    };
    onClick?: () => void;
    linkTo?: string;
}

const DiseaseCard: React.FC<DiseaseCardProps> = ({ disease, onClick, linkTo }) => {
    const IconComponent = disease.icon;

    const cardContent = (
        <div className={`${disease.bgColor} p-6 rounded-xl border ${disease.borderColor} hover:shadow-lg transition-shadow cursor-pointer`}>
            <div className="flex items-center space-x-4 mb-4">
                <div className={`w-12 h-12 ${disease.color} rounded-lg flex items-center justify-center`}>
                    <IconComponent className="w-6 h-6" />
                </div>
                <div>
                    <h3 className="text-lg font-semibold text-gray-900">{disease.name}</h3>
                    <p className="text-sm text-gray-600">{disease.severity}</p>
                </div>
            </div>
            <p className="text-gray-700">{disease.description}</p>
        </div>
    );

    if (linkTo) {
        return (
            <Link href={linkTo}>
                {cardContent}
            </Link>
        );
    }

    return (
        <div onClick={onClick}>
            {cardContent}
        </div>
    );
};

export default DiseaseCard; 