// ============================================
// Dashboard Page Renderer
// ============================================

function render_dashboard() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Dashboard</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Upload code for analysis</p>
        </div>
        <div class="grid grid-cols-3 gap-4">
            <div class="bg-stone-50 border border-stone-200 p-4">
                <div class="font-mono text-xs text-stone-500 uppercase mb-1">Files Analyzed</div>
                <div class="text-3xl font-black text-stone-900">847</div>
            </div>
            <div class="bg-stone-50 border border-stone-200 p-4">
                <div class="font-mono text-xs text-stone-500 uppercase mb-1">Avg Accuracy</div>
                <div class="text-3xl font-black text-primary-container">92.3%</div>
            </div>
            <div class="bg-stone-50 border border-stone-200 p-4">
                <div class="font-mono text-xs text-stone-500 uppercase mb-1">Active Agents</div>
                <div class="text-3xl font-black text-emerald-600">5/5</div>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-3 gap-8">
        <!-- Upload Section -->
        <div class="col-span-2">
            <div class="bg-white border-2 border-dashed border-stone-200 p-12 text-center code-shadow hover:border-primary transition-colors">
                <span class="material-symbols-outlined text-6xl text-stone-200 mx-auto block mb-4">cloud_upload</span>
                <h3 class="font-headline text-xl font-bold uppercase mb-2">Drop Your Code Here</h3>
                <p class="font-mono text-sm text-stone-500 mb-6">Drag and drop a file or click to browse</p>
                <button class="px-6 py-3 bg-primary-container text-on-primary-fixed font-headline text-sm font-bold uppercase hover:bg-primary transition-colors">
                    Select File
                </button>
                <p class="font-mono text-xs text-stone-400 mt-4">Supports: .py, .js, .ts, .java, .go, .rs</p>
            </div>
        </div>

        <!-- Recent Analysis -->
        <div class="col-span-1 bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase text-sm mb-4">Recent Analysis</h3>
            <div class="space-y-3">
                <div class="border-b border-stone-100 pb-3">
                    <div class="font-mono text-xs text-stone-500">main.py</div>
                    <div class="flex justify-between">
                        <span class="text-sm font-bold">✓ Complete</span>
                        <span class="font-mono text-xs text-stone-400">2m ago</span>
                    </div>
                </div>
                <div class="border-b border-stone-100 pb-3">
                    <div class="font-mono text-xs text-stone-500">api.ts</div>
                    <div class="flex justify-between">
                        <span class="text-sm font-bold">✓ Complete</span>
                        <span class="font-mono text-xs text-stone-400">15m ago</span>
                    </div>
                </div>
                <div>
                    <div class="font-mono text-xs text-stone-500">utils.js</div>
                    <div class="flex justify-between">
                        <span class="text-sm font-bold">✓ Complete</span>
                        <span class="font-mono text-xs text-stone-400">1h ago</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    `;
}
