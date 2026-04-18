// ============================================
// Tasks Page Renderer
// ============================================

function render_tasks() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Task Queue</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Pending & completed analysis tasks</p>
        </div>
    </div>

    <div class="bg-white border border-stone-200 code-shadow">
        <div class="border-b border-stone-200 px-6 py-4 bg-stone-50 font-bold text-xs uppercase tracking-widest grid grid-cols-6 gap-4">
            <span>Task ID</span>
            <span>Agent</span>
            <span>File</span>
            <span>Status</span>
            <span>Progress</span>
            <span>Time</span>
        </div>
        
        <div class="divide-y divide-stone-200">
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1047</span>
                <span>Security</span>
                <span>auth.py</span>
                <span><span class="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs">COMPLETE</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-emerald-500 h-full" style="width: 100%"></div></div>
                <span class="font-mono text-stone-500">2.3s</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1046</span>
                <span>Performance</span>
                <span>database.js</span>
                <span><span class="px-2 py-1 bg-blue-50 text-blue-700 font-bold text-xs">PROCESSING</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-primary-container h-full" style="width: 65%"></div></div>
                <span class="font-mono text-stone-500">1.8s</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1045</span>
                <span>Code Quality</span>
                <span>utils.ts</span>
                <span><span class="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs">COMPLETE</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-emerald-500 h-full" style="width: 100%"></div></div>
                <span class="font-mono text-stone-500">1.5s</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1044</span>
                <span>Documentation</span>
                <span>api.go</span>
                <span><span class="px-2 py-1 bg-amber-50 text-amber-700 font-bold text-xs">QUEUED</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-amber-500 h-full" style="width: 0%"></div></div>
                <span class="font-mono text-stone-500">-</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1043</span>
                <span>LLM Reasoning</span>
                <span>main.rs</span>
                <span><span class="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs">COMPLETE</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-emerald-500 h-full" style="width: 100%"></div></div>
                <span class="font-mono text-stone-500">3.2s</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1042</span>
                <span>Security</span>
                <span>routes.js</span>
                <span><span class="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs">COMPLETE</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-emerald-500 h-full" style="width: 100%"></div></div>
                <span class="font-mono text-stone-500">1.9s</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1041</span>
                <span>Performance</span>
                <span>worker.java</span>
                <span><span class="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs">COMPLETE</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-emerald-500 h-full" style="width: 100%"></div></div>
                <span class="font-mono text-stone-500">2.7s</span>
            </div>
            <div class="px-6 py-4 grid grid-cols-6 gap-4 items-center text-sm">
                <span class="font-mono">#1040</span>
                <span>Code Quality</span>
                <span>config.py</span>
                <span><span class="px-2 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs">COMPLETE</span></span>
                <div class="w-full bg-stone-100 h-2"><div class="bg-emerald-500 h-full" style="width: 100%"></div></div>
                <span class="font-mono text-stone-500">1.4s</span>
            </div>
        </div>
    </div>
</div>
    `;
}
