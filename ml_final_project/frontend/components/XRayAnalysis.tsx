'use client';

import React, { useState } from 'react';
import { FileImage } from 'lucide-react';

interface AnalysisResult {
    confidence: number;
    likelihood: number;
    recommendations: string[];
    technicalDetails: {
        imageQuality: string;
        analysisTime: string;
        modelVersion: string;
    };
}

interface XRayAnalysisProps {
    selectedDisease: string;
    className?: string;
}

const XRayAnalysis: React.FC<XRayAnalysisProps> = ({ selectedDisease, className = '' }) => {
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [dragActive, setDragActive] = useState(false);

    const handleFileUpload = (file: File) => {
        if (file && file.type.startsWith('image/')) {
            setUploadedFile(file);
            // Simulate AI analysis
            simulateAnalysis();
        }
    };

    const simulateAnalysis = () => {
        setIsAnalyzing(true);
        setTimeout(() => {
            setAnalysisResult({
                confidence: Math.floor(Math.random() * 40) + 60, // 60-100%
                likelihood: Math.floor(Math.random() * 30) + 40, // 40-70%
                recommendations: [
                    'Consult with a pulmonologist for professional diagnosis',
                    'Consider additional imaging tests (CT scan)',
                    'Monitor symptoms closely',
                    'Follow up in 2-4 weeks if symptoms persist'
                ],
                technicalDetails: {
                    imageQuality: 'Good',
                    analysisTime: '2.3s',
                    modelVersion: 'LungAI v2.1'
                }
            });
            setIsAnalyzing(false);
        }, 2000);
    };

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFileUpload(e.target.files[0]);
        }
    };

    return (
        <div className={className}>
            <div className="bg-white p-6 rounded-xl shadow-sm border">
                <h3 className="text-lg font-semibold mb-4">X-Ray Analysis</h3>

                {/* File Upload Area */}
                <div
                    className={`border-2 border-dashed rounded-lg p-8 text-center ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <FileImage className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">
                        Drag and drop your chest X-ray here, or click to select
                    </p>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleInputChange}
                        className="hidden"
                        id="xray-upload"
                    />
                    <label
                        htmlFor="xray-upload"
                        className="bg-blue-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-700 transition-colors"
                    >
                        Choose File
                    </label>
                </div>

                {/* Analysis Results */}
                {isAnalyzing && (
                    <div className="mt-6 text-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="text-gray-600 mt-2">Analyzing X-ray...</p>
                    </div>
                )}

                {analysisResult && !isAnalyzing && (
                    <div className="mt-6 space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-blue-50 p-4 rounded-lg">
                                <h4 className="font-semibold text-blue-900">Confidence Score</h4>
                                <p className="text-2xl font-bold text-blue-600">{analysisResult.confidence}%</p>
                            </div>
                            <div className="bg-green-50 p-4 rounded-lg">
                                <h4 className="font-semibold text-green-900">Likelihood</h4>
                                <p className="text-2xl font-bold text-green-600">{analysisResult.likelihood}%</p>
                            </div>
                        </div>

                        <div>
                            <h4 className="font-semibold mb-2">Recommendations</h4>
                            <ul className="list-disc list-inside space-y-1 text-gray-700">
                                {analysisResult.recommendations.map((rec, index) => (
                                    <li key={index}>{rec}</li>
                                ))}
                            </ul>
                        </div>

                        <div className="bg-gray-50 p-4 rounded-lg">
                            <h4 className="font-semibold mb-2">Technical Details</h4>
                            <div className="text-sm text-gray-600 space-y-1">
                                <p>Image Quality: {analysisResult.technicalDetails.imageQuality}</p>
                                <p>Analysis Time: {analysisResult.technicalDetails.analysisTime}</p>
                                <p>Model Version: {analysisResult.technicalDetails.modelVersion}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default XRayAnalysis; 