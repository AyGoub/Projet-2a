import React, { useCallback, useState } from 'react';
import { Upload, FileJson, AlertCircle, Archive } from 'lucide-react';
import JSZip from 'jszip';

interface DataUploaderProps {
  onFileUpload: (file: File) => void;
  isLoading: boolean;
}

function DataUploader({ onFileUpload, isLoading }: DataUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const processZipFile = async (file: File) => {
    try {
      setError(null);
      const zip = new JSZip();
      const contents = await zip.loadAsync(file);
      
      // Look for the Instagram data JSON file
      let jsonFile: File | null = null;
      
      for (const [path, zipEntry] of Object.entries(contents.files)) {
        if (path.endsWith('.json') && path.includes('content')) {
          const blob = await zipEntry.async('blob');
          jsonFile = new File([blob], 'instagram_data.json', { type: 'application/json' });
          break;
        }
      }

      if (jsonFile) {
        onFileUpload(jsonFile);
      } else {
        setError('No Instagram data found in the ZIP file. Please make sure you uploaded the correct export.');
      }
    } catch (err) {
      setError('Error processing ZIP file. Please make sure it\'s a valid Instagram data export.');
    }
  };

  const handleFile = async (file: File) => {
    if (file.type === 'application/zip' || file.name.endsWith('.zip')) {
      await processZipFile(file);
    } else if (file.type === 'application/json') {
      onFileUpload(file);
    } else {
      setError('Please upload a ZIP file or JSON file from your Instagram data export.');
    }
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gradient-to-br from-purple-50 via-white to-pink-50">
      <div className="max-w-2xl w-full animate-fade-in">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-6 gradient-text">Instagram Insights</h1>
          <p className="text-xl text-gray-600">Discover your Instagram journey through data</p>
        </div>

        <div
          className={`
            border-3 border-dashed rounded-2xl p-12 text-center cursor-pointer
            transition-all duration-300 transform
            ${isDragging 
              ? 'border-purple-400 bg-purple-50 scale-102'
              : 'border-purple-200 hover:border-purple-300 hover:bg-purple-50/30'
            }
          `}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileInput')?.click()}
        >
          <input
            type="file"
            id="fileInput"
            className="hidden"
            accept=".zip,.json"
            onChange={handleFileInput}
          />
          
          {isLoading ? (
            <div className="space-y-4">
              <div className="w-16 h-16 border-4 border-purple-400 border-t-transparent rounded-full animate-spin mx-auto"/>
              <p className="text-lg text-purple-600 font-medium">Processing your data...</p>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="relative">
                <Archive className="w-20 h-20 mx-auto text-purple-400 animate-pulse" />
                <Upload className="w-8 h-8 text-purple-500 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
              </div>
              <div>
                <p className="text-2xl font-semibold text-gray-700 mb-2">
                  Drop your Instagram data ZIP file here
                </p>
                <p className="text-gray-500">or click to browse your files</p>
              </div>
              {error && (
                <div className="mt-4 p-4 bg-red-50 rounded-lg text-red-600 text-sm">
                  {error}
                </div>
              )}
            </div>
          )}
        </div>

        <div className="mt-12 space-y-6">
          <div className="card">
            <div className="card-header">
              <AlertCircle className="w-5 h-5 text-purple-500 mr-2" />
              <h2 className="card-title">How to Get Your Data</h2>
            </div>
            <ol className="space-y-4 text-gray-600">
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-medium mr-3">1</span>
                Open Instagram Settings
              </li>
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-medium mr-3">2</span>
                Go to "Privacy and Security"
              </li>
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-medium mr-3">3</span>
                Find "Data Download"
              </li>
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-medium mr-3">4</span>
                Request your data in JSON format
              </li>
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-medium mr-3">5</span>
                Upload the ZIP file when received
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataUploader;