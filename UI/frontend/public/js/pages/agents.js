// ============================================
// Agents Page Renderer
// ============================================

function render_agents() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Agents</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Manage 5 autonomous analysis agents</p>
        </div>
    </div>

    <div class="grid grid-cols-2 gap-6 mb-10">
        <!-- Security Agent -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-2xl text-red-500">security</span>
                        <h3 class="font-headline font-bold text-lg uppercase">Security Agent</h3>
                    </div>
                    <p class="font-mono text-xs text-stone-500">Vulnerability & threat detection</p>
                </div>
            </div>
            <div class="space-y-3">
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Accuracy</span>
                    <span class="font-bold">94.2%</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Tasks Completed</span>
                    <span class="font-bold">234</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Response Time</span>
                    <span class="font-bold">1.2s</span>
                </div>
            </div>
            <div class="mt-4 flex gap-2">
                <button class="flex-1 px-3 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Enable</button>
                <button class="flex-1 px-3 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">Configure</button>
            </div>
        </div>

        <!-- Performance Agent -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-2xl text-blue-500">speed</span>
                        <h3 class="font-headline font-bold text-lg uppercase">Performance Agent</h3>
                    </div>
                    <p class="font-mono text-xs text-stone-500">Optimization &amp; bottleneck analysis</p>
                </div>
            </div>
            <div class="space-y-3">
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Accuracy</span>
                    <span class="font-bold">91.5%</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Tasks Completed</span>
                    <span class="font-bold">189</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Response Time</span>
                    <span class="font-bold">980ms</span>
                </div>
            </div>
            <div class="mt-4 flex gap-2">
                <button class="flex-1 px-3 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Enable</button>
                <button class="flex-1 px-3 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">Configure</button>
            </div>
        </div>

        <!-- Code Quality Agent -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-2xl text-green-500">grade</span>
                        <h3 class="font-headline font-bold text-lg uppercase">Code Quality Agent</h3>
                    </div>
                    <p class="font-mono text-xs text-stone-500">Quality metrics &amp; complexity analysis</p>
                </div>
            </div>
            <div class="space-y-3">
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Accuracy</span>
                    <span class="font-bold">89.7%</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Tasks Completed</span>
                    <span class="font-bold">156</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Response Time</span>
                    <span class="font-bold">1.1s</span>
                </div>
            </div>
            <div class="mt-4 flex gap-2">
                <button class="flex-1 px-3 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Enable</button>
                <button class="flex-1 px-3 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">Configure</button>
            </div>
        </div>

        <!-- Documentation Agent -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-2xl text-purple-500">description</span>
                        <h3 class="font-headline font-bold text-lg uppercase">Documentation Agent</h3>
                    </div>
                    <p class="font-mono text-xs text-stone-500">Auto-generate docs &amp; comments</p>
                </div>
            </div>
            <div class="space-y-3">
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Accuracy</span>
                    <span class="font-bold">93.1%</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Tasks Completed</span>
                    <span class="font-bold">142</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Response Time</span>
                    <span class="font-bold">1.5s</span>
                </div>
            </div>
            <div class="mt-4 flex gap-2">
                <button class="flex-1 px-3 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Enable</button>
                <button class="flex-1 px-3 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">Configure</button>
            </div>
        </div>

        <!-- LLM Reasoning Agent -->
        <div class="col-span-2 bg-white border border-stone-200 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-2xl text-orange-500">psychology</span>
                        <h3 class="font-headline font-bold text-lg uppercase">LLM Reasoning Agent</h3>
                    </div>
                    <p class="font-mono text-xs text-stone-500">Advanced pattern recognition &amp; reasoning</p>
                </div>
            </div>
            <div class="grid grid-cols-4 gap-4">
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Accuracy</span>
                    <span class="font-bold">96.8%</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Tasks Completed</span>
                    <span class="font-bold">326</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Response Time</span>
                    <span class="font-bold">2.3s</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="font-mono text-xs uppercase text-stone-500">Status</span>
                    <span class="font-bold text-emerald-600">Active</span>
                </div>
            </div>
            <div class="mt-4 flex gap-2">
                <button class="flex-1 px-3 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Enable</button>
                <button class="flex-1 px-3 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">Configure</button>
            </div>
        </div>
    </div>
</div>
    `;
}
