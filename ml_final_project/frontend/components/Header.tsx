import React from 'react';
import Link from 'next/link';
import { Activity } from 'lucide-react';

interface HeaderProps {
    currentPage: 'home' | 'library' | 'about';
}

const Header: React.FC<HeaderProps> = ({ currentPage }) => {
    return (
        <header className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center py-4">
                    {/* Logo and Title */}
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                            <Activity className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900">LungAI</h1>
                            <p className="text-sm text-gray-500">Lung Disease Detection</p>
                        </div>
                    </div>

                    {/* Navigation */}
                    <nav className="flex space-x-8">
                        <Link
                            href="/"
                            className={`text-sm font-medium transition-colors ${currentPage === 'home'
                                    ? 'text-blue-600 border-b-2 border-blue-600 pb-1'
                                    : 'text-gray-600 hover:text-gray-900'
                                }`}
                        >
                            Home
                        </Link>
                        <Link
                            href="/library"
                            className={`text-sm font-medium transition-colors ${currentPage === 'library'
                                    ? 'text-blue-600 border-b-2 border-blue-600 pb-1'
                                    : 'text-gray-600 hover:text-gray-900'
                                }`}
                        >
                            Disease Library
                        </Link>
                        <Link
                            href="/about"
                            className={`text-sm font-medium transition-colors ${currentPage === 'about'
                                    ? 'text-blue-600 border-b-2 border-blue-600 pb-1'
                                    : 'text-gray-600 hover:text-gray-900'
                                }`}
                        >
                            About
                        </Link>
                    </nav>
                </div>
            </div>
        </header>
    );
};

export default Header; 