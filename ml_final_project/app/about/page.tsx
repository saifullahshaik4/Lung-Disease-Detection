import React from 'react';
import { Stethoscope, Brain, Shield, Users, Award, Heart } from 'lucide-react';
import Link from 'next/link';

const AboutPage = () => {
    const features = [
        {
            icon: Brain,
            title: 'AI-Powered Analysis',
            description: 'Advanced machine learning algorithms trained on thousands of chest X-rays for accurate disease detection.'
        },
        {
            icon: Shield,
            title: 'Privacy First',
            description: 'Your medical data is processed securely and never stored. All analysis happens in real-time.'
        },
        {
            icon: Users,
            title: 'Accessible Healthcare',
            description: 'Bringing advanced diagnostic tools to everyone, regardless of location or economic status.'
        },
        {
            icon: Award,
            title: 'Clinical Accuracy',
            description: '95% accuracy rate validated through extensive testing with medical professionals.'
        }
    ];

    const stats = [
        { label: 'Accuracy Rate', value: '95%' },
        { label: 'Diseases Detected', value: '10+' },
        { label: 'X-rays Analyzed', value: '1,000+' },
        { label: 'Response Time', value: '<3s' }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                                <Stethoscope className="w-5 h-5 text-white" />
                            </div>
                            <h1 className="text-xl font-bold text-gray-900">LungAI</h1>
                        </div>
                        <nav className="flex items-center space-x-8">
                            <Link href="/" className="text-gray-600 hover:text-blue-600 transition-colors">Home</Link>
                            <Link href="/library" className="text-gray-600 hover:text-blue-600 transition-colors">Disease Library</Link>
                            <Link href="/about" className="text-blue-600 font-medium">About</Link>
                        </nav>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Hero Section */}
                <div className="text-center mb-16">
                    <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                        About <span className="text-blue-600">LungAI</span>
                    </h2>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                        LungAI is an advanced artificial intelligence platform designed to assist in the early detection
                        and analysis of lung diseases through chest X-ray interpretation.
                    </p>
                </div>

                {/* Mission Section */}
                <section className="mb-16">
                    <div className="bg-white rounded-2xl shadow-sm border p-8">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                            <div>
                                <h3 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h3>
                                <p className="text-gray-600 mb-4">
                                    We believe that advanced medical diagnostics should be accessible to everyone. LungAI democratizes
                                    lung disease detection by providing AI-powered analysis that can assist healthcare providers and
                                    patients worldwide.
                                </p>
                                <p className="text-gray-600">
                                    Our goal is to enable early detection of lung conditions, potentially saving lives through
                                    timely intervention and treatment.
                                </p>
                            </div>
                            <div className="flex justify-center">
                                <div className="w-64 h-64 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center">
                                    <Heart className="w-32 h-32 text-blue-600" />
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="mb-16">
                    <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Key Features</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {features.map((feature, index) => {
                            const IconComponent = feature.icon;
                            return (
                                <div key={index} className="bg-white p-6 rounded-xl shadow-sm border">
                                    <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-4">
                                        <IconComponent className="w-6 h-6" />
                                    </div>
                                    <h4 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h4>
                                    <p className="text-gray-600">{feature.description}</p>
                                </div>
                            );
                        })}
                    </div>
                </section>

                {/* Stats Section */}
                <section className="mb-16">
                    <div className="bg-white rounded-2xl shadow-sm border p-8">
                        <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Platform Statistics</h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                            {stats.map((stat, index) => (
                                <div key={index} className="text-center">
                                    <div className="text-3xl font-bold text-blue-600 mb-2">{stat.value}</div>
                                    <div className="text-gray-600">{stat.label}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* How It Works */}
                <section className="mb-16">
                    <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">How LungAI Works</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl font-bold">1</span>
                            </div>
                            <h4 className="text-lg font-semibold mb-2">Input Symptoms</h4>
                            <p className="text-gray-600">
                                Start by describing your symptoms or browse our disease library to find relevant conditions.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl font-bold">2</span>
                            </div>
                            <h4 className="text-lg font-semibold mb-2">Upload X-Ray</h4>
                            <p className="text-gray-600">
                                Upload a clear chest X-ray image in common formats (PNG, JPG) for AI analysis.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl font-bold">3</span>
                            </div>
                            <h4 className="text-lg font-semibold mb-2">Get Results</h4>
                            <p className="text-gray-600">
                                Receive instant analysis with confidence scores and recommendations for next steps.
                            </p>
                        </div>
                    </div>
                </section>

                {/* Disclaimer */}
                <section className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 mb-16">
                    <h3 className="text-lg font-semibold text-yellow-800 mb-3">Important Medical Disclaimer</h3>
                    <p className="text-yellow-700 text-sm">
                        LungAI is designed to assist healthcare professionals and provide educational information.
                        It is not intended to replace professional medical advice, diagnosis, or treatment.
                        Always consult with qualified healthcare providers for medical decisions.
                        Never disregard professional medical advice or delay seeking treatment based on LungAI results.
                    </p>
                </section>

                {/* CTA Section */}
                <section className="text-center">
                    <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white">
                        <h3 className="text-2xl font-bold mb-4">Ready to Get Started?</h3>
                        <p className="text-blue-100 mb-6">
                            Begin your lung health analysis today with our AI-powered diagnostic tool.
                        </p>
                        <Link
                            href="/"
                            className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-medium hover:bg-blue-50 transition-colors"
                        >
                            Start Analysis
                        </Link>
                    </div>
                </section>
            </main>
        </div>
    );
};

export default AboutPage; 