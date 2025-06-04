import React, { useState, useCallback } from 'react';
import axios from 'axios';
import './App.css'; // We'll create this for component-specific styles

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [caption, setCaption] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    setCaption('');
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      setSelectedFile(null);
      setPreview(null);
    }
  };

  const handleSubmit = useCallback(async () => {
    if (!selectedFile) {
      setError('Please select an image file first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    setIsLoading(true);
    setError('');
    setCaption('');    try {
      // Use environment variable for API URL, fallback to development proxy
      const baseUrl = import.meta.env.VITE_API_URL || '';
      const apiUrl = baseUrl ? `${baseUrl}/api/caption` : '/api/caption';
      console.log('Making request to:', apiUrl);
      
      const response = await axios.post(apiUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });
      setCaption(response.data.caption);    } catch (err: any) {
      console.error("Error uploading image:", err);
      if (err.code === 'ECONNABORTED') {
        setError('Request timeout. Please try again.');
      } else if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else if (err.message) {
        setError(`Network error: ${err.message}`);
      } else {
        setError('An unknown error occurred while generating the caption.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [selectedFile]);

  return (
    <div className="container">      <header>
        <h1>🖼️ Image Captioning</h1>
        <p>Upload an image and generate a caption for it!</p>
      </header>

      <main>
        <div className="upload-section">
          <input type="file" id="fileInput" onChange={handleFileChange} accept="image/png, image/jpeg, image/gif" />
          <label htmlFor="fileInput" className="file-label">
            {selectedFile ? selectedFile.name : 'Choose an image'}
          </label>
        </div>

        {preview && (
          <div className="image-preview-container">
            <h2>Image Preview:</h2>
            <img src={preview} alt="Selected preview" className="image-preview" />
          </div>
        )}

        {selectedFile && (
          <button onClick={handleSubmit} disabled={isLoading} className="submit-button">
            {isLoading ? 'Generating Caption...' : '✨ Generate Caption'}
          </button>
        )}        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Processing...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}

        {caption && !isLoading && (
          <div className="caption-result">
            <h2>Generated Caption:</h2>
            <p>{caption}</p>
          </div>
        )}
      </main>      <footer>
        <p>Powered by advanced image captioning</p>
      </footer>
    </div>
  );
}

export default App;
