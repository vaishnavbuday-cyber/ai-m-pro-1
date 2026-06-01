import axios from 'axios';

const API = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 30000,
});

export async function login(email, password) {
    const res = await API.post('/login', { email, password });
    return res.data;
}

export async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await API.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
}

export async function getSummary() {
    const res = await API.get('/summary');
    return res.data;
}

export async function getAnalysis(params = {}) {
    const res = await API.get('/analysis', { params });
    return res.data;
}

export async function getCharts() {
    const res = await API.get('/charts');
    return res.data;
}

export async function getHealth() {
    const res = await API.get('/health');
    return res.data;
}

export default API;
