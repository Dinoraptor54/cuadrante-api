// app.js - Main Application Logic
import { auth } from './auth.js';
import { api } from './api.js';
import { ui } from './ui.js';

// App State
const state = {
    currentUser: null,
    currentDate: new Date(),
    allEmployees: [],  // Lista de todos los empleados
    selectedEmployeeIndex: 0  // Empleado actualmente seleccionado
};

// Initialize App
async function init() {
    registerServiceWorker();
    setupEventListeners();
    handleRouting();
}

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js')
            .then(() => console.log('Service Worker Registered'))
            .catch(err => console.error('SW Error:', err));
    }
}

// Event Listeners
function setupEventListeners() {
    // Login Form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const user = document.getElementById('username').value;
            const pass = document.getElementById('password').value;

            const success = await auth.login(user, pass);
            if (success) {
                window.location.hash = '#dashboard';
            } else {
                ui.showError('Usuario o contraseña incorrectos');
                alert('Error al acceder: Verifica usuario/contraseña o tu conexión.');
            }
        });
    }

    // Logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            auth.logout();
        });
    }

    // Month Navigation
    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');

    if (prevBtn) prevBtn.addEventListener('click', () => changeMonth(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => changeMonth(1));

    // Hash Change (Routing)
    window.addEventListener('hashchange', handleRouting);
}

// Routing Logic
async function handleRouting() {
    const hash = window.location.hash || '#login';

    if (!auth.isAuthenticated() && hash !== '#login') {
        window.location.hash = '#login';
        return;
    }

    if (auth.isAuthenticated() && hash === '#login') {
        window.location.hash = '#dashboard';
        return;
    }

    switch (hash) {
        case '#login':
            ui.showView('login-view');
            break;
        case '#dashboard':
            await loadDashboard();
            ui.showView('dashboard-view');
            break;
        case '#schedule':
            loadSchedule();
            ui.showView('schedule-view');
            break;
        case '#vacation':
            ui.showView('vacation-view');
            break;
        default:
            ui.showView('dashboard-view');
    }
}

// ... (existing code) ...

// Event Listeners (Update)
function setupEventListeners() {
    // ... (existing listeners) ...

    // Vacation Form
    const vacationForm = document.getElementById('vacation-form');
    if (vacationForm) {
        vacationForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const start = document.getElementById('vac-start').value;
            const end = document.getElementById('vac-end').value;
            const reason = document.getElementById('vac-reason').value;
            const msgEl = document.getElementById('vacation-msg');

            try {
                msgEl.textContent = 'Enviando...';
                msgEl.style.color = 'var(--text-main)';

                const token = auth.getToken();
                await api.requestVacation(token, start, end, reason);

                msgEl.textContent = '✅ ¡Solicitud enviada correctamente!';
                msgEl.style.color = 'var(--success)';

                setTimeout(() => {
                    window.location.hash = '#dashboard';
                    vacationForm.reset();
                    msgEl.textContent = '';
                }, 2000);

            } catch (error) {
                msgEl.textContent = `❌ Error: ${error.message}`;
                msgEl.style.color = 'var(--error)';
            }
        });
    }

    // ... (rest of listeners) ...
}

// Change Month
function changeMonth(delta) {
    state.currentDate.setMonth(state.currentDate.getMonth() + delta);
    loadSchedule();
}

// Change Employee
function changeEmployee(delta) {
    const newIndex = state.selectedEmployeeIndex + delta;
    if (newIndex >= 0 && newIndex < state.allEmployees.length) {
        state.selectedEmployeeIndex = newIndex;
        ui.renderEmployeeList(state.allEmployees, state.selectedEmployeeIndex);
        ui.renderProfile(state.allEmployees[newIndex]);
        loadSchedule();
    }
}

// Load Dashboard Data
async function loadDashboard() {
    try {
        const token = auth.getToken();
        const employees = await api.getMe(token);

        // employees es un array de empleados
        state.allEmployees = Array.isArray(employees) ? employees : [employees];
        state.selectedEmployeeIndex = 0;

        // Mostrar lista de empleados y cargar el primero
        ui.renderEmployeeList(state.allEmployees, state.selectedEmployeeIndex);
        ui.renderProfile(state.allEmployees[0]);

        // Cargar turnos
        loadSchedule();

    } catch (error) {
        console.error(error);
        auth.logout();
    }
}

// Load Schedule Data
async function loadSchedule() {
    const year = state.currentDate.getFullYear();
    const month = state.currentDate.getMonth() + 1;

    try {
        const token = auth.getToken();
        // Fetch real data
        const data = await api.getSchedule(token, year, month);

        // Obtener el empleado seleccionado
        const selectedEmployee = state.allEmployees[state.selectedEmployeeIndex];

        // Renderizar calendario del empleado seleccionado
        ui.renderCalendar(data, selectedEmployee.nombre_completo, year, month);
    } catch (error) {
        console.error("No schedule found or error", error);
        // Render empty calendar if error (e.g. 404 no data)
        ui.renderCalendar(null, null, year, month);
    }
}

// Start App
init();
