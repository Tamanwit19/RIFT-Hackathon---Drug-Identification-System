import React from 'react';
import Dashboard from './pages/Dashboard';


function App() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans antialiased text-slate-900 selection:bg-blue-100 selection:text-blue-900">
      
      {/* Navigation Header */}
      <nav className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-linear-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg shadow-blue-200">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-slate-900">
                PharmaGenie <span className="text-blue-600 font-medium">Pro</span>
              </span>
              <div className="flex items-center space-x-1">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">System Ready</span>
              </div>
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            <a href="#guidelines" className="text-sm font-semibold text-slate-600 hover:text-blue-600 transition-colors">CPIC Library</a>
            <a href="#docs" className="text-sm font-semibold text-slate-600 hover:text-blue-600 transition-colors">API Docs</a>
            <button className="bg-slate-900 text-white px-5 py-2.5 rounded-xl text-sm font-bold hover:bg-slate-800 transition-all active:scale-95 shadow-md shadow-slate-200">
              Provider Login
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="relative">
        <Dashboard />
      </main>

      {/* Footer Component */}
      <footer className="bg-white border-t border-slate-200 py-12 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <p className="text-slate-500 text-sm leading-relaxed max-w-md">
                This platform is a clinical decision support tool designed to assist healthcare professionals. 
                All genetic interpretations are based on current CPIC guidelines.
              </p>
            </div>
            <div className="flex flex-col md:items-end space-y-2">
              <div className="flex space-x-6 text-xs font-bold text-slate-400 uppercase tracking-widest">
                <a href="#" className="hover:text-blue-600 transition-colors">Privacy</a>
                <a href="#" className="hover:text-blue-600 transition-colors">Security</a>
                <a href="#" className="hover:text-blue-600 transition-colors">HIPAA Compliance</a>
              </div>
              <p className="text-slate-400 text-xs mt-4 italic">
                © 2026 PharmaGenie Precision Systems. Data encrypted at rest (AES-256).
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;