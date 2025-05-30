import type { Metadata } from "next";
import { Bricolage_Grotesque } from "next/font/google";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
    variable: "--font-bricolage",
    subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "LungAI - Lung Disease Detection",
    description: "AI-powered lung disease detection and analysis platform",
    icons: {
        icon: '/icons/icon.svg',
        shortcut: '/icons/icon.svg',
        apple: '/icons/icon.svg',
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={`${bricolage.variable} antialiased`}>{children}</body>
        </html>
    );
} 