import React, { useState, useEffect } from 'react';
import { getSummary, getHealth } from '../api';

export default function Settings() {
    const [health, setHealth] = useState(null);
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        async function fetchStatus() {
            try {
                const [h, s] = await Promise.all([getHealth(), getSummary().catch(() => null)]);
                setHealth(h);
                setSummary(s);
            } catch {
                // silent
            }
        }
        fetchStatus();
    }, []);

    return (
        <div className="page-content">
            <div className="page-header">
                <h1 className="page-title">⚙️ Settings</h1>
                <p className="page-subtitle">System status, configuration, and data management</p>
            </div>

            <div className="settings-grid">
                {/* System Status */}
                <div className="settings-card">
                    <div className="settings-title">📡 System Status</div>

                    <div className="filter-group">
                        <span className="filter-label">Backend Server</span>
                        <div className={`status-badge ${health ? 'online' : 'offline'}`} style={{ display: 'inline-flex' }}>
                            <span className="status-dot"></span>
                            {health ? 'Connected' : 'Disconnected'}
                        </div>
                    </div>

                    {health && (
                        <>
                            <div className="filter-group">
                                <span className="filter-label">Data Loaded</span>
                                <div className={`status-badge ${health.dataLoaded ? 'online' : 'offline'}`} style={{ display: 'inline-flex' }}>
                                    <span className="status-dot"></span>
                                    {health.dataLoaded ? `Yes — ${health.recordCount} records` : 'No data loaded'}
                                </div>
                            </div>
                        </>
                    )}

                    {summary && (
                        <>
                            <div className="filter-group">
                                <span className="filter-label">Processing Status</span>
                                {summary.preprocessing && (
                                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                                        ✅ {summary.preprocessing.total_records} records loaded<br />
                                        🔄 {summary.preprocessing.duplicates_removed} duplicates removed<br />
                                        🔧 {summary.preprocessing.missing_fixed} missing values fixed
                                    </div>
                                )}
                            </div>
                        </>
                    )}
                </div>

                {/* Quick Stats */}
                <div className="settings-card">
                    <div className="settings-title">📊 Quick Stats Summary</div>

                    {summary ? (
                        <div style={{ display: 'grid', gap: '12px' }}>
                            <div className="filter-group">
                                <span className="filter-label">Total Accidents</span>
                                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-blue)' }}>{summary.total}</div>
                            </div>
                            <div className="filter-group">
                                <span className="filter-label">Fatal / Major / Minor</span>
                                <div style={{ display: 'flex', gap: '16px', fontSize: '0.9rem' }}>
                                    <span style={{ color: 'var(--accent-red)' }}>💀 {summary.fatal}</span>
                                    <span style={{ color: 'var(--accent-orange)' }}>⚠️ {summary.major}</span>
                                    <span style={{ color: 'var(--accent-green)' }}>🩹 {summary.minor}</span>
                                </div>
                            </div>
                            <div className="filter-group">
                                <span className="filter-label">Peak Hour</span>
                                <div style={{ color: 'var(--text-primary)', fontSize: '0.9rem' }}>
                                    {summary.peakHour != null ? `${summary.peakHour}:00` : 'N/A'}
                                </div>
                            </div>
                            <div className="filter-group">
                                <span className="filter-label">Most Dangerous Area</span>
                                <div style={{ color: 'var(--accent-red)', fontSize: '0.9rem' }}>
                                    {summary.mostDangerous || 'N/A'}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Upload a dataset to see statistics.</p>
                    )}
                </div>

                {/* About */}
                <div className="settings-card">
                    <div className="settings-title">ℹ️ About This System</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
                        <p><strong>Traffic Accident Analysis System</strong></p>
                        <p>An intelligent, user-friendly system that analyzes traffic accident data and presents meaningful
                            insights through interactive visualizations, reports, and predictive indicators.</p>
                        <br />
                        <p><strong>Tech Stack:</strong></p>
                        <p>Backend: Python Flask, Pandas, NumPy</p>
                        <p>Frontend: React + Vite, Recharts, Axios</p>
                    </div>
                </div>

                {/* How to Use */}
                <div className="settings-card">
                    <div className="settings-title">📖 How to Use</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
                        <ol style={{ paddingLeft: '20px' }}>
                            <li>Go to <strong>Home</strong> page and upload your CSV/Excel dataset</li>
                            <li>Navigate to <strong>Dashboard</strong> to see overview statistics and charts</li>
                            <li>Visit <strong>Analysis</strong> for detailed breakdowns by weather, cause, and vehicle type</li>
                            <li>Check <strong>Settings</strong> for system status and summary</li>
                        </ol>
                        <br />
                        <p><strong>Expected Columns:</strong> Location, Date, Time, Vehicle_Type, Weather, Severity, Cause, Latitude, Longitude, Injuries, Fatalities</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
