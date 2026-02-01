// Глобальные переменные
let scheduleData = {
    employees: []
};

let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth();

const shiftsData = window.shiftsData;

console.log(shiftsData);

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', async function() {
    await loadScheduleData();
    generateWeeksView();
});

// Загрузка данных
async function loadScheduleData() {
    scheduleData = window.shiftsData;
    console.log("Загружено сотрудников:", scheduleData.employees.length);
}

// Генерация недельного представления
function generateWeeksView() {
    const weeksContainer = document.getElementById('weeks-container');
    if (!weeksContainer) return;
    
    weeksContainer.innerHTML = '';
    
    // Получаем недели месяца
    const weeks = getWeeksOfMonth(currentYear, currentMonth);
    
    // Для каждой недели создаем блок
    weeks.forEach((week, weekIndex) => {
        const weekBlock = createWeekBlock(week, weekIndex);
        weeksContainer.appendChild(weekBlock);
    });
    
    // Добавляем индикаторы скролла
    setTimeout(addScrollIndicator, 50);
}

// Получение недель месяца - ИСПРАВЛЕННАЯ ВЕРСИЯ
function getWeeksOfMonth(year, month) {
    const weeks = [];
    
    // Получаем первый день месяца
    const firstDayOfMonth = new Date(year, month, 1);
    
    // Получаем последний день месяца
    const lastDayOfMonth = new Date(year, month + 1, 0);
    
    // Начинаем с понедельника, даже если он в предыдущем месяце
    let currentDate = new Date(firstDayOfMonth);
    
    // Получаем день недели (0 - воскресенье, 1 - понедельник, ..., 6 - суббота)
    const dayOfWeek = currentDate.getDay();
    
    // Если день недели не понедельник (1), откатываемся назад к предыдущему понедельнику
    if (dayOfWeek !== 1) {
        // Для воскресенья (0) отнимаем 6 дней, для других дней отнимаем (dayOfWeek - 1) дней
        const daysToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
        currentDate.setDate(currentDate.getDate() - daysToMonday);
    }
    
    // Собираем недели
    while (currentDate <= lastDayOfMonth || weeks.length < 6) {
        const week = [];
        for (let i = 0; i < 7; i++) {
            const date = new Date(currentDate);
            week.push(date);
            currentDate.setDate(currentDate.getDate() + 1);
        }
        weeks.push(week);
        
        // Если следующая неделя полностью за пределами месяца, проверяем нужно ли продолжать
        if (currentDate > lastDayOfMonth) {
            // Проверяем, есть ли в следующей неделе хотя бы один день текущего месяца
            const nextWeekStart = new Date(currentDate);
            let hasCurrentMonthDay = false;
            
            for (let i = 0; i < 7; i++) {
                if (nextWeekStart.getMonth() === month) {
                    hasCurrentMonthDay = true;
                    break;
                }
                nextWeekStart.setDate(nextWeekStart.getDate() + 1);
            }
            
            // Если в следующей неделе нет дней текущего месяца, выходим
            if (!hasCurrentMonthDay) {
                break;
            }
        }
    }
    
    // Убедимся, что у нас всегда есть хотя бы 4 недели для отображения
    while (weeks.length < 4) {
        const lastWeek = weeks[weeks.length - 1];
        const lastDate = new Date(lastWeek[6]);
        
        const week = [];
        for (let i = 0; i < 7; i++) {
            const date = new Date(lastDate);
            date.setDate(date.getDate() + 1);
            week.push(date);
            lastDate.setDate(lastDate.getDate() + 1);
        }
        weeks.push(week);
    }
    
    console.log(`Сгенерировано недель для ${year}-${month + 1}:`, weeks.length);
    console.log("Первая неделя начинается с:", weeks[0][0].toDateString());
    console.log("Последняя неделя заканчивается:", weeks[weeks.length - 1][6].toDateString());
    
    return weeks;
}

// Создание блока недели
function createWeekBlock(weekDays, weekIndex) {
    const weekBlock = document.createElement('div');
    weekBlock.className = 'week-block';
    
    // Заголовок недели
    const weekHeader = document.createElement('div');
    weekHeader.className = 'week-header';
    
    const firstDate = weekDays[0];
    const lastDate = weekDays[6];
    
    weekHeader.textContent = `Неделя ${weekIndex + 1}: ${formatDateDisplay(firstDate)} - ${formatDateDisplay(lastDate)}`;
    weekBlock.appendChild(weekHeader);
    
    // Таблица недели
    const table = createWeekTable(weekDays);
    weekBlock.appendChild(table);
    
    return weekBlock;
}

