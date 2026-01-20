document.addEventListener('DOMContentLoaded', function() {
    const selectInput = document.getElementById('employeeSearch');
    const selectWrapper = document.querySelector('.select-wrapper');
    const employeeDropdown = document.getElementById('employeeDropdown');
    const dropdownSearch = document.getElementById('dropdownSearch');
    const employeeList = document.getElementById('employeeList');
    const selectedUsername = document.getElementById('selectedUsername');
    const generateBtn = document.getElementById('generateBtn');
    const employeeError = document.getElementById('employeeError');
    const employeeCount = document.getElementById('employeeCount');
    
    let allEmployees = [];
    
    // Собираем данные о сотрудниках из HTML
    function collectEmployeesData() {
        const items = employeeList.querySelectorAll('.dropdown-item[data-username]');
        allEmployees = Array.from(items).map(item => {
            return {
                element: item,
                username: item.getAttribute('data-username'),
                name: item.querySelector('.employee-name').textContent.toLowerCase(),
                text: item.querySelector('.employee-name').textContent.toLowerCase()
            };
        });
    }
    
    // Фильтрация списка сотрудников
    function filterEmployees(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        
        if (!term) {
            // Показываем всех сотрудников
            allEmployees.forEach(emp => {
                emp.element.style.display = '';
            });
            updateEmployeeCount(allEmployees.length);
            return;
        }
        
        let visibleCount = 0;
        allEmployees.forEach(emp => {
            if (emp.text.includes(term)) {
                emp.element.style.display = '';
                visibleCount++;
            } else {
                emp.element.style.display = 'none';
            }
        });
        
        updateEmployeeCount(visibleCount);
        
        // Если ничего не найдено
        const noResults = employeeList.querySelector('.dropdown-empty');
        if (visibleCount === 0 && !noResults) {
            const li = document.createElement('li');
            li.className = 'dropdown-empty';
            li.textContent = 'Сотрудники не найдены';
            employeeList.appendChild(li);
        } else if (visibleCount > 0 && noResults) {
            noResults.remove();
        }
    }
    
    // Обновление счетчика сотрудников
    function updateEmployeeCount(count) {
        if (employeeCount) {
            employeeCount.textContent = `Найдено сотрудников: ${count}`;
        }
    }
    
    // Выбор сотрудника
    function selectEmployee(item) {
        const username = item.getAttribute('data-username');
        const name = item.querySelector('.employee-name').textContent;
        
        // Обновляем поле ввода
        selectInput.value = name;
        selectedUsername.value = username;
        
        // Снимаем выделение со всех элементов
        allEmployees.forEach(emp => {
            emp.element.classList.remove('selected');
        });
        
        // Выделяем выбранный элемент
        item.classList.add('selected');
        
        // Активируем кнопку
        generateBtn.disabled = false;
        
        // Скрываем ошибку если была
        employeeError.style.display = 'none';
        selectInput.classList.remove('error');
        
        // Закрываем выпадающий список
        closeDropdown();
    }
    
    // Открытие выпадающего списка
    function openDropdown() {
        selectWrapper.classList.add('active');
        dropdownSearch.focus();
        
        // Собираем данные при первом открытии
        if (allEmployees.length === 0) {
            collectEmployeesData();
        }
    }
    
    // Закрытие выпадающего списка
    function closeDropdown() {
        selectWrapper.classList.remove('active');
        dropdownSearch.value = '';
        
        // Сбрасываем фильтр
        filterEmployees('');
    }
    
    // Обработчики событий
    selectInput.addEventListener('click', openDropdown);
    
    dropdownSearch.addEventListener('input', function() {
        filterEmployees(this.value);
    });
    
    dropdownSearch.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDropdown();
        }
    });
    
    // Обработчик клика по сотруднику
    employeeList.addEventListener('click', function(e) {
        const item = e.target.closest('.dropdown-item[data-username]');
        if (item) {
            selectEmployee(item);
        }
    });
    
    // Закрытие при клике вне области
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.select-wrapper')) {
            closeDropdown();
        }
    });
    
    // Обработчик отправки формы
    document.querySelector('.generate-form').addEventListener('submit', function(event) {
        if (!selectedUsername.value) {
            event.preventDefault();
            employeeError.style.display = 'block';
            selectInput.classList.add('error');
            selectInput.focus();
        }
    });
    
    // Инициализация счетчика
    if (employeeCount) {
        const totalItems = employeeList.querySelectorAll('.dropdown-item[data-username]').length;
        updateEmployeeCount(totalItems);
    }
});