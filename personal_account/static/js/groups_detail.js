// Поиск сотрудников
document.getElementById('employee-search').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const employeeCards = document.querySelectorAll('.employee-card');
    
    employeeCards.forEach(card => {
        const employeeName = card.querySelector('h3').textContent.toLowerCase();
        if (employeeName.includes(searchTerm)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
});

// Фильтрация по статусу
document.getElementById('status-filter').addEventListener('change', function(e) {
    const status = e.target.value;
    const employeeCards = document.querySelectorAll('.employee-card');
    
    employeeCards.forEach(card => {
        if (status === 'all') {
            card.style.display = 'flex';
        } else if (card.classList.contains(status)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
});

// Сортировка сотрудников
document.getElementById('sort-by').addEventListener('change', function(e) {
    const sortBy = e.target.value;
    const employeesList = document.querySelector('.employees-list');
    const employeeCards = Array.from(document.querySelectorAll('.employee-card'));
    
    if (sortBy === 'name') {
        employeeCards.sort((a, b) => {
            const nameA = a.querySelector('h3').textContent;
            const nameB = b.querySelector('h3').textContent;
            return nameA.localeCompare(nameB);
        });
    } else if (sortBy === 'status') {
        employeeCards.sort((a, b) => {
            // Сначала работающие, затем на выходном
            if (a.classList.contains('working') && b.classList.contains('dayoff')) {
                return -1;
            } else if (a.classList.contains('dayoff') && b.classList.contains('working')) {
                return 1;
            } else {
                return 0;
            }
        });
    }
    
    // Очищаем контейнер и добавляем отсортированные карточки
    employeesList.innerHTML = '';
    employeeCards.forEach(card => {
        employeesList.appendChild(card);
    });
});

// Обновление времени для работающих сотрудников
function updateWorkingTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    
    document.querySelectorAll('.employee-card.working .employee-status p:nth-child(3)').forEach(el => {
        el.textContent = `Текущее время: ${timeString}`;
    });
}

// Обновляем время каждую минуту
setInterval(updateWorkingTime, 60000);
updateWorkingTime(); // Первоначальное обновление