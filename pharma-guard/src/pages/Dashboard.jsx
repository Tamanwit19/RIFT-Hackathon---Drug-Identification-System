import React, { useState } from 'react';
import { Search, Loader2, Download, Clipboard, Beaker } from 'lucide-react';
import UploadPanel from '../components/UploadPanel';
import ResultCard from '../components/ResultCard';
import StatusStepper from '../components/StatusStepper';
import { useAnalysis } from '../hooks/useAnalysis';

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [drugs, setDrugs] = useState("");
  const { analyzeData, loading, progress, currentStep, results } = useAnalysis();

  const handleCopyResults = () => {
    if (results) {
      navigator.clipboard.writeText(JSON.stringify(results, null, 2));
      alert("JSON results copied to clipboard!");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <div className="flex items-center space-x-2 mb-2">
            <Beaker className="text-blue-600 w-6 h-6" />
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Clinical PGx Dashboard</h1>
          </div>
          <p className="text-slate-500 text-sm">Upload VCF genomic data to evaluate pharmacogenomic drug safety.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Controls */}
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h2 className="text-xs font-bold uppercase text-slate-400 mb-4 tracking-widest">Step 1: Genomic Data</h2>
              <UploadPanel onFileSelect={setFile} selectedFile={file} />
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <h2 className="text-xs font-bold uppercase text-slate-400 mb-4 tracking-widest">Step 2: Medications</h2>
              <div className="relative mb-4">
                <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                <input 
                  type="text"
                  placeholder="e.g. Clopidogrel, Warfarin"
                  className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                  value={drugs}
                  onChange={(e) => setDrugs(e.target.value)}
                />
              </div>
              
              <button 
                onClick={() => analyzeData(file, drugs)}
                disabled={loading || !file || !drugs}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center shadow-lg shadow-blue-100"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" /> 
                    Analyzing...
                  </>
                ) : (
                  "Run PGx Analysis"
                )}
              </button>

              {loading && (
                <div className="mt-4">
                  <StatusStepper progress={progress} currentStep={currentStep} />
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-2">
            {results ? (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-lg font-bold text-slate-800 flex items-center">
                    Analysis Results 
                    <span className="ml-2 px-2 py-0.5 bg-slate-200 text-slate-600 rounded text-xs font-mono">
                      {results.length} Drugs
                    </span>
                  </h2>
                  <div className="flex space-x-2">
                    <button 
                      onClick={handleCopyResults}
                      className="flex items-center space-x-2 px-3 py-1.5 text-xs font-semibold text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-50"
                    >
                      <Clipboard className="w-3.5 h-3.5" />
                      <span>Copy JSON</span>
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  {results.map((res, i) => (
                    <ResultCard key={i} result={res} />
                  ))}
                </div>
              </div>
            ) : !loading ? (
              <div className="h-full min-h-[400px] border-2 border-dashed border-slate-200 rounded-2xl flex flex-col items-center justify-center text-center p-8 bg-white/50">
                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                  <Beaker className="w-8 h-8 text-slate-300" />
                </div>
                <h3 className="text-slate-900 font-bold mb-1">No Analysis Performed</h3>
                <p className="text-slate-500 text-sm max-w-xs">
                  Upload a standard VCF file and enter clinical drug names to begin the genomic screening process.
                </p>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;