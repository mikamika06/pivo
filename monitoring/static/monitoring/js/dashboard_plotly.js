document.addEventListener('DOMContentLoaded', function() {
    const priceMinInput = document.getElementById('price_min');
    const priceMaxInput = document.getElementById('price_max');
    const priceDisplay = document.getElementById('price_range_display');
    
    if (priceMinInput && priceMaxInput && priceDisplay) {
        function updatePriceDisplay() {
            const minValue = parseInt(priceMinInput.value);
            const maxValue = parseInt(priceMaxInput.value);
            
            if (minValue > maxValue) {
                priceMinInput.value = maxValue;
            }
            
            priceDisplay.textContent = `${priceMinInput.value} - ${priceMaxInput.value} грн`;
        }
        
        priceMinInput.addEventListener('input', updatePriceDisplay);
        priceMaxInput.addEventListener('input', updatePriceDisplay);
        
        updatePriceDisplay();
    }
    
    const form = document.getElementById('filters-form');
    if (form) {
        const selects = form.querySelectorAll('select');
        
        selects.forEach(select => {
            select.addEventListener('change', function() {
                showLoadingSpinner();
                form.submit();
            });
        });
        
        const dateInputs = form.querySelectorAll('input[type="date"]');
        dateInputs.forEach(input => {
            input.addEventListener('change', function() {
                showLoadingSpinner();
                form.submit();
            });
        });
    }
    
    animateCards();
    
    configurePlotlyCharts();
});

function resetFilters() {
    const currentPath = window.location.pathname;
    window.location.href = currentPath;
}

function showLoadingSpinner() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border text-light';
    spinner.setAttribute('role', 'status');
    spinner.style.width = '3rem';
    spinner.style.height = '3rem';
    
    const spinnerText = document.createElement('span');
    spinnerText.className = 'visually-hidden';
    spinnerText.textContent = 'Завантаження...';
    
    spinner.appendChild(spinnerText);
    overlay.appendChild(spinner);
    document.body.appendChild(overlay);
}

function animateCards() {
    const cards = document.querySelectorAll('.card, .stats-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

function configurePlotlyCharts() {
    const plotlyDivs = document.querySelectorAll('.js-plotly-plot');
    
    plotlyDivs.forEach(div => {
        window.addEventListener('resize', function() {
            Plotly.Relayout(div, {
                'xaxis.autorange': true,
                'yaxis.autorange': true
            });
        });
        
        div.on('plotly_click', function(data) {
            handleChartClick(data);
        });
        
        div.on('plotly_hover', function(data) {
            handleChartHover(data);
        });
    });
}

function handleChartClick(data) {
    console.log('Chart clicked:', data);
    
    if (data.points && data.points.length > 0) {
        const point = data.points[0];
        
        console.log('Selected point:', {
            x: point.x,
            y: point.y,
            label: point.label
        });
    }
}

function handleChartHover(data) {
    if (data.points && data.points.length > 0) {
        const point = data.points[0];
        
        if (point.data && point.data.type === 'bar') {
            data.event.target.style.cursor = 'pointer';
        }
    }
}

function exportChartAsPNG(chartId, filename) {
    const chartElement = document.getElementById(chartId);
    
    if (chartElement) {
        Plotly.downloadImage(chartElement, {
            format: 'png',
            width: 1200,
            height: 800,
            filename: filename || 'chart'
        });
    }
}

function exportChartAsSVG(chartId, filename) {
    const chartElement = document.getElementById(chartId);
    
    if (chartElement) {
        Plotly.downloadImage(chartElement, {
            format: 'svg',
            width: 1200,
            height: 800,
            filename: filename || 'chart'
        });
    }
}

function printDashboard() {
    window.print();
}

function exportDataToCSV() {
    console.log('Export to CSV - to be implemented');
}

function syncCharts(selectedFilter) {
    console.log('Syncing charts with filter:', selectedFilter);
}

function updateChartsAjax(filters) {
    console.log('Updating charts with filters:', filters);
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

function saveFiltersToLocalStorage() {
    const form = document.getElementById('filters-form');
    if (form) {
        const formData = new FormData(form);
        const filters = {};
        
        for (let [key, value] of formData.entries()) {
            filters[key] = value;
        }
        
        localStorage.setItem('dashboardFilters', JSON.stringify(filters));
    }
}

function loadFiltersFromLocalStorage() {
    const savedFilters = localStorage.getItem('dashboardFilters');
    
    if (savedFilters) {
        const filters = JSON.parse(savedFilters);
        const form = document.getElementById('filters-form');
        
        if (form) {
            Object.keys(filters).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = filters[key];
                }
            });
        }
    }
}

function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('uk-UA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

window.dashboardUtils = {
    resetFilters,
    exportChartAsPNG,
    exportChartAsSVG,
    printDashboard,
    exportDataToCSV,
    toggleDarkMode,
    formatNumber,
    formatDate
};
