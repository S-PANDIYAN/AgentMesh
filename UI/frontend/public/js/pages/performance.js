// ============================================
// Performance Page Renderer
// ============================================

function render_performance() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Performance Analysis</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">7 Issues Found • 4 Optimize Now</p>
        </div>
    </div>

    <div class="space-y-6">
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">🔴 Critical Issues</h3>
            <div class="space-y-4">
                <div class="border-l-4 border-red-500 pl-4">
                    <div class="font-bold text-red-600">N+1 Query Problem in getAllUsers()</div>
                    <div class="font-mono text-xs text-stone-600 mt-1">Performing 1000+ database queries in loop</div>
                    <div class="mt-2">
                        <span class="inline-block px-3 py-1 bg-red-50 text-red-700 font-bold text-xs mr-2">Impact: Huge</span>
                        <span class="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 font-bold text-xs">Difficulty: Medium</span>
                    </div>
                    <button class="mt-3 px-4 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Fix Suggestion</button>
                </div>

                <div class="border-l-4 border-orange-500 pl-4 pt-4">
                    <div class="font-bold text-orange-600">Memory Leak in Event Listeners</div>
                    <div class="font-mono text-xs text-stone-600 mt-1">Component.js not cleaning up event listeners on destroy</div>
                    <div class="mt-2">
                        <span class="inline-block px-3 py-1 bg-orange-50 text-orange-700 font-bold text-xs mr-2">Impact: High</span>
                        <span class="inline-block px-3 py-1 bg-green-50 text-green-700 font-bold text-xs">Difficulty: Easy</span>
                    </div>
                    <button class="mt-3 px-4 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">Fix Suggestion</button>
                </div>
            </div>
        </div>

        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">🟡 Medium Issues</h3>
            <div class="space-y-4">
                <div class="border-l-4 border-yellow-500 pl-4">
                    <div class="font-bold text-yellow-600">Inefficient Array Operations</div>
                    <div class="font-mono text-xs text-stone-600 mt-1">Using find() in nested loops - O(n²) complexity</div>
                    <div class="mt-2">
                        <span class="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 font-bold text-xs mr-2">Impact: Medium</span>
                        <span class="inline-block px-3 py-1 bg-green-50 text-green-700 font-bold text-xs">Difficulty: Easy</span>
                    </div>
                </div>

                <div class="border-l-4 border-yellow-500 pl-4 pt-4">
                    <div class="font-bold text-yellow-600">Unoptimized Images</div>
                    <div class="font-mono text-xs text-stone-600 mt-1">18 images not compressed or resized for web</div>
                    <div class="mt-2">
                        <span class="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 font-bold text-xs mr-2">Impact: Medium</span>
                        <span class="inline-block px-3 py-1 bg-green-50 text-green-700 font-bold text-xs">Difficulty: Easy</span>
                    </div>
                </div>

                <div class="border-l-4 border-yellow-500 pl-4 pt-4">
                    <div class="font-bold text-yellow-600">Missing Caching Strategy</div>
                    <div class="font-mono text-xs text-stone-600 mt-1">API calls not cached, causing redundant requests</div>
                    <div class="mt-2">
                        <span class="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 font-bold text-xs mr-2">Impact: Medium</span>
                        <span class="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 font-bold text-xs">Difficulty: Medium</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    `;
}
