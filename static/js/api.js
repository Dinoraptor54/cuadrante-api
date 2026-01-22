// api.js - API Integration

// Detectar URL del API
const getAPIURL = () => {
    // Si estamos en localhost desarrollando el backend:
    if (window.location.hostname === 'localhost' && window.location.port === '8000') {
        return 'http://localhost:8000';
    }
    // Para todo lo demás (frontend local, deploy, móvil, etc), usar Producción:
    return 'https://cuadrante-api.onrender.com';
};

const API_URL = getAPIURL();

export const api = {
    // Login to get token
    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Credenciales incorrectas');
        }

        return await response.json();
    },

    // Get current user info
    async getMe(token) {
        const response = await fetch(`${API_URL}/api/empleados/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener perfil');
        }

        return await response.json();
    },

    // Get schedule for a specific month
    async getSchedule(token, year, month) {
        const response = await fetch(`${API_URL}/api/schedule/${year}/${month}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener cuadrante');
        }

        return await response.json();
    },

    // Request Vacation
    async requestVacation(token, startDate, endDate, reason) {
        const response = await fetch(`${API_URL}/api/vacaciones/solicitar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                fecha_inicio: startDate,
                fecha_fin: endDate,
                motivo: reason
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al solicitar vacaciones');
        }

        return await response.json();
    }
};
