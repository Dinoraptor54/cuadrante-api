// auth.js - Authentication Logic
import { api } from './api.js';

const TOKEN_KEY = 'cuadrante_auth_token';

export const auth = {
    // Check if user is logged in
    isAuthenticated() {
        return !!localStorage.getItem(TOKEN_KEY);
    },

    // Get stored token
    getToken() {
        return localStorage.getItem(TOKEN_KEY);
    },

    // Perform login
    async login(username, password) {
        try {
            const data = await api.login(username, password);
            localStorage.setItem(TOKEN_KEY, data.access_token);
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    },

    // Perform logout
    logout() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem('user_info');
        window.location.reload();
    }
};
