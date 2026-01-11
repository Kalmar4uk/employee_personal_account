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

// Обновление времени для работающих сотрудников
function updateWorkingTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    
    document.querySelectorAll('.employee-card.working .employee-status p:nth-child(3)').forEach(el => {
        el.textContent = `Текущее время: ${timeString}`;
    });
}

setInterval(updateWorkingTime, 60000);
updateWorkingTime();