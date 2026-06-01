import React, { useState, useRef } from 'react';
import { uploadFile } from '../api';

export default function Home({ onUploadSuccess }) {
    const [dragover, setDragover] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);

    const handleFile = async (file) => {
        if (!file) return;
        setUploading(true);
        setError(null);
        setResult(null);

        try {
            const data = await uploadFile(file);
            setResult(data);
            if (onUploadSuccess) onUploadSuccess(data);
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Is the backend running on port 5000?');
        } finally {
            setUploading(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragover(false);
        const file = e.dataTransfer.files[0];
        handleFile(file);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragover(true);
    };

    const handleDragLeave = () => setDragover(false);

    const handleClick = () => fileInputRef.current?.click();

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        handleFile(file);
    };

    return (
        <div className="page-content">
            <div className="page-header">
                <h1 className="page-title">🏠 Home</h1>
                <p className="page-subtitle">Upload your traffic accident dataset to get started with analysis</p>
            </div>

            {error && <div className="error-box">❌ {error}</div>}
            {result && (
                <div className="success-box">
                    ✅ Successfully loaded {result.rows} records from "{result.filename}"
                    {result.preprocessing && (
                        <span> — {result.preprocessing.duplicates_removed} duplicates removed, {result.preprocessing.missing_fixed} missing values fixed</span>
                    )}
                </div>
            )}

            <div
                className={`upload-zone ${dragover ? 'dragover' : ''}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={handleClick}
            >
                <div className="upload-icon">📁</div>
                <div className="upload-text">
                    {uploading ? 'Uploading...' : 'Drag & Drop your dataset here'}
                </div>
                <div className="upload-hint">Supported formats: CSV, Excel (.xlsx, .xls)</div>
                <button className="upload-btn" disabled={uploading}>
                    {uploading ? '⏳ Processing...' : '📤 Choose File'}
                </button>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    style={{ display: 'none' }}
                    onChange={handleFileChange}
                />
            </div>

            {result && result.preview && result.preview.length > 0 && (
                <div className="data-table-wrapper">
                    <div className="data-table-header">
                        📋 Dataset Preview — Showing first {result.preview.length} of {result.rows} rows
                    </div>
                    <div style={{ overflowX: 'auto' }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    {result.columns.slice(0, 10).map((col) => (
                                        <th key={col}>{col}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {result.preview.map((row, i) => (
                                    <tr key={i}>
                                        {result.columns.slice(0, 10).map((col) => (
                                            <td key={col}>{row[col] != null ? String(row[col]) : ''}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
