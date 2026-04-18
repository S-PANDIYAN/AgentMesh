// ============================================
// AgentMesh SPA - Main Application
// ============================================

class AgentMeshApp {
    constructor() {
        this.currentPage = 'dashboard';
        this.pages = ['dashboard', 'agents', 'results', 'tasks', 'security', 'performance', 'quality', 'settings', 'diff-viewer', 'issue-details', 'file-browser', 'analysis-history'];
        this.navItems = [
            { id: 'dashboard', icon: 'dashboard', label: 'Dashboard', href: '#dashboard' },
            { id: 'agents', icon: 'smart_toy', label: 'Agents', href: '#agents' },
            { id: 'results', icon: 'assignment_turned_in', label: 'Results', href: '#results' },
            { id: 'tasks', icon: 'checklist', label: 'Tasks', href: '#tasks' },
            { id: 'security', icon: 'security', label: 'Security', href: '#security' },
            { id: 'performance', icon: 'speed', label: 'Performance', href: '#performance' },
            { id: 'quality', icon: 'grade', label: 'Quality', href: '#quality' },
            { id: 'settings', icon: 'settings', label: 'Settings', href: '#settings' },
            { id: 'diff-viewer', icon: 'difference', label: 'Diff Viewer', href: '#diff-viewer' },
            { id: 'issue-details', icon: 'bug_report', label: 'Issue Details', href: '#issue-details' },
            { id: 'file-browser', icon: 'folder', label: 'File Browser', href: '#file-browser' },
            { id: 'analysis-history', icon: 'history', label: 'Analysis History', href: '#analysis-history' }
        ];
        
        this.init();
    }

    init() {
        console.log('🚀 AgentMesh SPA Initializing...');
        this.setupNavigation();
        this.setupRouting();
        this.loadPage('dashboard');
    }

    setupNavigation() {
        const navLinks = document.getElementById('nav-links');
        navLinks.innerHTML = '';

        this.navItems.forEach(item => {
            const link = document.createElement('a');
            link.href = item.href;
            link.className = `flex items-center gap-3 px-4 py-3 font-headline text-xs font-bold uppercase tracking-widest text-stone-600 hover:bg-stone-200 transition-all`;
            link.setAttribute('data-page', item.id);
            
            if (item.id === 'dashboard') {
                link.className += ' bg-primary-container text-on-primary-fixed hover:bg-primary';
            }

            link.innerHTML = `
                <span class="material-symbols-outlined text-lg">${item.icon}</span>
                ${item.label}
            `;

            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.loadPage(item.id);
            });

            navLinks.appendChild(link);
        });
    }

    setupRouting() {
        window.addEventListener('hashchange', () => {
            const page = window.location.hash.substring(1) || 'dashboard';
            if (this.pages.includes(page)) {
                this.loadPage(page);
            }
        });
    }

    loadPage(pageId) {
        if (!this.pages.includes(pageId)) {
            console.warn(`⚠️ Page "${pageId}" not found`);
            return;
        }

        console.log(`📄 Loading page: ${pageId}`);
        this.currentPage = pageId;

        // Update browser history
        window.location.hash = pageId;

        // Update nav active state
        this.updateNavActiveState(pageId);

        // Load page content
        this.loadPageContent(pageId);
    }

    updateNavActiveState(pageId) {
        const navLinks = document.querySelectorAll('#nav-links a');
        navLinks.forEach(link => {
            link.classList.remove('bg-primary-container', 'text-on-primary-fixed', 'hover:bg-primary');
            link.classList.add('text-stone-600', 'hover:bg-stone-200');
            
            if (link.getAttribute('data-page') === pageId) {
                link.classList.remove('text-stone-600', 'hover:bg-stone-200');
                link.classList.add('bg-primary-container', 'text-on-primary-fixed', 'hover:bg-primary');
            }
        });
    }

    loadPageContent(pageId) {
        const appContainer = document.getElementById('app');
        appContainer.innerHTML = '<p class="text-stone-400">Loading...</p>';

        // Call page-specific renderer
        const pageRenderer = window[`render_${pageId}`];
        if (typeof pageRenderer === 'function') {
            pageRenderer();
        } else {
            console.warn(`⚠️ No renderer found for page: ${pageId}`);
            appContainer.innerHTML = `<p class="text-stone-400">Page ${pageId} not found</p>`;
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AgentMeshApp();
});
