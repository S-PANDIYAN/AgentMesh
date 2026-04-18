// ============================================
// Quality Page Renderer
// ============================================

function render_quality() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Code Quality</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Quality Score: 6.8/10</p>
        </div>
    </div>

    <div class="grid grid-cols-3 gap-6 mb-10">
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="text-center">
                <div class="text-4xl font-black text-primary-container mb-2">6.8</div>
                <div class="font-mono text-xs text-stone-500 uppercase">Quality Score</div>
                <div class="mt-4 w-full bg-stone-100 h-3">
                    <div class="bg-primary-container h-full" style="width: 68%"></div>
                </div>
            </div>
        </div>

        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="text-center">
                <div class="text-4xl font-black text-yellow-600 mb-2">7.2</div>
                <div class="font-mono text-xs text-stone-500 uppercase">Maintainability</div>
                <div class="mt-4 w-full bg-stone-100 h-3">
                    <div class="bg-yellow-500 h-full" style="width: 72%"></div>
                </div>
            </div>
        </div>

        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="text-center">
                <div class="text-4xl font-black text-orange-600 mb-2">5.9</div>
                <div class="font-mono text-xs text-stone-500 uppercase">Reliability</div>
                <div class="mt-4 w-full bg-stone-100 h-3">
                    <div class="bg-orange-500 h-full" style="width: 59%"></div>
                </div>
            </div>
        </div>
    </div>

    <div class="space-y-6">
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">Complexity Analysis</h3>
            <div class="space-y-3">
                <div class="flex justify-between items-center pb-3 border-b border-stone-100">
                    <span>processData()</span>
                    <div class="flex items-center gap-3">
                        <span class="font-mono text-xs bg-red-50 text-red-700 px-2 py-1">Complexity: 18</span>
                        <span class="font-bold text-red-600">TOO HIGH</span>
                    </div>
                </div>
                <div class="flex justify-between items-center pb-3 border-b border-stone-100">
                    <span>validateInput()</span>
                    <div class="flex items-center gap-3">
                        <span class="font-mono text-xs bg-yellow-50 text-yellow-700 px-2 py-1">Complexity: 12</span>
                        <span class="font-bold text-yellow-600">HIGH</span>
                    </div>
                </div>
                <div class="flex justify-between items-center">
                    <span>parseConfig()</span>
                    <div class="flex items-center gap-3">
                        <span class="font-mono text-xs bg-green-50 text-green-700 px-2 py-1">Complexity: 5</span>
                        <span class="font-bold text-green-600">GOOD</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">Issues Detected</h3>
            <div class="space-y-3">
                <div class="flex items-start gap-3 pb-3 border-b border-stone-100">
                    <span class="text-red-600 font-bold">❌</span>
                    <div>
                        <div class="font-bold">Unused Variables</div>
                        <div class="font-mono text-xs text-stone-600">tempBuffer, oldConfig, legacyData in main.py</div>
                    </div>
                </div>
                <div class="flex items-start gap-3 pb-3 border-b border-stone-100">
                    <span class="text-yellow-600 font-bold">⚠️</span>
                    <div>
                        <div class="font-bold">Code Duplication</div>
                        <div class="font-mono text-xs text-stone-600">validateEmail() repeated 3 times - consider extracting</div>
                    </div>
                </div>
                <div class="flex items-start gap-3">
                    <span class="text-orange-600 font-bold">⚠️</span>
                    <div>
                        <div class="font-bold">Missing Error Handling</div>
                        <div class="font-mono text-xs text-stone-600">fetch() calls without try-catch in DataLoader.js</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">Recommendations</h3>
            <div class="space-y-2">
                <button class="w-full text-left px-4 py-2 bg-stone-50 hover:bg-stone-100 border border-stone-200 font-bold text-sm">✓ Refactor processData() to reduce complexity</button>
                <button class="w-full text-left px-4 py-2 bg-stone-50 hover:bg-stone-100 border border-stone-200 font-bold text-sm">✓ Remove unused variables (save 152 bytes)</button>
                <button class="w-full text-left px-4 py-2 bg-stone-50 hover:bg-stone-100 border border-stone-200 font-bold text-sm">✓ Extract validateEmail() to shared utility</button>
                <button class="w-full text-left px-4 py-2 bg-stone-50 hover:bg-stone-100 border border-stone-200 font-bold text-sm">✓ Add error handling to async operations</button>
            </div>
        </div>
    </div>
</div>
    `;
}
