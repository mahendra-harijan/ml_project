import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, FileText, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const ResumeScreening = () => {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("Software Engineer with 3+ years experience in React, Node.js, MongoDB.");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (selected.type !== 'application/pdf') {
        setError('Only PDF files are supported.');
        setFile(null);
        return;
      }
      setError(null);
      setFile(selected);
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a resume first.');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please provide a job description.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post('http://localhost:8000/api/predict/resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto animate-in fade-in duration-500 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Resume Screening</h1>
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* Left Column: Input Form */}
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6 border border-gray-100">
            <h2 className="text-lg font-medium text-gray-900 mb-4">1. Upload Candidate Resume</h2>
            
            <div 
              className={`mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md transition-colors ${
                file ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-gray-400'
              }`}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="space-y-1 text-center cursor-pointer">
                <Upload className={`mx-auto h-12 w-12 ${file ? 'text-indigo-500' : 'text-gray-400'}`} />
                <div className="flex text-sm text-gray-600 justify-center">
                  <span className="relative rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                    {file ? file.name : "Upload a PDF file"}
                  </span>
                </div>
                <p className="text-xs text-gray-500">PDF up to 10MB</p>
              </div>
            </div>
            <input 
              type="file" 
              className="hidden" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              accept="application/pdf"
            />
          </div>

          <div className="bg-white shadow rounded-lg p-6 border border-gray-100">
            <h2 className="text-lg font-medium text-gray-900 mb-4">2. Job Description & Requirements</h2>
            <textarea
              rows={6}
              className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-3 border"
              placeholder="Paste job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading || !file}
            className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
              loading || !file ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
            } transition-colors`}
          >
            {loading ? (
              <span className="flex items-center">
                <div className="animate-spin -ml-1 mr-3 h-5 w-5 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                Analyzing Candidate...
              </span>
            ) : "Analyze & Predict"}
          </button>
          
          {error && (
            <div className="rounded-md bg-red-50 p-4 border border-red-200">
              <div className="flex">
                <div className="flex-shrink-0">
                  <AlertCircle className="h-5 w-5 text-red-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Results */}
        <div className="space-y-6">
          {result ? (
            <>
              {/* Prediction Card */}
              <div className={`shadow rounded-lg p-6 border-l-4 ${
                result.prediction === 'Selected' ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'
              }`}>
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-sm font-medium text-gray-500 uppercase tracking-wide">Prediction Result</h2>
                    <div className="mt-2 flex items-center">
                      {result.prediction === 'Selected' ? (
                        <CheckCircle className="h-8 w-8 text-green-500 mr-2" />
                      ) : (
                        <XCircle className="h-8 w-8 text-red-500 mr-2" />
                      )}
                      <span className={`text-3xl font-extrabold ${
                        result.prediction === 'Selected' ? 'text-green-700' : 'text-red-700'
                      }`}>
                        {result.prediction}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-500">Confidence</div>
                    <div className="text-2xl font-bold text-gray-900">
                      {result.probability !== null ? `${(result.probability * 100).toFixed(1)}%` : 'N/A'}
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-gray-200/50">
                  <p className="text-xs text-gray-500 flex items-center justify-between">
                    <span><strong>Model Used:</strong> {result.model} (v{result.model_version || '1.0'})</span>
                  </p>
                  <p className="text-xs text-gray-400 mt-2 italic flex items-start">
                    <AlertCircle className="h-4 w-4 mr-1 flex-shrink-0 inline" />
                    {result.disclaimer}
                  </p>
                </div>
              </div>

              {/* Extracted Info & Match */}
              <div className="bg-white shadow rounded-lg p-6 border border-gray-100">
                <h3 className="text-lg font-medium text-gray-900 mb-4 border-b pb-2">Candidate Profile</h3>
                
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Education</dt>
                    <dd className="mt-1 text-sm text-gray-900">{result.candidate.education} (CGPA: {result.candidate.cgpa})</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Experience</dt>
                    <dd className="mt-1 text-sm text-gray-900">{result.candidate.experience_years} years</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Projects / Internships</dt>
                    <dd className="mt-1 text-sm text-gray-900">{result.candidate.projects} / {result.candidate.internships}</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Certifications</dt>
                    <dd className="mt-1 text-sm text-gray-900">{result.candidate.certifications}</dd>
                  </div>
                </dl>

                <div className="mt-6 pt-4 border-t border-gray-100">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="text-sm font-medium text-gray-900">Skill Match Analysis</h4>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Score: {result.skill_match_score}%
                    </span>
                  </div>
                  
                  <div className="mt-3">
                    <p className="text-xs text-gray-500 mb-1">Matched Skills</p>
                    <div className="flex flex-wrap gap-1">
                      {result.matched_skills.length > 0 ? result.matched_skills.map((skill, i) => (
                        <span key={i} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-md">✓ {skill}</span>
                      )) : <span className="text-sm text-gray-500">None found</span>}
                    </div>
                  </div>
                  
                  <div className="mt-3">
                    <p className="text-xs text-gray-500 mb-1">Missing Requirements</p>
                    <div className="flex flex-wrap gap-1">
                      {result.missing_skills.length > 0 ? result.missing_skills.map((skill, i) => (
                        <span key={i} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-md">✗ {skill}</span>
                      )) : <span className="text-sm text-gray-500">All requirements met!</span>}
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white shadow rounded-lg p-6 border border-gray-100 h-full flex flex-col justify-center items-center text-center text-gray-400 min-h-[400px]">
              <FileText className="h-16 w-16 mb-4 text-gray-300" />
              <p className="text-lg font-medium text-gray-500">No Analysis Yet</p>
              <p className="text-sm max-w-sm mt-2">Upload a resume and click analyze to see the candidate profile and AI selection prediction.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResumeScreening;