// Создание таблицы недели
function createWeekTable(weekDays) {
    const table = document.createElement('table');
    table.className = 'week-table';
    
    // Заголовок таблицы - только дни недели
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // Заголовки дней
    weekDays.forEach(day => {
        const dayHeader = document.createElement('th');
        const isToday = isSameDay(day, new Date());
        const isCurrentMonth = day.getMonth() === currentMonth;
        
        dayHeader.innerHTML = `
            <div class="day-header">
                <div class="day-date">${day.getDate()}</div>
                <div class="day-weekday">${getWeekdayName(day)}</div>
                ${isToday ? '<div class="today">✓</div>' : ''}
                ${!isCurrentMonth ? '<div style="color:#bdc3c7;font-size:10px;margin-top:2px;">др.мес</div>' : ''}
            </div>
        `;
        
        if (!isCurrentMonth) {
            dayHeader.style.opacity = '0.6';
            dayHeader.style.backgroundColor = '#f5f5f5';
        }
        
        headerRow.appendChild(dayHeader);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Тело таблицы - одна строка с ячейками для каждого дня
    const tbody = document.createElement('tbody');
    const contentRow = document.createElement('tr');
    
    // Создаем ячейки для каждого дня недели
    weekDays.forEach(day => {
        const dateString = formatDate(day);
        const cell = createDayCell(day, dateString);
        contentRow.appendChild(cell);
    });
    
    tbody.appendChild(contentRow);
    table.appendChild(tbody);
    
    return table;
}

// Создание ячейки для дня
function createDayCell(day, dateString) {
    const cell = document.createElement('td');
    
    if (day.getMonth() !== currentMonth) {
        // Дни другого месяца - прочерк
        cell.innerHTML = '<div class="empty-day">-</div>';
    } else {
        // Получаем всех сотрудников, работающих в этот день
        const employeesInDay = getEmployeesForDay(dateString);
        
        if (employeesInDay.length > 0) {
            // Создаем контейнер для сотрудников этого дня
            const dayEmployees = document.createElement('div');
            dayEmployees.className = 'day-employees';
            
            // Сортируем сотрудников по времени начала смены
            employeesInDay.sort((a, b) => {
                const timeA = a.schedule[dateString].time;
                const timeB = b.schedule[dateString].time;
                return timeB.localeCompare(timeA);
            });
            
            // Добавляем карточки сотрудников
            employeesInDay.forEach(employee => {
                const employeeCard = createEmployeeCard(employee, dateString);
                dayEmployees.appendChild(employeeCard);
            });
            
            cell.appendChild(dayEmployees);
        } else {
            // Нет сотрудников в этот день - прочерк
            cell.innerHTML = '<div class="empty-day">-</div>';
        }
    }
    
    return cell;
}

// Получение сотрудников для конкретного дня
function getEmployeesForDay(dateString) {
    return scheduleData.employees.filter(employee => {
        return employee.schedule && employee.schedule[dateString];
    });
}

// Создание карточки сотрудника с учетом адаптивности
function createEmployeeCard(employee, dateString) {
    const schedule = employee.schedule[dateString];
    
    // Определяем тип смены по времени
    const shiftType = getShiftTypeFromTime(schedule.type_shift);
    
    const card = document.createElement('div');
    card.className = `employee-card-calendar shift-${shiftType}`;
    card.title = `${employee.name} - ${employee.position}\n${schedule.time}`;
    
    // Время смены
    const timeElement = document.createElement('div');
    timeElement.className = 'employee-time';
    timeElement.textContent = schedule.time;
    
    // Информация о сотруднике
    const infoElement = document.createElement('div');
    infoElement.className = 'employee-info-calendar';
    
    // Инициалы
    const initialsElement = document.createElement('div');
    initialsElement.className = 'employee-initials';
    initialsElement.style.backgroundColor = getRandomColor(employee.id);
    initialsElement.textContent = employee.initials || getInitials(employee.name);
    initialsElement.title = employee.name;
    
    // Детали
    const detailsElement = document.createElement('div');
    detailsElement.className = 'employee-details';
    
    // Имя (с переносами)
    const nameElement = document.createElement('div');
    nameElement.className = 'employee-name';
    nameElement.textContent = employee.name;
    
    // Должность (с переносами)
    const positionElement = document.createElement('div');
    positionElement.className = 'employee-position';
    positionElement.textContent = schedule.type_shift;
    
    detailsElement.appendChild(nameElement);
    detailsElement.appendChild(positionElement);
    
    infoElement.appendChild(initialsElement);
    infoElement.appendChild(detailsElement);
    
    card.appendChild(timeElement);
    card.appendChild(infoElement);
    
    return card;
}

// Определение типа смены по времени
function getShiftTypeFromTime(type_shift) {
    if (!type_shift) return 'day';
    
    if (type_shift.includes('Ночное дежурство')) {
        return 'night';
    } else if (type_shift.toLowerCase().includes('Отпуск')) {
        return 'vacation';
    } else {
        return 'day';
    }
}

// Вспомогательные функции
function formatDate(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function formatDateDisplay(date) {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    return `${day}.${month}`;
}

function getWeekdayName(date) {
    const weekdays = ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'];
    return weekdays[date.getDay()];
}

function isSameDay(date1, date2) {
    return date1.getDate() === date2.getDate() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getFullYear() === date2.getFullYear();
}

function getInitials(fullName) {
    return fullName.split(' ').map(word => word[0]).join('').toUpperCase();
}

function getRandomColor(id) {
    const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', 
                   '#9b59b6', '#1abc9c', '#d35400', '#c0392b'];
    return colors[parseInt(id) % colors.length];
}

// Функция для добавления индикатора скролла
function addScrollIndicator() {
    const weekBlocks = document.querySelectorAll('.week-block');
    
    weekBlocks.forEach(block => {
        if (block.scrollWidth > block.clientWidth) {
            block.addEventListener('scroll', function() {
                const scrollLeft = this.scrollLeft;
                const maxScroll = this.scrollWidth - this.clientWidth;
                
                if (scrollLeft > 0 && scrollLeft < maxScroll) {
                    this.classList.add('scrolling');
                } else {
                    this.classList.remove('scrolling');
                }
            });
            
            setTimeout(() => {
                if (block.scrollWidth > block.clientWidth) {
                    block.classList.add('scrolling');
                }
            }, 100);
        }
    });
}