import React from 'react';

/**
 * Skeleton loader component for loading states.
 * Usage: <Skeleton width="100%" height="200px" />
 * Or use the presets: <Skeleton.Card />, <Skeleton.Chart />, <Skeleton.StatCard />
 */
export default function Skeleton({ width = '100%', height = '20px', borderRadius = '8px', style = {} }) {
    return (
        <div
            className="skeleton"
            style={{
                width,
                height,
                borderRadius,
                ...style,
            }}
        />
    );
}

Skeleton.StatCard = function SkeletonStatCard() {
    return (
        <div className="stat-card">
            <Skeleton width="60%" height="14px" style={{ margin: '0 auto 12px' }} />
            <Skeleton width="40%" height="36px" style={{ margin: '0 auto 8px' }} />
            <Skeleton width="80%" height="12px" style={{ margin: '0 auto' }} />
        </div>
    );
};

Skeleton.Chart = function SkeletonChart() {
    return (
        <div className="chart-card">
            <div className="chart-header">
                <Skeleton width="150px" height="18px" />
            </div>
            <Skeleton width="100%" height="300px" borderRadius="12px" />
        </div>
    );
};

Skeleton.Row = function SkeletonRow({ count = 4 }) {
    return (
        <div className="stats-grid">
            {Array.from({ length: count }).map((_, i) => (
                <Skeleton.StatCard key={i} />
            ))}
        </div>
    );
};
