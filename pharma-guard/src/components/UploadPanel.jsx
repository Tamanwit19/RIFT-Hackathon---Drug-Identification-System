import React, { useState } from 'react';
import { Upload, FileText, X } from 'lucide-react';

const UploadPanel = ({ onFileSelect, selectedFile }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (file) => {
    if (file && (file.name.endsWith('.vcf') || file.name.endsWith('.vcf.gz'))) {
      onFileSelect(file);
    } else {
      alert("Please upload a valid VCF file.");
    }
  };

  return (
    <div 
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => { e.preventDefault(); setIsDragging(false); handleFile(e.dataTransfer.files[0]); }}
      className={`border-2 border-dashed rounded-xl p-8 transition-all ${
        isDragging ? 'border-blue-500 bg-blue-50' : 'border-slate-300 bg-white'
      }`}
    >
      {!selectedFile ? (
        <div className="flex flex-col items-center">
          <Upload className="w-12 h-12 text-slate-400 mb-4" />
          <p className="text-sm font-medium text-slate-700">Drag and drop VCF file</p>
          <p className="text-xs text-slate-500 mt-1 mb-4">Max size: 5MB (v4.2 Standard)</p>
          <label className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700">
            Browse Files
            <input type="file" className="hidden" onChange={(e) => handleFile(e.target.files[0])} accept=".vcf" />
          </label>
        </div>
      ) : (
        <div className="flex items-center justify-between bg-slate-50 p-4 rounded-lg">
          <div className="flex items-center space-x-3">
            <FileText className="text-blue-600" />
            <span className="text-sm font-semibold truncate max-w-[200px]">{selectedFile.name}</span>
          </div>
          <button onClick={() => onFileSelect(null)} className="text-slate-400 hover:text-red-500">
            <X className="w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadPanel;