import React from 'react';

const NAV_ITEMS = [
    { id: 'home', icon: '🏠', label: 'Home' },
    { id: 'dashboard', icon: '📊', label: 'Dashboard' },
    { id: 'analysis', icon: '🔬', label: 'Analysis' },
    { id: 'settings', icon: '⚙️', label: 'Settings' },
];

export default function Sidebar({ activePage, setActivePage, collapsed, setCollapsed }) {
    return (
        <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
            <div className="sidebar-header">
                <span className="sidebar-logo">🚦</span>
                <span className="sidebar-title">Traffic Analysis</span>
            </div>

            <nav className="sidebar-nav">
                {NAV_ITEMS.map((item) => (
                    <button
                        key={item.id}
                        className={`nav-item ${activePage === item.id ? 'active' : ''}`}
                        onClick={() => setActivePage(item.id)}
                        title={item.label}
                    >
                        <span className="nav-icon">{item.icon}</span>
                        <span className="nav-label">{item.label}</span>
                    </button>
                ))}
            </nav>

            <button className="sidebar-toggle" onClick={() => setCollapsed(!collapsed)} title="Toggle sidebar">
                {collapsed ? '→' : '←'}
            </button>
        </aside>
    );
}
