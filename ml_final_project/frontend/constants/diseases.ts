import { Activity, Heart, Thermometer, Shield, Wind, Zap } from 'lucide-react';
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
        id: 'tuberculosis',
        name: 'Tuberculosis',
        description: 'Bacterial infection that mainly affects the lungs',
        details: 'Tuberculosis (TB) is a serious infectious disease that mainly affects the lungs. The bacteria that cause TB are spread through the air when people with active TB cough, spit, speak, or sneeze. TB is treatable and curable with proper medication.',
        symptoms: ['Persistent cough', 'Coughing up blood', 'Night sweats', 'Fever', 'Weight loss', 'Fatigue'],
        severity: 'Severe',
        commonAge: 'All ages, higher risk in certain populations',
        icon: Thermometer,
        color: 'bg-orange-100 text-orange-600',
        bgColor: 'bg-orange-50',
        borderColor: 'border-orange-200'
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
        id: 'asthma',
        name: 'Asthma',
        description: 'Chronic condition affecting airways in the lungs',
        details: 'Asthma is a chronic respiratory condition in which airways become inflamed, narrow, and produce extra mucus. This makes breathing difficult and triggers coughing, wheezing, and shortness of breath. Asthma can be managed with proper treatment.',
        symptoms: ['Wheezing', 'Shortness of breath', 'Chest tightness', 'Coughing', 'Rapid breathing', 'Fatigue'],
        severity: 'Mild to Moderate',
        commonAge: 'All ages, often starts in childhood',
        icon: Wind,
        color: 'bg-green-100 text-green-600',
        bgColor: 'bg-green-50',
        borderColor: 'border-green-200'
    },
    {
        id: 'copd',
        name: 'COPD',
        description: 'Chronic obstructive pulmonary disease',
        details: 'COPD is a group of progressive lung diseases including emphysema and chronic bronchitis. It blocks airflow and makes breathing difficult. COPD is primarily caused by long-term exposure to irritating gases or particulate matter, most often from cigarette smoke.',
        symptoms: ['Chronic cough', 'Shortness of breath', 'Wheezing', 'Chest tightness', 'Fatigue', 'Frequent infections'],
        severity: 'Moderate to Severe',
        commonAge: '40 and older',
        icon: Zap,
        color: 'bg-yellow-100 text-yellow-600',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-200'
    }
]; 