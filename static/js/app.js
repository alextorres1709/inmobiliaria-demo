// ─── Theme toggle ───────────────────────────────────
function isDark() { return document.documentElement.getAttribute('data-theme') === 'dark'; }

function toggleTheme() {
    var theme = isDark() ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('immo-theme', theme);
    window.dispatchEvent(new CustomEvent('themechange'));
}

function getChartTheme() {
    var d = isDark();
    return {
        primary: d ? '#818cf8' : '#1a3a5c',
        primaryA: function (a) { return d ? 'rgba(129,140,248,' + a + ')' : 'rgba(26,58,92,' + a + ')'; },
        secondary: d ? '#22d3ee' : '#1b6b8a',
        secondaryA: function (a) { return d ? 'rgba(34,211,238,' + a + ')' : 'rgba(27,107,138,' + a + ')'; },
        indigoA: function (a) { return d ? 'rgba(167,139,250,' + a + ')' : 'rgba(36,89,128,' + a + ')'; },
        amberA: function (a) { return 'rgba(245,158,11,' + a + ')'; },
        text: d ? '#a0aec0' : '#94a3b8',
        grid: d ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
        tip: { bg: d ? '#1a1a28' : '#f8fafb', title: d ? '#e2e8f0' : '#0f172a', body: d ? '#a0aec0' : '#334155', border: d ? '#2a2a3e' : '#d0d8e0' },
        card: d ? '#0f0f18' : '#f8fafb',
        palette: d
            ? ['#818cf8', '#22d3ee', '#f59e0b', '#ef4444', '#a78bfa', '#ec4899', '#34d399', '#64748b']
            : ['#1a3a5c', '#245980', '#1b6b8a', '#2a7da8', '#3a8ab5', '#1b7a6e', '#c75a3a', '#5a7d95']
    };
}

// ─── Modal helpers ──────────────────────────────────
function openModal(id) {
    document.getElementById(id).classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
    document.body.style.overflow = '';
}

// Close modal on overlay click
let modalMouseDownTarget = null;
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('mousedown', (e) => {
        modalMouseDownTarget = e.target;
    });
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay && modalMouseDownTarget === overlay) {
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
        modalMouseDownTarget = null;
    });
});

// Close modal on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => {
            m.classList.remove('active');
        });
        document.body.style.overflow = '';
    }
});

// ─── Flash messages auto-dismiss ────────────────────
document.querySelectorAll('.flash-message').forEach(msg => {
    setTimeout(() => {
        msg.style.display = 'none';
    }, 4000);
});

// ─── Sidebar toggle for mobile ──────────────────────
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
}

// Close sidebar when clicking outside
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.getElementById('sidebarOverlay');

    if (sidebar && sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        hamburger && !hamburger.contains(e.target) &&
        e.target !== overlay) {
        sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
    }
});

// Close sidebar when clicking a nav link (mobile UX)
document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        if (sidebar && window.innerWidth <= 768) {
            sidebar.classList.remove('open');
            if (overlay) overlay.classList.remove('active');
        }
    });
});

// ─── Capability toggle ─────────────────────────────
document.querySelectorAll('.capability-toggle').forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('open');
    });
});
