const { useState, useEffect, useRef, useMemo } = React;
const { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, Legend, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } = Recharts;

// ═══════════════════ Sidebar ═══════════════════
function Sidebar({ activePage, setActivePage, collapsed, setCollapsed }) {
    const pages = [
        { id: "dashboard", icon: "📊", label: "Dashboard" },
        { id: "analytics", icon: "📈", label: "Analytics" },
        { id: "map", icon: "🗺️", label: "Map View" },
        { id: "reports", icon: "📄", label: "Reports" },
    ];
    return (
        <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
            <div className="sidebar-logo">
                <span className="sidebar-logo-icon">🚦</span>
                <h2>TrafficAnalytics</h2>
            </div>
            {pages.map(p => (
                <div key={p.id} className={`nav-item ${activePage === p.id ? 'active' : ''}`} onClick={() => { setActivePage(p.id); if (window.innerWidth < 1024) setCollapsed(true); }}>
                    <span>{p.icon}</span><span>{p.label}</span>
                </div>
            ))}
            <div style={{ flex: 1 }} />
            <div className="nav-item" style={{ color: 'var(--text-muted)', fontSize: '0.78rem', textAlign: 'center' }}>
                v1.0 — Traffic Analysis System
            </div>
        </aside>
    );
}

// ═══════════════════ Navbar ═══════════════════
function Navbar({ collapsed, setCollapsed, darkMode, setDarkMode }) {
    return (
        <nav className="navbar">
            <div className="navbar-left">
                <button className="menu-btn" onClick={() => setCollapsed(!collapsed)}>☰</button>
                <input className="search-box" placeholder="Search locations, data..." />
            </div>
            <div className="navbar-right">
                <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
                    {darkMode ? '☀️' : '🌙'}
                </button>
                <div className="user-avatar">TA</div>
            </div>
        </nav>
    );
}

// ═══════════════════ Stat Card ═══════════════════
function StatCard({ label, value, detail, icon, accentColor, delay }) {
    return (
        <div className={`stat-card animate-in animate-in-delay-${delay}`} style={{ '--card-accent': accentColor }}>
            <span className="stat-card-icon">{icon}</span>
            <div className="stat-card-label">{label}</div>
            <div className="stat-card-value" style={{ color: accentColor }}>{value}</div>
            {detail && <div className="stat-card-detail">{detail}</div>}
        </div>
    );
}

// ═══════════════════ Chart Card ═══════════════════
function ChartCard({ title, icon, children }) {
    return (
        <div className="chart-card animate-in">
            <div className="chart-card-title">{icon} {title}</div>
            {children}
        </div>
    );
}

// ═══════════════════ Filter Panel ═══════════════════
function FilterPanel({ filters, setFilters }) {
    return (
        <div className="filter-panel animate-in">
            <div className="filter-group">
                <label className="filter-label">📍 Location</label>
                <select className="filter-select" value={filters.location} onChange={e => setFilters({ ...filters, location: e.target.value })}>
                    <option value="All">All Locations</option>
                    {LOCATIONS.map(l => <option key={l.name} value={l.name}>{l.name}</option>)}
                </select>
            </div>
            <div className="filter-group">
                <label className="filter-label">⚠️ Severity</label>
                <select className="filter-select" value={filters.severity} onChange={e => setFilters({ ...filters, severity: e.target.value })}>
                    <option value="All">All</option>
                    <option value="Fatal">Fatal</option>
                    <option value="Major">Major</option>
                    <option value="Minor">Minor</option>
                </select>
            </div>
            <div className="filter-group">
                <label className="filter-label">🚗 Vehicle Type</label>
                <select className="filter-select" value={filters.vehicle} onChange={e => setFilters({ ...filters, vehicle: e.target.value })}>
                    <option value="All">All Types</option>
                    {VEHICLE_TYPES.map(v => <option key={v} value={v}>{v}</option>)}
                </select>
            </div>
            <div className="filter-group">
                <label className="filter-label">🌦️ Weather</label>
                <select className="filter-select" value={filters.weather} onChange={e => setFilters({ ...filters, weather: e.target.value })}>
                    <option value="All">All Weather</option>
                    {WEATHER.map(w => <option key={w} value={w}>{w}</option>)}
                </select>
            </div>
            <div className="filter-group">
                <label className="filter-label">📅 Year</label>
                <select className="filter-select" value={filters.year} onChange={e => setFilters({ ...filters, year: e.target.value })}>
                    <option value="All">All Years</option>
                    <option value="2022">2022</option>
                    <option value="2023">2023</option>
                    <option value="2024">2024</option>
                </select>
            </div>
        </div>
    );
}

