// ============================================
// AgentMesh SPA - Router
// ============================================

class Router {
    constructor(pages) {
        this.pages = pages;
        this.currentPage = 'dashboard';
        this.history = [];
    }

    navigate(pageId) {
        if (!this.pages.includes(pageId)) {
            console.warn(`⚠️ Router: Page "${pageId}" not found`);
            return false;
        }

        // Update browser history
        if (window.location.hash !== `#${pageId}`) {
            window.location.hash = pageId;
        }

        // Add to history
        if (this.currentPage !== pageId) {
            this.history.push(pageId);
        }

        this.currentPage = pageId;
        return true;
    }

    back() {
        if (this.history.length > 1) {
            this.history.pop();
            const previousPage = this.history[this.history.length - 1];
            this.navigate(previousPage);
        }
    }

    forward() {
        // Implement if needed
    }

    getCurrentPage() {
        return this.currentPage;
    }

    getHistory() {
        return this.history;
    }
}

// Export router if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Router;
}
