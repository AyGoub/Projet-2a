import React, { useState } from 'react';
import { Upload, BarChart2, Users, MessageCircle, Heart, Image, Clock } from 'lucide-react';
import DataUploader from './components/DataUploader';
import Dashboard from './components/Dashboard';
import { InstagramData } from './types';

function App() {
  const [data, setData] = useState<InstagramData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    try {
      const fileContent = await file.text();
      const jsonData = JSON.parse(fileContent);
      setData(jsonData);
    } catch (error) {
      console.error('Error parsing JSON:', error);
      alert('Error parsing JSON file. Please make sure it\'s a valid Instagram data export.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      {!data ? (
        <DataUploader onFileUpload={handleFileUpload} isLoading={isLoading} />
      ) : (
        <Dashboard data={data} />
      )}
    </div>
  );
}

export default App;