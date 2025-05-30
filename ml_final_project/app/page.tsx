'use client';

import React, { useState } from 'react';
import { Search, Stethoscope, Activity, Heart, AlertCircle } from 'lucide-react';
import Link from 'next/link';

const HomePage = () => {
  const [symptoms, setSymptoms] = useState('');

  const featuredDiseases = [
    {
      name: 'Pneumonia',
      description: 'Inflammation of air sacs in lungs',
      icon: Activity,
      color: 'bg-red-100 text-red-600',
      bgColor: 'bg-gradient-to-br from-red-50 to-red-100'
    },
    {
      name: 'Lung Cancer',
      description: 'Malignant lung tumor detection',
      icon: AlertCircle,
      color: 'bg-purple-100 text-purple-600',
      bgColor: 'bg-gradient-to-br from-purple-50 to-purple-100'
    },
    {
      name: 'Tuberculosis',
      description: 'Bacterial infection of the lungs',
      icon: Stethoscope,
      color: 'bg-orange-100 text-orange-600',
      bgColor: 'bg-gradient-to-br from-orange-50 to-orange-100'
    },
    {
      name: 'COVID-19',
      description: 'Coronavirus lung complications',
      icon: Heart,
      color: 'bg-blue-100 text-blue-600',
      bgColor: 'bg-gradient-to-br from-blue-50 to-blue-100'
    }
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
              <Link href="/" className="text-blue-600 font-medium">Home</Link>
              <Link href="/library" className="text-gray-600 hover:text-blue-600 transition-colors">Disease Library</Link>
              <Link href="/about" className="text-gray-600 hover:text-blue-600 transition-colors">About</Link>
            </nav>
          </div>
        </div>
      </header>

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
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Describe your symptoms (e.g., chest pain, shortness of breath, cough...)"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl text-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
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
            {featuredDiseases.map((disease, index) => {
              const IconComponent = disease.icon;
              return (
                <Link
                  key={index}
                  href={`/library?disease=${disease.name.toLowerCase().replace(/\s+/g, '-')}`}
                  className={`${disease.bgColor} p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border border-gray-100`}
                >
                  <div className={`w-12 h-12 ${disease.color} rounded-lg flex items-center justify-center mb-4`}>
                    <IconComponent className="w-6 h-6" />
                  </div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">{disease.name}</h4>
                  <p className="text-gray-600 text-sm">{disease.description}</p>
                </Link>
              );
            })}
          </div>
        </section>

        {/* Quick Stats */}
        <section className="bg-white rounded-2xl shadow-sm border p-8 mb-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">95%</div>
              <div className="text-gray-600">Accuracy Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600 mb-2">10+</div>
              <div className="text-gray-600">Disease Types</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-600 mb-2">1000+</div>
              <div className="text-gray-600">Analyses Completed</div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-8">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="font-bold text-lg">1</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Input Symptoms</h4>
              <p className="text-gray-600">Describe your symptoms to find relevant lung conditions</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-green-100 text-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="font-bold text-lg">2</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Upload X-Ray</h4>
              <p className="text-gray-600">Upload your chest X-ray for AI analysis</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="font-bold text-lg">3</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Get Analysis</h4>
              <p className="text-gray-600">Receive detailed probability scores and insights</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default HomePage;