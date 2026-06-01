import React from 'react';
import { useTheme } from '../ThemeContext';

export default function Navbar({ dataLoaded, recordCount }) {
    const { theme, toggleTheme } = useTheme();

    return (
        <nav className="navbar">
            <div className="navbar-left">
                <span className="navbar-title">Traffic Accident Analysis System</span>
            </div>

            <div className="navbar-right">
                <button
                    className="theme-toggle-btn"
                    onClick={toggleTheme}
                    title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
                >
                    {theme === 'dark' ? '☀️' : '🌙'}
                </button>
                <div className={`status-badge ${dataLoaded ? 'online' : 'offline'}`}>
                    <span className="status-dot"></span>
                    {dataLoaded ? `${recordCount} records loaded` : 'No data loaded'}
                </div>
            </div>
        </nav>
    );
}
