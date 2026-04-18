// ============================================
// Settings Page Renderer
// ============================================

function render_settings() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-4xl mx-auto">
    <div class="mb-10">
        <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Settings</h1>
        <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Configuration & integrations</p>
    </div>

    <div class="bg-white border border-stone-200 code-shadow">
        <div class="border-b border-stone-200 px-6">
            <div class="flex gap-0">
                <button class="px-6 py-4 font-bold text-sm uppercase border-b-2 border-primary-container text-on-primary-fixed">General</button>
                <button class="px-6 py-4 font-bold text-sm uppercase text-stone-500 hover:text-on-surface">API Settings</button>
                <button class="px-6 py-4 font-bold text-sm uppercase text-stone-500 hover:text-on-surface">Integrations</button>
                <button class="px-6 py-4 font-bold text-sm uppercase text-stone-500 hover:text-on-surface">Advanced</button>
            </div>
        </div>

        <div class="p-6 space-y-8">
            <!-- General Settings -->
            <div>
                <h3 class="font-headline font-bold uppercase mb-4">General Settings</h3>
                <div class="space-y-4">
                    <div class="flex justify-between items-center">
                        <div>
                            <div class="font-bold">Analysis Timeout</div>
                            <div class="font-mono text-xs text-stone-500">Max seconds per file analysis</div>
                        </div>
                        <input type="number" value="30" class="w-20 px-3 py-2 border border-stone-200 font-mono text-sm">
                    </div>
                    <div class="flex justify-between items-center border-t border-stone-100 pt-4">
                        <div>
                            <div class="font-bold">Max File Size</div>
                            <div class="font-mono text-xs text-stone-500">Maximum file size to analyze (MB)</div>
                        </div>
                        <input type="number" value="100" class="w-20 px-3 py-2 border border-stone-200 font-mono text-sm">
                    </div>
                    <div class="flex justify-between items-center border-t border-stone-100 pt-4">
                        <div>
                            <div class="font-bold">Parallel Tasks</div>
                            <div class="font-mono text-xs text-stone-500">Number of tasks to run in parallel</div>
                        </div>
                        <input type="number" value="5" class="w-20 px-3 py-2 border border-stone-200 font-mono text-sm">
                    </div>
                    <div class="flex justify-between items-center border-t border-stone-100 pt-4">
                        <div>
                            <div class="font-bold">Auto Save Results</div>
                            <div class="font-mono text-xs text-stone-500">Automatically save analysis results</div>
                        </div>
                        <label class="flex items-center cursor-pointer">
                            <input type="checkbox" checked class="w-5 h-5">
                        </label>
                    </div>
                </div>
            </div>

            <div class="border-t border-stone-200 pt-8">
                <h3 class="font-headline font-bold uppercase mb-4">Agent Configuration</h3>
                <div class="space-y-4">
                    <div class="flex justify-between items-center">
                        <div>
                            <div class="font-bold">Security Agent</div>
                            <div class="font-mono text-xs text-stone-500">CWE/CVE detection enabled</div>
                        </div>
                        <label class="flex items-center cursor-pointer">
                            <input type="checkbox" checked class="w-5 h-5">
                        </label>
                    </div>
                    <div class="flex justify-between items-center border-t border-stone-100 pt-4">
                        <div>
                            <div class="font-bold">Performance Agent</div>
                            <div class="font-mono text-xs text-stone-500">Bottleneck detection enabled</div>
                        </div>
                        <label class="flex items-center cursor-pointer">
                            <input type="checkbox" checked class="w-5 h-5">
                        </label>
                    </div>
                    <div class="flex justify-between items-center border-t border-stone-100 pt-4">
                        <div>
                            <div class="font-bold">Code Quality Agent</div>
                            <div class="font-mono text-xs text-stone-500">Complexity analysis enabled</div>
                        </div>
                        <label class="flex items-center cursor-pointer">
                            <input type="checkbox" checked class="w-5 h-5">
                        </label>
                    </div>
                    <div class="flex justify-between items-center border-t border-stone-100 pt-4">
                        <div>
                            <div class="font-bold">LLM Reasoning Agent</div>
                            <div class="font-mono text-xs text-stone-500">Advanced pattern recognition</div>
                        </div>
                        <label class="flex items-center cursor-pointer">
                            <input type="checkbox" checked class="w-5 h-5">
                        </label>
                    </div>
                </div>
            </div>

            <div class="border-t border-stone-200 pt-8">
                <h3 class="font-headline font-bold uppercase mb-4">API Configuration</h3>
                <div class="space-y-4">
                    <div>
                        <label class="font-bold block mb-2">Groq API Key</label>
                        <input type="password" placeholder="••••••••••••" class="w-full px-4 py-2 border border-stone-200 font-mono text-sm">
                    </div>
                    <div>
                        <label class="font-bold block mb-2">API Endpoint</label>
                        <input type="text" value="https://api.groq.com/v1" class="w-full px-4 py-2 border border-stone-200 font-mono text-sm">
                    </div>
                </div>
            </div>

            <div class="border-t border-stone-200 pt-8 flex gap-4">
                <button class="px-6 py-3 bg-primary-container text-on-primary-fixed font-bold text-sm uppercase hover:bg-primary transition">Save Changes</button>
                <button class="px-6 py-3 border border-stone-200 text-stone-600 font-bold text-sm uppercase hover:bg-stone-50 transition">Reset to Defaults</button>
                <button class="px-6 py-3 border border-stone-200 text-stone-600 font-bold text-sm uppercase hover:bg-stone-50 transition">Export Settings</button>
            </div>
        </div>
    </div>
</div>
    `;
}
