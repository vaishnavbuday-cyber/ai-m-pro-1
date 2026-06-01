import React, { useState } from 'react';
import { login } from '../api';

export default function Login({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError('');
        
        try {
            await login(email, password);
            onLogin();
        } catch (err) {
            if (err.message === 'Network Error' || !err.response) {
                setError('Cannot connect to server. Please restart the backend (start_backend.bat).');
            } else {
                setError(err.response?.data?.error || 'Failed to login. Please try again.');
            }
            setIsSubmitting(false);
        }
    };

    return (
        <div className="login-container">
            {/* Background decorative elements */}
            <div className="login-bg-shape shape-1"></div>
            <div className="login-bg-shape shape-2"></div>
            <div className="login-bg-shape shape-3"></div>

            <div className="login-card">
                <div className="login-header">
                    <div className="login-logo-icon">🚦</div>
                    <h2>Welcome Back</h2>
                    <p>Sign in to the Traffic Accident Analysis System</p>
                </div>
                
                <form className="login-form" onSubmit={handleSubmit}>
                    {error && <div className="error-box" style={{marginBottom: '10px', padding: '10px'}}>{error}</div>}
                    <div className="input-group">
                        <label>Email (Gmail)</label>
                        <div className="input-wrapper">
                            <span className="input-icon">📧</span>
                            <input 
                                type="email" 
                                placeholder="name@gmail.com" 
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required 
                            />
                        </div>
                    </div>
                    
                    <div className="input-group">
                        <label>Password</label>
                        <div className="input-wrapper">
                            <span className="input-icon">🔒</span>
                            <input 
                                type="password" 
                                placeholder="••••••••" 
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required 
                            />
                        </div>
                    </div>

                    <div className="login-options">
                        <label className="checkbox-label">
                            <input type="checkbox" /> Remember me
                        </label>
                        <a href="#" className="forgot-password">Forgot Password?</a>
                    </div>

                    <button type="submit" className={`login-btn ${isSubmitting ? 'submitting' : ''}`} disabled={isSubmitting}>
                        {isSubmitting ? (
                            <div className="loading-spinner-tiny"></div>
                        ) : (
                            'Sign In'
                        )}
                    </button>
                </form>
                
                <div className="login-footer">
                    <p>Don't have an account? <a href="#">Contact Admin</a></p>
                </div>
            </div>
        </div>
    );
}
