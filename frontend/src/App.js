import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setLoading(true);
    setError("");
    setData(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/process", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        setData(result);
      } else {
        setError(result.error || "Processing failed");
      }
    } catch (err) {
      setError("Server error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 LexScan-Auto - Week 3 Demo</h1>
        <p>
          Rule-Based Layer & Precision | ISO 8601 Dates | Amount Parsing |
          Quality Scoring
        </p>
      </header>

      <div className="upload-section">
        <input
          type="file"
          accept=".pdf,.jpg,.png"
          onChange={handleFileUpload}
          disabled={loading}
        />
        {loading && <p>⏳ Processing with Week 3 Pipeline...</p>}
        {file && <p>📄 Selected: {file.name}</p>}
      </div>

      {error && (
        <div
          className="error"
          style={{ color: "red", padding: "20px", background: "#f8d7da" }}
        >
          ❌ {error}
        </div>
      )}

      <div className="results">
        {data && data.success && (
          <div>
            {/* ⭐ WEEK 3: Quality Score Badge */}
            <div className="quality-badge">
              ⭐ Quality Score:{" "}
              {data.quality_score ? data.quality_score.toFixed(2) : "N/A"}/1.0
            </div>

            {/* ⚠️ WEEK 3: Warnings List */}
            {data.warnings && data.warnings.length > 0 && (
              <div className="warnings">
                <h3>⚠️ Validation Warnings ({data.warnings.length})</h3>
                {data.warnings.map((warning, i) => (
                  <p key={i}>• {warning}</p>
                ))}
              </div>
            )}

            {/* 📊 WEEK 3: Enhanced Entities Display */}
            <h2>📊 Extracted Entities ({data.summary?.total_entities || 0})</h2>

            {Object.entries(data.entities || {}).map(([label, items]) =>
              items && items.length > 0 ? (
                <div key={label} className="entity-group">
                  <h3>
                    {label} ({items.length})
                  </h3>
                  {items.map((entity, i) => (
                    <div key={i} className="entity-card">
                      {entity.original ? (
                        <>
                          <strong>{entity.original}</strong>
                          {entity.standardized && (
                            <div>
                              <small>
                                📅 ISO: <code>{entity.standardized}</code>
                              </small>
                            </div>
                          )}
                          {entity.value !== undefined && (
                            <div>
                              <small>
                                💰 Value:{" "}
                                <code>${entity.value?.toLocaleString()}</code>{" "}
                                {entity.currency}
                              </small>
                            </div>
                          )}
                        </>
                      ) : entity.text ? (
                        <strong>{entity.text}</strong>
                      ) : (
                        <strong>{JSON.stringify(entity)}</strong>
                      )}
                    </div>
                  ))}
                </div>
              ) : null
            )}

            {/* 📈 WEEK 3 Summary */}
            {data.summary && (
              <div className="summary">
                <h3>📈 Processing Summary</h3>
                <p>Total Entities: {data.summary.total_entities}</p>
                <p>Quality: {data.summary.quality}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
