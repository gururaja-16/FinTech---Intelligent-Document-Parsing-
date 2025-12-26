import React, { useState } from "react";
import "./App.css";

function DocumentParser() {
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
    <div
      style={{
        padding: "20px",
        maxWidth: "1200px",
        margin: "0 auto",
        background: "#f8f9fa",
        minHeight: "100vh",
      }}
    >
      {/* Header */}
      <div
        style={{
          background:
            "linear-gradient(135deg, #667eea 0%, #764ba2 40%, #a855f7 100%)",
          color: "white",
          padding: "40px 32px",
          borderRadius: "20px",
          marginBottom: "24px",
          boxShadow: "0 12px 30px rgba(15,23,42,0.25)",
        }}
      >
        <h1
          style={{
            margin: "0 0 8px 0",
            fontSize: "2.4em",
            letterSpacing: "0.03em",
          }}
        >
          🚀 LexScan-Auto - Week 1, 2 & 3
        </h1>
        <p style={{ margin: 0, fontSize: "14px", opacity: 0.95 }}>
          Extract structured data from financial and legal documents using OCR,
          NER, and Rule-Based Post-Processing
        </p>
      </div>

      {/* Upload Section */}
      <div
        style={{
          background: "white",
          padding: "32px 28px",
          borderRadius: "20px",
          marginBottom: "24px",
          boxShadow: "0 10px 25px rgba(15,23,42,0.08)",
        }}
      >
        <h3
          style={{
            margin: "0 0 20px 0",
            fontSize: "18px",
            fontWeight: 700,
            display: "flex",
            alignItems: "center",
            gap: "8px",
            color: "#111827",
          }}
        >
          <span style={{ fontSize: "20px" }}>🗎</span>
          <span>Upload Document</span>
        </h3>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <input
            type="file"
            accept=".pdf,.jpg,.png"
            onChange={handleFileUpload}
            disabled={loading}
            style={{
              display: "block",
              padding: "12px 16px",
              border: "2px dashed #2563eb",
              borderRadius: "10px",
              background: "#f9fafb",
              fontSize: "14px",
              maxWidth: "360px",
              width: "100%",
              cursor: loading ? "not-allowed" : "pointer",
              textAlign: "center",
            }}
          />
          {loading && (
            <p style={{ color: "#6b7280", fontSize: "12px", margin: 0 }}>
              ⏳ Processing...
            </p>
          )}
          {file && !loading && (
            <p style={{ color: "#6b7280", fontSize: "12px", margin: 0 }}>
              ✓ Selected: {file.name}
            </p>
          )}
        </div>
      </div>

      {error && (
        <div
          style={{
            color: "#c33",
            padding: "12px 16px",
            background: "#f8d7da",
            borderRadius: "8px",
            marginBottom: "20px",
            fontSize: "13px",
          }}
        >
          ❌ {error}
        </div>
      )}

      {data && data.success && (
        <div>
          {/* Summary Cards */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: "12px",
              marginBottom: "20px",
            }}
          >
            <div
              style={{
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                color: "white",
                padding: "16px",
                borderRadius: "10px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: "24px", fontWeight: "bold" }}>
                {data.summary?.total_entities || 0}
              </div>
              <div style={{ fontSize: "12px", opacity: "0.9" }}>
                Total Entities
              </div>
            </div>

            <div
              style={{
                background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                color: "white",
                padding: "16px",
                borderRadius: "10px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: "24px", fontWeight: "bold" }}>
                {data.summary?.entity_types || 0}
              </div>
              <div style={{ fontSize: "12px", opacity: "0.9" }}>
                Entity Types
              </div>
            </div>

            <div
              style={{
                background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                color: "white",
                padding: "16px",
                borderRadius: "10px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: "24px", fontWeight: "bold" }}>
                {data.quality_score?.toFixed(2) || "N/A"}
              </div>
              <div style={{ fontSize: "12px", opacity: "0.9" }}>
                Quality Score
              </div>
            </div>
          </div>

          {/* Warnings */}
          {data.validation_report?.warnings &&
            data.validation_report.warnings.length > 0 && (
              <div
                style={{
                  background: "#fff8e1",
                  border: "1px solid #ffc107",
                  borderRadius: "10px",
                  padding: "12px 16px",
                  marginBottom: "20px",
                  fontSize: "12px",
                }}
              >
                <strong style={{ color: "#856404" }}>
                  ⚠️ {data.validation_report.warnings.length} Warning(s)
                </strong>
                <div style={{ marginTop: "6px" }}>
                  {data.validation_report.warnings.map((w, i) => (
                    <div key={i} style={{ color: "#856404", marginTop: "4px" }}>
                      • {w}
                    </div>
                  ))}
                </div>
              </div>
            )}

          {/* Entities - Simple Table Format */}
          <div style={{ marginBottom: "20px" }}>
            <h3
              style={{ margin: "0 0 12px 0", fontSize: "14px", color: "#333" }}
            >
              🎯 Detected Entities
            </h3>
            {data.entities &&
              Object.entries(data.entities).map(([label, items]) =>
                items && items.length > 0 ? (
                  <div
                    key={label}
                    style={{
                      background: "white",
                      border: "1px solid #e0e0e0",
                      borderRadius: "10px",
                      marginBottom: "12px",
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        background: "#f8f9fa",
                        padding: "10px 12px",
                        borderBottom: "1px solid #e0e0e0",
                        fontSize: "13px",
                        fontWeight: "600",
                        color: "#4A90E2",
                      }}
                    >
                      {label} ({items.length})
                    </div>
                    <div
                      style={{
                        maxHeight: "200px",
                        overflowY: "auto",
                      }}
                    >
                      {items.map((entity, i) => (
                        <div
                          key={i}
                          style={{
                            padding: "8px 12px",
                            borderBottom:
                              i < items.length - 1
                                ? "1px solid #f0f0f0"
                                : "none",
                            fontSize: "12px",
                            background: i % 2 === 0 ? "white" : "#fafafa",
                          }}
                        >
                          <div style={{ fontWeight: "500", color: "#333" }}>
                            {entity.original || entity.text}
                          </div>
                          {entity.standardized && (
                            <div
                              style={{
                                fontSize: "11px",
                                color: "#999",
                                marginTop: "2px",
                              }}
                            >
                              ISO: {entity.standardized}
                            </div>
                          )}
                          {entity.value !== undefined && (
                            <div
                              style={{
                                fontSize: "11px",
                                color: "#999",
                                marginTop: "2px",
                              }}
                            >
                              Value: ${entity.value?.toLocaleString()}{" "}
                              {entity.currency || ""}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : null
              )}
          </div>

          {/* Extracted Text */}
          <div
            style={{
              background: "white",
              border: "1px solid #e0e0e0",
              borderRadius: "10px",
              padding: "12px",
              fontSize: "12px",
            }}
          >
            <h3 style={{ margin: "0 0 8px 0", fontSize: "13px" }}>
              📝 Extracted Text ({data.text_length || 0} chars)
            </h3>
            <div
              style={{
                background: "#f8f9fa",
                padding: "10px",
                borderRadius: "6px",
                maxHeight: "150px",
                overflowY: "auto",
                fontFamily: "monospace",
                fontSize: "11px",
                color: "#555",
                lineHeight: "1.4",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
            >
              {data.text
                ? data.text.substring(0, 500) +
                  (data.text.length > 500 ? "..." : "")
                : "No text extracted"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DocumentParser;
