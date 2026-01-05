// JavaScript для улучшения UX
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileWrapper = document.querySelector('.file-input-wrapper');
    const submitBtn = document.querySelector('.submit-btn');
    
    // Обработка выбора файла
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const file = this.files[0];
            
            // Показываем информацию о файле
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.style.display = 'block';
            
            // Добавляем стиль для выбранного файла
            fileWrapper.classList.add('file-selected');
            
            // Включаем кнопку отправки
            submitBtn.disabled = false;
        } else {
            // Скрываем информацию если файл не выбран
            fileInfo.style.display = 'none';
            fileWrapper.classList.remove('file-selected');
            submitBtn.disabled = true;
        }
    });
    
    // Drag & Drop функциональность
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileWrapper.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileWrapper.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileWrapper.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        fileWrapper.classList.add('drag-over');
    }
    
    function unhighlight() {
        fileWrapper.classList.remove('drag-over');
    }
    
    // Обработка drop
    fileWrapper.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
    
    // Форматирование размера файла
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Проверка размера файла перед отправкой
    const form = document.querySelector('.upload-form');
    form.addEventListener('submit', function(e) {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const maxSize = 10 * 1024 * 1024; // 10 MB
            
            if (file.size > maxSize) {
                e.preventDefault();
                alert('Файл слишком большой. Максимальный размер: 10 MB');
                return false;
            }
            
            // Показываем состояние загрузки
            submitBtn.innerHTML = `
                <svg class="btn-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2v4"></path>
                    <path d="m12 18 4-4-4-4"></path>
                    <path d="M20 12h-8"></path>
                    <path d="M4 12h4"></path>
                </svg>
                Загрузка...
            `;
            submitBtn.disabled = true;
        }
    });
});

// Дополнительный JavaScript для улучшения UX формы
document.addEventListener('DOMContentLoaded', function() {
    const dataTypeSelect = document.getElementById('dataType');
    const groupTypeSelect = document.getElementById('groupType');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileWrapper = document.querySelector('.file-input-wrapper');
    const submitBtn = document.querySelector('.submit-btn');
    const form = document.querySelector('.upload-form');
    
    // Проверка заполненности полей
    function validateForm() {
        const isDataTypeValid = dataTypeSelect.value !== '';
        const isGroupTypeValid = groupTypeSelect.value !== '';
        const isFileValid = fileInput.files.length > 0;
        
        submitBtn.disabled = !(isDataTypeValid && isGroupTypeValid && isFileValid);
        
        return isDataTypeValid && isGroupTypeValid && isFileValid;
    }
    
    // Слушатели изменений для выпадающих списков
    dataTypeSelect.addEventListener('change', function() {
        validateForm();
        updateFormBasedOnDataType();
    });
    
    groupTypeSelect.addEventListener('change', function() {
        validateForm();
    });
    
    // Обработка выбора файла
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            const file = this.files[0];
            
            // Показываем информацию о файле
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.style.display = 'block';
            
            // Добавляем стиль для выбранного файла
            fileWrapper.classList.add('file-selected');
        } else {
            // Скрываем информацию если файл не выбран
            fileInfo.style.display = 'none';
            fileWrapper.classList.remove('file-selected');
        }
        
        validateForm();
    });
    
    // Обновление формы в зависимости от типа данных
    function updateFormBasedOnDataType() {
        const dataType = dataTypeSelect.value;
        const fileHint = document.querySelector('.file-hint');
        
        if (dataType === 'shifts') {
            fileHint.textContent = 'Загрузите файл с расписанием смен (.xlsx, .xls)';
        } else if (dataType === 'vacations') {
            fileHint.textContent = 'Загрузите файл с информацией об отпусках (.xlsx, .xls)';
        } else {
            fileHint.textContent = 'Нажмите для выбора файла';
        }
    }
    
    // Drag & Drop функциональность
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileWrapper.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileWrapper.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileWrapper.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        fileWrapper.classList.add('drag-over');
    }
    
    function unhighlight() {
        fileWrapper.classList.remove('drag-over');
    }
    
    // Обработка drop
    fileWrapper.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
    
    // Форматирование размера файла
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Проверка перед отправкой
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            alert('Пожалуйста, заполните все поля формы');
            return false;
        }
        
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const maxSize = 10 * 1024 * 1024; // 10 MB
            
            // Проверка размера файла
            if (file.size > maxSize) {
                e.preventDefault();
                alert('Файл слишком большой. Максимальный размер: 10 MB');
                return false;
            }
            
            // Проверка расширения файла
            const allowedExtensions = ['.xlsx', '.xls'];
            const fileName = file.name.toLowerCase();
            const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
            
            if (!isValidExtension) {
                e.preventDefault();
                alert('Неподдерживаемый формат файла. Разрешенные форматы: .xlsx, .xls');
                return false;
            }
            
            // Показываем состояние загрузки
            submitBtn.innerHTML = `
                <svg class="btn-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" stroke-width="2"></circle>
                    <path d="M12 6v6l4 2" stroke-width="2"></path>
                </svg>
                Загрузка...
            `;
            submitBtn.disabled = true;
        }
    });
    
    // Инициализация
    validateForm(); // Изначально кнопка отключена
});