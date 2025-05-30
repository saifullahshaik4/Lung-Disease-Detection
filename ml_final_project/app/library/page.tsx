'use client';

import React, { useState } from 'react';
import { Upload, Activity, Heart, AlertCircle, Stethoscope, Microscope, Wind, FileImage, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

const LibraryPage = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedDisease, setSelectedDisease] = useState<string | null>(null);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [analysisResult, setAnalysisResult] = useState<any>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    const diseases = [
        {
            id: 'pneumonia',
            name: 'Pneumonia',
            description: 'Inflammation of air sacs in one or both lungs',
            symptoms: ['Chest pain', 'Shortness of breath', 'Cough with phlegm', 'Fever', 'Chills'],
            icon: Activity,
            color: 'bg-red-100 text-red-600',
            bgColor: 'bg-gradient-to-br from-red-50 to-red-100',
            borderColor: 'border-red-200',
            severity: 'Moderate to Severe',
            commonAge: '65+ years, children under 2',
            details: 'Pneumonia is an infection that inflames air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing.'
        },
        {
            id: 'lung-cancer',
            name: 'Lung Cancer',
            description: 'Malignant tumor in the lung tissue',
            symptoms: ['Persistent cough', 'Chest pain', 'Weight loss', 'Shortness of breath', 'Coughing up blood'],
            icon: AlertCircle,
            color: 'bg-purple-100 text-purple-600',
            bgColor: 'bg-gradient-to-br from-purple-50 to-purple-100',
            borderColor: 'border-purple-200',
            severity: 'Severe',
            commonAge: '55+ years',
            details: 'Lung cancer is a type of cancer that begins in the lungs. It\'s the leading cause of cancer deaths worldwide. Early detection through screening can significantly improve outcomes.'
        },
        {
            id: 'tuberculosis',
            name: 'Tuberculosis',
            description: 'Bacterial infection affecting the lungs',
            symptoms: ['Persistent cough', 'Night sweats', 'Weight loss', 'Fatigue', 'Chest pain'],
            icon: Stethoscope,
            color: 'bg-orange-100 text-orange-600',
            bgColor: 'bg-gradient-to-br from-orange-50 to-orange-100',
            borderColor: 'border-orange-200',
            severity: 'Moderate to Severe',
            commonAge: 'All ages',
            details: 'Tuberculosis (TB) is a potentially serious infectious disease that mainly affects the lungs. It spreads through the air when people with active TB cough, sneeze, or spit.'
        },
        {
            id: 'covid-19',
            name: 'COVID-19',
            description: 'Coronavirus respiratory complications',
            symptoms: ['Dry cough', 'Fever', 'Fatigue', 'Loss of taste/smell', 'Difficulty breathing'],
            icon: Heart,
            color: 'bg-blue-100 text-blue-600',
            bgColor: 'bg-gradient-to-br from-blue-50 to-blue-100',
            borderColor: 'border-blue-200',
            severity: 'Mild to Severe',
            commonAge: 'All ages',
            details: 'COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. It can range from mild symptoms to severe respiratory complications requiring hospitalization.'
        },
        {
            id: 'asthma',
            name: 'Asthma',
            description: 'Chronic respiratory condition with airway inflammation',
            symptoms: ['Wheezing', 'Shortness of breath', 'Chest tightness', 'Persistent cough'],
            icon: Wind,
            color: 'bg-green-100 text-green-600',
            bgColor: 'bg-gradient-to-br from-green-50 to-green-100',
            borderColor: 'border-green-200',
            severity: 'Mild to Moderate',
            commonAge: 'All ages',
            details: 'Asthma is a condition in which airways narrow and swell and may produce extra mucus. This can make breathing difficult and trigger coughing and wheezing.'
        },
        {
            id: 'copd',
            name: 'COPD',
            description: 'Chronic obstructive pulmonary disease',
            symptoms: ['Chronic cough', 'Shortness of breath', 'Wheezing', 'Chest tightness', 'Frequent infections'],
            icon: Microscope,
            color: 'bg-yellow-100 text-yellow-600',
            bgColor: 'bg-gradient-to-br from-yellow-50 to-yellow-100',
            borderColor: 'border-yellow-200',
            severity: 'Moderate to Severe',
            commonAge: '40+ years',
            details: 'COPD is a chronic inflammatory lung disease that causes obstructed airflow from the lungs. It\'s commonly caused by long-term exposure to irritating gases or particulate matter.'
        }
    ];

    // Filter diseases based on search term
    const filteredDiseases = diseases.filter(disease =>
        disease.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        disease.symptoms.some(symptom => symptom.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    // Handle file upload
    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setUploadedFile(file);
            setAnalysisResult(null);
        }
    };

    // Simulate AI analysis
    const handleAnalysis = async () => {
        if (!uploadedFile || !selectedDisease) return;

        setIsAnalyzing(true);

        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Mock analysis results - generate random values only during user interaction
        const confidence = Math.floor(Math.random() * 40 + 60); // 60-100%
        const likelihood = Math.floor(Math.random() * 30 + 40); // 40-70%

        const mockResults = {
            confidence,
            likelihood,
            recommendations: [
                'Consult with a pulmonologist for further evaluation',
                'Consider additional imaging studies if symptoms persist',
                'Monitor symptoms and seek immediate care if they worsen'
            ],
            technicalDetails: {
                imageQuality: 'Good',
                analysisTime: '2.3 seconds',
                modelVersion: 'LungAI v2.1'
            }
        };

        setAnalysisResult(mockResults);
        setIsAnalyzing(false);
    };

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
                            <Link href="/library" className="text-blue-600 font-medium">Disease Library</Link>
                            <Link href="/about" className="text-gray-600 hover:text-blue-600 transition-colors">About</Link>
                        </nav>
                    </div>
                </div>
            </header>

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

                        {(() => {
                            const disease = diseases.find(d => d.id === selectedDisease);
                            if (!disease) return null;
                            const IconComponent = disease.icon;

                            return (
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                    {/* Disease Information */}
                                    <div className="space-y-6">
                                        <div className={`${disease.bgColor} p-6 rounded-xl border ${disease.borderColor}`}>
                                            <div className="flex items-center space-x-4 mb-4">
                                                <div className={`w-12 h-12 ${disease.color} rounded-lg flex items-center justify-center`}>
                                                    <IconComponent className="w-6 h-6" />
                                                </div>
                                                <div>
                                                    <h2 className="text-2xl font-bold text-gray-900">{disease.name}</h2>
                                                    <p className="text-gray-600">{disease.description}</p>
                                                </div>
                                            </div>
                                            <p className="text-gray-700">{disease.details}</p>
                                        </div>

                                        <div className="bg-white p-6 rounded-xl shadow-sm border">
                                            <h3 className="text-lg font-semibold mb-4">Common Symptoms</h3>
                                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                                {disease.symptoms.map((symptom, index) => (
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
                                                <p className="text-gray-600">{disease.severity}</p>
                                            </div>
                                            <div className="bg-white p-4 rounded-lg shadow-sm border">
                                                <h4 className="font-semibold text-gray-900 mb-2">Common Age Groups</h4>
                                                <p className="text-gray-600">{disease.commonAge}</p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* X-Ray Upload and Analysis */}
                                    <div className="space-y-6">
                                        <div className="bg-white p-6 rounded-xl shadow-sm border">
                                            <h3 className="text-lg font-semibold mb-4">X-Ray Analysis</h3>

                                            {/* File Upload */}
                                            <div className="mb-6">
                                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                                    Upload Chest X-Ray
                                                </label>
                                                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                                                    <input
                                                        type="file"
                                                        accept="image/*"
                                                        onChange={handleFileUpload}
                                                        className="hidden"
                                                        id="xray-upload"
                                                    />
                                                    <label htmlFor="xray-upload" className="cursor-pointer">
                                                        <FileImage className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                                                        <p className="text-gray-600">Click to upload or drag and drop</p>
                                                        <p className="text-sm text-gray-500 mt-1">PNG, JPG up to 10MB</p>
                                                    </label>
                                                </div>
                                                {uploadedFile && (
                                                    <p className="mt-2 text-sm text-green-600">
                                                        Uploaded: {uploadedFile.name}
                                                    </p>
                                                )}
                                            </div>

                                            {/* Analysis Button */}
                                            <button
                                                onClick={handleAnalysis}
                                                disabled={!uploadedFile || isAnalyzing}
                                                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                                            >
                                                {isAnalyzing ? 'Analyzing...' : 'Analyze X-Ray'}
                                            </button>

                                            {/* Analysis Results */}
                                            {analysisResult && (
                                                <div className="mt-6 space-y-4">
                                                    <h4 className="font-semibold text-gray-900">Analysis Results</h4>

                                                    <div className="grid grid-cols-2 gap-4">
                                                        <div className="bg-blue-50 p-4 rounded-lg">
                                                            <div className="text-2xl font-bold text-blue-600">
                                                                {analysisResult.confidence}%
                                                            </div>
                                                            <div className="text-sm text-gray-600">Model Confidence</div>
                                                        </div>
                                                        <div className="bg-orange-50 p-4 rounded-lg">
                                                            <div className="text-2xl font-bold text-orange-600">
                                                                {analysisResult.likelihood}%
                                                            </div>
                                                            <div className="text-sm text-gray-600">Disease Likelihood</div>
                                                        </div>
                                                    </div>

                                                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                                                        <h5 className="font-medium text-yellow-800 mb-2">Recommendations:</h5>
                                                        <ul className="space-y-1">
                                                            {analysisResult.recommendations.map((rec: string, index: number) => (
                                                                <li key={index} className="text-yellow-700 text-sm">• {rec}</li>
                                                            ))}
                                                        </ul>
                                                    </div>

                                                    <div className="text-xs text-gray-500 space-y-1">
                                                        <p>Image Quality: {analysisResult.technicalDetails.imageQuality}</p>
                                                        <p>Analysis Time: {analysisResult.technicalDetails.analysisTime}</p>
                                                        <p>Model: {analysisResult.technicalDetails.modelVersion}</p>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
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
                            {filteredDiseases.map((disease) => {
                                const IconComponent = disease.icon;
                                return (
                                    <div
                                        key={disease.id}
                                        onClick={() => setSelectedDisease(disease.id)}
                                        className={`${disease.bgColor} p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer border ${disease.borderColor}`}
                                    >
                                        <div className={`w-12 h-12 ${disease.color} rounded-lg flex items-center justify-center mb-4`}>
                                            <IconComponent className="w-6 h-6" />
                                        </div>
                                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{disease.name}</h3>
                                        <p className="text-gray-600 text-sm mb-3">{disease.description}</p>
                                        <div className="text-xs text-gray-500">
                                            <span className="font-medium">Severity:</span> {disease.severity}
                                        </div>
                                    </div>
                                );
                            })}
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

export default LibraryPage; 