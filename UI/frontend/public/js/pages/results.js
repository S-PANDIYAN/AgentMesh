// ============================================
// Results Page Renderer
// ============================================

function render_results() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Analysis Results</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Findings grouped by agent</p>
        </div>
        <div class="flex gap-2">
            <button class="px-4 py-2 bg-white border border-stone-200 font-bold text-xs uppercase hover:bg-stone-50">🔴 Critical</button>
            <button class="px-4 py-2 bg-white border border-stone-200 font-bold text-xs uppercase hover:bg-stone-50">🟠 High</button>
            <button class="px-4 py-2 bg-white border border-stone-200 font-bold text-xs uppercase hover:bg-stone-50">🟡 Medium</button>
        </div>
    </div>

    <div class="space-y-6">
        <!-- Security Findings -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold text-lg uppercase mb-4 flex items-center gap-2">
                <span class="material-symbols-outlined">security</span>
                Security Issues (3)
            </h3>
            <div class="space-y-3">
                <div class="border-l-4 border-red-500 pl-4 py-2">
                    <div class="font-bold text-red-600">SQL Injection Vulnerability</div>
                    <div class="font-mono text-xs text-stone-500">Line 145: database.query(\`SELECT * FROM users WHERE id = \${userId}\`)</div>
                </div>
                <div class="border-l-4 border-orange-500 pl-4 py-2">
                    <div class="font-bold text-orange-600">Hardcoded API Keys</div>
                    <div class="font-mono text-xs text-stone-500">Line 23: const API_KEY = "sk-abc123xyz"</div>
                </div>
                <div class="border-l-4 border-yellow-500 pl-4 py-2">
                    <div class="font-bold text-yellow-600">Missing Input Validation</div>
                    <div class="font-mono text-xs text-stone-500">Line 89: function processUserInput(input) { ... }</div>
                </div>
            </div>
        </div>

        <!-- Performance Findings -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold text-lg uppercase mb-4 flex items-center gap-2">
                <span class="material-symbols-outlined">speed</span>
                Performance Issues (2)
            </h3>
            <div class="space-y-3">
                <div class="border-l-4 border-orange-500 pl-4 py-2">
                    <div class="font-bold text-orange-600">N+1 Query Problem</div>
                    <div class="font-mono text-xs text-stone-500">Loop queries in getAllUsers() - causing 1000+ DB calls</div>
                </div>
                <div class="border-l-4 border-yellow-500 pl-4 py-2">
                    <div class="font-bold text-yellow-600">Memory Leak Detected</div>
                    <div class="font-mono text-xs text-stone-500">Event listeners not properly cleaned up in component destruction</div>
                </div>
            </div>
        </div>

        <!-- Quality Findings -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold text-lg uppercase mb-4 flex items-center gap-2">
                <span class="material-symbols-outlined">grade</span>
                Code Quality Issues (4)
            </h3>
            <div class="space-y-3">
                <div class="border-l-4 border-yellow-500 pl-4 py-2">
                    <div class="font-bold">High Cyclomatic Complexity</div>
                    <div class="font-mono text-xs text-stone-500">processData() function has complexity score of 18</div>
                </div>
                <div class="border-l-4 border-yellow-500 pl-4 py-2">
                    <div class="font-bold">Unused Variables</div>
                    <div class="font-mono text-xs text-stone-500">tempBuffer, oldConfig, legacyData declared but never used</div>
                </div>
                <div class="border-l-4 border-green-500 pl-4 py-2">
                    <div class="font-bold">Code Duplication</div>
                    <div class="font-mono text-xs text-stone-500">validateEmail() repeated in 3 modules</div>
                </div>
                <div class="border-l-4 border-green-500 pl-4 py-2">
                    <div class="font-bold">Missing Error Handling</div>
                    <div class="font-mono text-xs text-stone-500">fetch() calls without try-catch in DataLoader</div>
                </div>
            </div>
        </div>
    </div>
</div>
    `;
}
