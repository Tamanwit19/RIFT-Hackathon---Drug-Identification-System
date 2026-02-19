import React from 'react';

const StatusStepper = ({ progress, currentStep }) => {
  return (
    <div className="mt-8 p-6 bg-white border border-slate-200 rounded-xl shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-sm font-bold text-slate-700 animate-pulse">
          {currentStep}
        </h3>
        <span className="text-xs font-mono text-blue-600 font-bold">{progress}%</span>
      </div>
      <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
        <div 
          className="bg-blue-600 h-full transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};

export default StatusStepper;