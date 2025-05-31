import { Activity, Heart, Shield, Zap } from 'lucide-react';
import { LucideIcon } from 'lucide-react';

export interface Disease {
    id: string;
    name: string;
    description: string;
    details: string;
    symptoms: string[];
    severity: string;
    commonAge: string;
    icon: LucideIcon;
    color: string;
    bgColor: string;
    borderColor: string;
}

export const diseases: Disease[] = [
    {
        id: 'pneumonia',
        name: 'Pneumonia',
        description: 'Infection that inflames air sacs in one or both lungs',
        details: 'Pneumonia is an infection that causes inflammation in the air sacs (alveoli) of the lungs. The air sacs may fill with fluid or pus, causing symptoms like cough with phlegm, fever, chills, and difficulty breathing. It can range from mild to life-threatening and affects people of all ages.',
        symptoms: ['Cough with phlegm', 'Fever', 'Shortness of breath', 'Chest pain', 'Fatigue', 'Nausea'],
        severity: 'Moderate to Severe',
        commonAge: 'All ages, especially children and seniors',
        icon: Activity,
        color: 'bg-red-100 text-red-600',
        bgColor: 'bg-red-50',
        borderColor: 'border-red-200'
    },
    {
        id: 'lung-cancer',
        name: 'Lung Cancer',
        description: 'Cancer that begins in the lungs',
        details: 'Lung cancer is a type of cancer that begins in the lungs. It is the leading cause of cancer deaths worldwide. There are two main types: non-small cell lung cancer and small cell lung cancer. Smoking is the primary risk factor, though non-smokers can also develop lung cancer.',
        symptoms: ['Persistent cough', 'Coughing up blood', 'Shortness of breath', 'Chest pain', 'Weight loss', 'Fatigue'],
        severity: 'Severe',
        commonAge: '55 and older',
        icon: Heart,
        color: 'bg-purple-100 text-purple-600',
        bgColor: 'bg-purple-50',
        borderColor: 'border-purple-200'
    },
    {
        id: 'covid-19',
        name: 'COVID-19',
        description: 'Respiratory illness caused by SARS-CoV-2 virus',
        details: 'COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. It can range from mild symptoms to severe illness. Some people may experience long-term effects. Vaccination and preventive measures help reduce transmission and severity.',
        symptoms: ['Cough', 'Fever', 'Shortness of breath', 'Loss of taste/smell', 'Body aches', 'Fatigue'],
        severity: 'Mild to Severe',
        commonAge: 'All ages, higher risk for seniors',
        icon: Shield,
        color: 'bg-blue-100 text-blue-600',
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-200'
    },
    {
        id: 'copd',
        name: 'COPD/Smoking Damage',
        description: 'Chronic lung disease primarily caused by smoking-related damage',
        details: 'COPD (Chronic Obstructive Pulmonary Disease) and smoking-related lung damage represent a group of progressive lung diseases including emphysema and chronic bronchitis. This condition is primarily caused by long-term smoking and exposure to harmful particles that damage the lungs and airways, making breathing increasingly difficult over time.',
        symptoms: ['Chronic cough', 'Shortness of breath', 'Wheezing', 'Chest tightness', 'Fatigue', 'Frequent infections'],
        severity: 'Moderate to Severe',
        commonAge: '40 and older, especially smokers',
        icon: Zap,
        color: 'bg-yellow-100 text-yellow-600',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-200'
    }
]; 