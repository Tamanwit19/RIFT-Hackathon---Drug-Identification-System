import { useState } from 'react';
import { fetchAnalysis } from '../services/api';

export const useAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState("");
  const [results, setResults] = useState(null);

  const analyzeData = async (file, drugInput) => {
    if (!file || !drugInput) return;

    setLoading(true);
    setResults(null);
    
    try {
      setCurrentStep("Identifying gene targets...");
      setProgress(30);

      // Fetch with dynamic drug parameter
      const data = await fetchAnalysis(file, drugInput);
      
      setResults([data]);
      setProgress(100);
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return { analyzeData, loading, progress, currentStep, results };
};