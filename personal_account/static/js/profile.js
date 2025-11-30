// Отображение дней недели
function generateWeek() {
    var days = [
        'Пн',
        'Вт',
        'Ср',
        'Чт',
        'Пт',
        'Сб',
        'Вс'
    ]
    const weekDays = document.getElementById('week-days');
    weekDays.innerHTML = '';

    days.forEach((day) => {
        const Day = document.createElement('div');
        Day.className = 'weekday';
        Day.textContent = `${day}`;
        weekDays.appendChild(Day);
    });
}

// Отображение календаря
const scheduleData = window.scheduleData;
const monthData = window.month

function generateCalendar(year, month) {
    const calendarDays = document.getElementById('calendar-days');
    calendarDays.innerHTML = '';
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const firstDayOfWeek = firstDay.getDay() === 0 ? 7 : firstDay.getDay();

    
    for (let i = 1; i < firstDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'day day-empty';
        calendarDays.appendChild(emptyDay);
    }
    
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const date = new Date(year, month, day);
        const dateString = formatDate(date);
        const dayData = scheduleData[dateString] || { type: 'day-off', time: 'Выходной' };
        const dayElement = document.createElement('div');
        dayElement.className = `day ${dayData.type}`;
        
        const today = new Date();
        if (date.toDateString() === today.toDateString()) {
            dayElement.classList.add('current-day');
        }
        
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        
        const dayContent = document.createElement('div');
        dayContent.className = 'day-content';
        dayContent.textContent = dayData.time;
        
        dayElement.appendChild(dayNumber);
        dayElement.appendChild(dayContent);
        
        calendarDays.appendChild(dayElement);
    }
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

document.addEventListener('DOMContentLoaded', function() {
    generateWeek();
    generateCalendar(2025, monthData);
});
