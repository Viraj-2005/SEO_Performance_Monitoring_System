// Common JavaScript utilities for SEO Monitor

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initTheme();

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading state to forms
    document.querySelectorAll('form[data-loading]').forEach(function(form) {
        form.addEventListener('submit', function() {
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popover initialization
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Theme Management
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const html = document.documentElement;

    // Get saved theme or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');

    applyTheme(initialTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
        console.log('Theme toggle initialized');
    } else {
        console.warn('Theme toggle button not found');
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });

    function applyTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        }
        // Update Chart.js colors if charts exist
        updateChartsTheme(theme);
    }
}

function updateChartsTheme(theme) {
    const isDark = theme === 'dark';
    const textColor = isDark ? '#cbd5e1' : '#6c757d';
    const gridColor = isDark ? '#334155' : '#e2e8f0';

    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;
    Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';

    // Update existing charts
    if (typeof Chart !== 'undefined' && Chart.instances) {
        Chart.instances.forEach(function(chart) {
            if (chart.options) {
                chart.options.scales = chart.options.scales || {};
                Object.keys(chart.options.scales).forEach(function(scaleKey) {
                    const scale = chart.options.scales[scaleKey];
                    if (scale) {
                        scale.grid = scale.grid || {};
                        scale.grid.color = gridColor;
                        scale.ticks = scale.ticks || {};
                        scale.ticks.color = textColor;
                    }
                });
                if (chart.options.plugins && chart.options.plugins.legend) {
                    chart.options.plugins.legend.labels.color = textColor;
                }
                chart.update('none');
            }
        });
    }
}

// Sentiment Analysis Modal
function showDetails(text, sentiment, score, scores) {
    const modalEl = document.getElementById('detailModal');
    const modalBody = document.getElementById('modalBody');
    
    if (!modalEl || !modalBody) {
        console.error('Modal elements not found');
        return;
    }

    const badgeClass = sentiment === 'positive' ? 'success' : sentiment === 'negative' ? 'danger' : 'warning';
    const icon = sentiment === 'positive' ? 'emoji-smile' : sentiment === 'negative' ? 'emoji-frown' : 'emoji-neutral';
    
    modalBody.innerHTML = `
        <div class="text-center mb-4">
            <i class="bi bi-${icon} display-1 text-${badgeClass}"></i>
            <h4 class="mt-2 text-capitalize">${sentiment}</h4>
            <span class="badge bg-${badgeClass} fs-6">${sentiment}</span>
        </div>
        <p class="mb-3"><strong>Analyzed Text:</strong></p>
        <div class="p-3 bg-secondary bg-opacity-25 rounded mb-4" style="white-space: pre-wrap; max-height: 200px; overflow-y: auto;">${text}</div>
        <div class="row g-3 mb-3">
            <div class="col-4">
                <div class="stats-card p-3 text-center">
                    <div class="text-muted small">Positive</div>
                    <div class="fw-bold fs-5 text-success">${(scores.pos * 100).toFixed(1)}%</div>
                </div>
            </div>
            <div class="col-4">
                <div class="stats-card p-3 text-center">
                    <div class="text-muted small">Neutral</div>
                    <div class="fw-bold fs-5 text-secondary">${(scores.neu * 100).toFixed(1)}%</div>
                </div>
            </div>
            <div class="col-4">
                <div class="stats-card p-3 text-center">
                    <div class="text-muted small">Negative</div>
                    <div class="fw-bold fs-5 text-danger">${(scores.neg * 100).toFixed(1)}%</div>
                </div>
            </div>
        </div>
        <div class="progress" style="height: 8px;">
            <div class="bg-success" style="width: ${(scores.pos * 100)}%"></div>
            <div class="bg-secondary" style="width: ${(scores.neu * 100)}%"></div>
            <div class="bg-danger" style="width: ${(scores.neg * 100)}%"></div>
        </div>
        <div class="mt-3 small text-muted">
            Compound Score: ${score}
        </div>
    `;
    
    const bsModal = new bootstrap.Modal(modalEl);
    bsModal.show();
}

// Utility functions
const SEOUtils = {
    formatScore: function(score) {
        if (score >= 80) return { class: 'success', label: 'Good' };
        if (score >= 60) return { class: 'warning', label: 'Needs Improvement' };
        return { class: 'danger', label: 'Poor' };
    },

    truncateUrl: function(url, maxLength = 50) {
        if (url.length <= maxLength) return url;
        return '...' + url.slice(-(maxLength - 3));
    },

    getSeverityBadge: function(severity) {
        const badges = {
            critical: 'bg-danger',
            warning: 'bg-warning text-dark',
            passed: 'bg-success'
        };
        return badges[severity] || 'bg-secondary';
    },

    formatNumber: function(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    },

    debounce: function(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    },

    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(function() {
            SEOUtils.showToast('Copied to clipboard!', 'success');
        }).catch(function() {
            SEOUtils.showToast('Failed to copy', 'danger');
        });
    },

    showToast: function(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer') || SEOUtils.createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    },

    createToastContainer: function() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }
};

// Chart.js default configuration
Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.color = '#6c757d';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 15;
Chart.defaults.plugins.legend.labels.font.size = 12;
Chart.defaults.scales = {
    x: {
        grid: { display: false },
        ticks: { padding: 8 }
    },
    y: {
        grid: { color: '#e2e8f0' },
        ticks: { padding: 8 }
    }
};

// Animation observer for scroll animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.feature-card, .stats-card, .card').forEach(function(el) {
        observer.observe(el);
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search focus (if search exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        const searchInput = document.querySelector('input[type="search"], input[name="url"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }

    // Escape to close modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(function(modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
    }
});

// Export for global use
window.SEOUtils = SEOUtils;
window.showDetails = showDetails;