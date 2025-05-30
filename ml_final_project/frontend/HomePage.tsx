'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Header from './components/Header';
import DiseaseCard from './components/DiseaseCard';
import StatsSection from './components/StatsSection';
import HowItWorksSection from './components/HowItWorksSection';
import { diseases } from './constants/diseases';

const HomePage = () => {
    const [symptoms, setSymptoms] = useState('');

    const featuredDiseases = diseases.slice(0, 4); // First 4 diseases for homepage

    const stats = [
        { label: 'Accuracy Rate', value: '95%', color: 'text-blue-600' },
        { label: 'Disease Types', value: '10+', color: 'text-green-600' },
        { label: 'Analyses Completed', value: '1000+', color: 'text-purple-600' }
    ];

    const howItWorksSteps = [
        {
            number: 1,
            title: 'Input Symptoms',
            description: 'Describe your symptoms to find relevant lung conditions'
        },
        {
            number: 2,
            title: 'Upload X-Ray',
            description: 'Upload your chest X-ray for AI analysis'
        },
        {
            number: 3,
            title: 'Get Analysis',
            description: 'Receive detailed probability scores and insights'
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
            <Header currentPage="home" />

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Hero Section */}
                <div className="text-center mb-16">
                    <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                        AI-Powered Lung Disease
                        <span className="text-blue-600 block">Detection & Analysis</span>
                    </h2>
                    <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                        Get instant AI-powered analysis of lung conditions. Input your symptoms to find relevant diseases,
                        then upload X-ray images for detailed diagnostic assistance.
                    </p>

                    {/* Symptom Input Bar */}
                    <div className="max-w-2xl mx-auto mb-8">
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Describe your symptoms (e.g., chest pain, shortness of breath, cough...)"
                                value={symptoms}
                                onChange={(e) => setSymptoms(e.target.value)}
                                className="w-full px-4 py-4 border border-gray-300 rounded-xl text-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                            />
                        </div>
                        <div className="mt-4 flex justify-center">
                            <Link
                                href={`/library${symptoms ? `?symptoms=${encodeURIComponent(symptoms)}` : ''}`}
                                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                            >
                                Find Matching Diseases
                            </Link>
                        </div>
                    </div>
                </div>

                {/* Featured Diseases */}
                <section className="mb-16">
                    <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">
                        Common Lung Conditions
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {featuredDiseases.map((disease) => (
                            <DiseaseCard
                                key={disease.id}
                                disease={disease}
                                linkTo={`/library?disease=${disease.name.toLowerCase().replace(/\s+/g, '-')}`}
                            />
                        ))}
                    </div>
                </section>

                {/* Quick Stats */}
                <StatsSection stats={stats} className="mb-16" />

                {/* How It Works */}
                <HowItWorksSection steps={howItWorksSteps} />
            </main>
        </div>
    );
};

export default HomePage; 