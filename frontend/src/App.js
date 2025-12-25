import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleTextChange = (e) => {
    setText(e.target.value);
    setError(null);
  };

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/api/process-document', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process document');
    } finally {
      setLoading(false);
    }
  };

  const handleTextAnalysis = async () => {
    if (!text.trim()) {
      setError('Please enter some text first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('http://localhost:5000/api/analyze-text', { text });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  const getEntityColor = (label) => {
    const colors = {
      PARTY: '#3b82f6',
      DATE: '#10b981',
      AMOUNT: '#f59e0b',
      JURISDICTION: '#8b5cf6',
    };
    return colors[label] || '#6b7280';
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>FinTech Document Parser</h1>
          <p>Extract structured data from financial and legal documents using AI</p>
        </header>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            Upload Document
          </button>
          <button
            className={`tab ${activeTab === 'text' ? 'active' : ''}`}
            onClick={() => setActiveTab('text')}
          >
            Analyze Text
          </button>
        </div>

        <div className="input-section">
          {activeTab === 'upload' ? (
            <div className="upload-area">
              <input
                type="file"
                onChange={handleFileChange}
                accept=".pdf,.txt"
                id="file-input"
                className="file-input"
              />
              <label htmlFor="file-input" className="file-label">
                <div className="upload-icon">+</div>
                <div>{file ? file.name : 'Choose a PDF or TXT file'}</div>
              </label>
              <button
                onClick={handleFileUpload}
                disabled={loading || !file}
                className="btn btn-primary"
              >
                {loading ? 'Processing...' : 'Process Document'}
              </button>
            </div>
          ) : (
            <div className="text-area">
              <textarea
                value={text}
                onChange={handleTextChange}
                placeholder="Paste your contract or financial document text here..."
                rows="10"
                className="text-input"
              />
              <button
                onClick={handleTextAnalysis}
                disabled={loading || !text.trim()}
                className="btn btn-primary"
              >
                {loading ? 'Analyzing...' : 'Analyze Text'}
              </button>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}

        {results && (
          <div className="results-section">
            <h2>Extraction Results</h2>
            
            <div className="summary-cards">
              <div className="summary-card">
                <div className="summary-number">{results.summary.total_entities}</div>
                <div className="summary-label">Total Entities Found</div>
              </div>
              <div className="summary-card">
                <div className="summary-number">{results.summary.entity_types}</div>
                <div className="summary-label">Entity Types</div>
              </div>
            </div>

            {Object.keys(results.entities).length > 0 ? (
              <div className="entities-grid">
                {Object.entries(results.entities).map(([label, entities]) => (
                  <div key={label} className="entity-category">
                    <h3 style={{ color: getEntityColor(label) }}>
                      {label}
                      <span className="entity-count">{entities.length}</span>
                    </h3>
                    <div className="entity-list">
                      {entities.map((entity, idx) => (
                        <div
                          key={idx}
                          className="entity-item"
                          style={{ borderLeftColor: getEntityColor(label) }}
                        >
                          {entity.text}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-entities">
                No entities found in the document.
              </div>
            )}

            {results.text && (
              <div className="extracted-text">
                <h3>Extracted Text</h3>
                <pre>{results.text}</pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