// ═══════════════════ Dashboard Page ═══════════════════
function DashboardPage({ stats, data }) {
    const COLORS = ['#ff4757', '#ffa502', '#2ed573', '#70a1ff', '#a29bfe', '#fd79a8', '#00cec9'];
    return (
        <div className="page-content">
            <h1 className="page-title">Dashboard Overview</h1>
            <p className="page-subtitle">Real-time traffic accident analysis and key metrics</p>
            <div className="stats-grid">
                <StatCard label="Total Accidents" value={stats.total} icon="🚗" accentColor="#70a1ff" delay={1} detail="All recorded incidents" />
                <StatCard label="Fatal" value={stats.fatal} icon="💀" accentColor="#ff4757" delay={2} detail={`${((stats.fatal / stats.total) * 100).toFixed(1)}% of total`} />
                <StatCard label="Major" value={stats.major} icon="🔶" accentColor="#ffa502" delay={3} detail={`${((stats.major / stats.total) * 100).toFixed(1)}% of total`} />
                <StatCard label="Minor" value={stats.minor} icon="🟢" accentColor="#2ed573" delay={4} detail={`${((stats.minor / stats.total) * 100).toFixed(1)}% of total`} />
            </div>
            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))' }}>
                <StatCard label="Peak Hour" value={`${stats.peakHour}:00`} icon="🕐" accentColor="#a29bfe" delay={1} />
                <StatCard label="Most Dangerous" value={stats.mostDangerous} icon="📍" accentColor="#ff6b81" delay={2} />
                <StatCard label="Total Fatalities" value={stats.totalFatalities} icon="☠️" accentColor="#ff4757" delay={3} />
            </div>
            <div className="charts-grid">
                <ChartCard title="Accidents Over Time" icon="📈">
                    <ResponsiveContainer width="100%" height={280}>
                        <AreaChart data={stats.byMonth}>
                            <defs><linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#70a1ff" stopOpacity={0.3} /><stop offset="95%" stopColor="#70a1ff" stopOpacity={0} /></linearGradient></defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                            <XAxis dataKey="name" tick={{ fill: '#8b95a5', fontSize: 11 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} />
                            <YAxis tick={{ fill: '#8b95a5', fontSize: 11 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                            <Area type="monotone" dataKey="count" stroke="#70a1ff" fillOpacity={1} fill="url(#colorCount)" strokeWidth={2.5} />
                        </AreaChart>
                    </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Severity Distribution" icon="🥧">
                    <ResponsiveContainer width="100%" height={280}>
                        <PieChart>
                            <Pie data={stats.bySeverity} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={5} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                                {stats.bySeverity.map((e, i) => <Cell key={i} fill={e.fill} />)}
                            </Pie>
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                        </PieChart>
                    </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Accidents by Location" icon="🏙️">
                    <ResponsiveContainer width="100%" height={280}>
                        <BarChart data={stats.byLocation.slice(0, 10)} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                            <XAxis type="number" tick={{ fill: '#8b95a5', fontSize: 11 }} />
                            <YAxis dataKey="name" type="category" width={120} tick={{ fill: '#8b95a5', fontSize: 10 }} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                                {stats.byLocation.slice(0, 10).map((e, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Accidents by Hour" icon="🕐">
                    <ResponsiveContainer width="100%" height={280}>
                        <BarChart data={stats.byHour}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                            <XAxis dataKey="name" tick={{ fill: '#8b95a5', fontSize: 9 }} interval={1} />
                            <YAxis tick={{ fill: '#8b95a5', fontSize: 11 }} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                            <Bar dataKey="count" fill="#a29bfe" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </ChartCard>
            </div>
        </div>
    );
}

// ═══════════════════ Analytics Page ═══════════════════
function AnalyticsPage({ stats }) {
    const COLORS = ['#70a1ff', '#ff4757', '#ffa502', '#2ed573', '#a29bfe', '#fd79a8', '#00cec9', '#fdcb6e', '#e17055', '#6c5ce7'];
    return (
        <div className="page-content">
            <h1 className="page-title">Advanced Analytics</h1>
            <p className="page-subtitle">Deep-dive into accident patterns and comparisons</p>
            <div className="charts-grid">
                <ChartCard title="Top Causes of Accidents" icon="⚠️">
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={stats.byCause} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                            <XAxis type="number" tick={{ fill: '#8b95a5', fontSize: 11 }} />
                            <YAxis dataKey="name" type="category" width={140} tick={{ fill: '#8b95a5', fontSize: 10 }} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                                {stats.byCause.map((e, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Weather Impact" icon="🌦️">
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie data={stats.byWeather.map((w, i) => ({ ...w, fill: COLORS[i % COLORS.length] }))} cx="50%" cy="50%" outerRadius={100} dataKey="count" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                                {stats.byWeather.map((e, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Pie>
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                        </PieChart>
                    </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Vehicle Type Analysis" icon="🚗">
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={stats.byVehicle}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                            <XAxis dataKey="name" tick={{ fill: '#8b95a5', fontSize: 9 }} angle={-30} textAnchor="end" height={60} />
                            <YAxis tick={{ fill: '#8b95a5', fontSize: 11 }} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                            <Bar dataKey="count" fill="#2ed573" radius={[6, 6, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Monthly Trend Comparison" icon="📊">
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={stats.byMonth}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                            <XAxis dataKey="name" tick={{ fill: '#8b95a5', fontSize: 9 }} angle={-30} textAnchor="end" height={60} />
                            <YAxis tick={{ fill: '#8b95a5', fontSize: 11 }} />
                            <Tooltip contentStyle={{ background: '#1a1f2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, color: '#e8eaed' }} />
                            <Line type="monotone" dataKey="count" stroke="#ffa502" strokeWidth={2.5} dot={{ fill: '#ffa502', r: 4 }} />
                        </LineChart>
                    </ResponsiveContainer>
                </ChartCard>
            </div>
        </div>
    );
}

// ═══════════════════ Map Page ═══════════════════
function MapPage({ data }) {
    const mapRef = useRef(null);
    const mapInstance = useRef(null);

    useEffect(() => {
        if (mapInstance.current) { mapInstance.current.remove(); mapInstance.current = null; }
        if (!mapRef.current) return;

        const m = L.map(mapRef.current).setView([18.5, 77.5], 5);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CartoDB', maxZoom: 18
        }).addTo(m);

        const colors = { Fatal: '#ff4757', Major: '#ffa502', Minor: '#2ed573' };
        data.forEach(d => {
            L.circleMarker([d.lat, d.lng], {
                radius: d.severity === 'Fatal' ? 8 : d.severity === 'Major' ? 6 : 4,
                fillColor: colors[d.severity] || '#70a1ff', color: colors[d.severity] || '#70a1ff',
                fillOpacity: 0.7, weight: 1
            }).bindPopup(`<b style="color:${colors[d.severity]}">${d.severity} Accident</b><br>📍 ${d.location}<br>📅 ${d.date}<br>🚗 ${d.vehicleType}<br>💥 ${d.cause}`).addTo(m);
        });

        // Legend
        const legend = L.control({ position: 'bottomleft' });
        legend.onAdd = function () {
            const div = L.DomUtil.create('div');
            div.innerHTML = '<div style="background:rgba(14,17,23,0.9);padding:12px 16px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);font-family:Inter,sans-serif;font-size:13px;color:white"><b>Severity</b><br><span style="color:#ff4757">● Fatal</span><br><span style="color:#ffa502">● Major</span><br><span style="color:#2ed573">● Minor</span></div>';
            return div;
        };
        legend.addTo(m);
        mapInstance.current = m;
        setTimeout(() => m.invalidateSize(), 100);
        return () => { if (mapInstance.current) { mapInstance.current.remove(); mapInstance.current = null; } };
    }, [data]);

    return (
        <div className="page-content">
            <h1 className="page-title">Accident Map</h1>
            <p className="page-subtitle">Geographic visualization of accident-prone areas</p>
            <div className="map-container animate-in"><div ref={mapRef} id="accident-map"></div></div>
        </div>
    );
}

// ═══════════════════ Reports Page ═══════════════════
function ReportsPage({ stats, data }) {
    const insights = [
        `📊 Total ${stats.total} accident records analyzed across ${new Set(data.map(d => d.location)).size} locations.`,
        `💀 Fatal accidents account for ${((stats.fatal / stats.total) * 100).toFixed(1)}% of all incidents.`,
        `📍 Most accident-prone area: <strong>${stats.mostDangerous}</strong> with ${stats.byLocation[0]?.count} incidents.`,
        `🕐 Peak accident hour: <strong>${stats.peakHour}:00</strong> hours.`,
        `☠️ Total fatalities recorded: <strong>${stats.totalFatalities}</strong>.`,
        `⚠️ Leading cause: <strong>${stats.byCause[0]?.name}</strong> (${stats.byCause[0]?.count} cases).`,
        `🌦 Most common weather: <strong>${stats.byWeather[0]?.name}</strong> (${stats.byWeather[0]?.count} incidents).`,
        `🚗 Most involved vehicle: <strong>${stats.byVehicle[0]?.name}</strong>.`,
    ];

    const downloadCSV = () => {
        const headers = "ID,Date,Time,Location,Severity,Vehicle Type,Weather,Cause,Injuries,Fatalities\n";
        const rows = data.map(d => `${d.id},${d.date},${d.time},${d.location},${d.severity},${d.vehicleType},${d.weather},${d.cause},${d.injuries},${d.fatalities}`).join('\n');
        const blob = new Blob([headers + rows], { type: 'text/csv' });
        const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'accident_report.csv'; a.click();
    };

    const downloadReport = () => {
        let text = "TRAFFIC ACCIDENT ANALYSIS REPORT\n" + "=".repeat(50) + "\n\n";
        text += `Total Accidents: ${stats.total}\nFatal: ${stats.fatal}\nMajor: ${stats.major}\nMinor: ${stats.minor}\nTotal Fatalities: ${stats.totalFatalities}\n\n`;
        text += "KEY INSIGHTS:\n";
        insights.forEach(i => { text += "  • " + i.replace(/<[^>]+>/g, '') + "\n"; });
        text += "\nTOP LOCATIONS:\n";
        stats.byLocation.slice(0, 10).forEach(l => { text += `  ${l.name}: ${l.count}\n`; });
        const blob = new Blob([text], { type: 'text/plain' });
        const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'analysis_report.txt'; a.click();
    };

    return (
        <div className="page-content">
            <h1 className="page-title">Reports & Insights</h1>
            <p className="page-subtitle">Key findings and downloadable reports</p>
            <div className="animate-in" style={{ marginBottom: 32 }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16 }}>💡 Key Insights</h3>
                {insights.map((ins, i) => <div key={i} className="insight-card" dangerouslySetInnerHTML={{ __html: ins }} />)}
            </div>
            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }} className="animate-in">
                <button className="report-btn" onClick={downloadCSV}>📥 Download Data (CSV)</button>
                <button className="report-btn secondary" onClick={downloadReport}>📄 Download Summary Report</button>
            </div>
        </div>
    );
}

// ═══════════════════ App ═══════════════════
function App() {
    const [activePage, setActivePage] = useState("dashboard");
    const [collapsed, setCollapsed] = useState(window.innerWidth < 1024);
    const [darkMode, setDarkMode] = useState(true);
    const [filters, setFilters] = useState({ location: 'All', severity: 'All', vehicle: 'All', weather: 'All', year: 'All' });

    useEffect(() => { document.body.className = darkMode ? '' : 'light-mode'; }, [darkMode]);

    const filteredData = useMemo(() => {
        return MOCK_DATA.filter(d => {
            if (filters.location !== 'All' && d.location !== filters.location) return false;
            if (filters.severity !== 'All' && d.severity !== filters.severity) return false;
            if (filters.vehicle !== 'All' && d.vehicleType !== filters.vehicle) return false;
            if (filters.weather !== 'All' && d.weather !== filters.weather) return false;
            if (filters.year !== 'All' && d.year !== parseInt(filters.year)) return false;
            return true;
        });
    }, [filters]);

    const stats = useMemo(() => computeStats(filteredData), [filteredData]);

    const renderPage = () => {
        switch (activePage) {
            case 'dashboard': return <DashboardPage stats={stats} data={filteredData} />;
            case 'analytics': return <AnalyticsPage stats={stats} />;
            case 'map': return <MapPage data={filteredData} />;
            case 'reports': return <ReportsPage stats={stats} data={filteredData} />;
            default: return <DashboardPage stats={stats} data={filteredData} />;
        }
    };

    return (
        <div className="app-layout">
            <Sidebar activePage={activePage} setActivePage={setActivePage} collapsed={collapsed} setCollapsed={setCollapsed} />
            <div className="main-content" style={{ marginLeft: collapsed ? 0 : 260 }}>
                <Navbar collapsed={collapsed} setCollapsed={setCollapsed} darkMode={darkMode} setDarkMode={setDarkMode} />
                <FilterPanel filters={filters} setFilters={setFilters} />
                {renderPage()}
            </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
