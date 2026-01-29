// ui.js - UI Rendering Functions

export const ui = {
    // Switch between views
    showView(viewId) {
        document.querySelectorAll('.view').forEach(el => {
            el.classList.remove('active');
            el.classList.add('hidden');
        });

        const activeView = document.getElementById(viewId);
        if (activeView) {
            activeView.classList.remove('hidden');
            activeView.classList.add('active');
        }
    },

    // Render employee list/selector
    renderEmployeeList(employees, selectedIndex) {
        const list = document.getElementById('employee-list');
        if (!list) return;

        list.innerHTML = '';
        employees.forEach((emp, idx) => {
            const div = document.createElement('div');
            div.className = 'employee-item';
            if (idx === selectedIndex) {
                div.classList.add('active');
            }
            div.textContent = emp.nombre_completo;
            div.onclick = () => {
                if (idx !== selectedIndex) {
                    // Llamar función global para cambiar empleado
                    if (typeof changeEmployee === 'function') {
                        changeEmployee(idx - selectedIndex);
                    }
                }
            };
            list.appendChild(div);
        });
    },

    // Render user profile
    renderProfile(user) {
        // user es un array, tomar el primer elemento
        if (Array.isArray(user) && user.length > 0) {
            user = user[0];
        }
        const nameEl = document.getElementById('user-name');
        const roleEl = document.getElementById('user-role');

        if (nameEl) nameEl.textContent = user.nombre_completo || 'Usuario';
        if (roleEl) roleEl.textContent = user.categoria || 'Vigilante';
    },

    // Render calendar grid
    renderCalendar(scheduleData, employeeName, year, month) {
        const grid = document.getElementById('calendar-grid');
        grid.innerHTML = ''; // Clear previous

        const daysInMonth = new Date(year, month, 0).getDate();
        const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        // Get shifts for the specific employee
        let userShifts = {};
        if (scheduleData && scheduleData.cuadrante && employeeName) {
            userShifts = scheduleData.cuadrante[employeeName] || {};
        }

        for (let i = 1; i <= daysInMonth; i++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'day-cell';

            // Check for weekend
            const date = new Date(year, month - 1, i);
            const dayOfWeek = date.getDay(); // 0 = Sunday, 6 = Saturday

            if (dayOfWeek === 0 || dayOfWeek === 6) {
                dayCell.classList.add('weekend');
            }

            const dayNum = document.createElement('span');
            dayNum.className = 'day-number';
            dayNum.textContent = i;

            dayCell.appendChild(dayNum);

            // Check if there is a shift for this day
            const turnoData = userShifts[i] || {};
            const shiftCode = typeof turnoData === 'object' ? turnoData.codigo : turnoData;
            const isHoliday = typeof turnoData === 'object' ? turnoData.es_festivo : false;

            if (isHoliday) {
                dayCell.classList.add('holiday');
            }

            if (shiftCode) {
                const shiftText = document.createElement('span');
                shiftText.className = 'shift-text';
                shiftText.classList.add(`shift-${shiftCode}`);
                shiftText.textContent = shiftCode; // Show "M", "T", "N", "D", "L"
                dayCell.appendChild(shiftText);
            }

            grid.appendChild(dayCell);
        }

        document.getElementById('current-month-display').textContent = `${monthNames[month - 1]} ${year}`;
    },

    showError(msg) {
        document.getElementById('login-error').textContent = msg;
    }
};
