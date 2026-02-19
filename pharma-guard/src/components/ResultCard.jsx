import React from 'react';
import { ChevronDown, AlertCircle, CheckCircle, Info } from 'lucide-react';
import { riskColorMap } from '../utils/riskColorMap';

const RiskBadge = ({ label }) => {
  const style = riskColorMap[label] || riskColorMap.Unknown;
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${style.bg} ${style.text} ${style.border}`}>
      {label}
    </span>
  );
};

const ResultCard = ({ result }) => {
  const { drug, risk_assessment, pharmacogenomic_profile, clinical_recommendation, llm_generated_explanation } = result;
  
  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow mb-6">
      <div className="p-6 border-b border-slate-100 flex justify-between items-center">
        <div>
          <h3 className="text-xl font-bold text-slate-800">{drug}</h3>
          <p className="text-sm text-slate-500">Target Gene: <span className="font-mono font-bold text-blue-600">{pharmacogenomic_profile.primary_gene}</span></p>
        </div>
        <div className="text-right">
          <RiskBadge label={risk_assessment.risk_label} />
          <p className="text-xs text-slate-400 mt-2">Severity: {risk_assessment.severity}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 bg-slate-50/50">
        <div className="bg-white p-4 rounded-lg border border-slate-100">
          <p className="text-xs text-slate-500 uppercase font-bold mb-1">Diplotype</p>
          <p className="text-lg font-mono font-bold text-slate-800">{pharmacogenomic_profile.diplotype}</p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-slate-100">
          <p className="text-xs text-slate-500 uppercase font-bold mb-1">Phenotype</p>
          <p className="text-lg font-bold text-slate-800">{pharmacogenomic_profile.phenotype}</p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-slate-100">
          <p className="text-xs text-slate-500 uppercase font-bold mb-1">Confidence</p>
          <p className="text-lg font-bold text-slate-800">{(risk_assessment.confidence_score * 100).toFixed(0)}%</p>
        </div>
      </div>

      <div className="p-6 space-y-4">
        <div className="flex items-start space-x-3">
          <div className="mt-1"><CheckCircle className="w-5 h-5 text-blue-600" /></div>
          <div>
            <h4 className="font-bold text-slate-800">Clinical Recommendation</h4>
            <p className="text-sm text-slate-600 leading-relaxed">{clinical_recommendation.text}</p>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="flex items-center text-sm font-bold text-blue-800 mb-2">
              <Info className="w-4 h-4 mr-2" /> AI-Generated Pathophysiology
            </h4>
            <p className="text-sm text-blue-900 leading-relaxed italic">
              "{llm_generated_explanation.summary}"
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              {pharmacogenomic_profile.detected_variants.map(v => (
                <span key={v.rsid} className="text-[10px] bg-white px-2 py-0.5 rounded border border-blue-200 font-mono">
                  {v.rsid}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;