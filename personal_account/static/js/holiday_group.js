document.addEventListener('DOMContentLoaded', function() {
    
    // Фильтрация сотрудников по имени
    const filterInput = document.querySelector('.filter-input');
    if (filterInput) {
        filterInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            document.querySelectorAll('.section details').forEach(details => {
                const summary = details.querySelector('summary');
                const employeeName = summary.textContent.toLowerCase();
                
                if (employeeName.includes(searchTerm)) {
                    details.style.display = 'block';
                } else {
                    details.style.display = 'none';
                }
            });
        });
    }
    
    // Кнопки "Открыть все"/"Закрыть все"
    const openAllBtn = document.querySelector('.open-all-btn');
    const closeAllBtn = document.querySelector('.close-all-btn');
    
    if (openAllBtn && closeAllBtn) {
        openAllBtn.addEventListener('click', function() {
            document.querySelectorAll('.section details').forEach(details => {
                details.open = true;
            });
        });
        
        closeAllBtn.addEventListener('click', function() {
            document.querySelectorAll('.section details').forEach(details => {
                details.open = false;
            });
        });
    }
});