import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import Settings from './pages/Settings';
import Login from './pages/Login';
import { getHealth } from './api';

export default function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [activePage, setActivePage] = useState('home');
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [recordCount, setRecordCount] = useState(0);

    // Check backend health on mount
    useEffect(() => {
        getHealth()
            .then((h) => {
                setDataLoaded(h.dataLoaded);
                setRecordCount(h.recordCount);
            })
            .catch(() => { });
    }, []);

    const handleUploadSuccess = (result) => {
        setDataLoaded(true);
        setRecordCount(result.rows);
    };

    const renderPage = () => {
        switch (activePage) {
            case 'home':
                return <Home onUploadSuccess={handleUploadSuccess} />;
            case 'dashboard':
                return <Dashboard />;
            case 'analysis':
                return <Analysis />;
            case 'settings':
                return <Settings />;
            default:
                return <Home onUploadSuccess={handleUploadSuccess} />;
        }
    };

    if (!isAuthenticated) {
        return <Login onLogin={() => setIsAuthenticated(true)} />;
    }

    return (
        <div className="app-layout">
            <Sidebar
                activePage={activePage}
                setActivePage={setActivePage}
                collapsed={sidebarCollapsed}
                setCollapsed={setSidebarCollapsed}
            />
            <div className="main-area">
                <Navbar dataLoaded={dataLoaded} recordCount={recordCount} />
                {renderPage()}
            </div>
        </div>
    );
}
