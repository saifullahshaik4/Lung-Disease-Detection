'use client';

import React, { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import Header from './components/Header';
import DiseaseCard from './components/DiseaseCard';
import XRayAnalysis from './components/XRayAnalysis';
import { diseases, Disease } from './constants/diseases';

const DiseaseLibrary = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedDisease, setSelectedDisease] = useState<string | null>(null);

    // Filter diseases based on search term
    const filteredDiseases = diseases.filter(disease =>
        disease.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        disease.symptoms.some(symptom => symptom.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    const selectedDiseaseData = diseases.find(d => d.id === selectedDisease);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
            <Header currentPage="library" />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {selectedDisease ? (
                    // Disease Detail View
                    <div className="space-y-8">
                        <div className="flex items-center space-x-4 mb-8">
                            <button
                                onClick={() => setSelectedDisease(null)}
                                className="flex items-center space-x-2 text-blue-600 hover:text-blue-700"
                            >
                                <ArrowLeft className="w-5 h-5" />
                                <span>Back to Library</span>
                            </button>
                        </div>

                        {selectedDiseaseData && (() => {
                            const IconComponent = selectedDiseaseData.icon;

                            return (
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                    {/* Disease Information */}
                                    <div className="space-y-6">
                                        <div className={`${selectedDiseaseData.bgColor} p-6 rounded-xl border ${selectedDiseaseData.borderColor}`}>
                                            <div className="flex items-center space-x-4 mb-4">
                                                <div className={`w-12 h-12 ${selectedDiseaseData.color} rounded-lg flex items-center justify-center`}>
                                                    <IconComponent className="w-6 h-6" />
                                                </div>
                                                <div>
                                                    <h2 className="text-2xl font-bold text-gray-900">{selectedDiseaseData.name}</h2>
                                                    <p className="text-gray-600">{selectedDiseaseData.description}</p>
                                                </div>
                                            </div>
                                            <p className="text-gray-700">{selectedDiseaseData.details}</p>
                                        </div>

                                        <div className="bg-white p-6 rounded-xl shadow-sm border">
                                            <h3 className="text-lg font-semibold mb-4">Common Symptoms</h3>
                                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                                {selectedDiseaseData.symptoms.map((symptom, index) => (
                                                    <div key={index} className="flex items-center space-x-2">
                                                        <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                                                        <span className="text-gray-700">{symptom}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                            <div className="bg-white p-4 rounded-lg shadow-sm border">
                                                <h4 className="font-semibold text-gray-900 mb-2">Severity</h4>
                                                <p className="text-gray-600">{selectedDiseaseData.severity}</p>
                                            </div>
                                            <div className="bg-white p-4 rounded-lg shadow-sm border">
                                                <h4 className="font-semibold text-gray-900 mb-2">Common Age Groups</h4>
                                                <p className="text-gray-600">{selectedDiseaseData.commonAge}</p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* X-Ray Upload and Analysis */}
                                    <div className="space-y-6">
                                        <XRayAnalysis selectedDisease={selectedDisease} />
                                    </div>
                                </div>
                            );
                        })()}
                    </div>
                ) : (
                    // Disease Library Grid View
                    <div>
                        <div className="text-center mb-8">
                            <h2 className="text-3xl font-bold text-gray-900 mb-4">Disease Library</h2>
                            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                                Browse our comprehensive library of lung diseases. Click on any condition to learn more and upload X-rays for AI analysis.
                            </p>
                        </div>

                        {/* Search Bar */}
                        <div className="max-w-2xl mx-auto mb-8">
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="Search diseases or symptoms..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-xl text-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                                />
                            </div>
                        </div>

                        {/* Disease Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredDiseases.map((disease) => (
                                <DiseaseCard
                                    key={disease.id}
                                    disease={disease}
                                    onClick={() => setSelectedDisease(disease.id)}
                                />
                            ))}
                        </div>

                        {filteredDiseases.length === 0 && (
                            <div className="text-center py-12">
                                <p className="text-gray-500">No diseases found matching your search.</p>
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
};

export default DiseaseLibrary; 