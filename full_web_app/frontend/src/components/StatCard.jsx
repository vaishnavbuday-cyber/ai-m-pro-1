import React from 'react';

export default function StatCard({ label, value, icon, accentColor, delay = 0 }) {
    return (
        <div
            className="stat-card"
            style={{
                '--card-accent': accentColor,
                animationDelay: `${delay * 0.1}s`,
            }}
        >
            <div className="stat-card-icon">{icon}</div>
            <div className="stat-card-value">{value}</div>
            <div className="stat-card-label">{label}</div>
        </div>
    );
}
