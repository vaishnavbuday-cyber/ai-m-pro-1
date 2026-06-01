import React, { useState, useEffect } from 'react';
import { getAnalysis, getSummary } from '../api';
import ChartCard from '../components/ChartCard';
import {
    BarChart, Bar, PieChart, Pie, Cell,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    Legend,
} from 'recharts';

const BAR_COLORS = ['#70a1ff', '#a29bfe', '#fd79a8', '#ffa502', '#2ed573', '#ff4757', '#6c5ce7', '#00cec9', '#e17055', '#fdcb6e'];

function CustomTooltip({ active, payload, label }) {
    if (!active || !payload?.length) return null;
    return (
        <div className="custom-tooltip">
            <p className="label">{label}</p>
            {payload.map((entry, i) => (
                <p key={i} className="value" style={{ color: entry.color }}>
                    {entry.name}: {entry.value}
                </p>
            ))}
        </div>
    );
}

export default function Analysis() {
    const [analysis, setAnalysis] = useState(null);
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [ageRange, setAgeRange] = useState({ age1: 25, age2: 40, age3: 60 });
    const [isUpdating, setIsUpdating] = useState(false);

    useEffect(() => {
        async function fetchData() {
            try {
                if (!analysis) setLoading(true);
                else setIsUpdating(true);

                const [anaData, sumData] = await Promise.all([
                    getAnalysis(ageRange),
                    getSummary()
                ]);
                setAnalysis(anaData);
                setInsights(sumData.insights || []);
            } catch (err) {
                setError(err.response?.data?.error || 'Failed to fetch analysis data.');
            } finally {
                setLoading(false);
                setIsUpdating(false);
            }
        }
        fetchData();
    }, [ageRange]);

    if (loading) {
        return (
            <div className="page-content">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading analysis...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="page-content">
                <div className="error-box">❌ {error}</div>
            </div>
        );
    }

    return (
        <div className="page-content">
            <div className="page-header">
                <h1 className="page-title">🔬 Detailed Analysis</h1>
                <p className="page-subtitle">In-depth breakdown of accident data by multiple dimensions</p>
            </div>

            <div className="settings-bar" style={{
                marginBottom: '2rem',
                padding: '1.5rem',
                background: 'var(--card-bg)',
                borderRadius: '12px',
                border: '1px solid var(--border-color)',
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '1.2rem' }}>⚙️</span>
                    <h3 style={{ margin: 0, fontSize: '1.1rem' }}>Customize Age Groups</h3>
                    {isUpdating && <span className="loading-spinner-tiny"></span>}
                </div>
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '1.5rem'
                }}>
                    <div className="range-control">
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                            Age Limit 1 (Youth): <strong>{ageRange.age1}</strong>
                        </label>
                        <input
                            type="range" min="15" max="30" value={ageRange.age1}
                            onChange={(e) => setAgeRange({ ...ageRange, age1: parseInt(e.target.value) })}
                            style={{ width: '100%' }}
                        />
                    </div>
                    <div className="range-control">
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                            Age Limit 2 (Adult): <strong>{ageRange.age2}</strong>
                        </label>
                        <input
                            type="range" min="31" max="55" value={ageRange.age2}
                            onChange={(e) => setAgeRange({ ...ageRange, age2: parseInt(e.target.value) })}
                            style={{ width: '100%' }}
                        />
                    </div>
                    <div className="range-control">
                        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                            Age Limit 3 (Middle): <strong>{ageRange.age3}</strong>
                        </label>
                        <input
                            type="range" min="56" max="75" value={ageRange.age3}
                            onChange={(e) => setAgeRange({ ...ageRange, age3: parseInt(e.target.value) })}
                            style={{ width: '100%' }}
                        />
                    </div>
                </div>
                <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)', opacity: 0.7 }}>
                    Groups: &lt;{ageRange.age1 + 1} | {ageRange.age1 + 1}-{ageRange.age2} | {ageRange.age2 + 1}-{ageRange.age3} | {ageRange.age3 + 1}+
                </p>
            </div>

            <div className="chart-grid">
                {/* By Weather */}
                {analysis.byWeather && (
                    <ChartCard title="Accidents by Weather" icon="🌦">
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={analysis.byWeather}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                <YAxis tick={{ fontSize: 11 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar dataKey="count" name="Accidents" radius={[4, 4, 0, 0]}>
                                    {analysis.byWeather.map((_, i) => (
                                        <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Cause */}
                {analysis.byCause && (
                    <ChartCard title="Top Causes of Accidents" icon="⚠️">
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={analysis.byCause} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis type="number" tick={{ fontSize: 11 }} />
                                <YAxis dataKey="name" type="category" width={140} tick={{ fontSize: 10 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar dataKey="count" name="Accidents" fill="#ff4757" radius={[0, 4, 4, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Age Group */}
                {analysis.byAgeGroup && (
                    <ChartCard title="Accidents by Age Group" icon="👥">
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={analysis.byAgeGroup}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                <YAxis tick={{ fontSize: 11 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar dataKey="count" name="Accidents" radius={[4, 4, 0, 0]}>
                                    {analysis.byAgeGroup.map((_, i) => (
                                        <Cell key={i} fill={BAR_COLORS[(i + 2) % BAR_COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Road Type */}
                {analysis.byRoadType && (
                    <ChartCard title="Accidents by Road Type" icon="🛣">
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={analysis.byRoadType} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis type="number" tick={{ fontSize: 11 }} />
                                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 10 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar dataKey="count" name="Accidents" fill="#ffa502" radius={[0, 4, 4, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Light Condition */}
                {analysis.byLight && (
                    <ChartCard title="Accidents by Light Conditions" icon="🌓">
                        <ResponsiveContainer width="100%" height={280}>
                            <PieChart>
                                <Pie
                                    data={analysis.byLight}
                                    cx="50%" cy="50%" outerRadius={80}
                                    dataKey="count" nameKey="name"
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                >
                                    {analysis.byLight.map((_, i) => (
                                        <Cell key={i} fill={BAR_COLORS[(i + 4) % BAR_COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip content={<CustomTooltip />} />
                            </PieChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Region */}
                {analysis.byRegion && (
                    <ChartCard title="Accidents by Indian Region" icon="🗺">
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={analysis.byRegion}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                <YAxis tick={{ fontSize: 11 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar dataKey="count" name="Accidents" radius={[4, 4, 0, 0]}>
                                    {analysis.byRegion.map((_, i) => (
                                        <Cell key={i} fill={BAR_COLORS[(i + 6) % BAR_COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Vehicle Type */}
                {analysis.byVehicle && (
                    <ChartCard title="Accidents by Vehicle Type" icon="🚗">
                        <ResponsiveContainer width="100%" height={280}>
                            <PieChart>
                                <Pie
                                    data={analysis.byVehicle}
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={95}
                                    dataKey="count"
                                    nameKey="name"
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                >
                                    {analysis.byVehicle.map((_, i) => (
                                        <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip content={<CustomTooltip />} />
                            </PieChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Vehicle Radar */}
                {analysis.byVehicle && (
                    <ChartCard title="Vehicle Type Distribution (Radar)" icon="🎯">
                        <ResponsiveContainer width="100%" height={280}>
                            <RadarChart data={analysis.byVehicle.slice(0, 8)}>
                                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                                <PolarAngleAxis dataKey="name" tick={{ fontSize: 10 }} />
                                <PolarRadiusAxis tick={{ fontSize: 9 }} />
                                <Radar name="Accidents" dataKey="count" stroke="#a29bfe" fill="rgba(162,155,254,0.2)" strokeWidth={2} />
                            </RadarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}
            </div>

            {/* Key Insights */}
            {insights.length > 0 && (
                <div className="insights-panel">
                    <div className="section-title">💡 Key Insights</div>
                    {insights.map((insight, i) => (
                        <div key={i} className="insight-card" style={{ animationDelay: `${i * 0.08}s` }}>
                            {insight}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
