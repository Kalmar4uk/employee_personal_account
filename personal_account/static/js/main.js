document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('menuOverlay');
    const body = document.body;
    
    // Проверяем, мобильное ли устройство
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Открытие/закрытие меню
    menuToggle.addEventListener('click', function() {
        if (!isMobile()) return; // На ПК ничего не делаем
        
        this.classList.toggle('active');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        body.classList.toggle('menu-open');
        
        // Блокируем прокрутку
        if (body.classList.contains('menu-open')) {
            body.style.overflow = 'hidden';
        } else {
            body.style.overflow = '';
        }
    });
    
    // Закрытие меню при клике на оверлей
    overlay.addEventListener('click', function() {
        if (!isMobile()) return;
        closeMenu();
    });
    
    // Закрытие меню при клике на ссылку
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            if (isMobile()) {
                closeMenu();
            }
        });
    });
    
    // Закрытие меню при изменении размера окна
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            closeMenu();
        }
    });
    
    // Функция закрытия меню
    function closeMenu() {
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        body.classList.remove('menu-open');
        body.style.overflow = '';
    }
});