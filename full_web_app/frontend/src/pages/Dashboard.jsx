import React, { useState, useEffect } from 'react';
import { getSummary, getAnalysis } from '../api';
import StatCard from '../components/StatCard';
import ChartCard from '../components/ChartCard';
import {
    BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    AreaChart, Area, Legend,
} from 'recharts';

const COLORS = ['#ff4757', '#ffa502', '#2ed573', '#70a1ff', '#a29bfe', '#fd79a8'];

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

export default function Dashboard() {
    const [summary, setSummary] = useState(null);
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                setLoading(true);
                const [sumData, anaData] = await Promise.all([getSummary(), getAnalysis()]);
                setSummary(sumData);
                setAnalysis(anaData);
            } catch (err) {
                setError(err.response?.data?.error || 'Failed to fetch data. Is the backend running?');
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="page-content">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading dashboard data...</p>
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
                <h1 className="page-title">📊 Dashboard</h1>
                <p className="page-subtitle">Overview of traffic accident statistics and trends</p>
            </div>

            {/* Stat Cards */}
            <div className="stat-grid">
                <StatCard label="Total Accidents" value={summary.total} icon="🚨" accentColor="#70a1ff" delay={0} />
                <StatCard label="Fatal" value={summary.fatal} icon="💀" accentColor="#ff4757" delay={1} />
                <StatCard label="Major" value={summary.major} icon="⚠️" accentColor="#ffa502" delay={2} />
                <StatCard label="Minor" value={summary.minor} icon="🩹" accentColor="#2ed573" delay={3} />
                <StatCard label="Total Fatalities" value={summary.totalFatalities} icon="☠️" accentColor="#ff6b81" delay={4} />
                <StatCard label="Peak Hour" value={summary.peakHour != null ? `${summary.peakHour}:00` : 'N/A'} icon="🕐" accentColor="#a29bfe" delay={5} />
            </div>

            {/* Charts */}
            <div className="chart-grid">
                {/* Monthly Trend */}
                {analysis.byMonth && (
                    <ChartCard title="Accident Trends Over Time" icon="📈">
                        <ResponsiveContainer width="100%" height={280}>
                            <AreaChart data={analysis.byMonth}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="name" tick={{ fontSize: 11 }} angle={-45} textAnchor="end" height={60} />
                                <YAxis tick={{ fontSize: 11 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Area type="monotone" dataKey="count" name="Accidents" stroke="#70a1ff" fill="rgba(112,161,255,0.15)" strokeWidth={2} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* By Location */}
                {analysis.byLocation && (
                    <ChartCard title="Accidents by Location" icon="📊">
                        <ResponsiveContainer width="100%" height={280}>
                            <BarChart data={analysis.byLocation.slice(0, 10)} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis type="number" tick={{ fontSize: 11 }} />
                                <YAxis dataKey="name" type="category" width={120} tick={{ fontSize: 10 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar dataKey="count" name="Accidents" fill="#70a1ff" radius={[0, 4, 4, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* Severity Pie */}
                {analysis.bySeverity && (
                    <ChartCard title="Severity Distribution" icon="🥧">
                        <ResponsiveContainer width="100%" height={280}>
                            <PieChart>
                                <Pie
                                    data={analysis.bySeverity}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    dataKey="value"
                                    nameKey="name"
                                    paddingAngle={3}
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                >
                                    {analysis.bySeverity.map((entry, index) => (
                                        <Cell key={index} fill={entry.fill || COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip content={<CustomTooltip />} />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}

                {/* Hourly Distribution */}
                {analysis.byHour && (
                    <ChartCard title="Accidents by Hour" icon="🕐">
                        <ResponsiveContainer width="100%" height={280}>
                            <LineChart data={analysis.byHour}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                                <YAxis tick={{ fontSize: 11 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Line type="monotone" dataKey="count" name="Accidents" stroke="#ffa502" strokeWidth={2} dot={{ r: 3 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    </ChartCard>
                )}
            </div>
        </div>
    );
}
