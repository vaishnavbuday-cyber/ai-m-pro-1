import React, { useRef, useCallback } from 'react';

export default function ChartCard({ title, icon, children }) {
    const chartRef = useRef(null);

    const handleExport = useCallback(() => {
        const svgElement = chartRef.current?.querySelector('svg');
        if (!svgElement) return;

        const svgData = new XMLSerializer().serializeToString(svgElement);
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = () => {
            canvas.width = img.width * 2;
            canvas.height = img.height * 2;
            ctx.scale(2, 2);
            ctx.fillStyle = getComputedStyle(document.documentElement)
                .getPropertyValue('--bg-primary').trim() || '#0e1117';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            const link = document.createElement('a');
            link.download = `${(title || 'chart').replace(/\s+/g, '_').toLowerCase()}.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();
        };

        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    }, [title]);

    return (
        <div className="chart-card">
            <div className="chart-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {icon && <span className="chart-icon">{icon}</span>}
                    <span className="chart-title">{title}</span>
                </div>
                <button
                    className="chart-export-btn"
                    onClick={handleExport}
                    title="Download chart as PNG"
                >
                    📥
                </button>
            </div>
            <div ref={chartRef}>
                {children}
            </div>
        </div>
    );
}
