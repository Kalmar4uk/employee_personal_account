        // Фильтрация графика работы
        document.querySelectorAll('.filter-btn').forEach(button => {
            button.addEventListener('click', function() {
                // Убираем активный класс у всех кнопок
                document.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Добавляем активный класс текущей кнопке
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const rows = document.querySelectorAll('.schedule-table tbody tr');
                
                rows.forEach(row => {
                    if (row.classList.contains('week-divider')) {
                        // Всегда показываем разделители недель
                        row.style.display = '';
                        return;
                    }
                    
                    if (filter === 'all') {
                        row.style.display = '';
                    } else if (filter === 'work') {
                        if (row.querySelector('.day-icon.work-day')) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    } else if (filter === 'weekend') {
                        if (row.querySelector('.day-icon.weekend')) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    } else if (filter === 'current') {
                        if (row.classList.contains('current-day') || 
                            row.previousElementSibling.classList.contains('week-divider') && 
                            row.previousElementSibling.textContent.includes('Неделя 5')) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    }
                });
            });
        });