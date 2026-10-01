// Common JavaScript utilities for SEO Monitor

document.addEventListener('DOMContentLoaded', function() {
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
});

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
    }
};

// Chart.js default configuration
Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.color = '#6c757d';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 15;