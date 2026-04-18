// ============================================
// Code Diff Viewer - Before/After Comparison
// ============================================

function render_diff_viewer() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Code Diff Viewer</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Before & After Code Comparison</p>
        </div>
        <div class="flex gap-2">
            <button class="px-4 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">
                Download Diff
            </button>
            <button class="px-4 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">
                Share
            </button>
        </div>
    </div>

    <div class="grid grid-cols-2 gap-6 mb-10">
        <!-- File Selector -->
        <div class="col-span-2 bg-white border border-stone-200 p-4 code-shadow">
            <label class="font-bold text-sm mb-2 block">Select File to Compare</label>
            <select class="w-full px-4 py-2 border border-stone-200 font-mono text-sm">
                <option>auth.py - Fixed SQL Injection</option>
                <option>database.js - Optimized N+1 Query</option>
                <option>utils.ts - Refactored Complexity</option>
                <option>api.go - Added Error Handling</option>
                <option>main.rs - Memory Leak Fix</option>
            </select>
        </div>

        <!-- Before Code -->
        <div class="bg-white border border-stone-200 p-4 code-shadow">
            <div class="font-bold uppercase text-sm mb-3 flex items-center gap-2">
                <span class="w-3 h-3 bg-red-500"></span>
                Before (Lines: 145-165)
            </div>
            <div class="bg-stone-50 p-3 border border-stone-200 font-mono text-[11px] leading-relaxed overflow-x-auto">
                <div class="text-red-600">- database.query(\`</div>
                <div class="text-red-600">-   SELECT * FROM users</div>
                <div class="text-red-600">-   WHERE id = \${userId}</div>
                <div class="text-red-600">- \`)</div>
                <div></div>
                <div>async function getUser(id) {</div>
                <div class="text-red-600">-   let user = await db.query(</div>
                <div class="text-red-600">-     \`SELECT * WHERE id = \${id}\`</div>
                <div class="text-red-600">-   )</div>
                <div class="text-red-600">-   return user</div>
                <div>}</div>
            </div>
            <div class="mt-3 px-3 py-2 bg-red-50 border border-red-200 text-red-700 text-xs font-bold">
                ⚠️ Vulnerable to SQL Injection
            </div>
        </div>

        <!-- After Code -->
        <div class="bg-white border border-stone-200 p-4 code-shadow">
            <div class="font-bold uppercase text-sm mb-3 flex items-center gap-2">
                <span class="w-3 h-3 bg-green-500"></span>
                After (Lines: 145-165)
            </div>
            <div class="bg-stone-50 p-3 border border-stone-200 font-mono text-[11px] leading-relaxed overflow-x-auto">
                <div class="text-green-600">+ database.query(</div>
                <div class="text-green-600">+   'SELECT * FROM users WHERE id = ?',</div>
                <div class="text-green-600">+   [userId]</div>
                <div class="text-green-600">+ )</div>
                <div></div>
                <div>async function getUser(id) {</div>
                <div class="text-green-600">+   let user = await db.query(</div>
                <div class="text-green-600">+     'SELECT * WHERE id = ?',</div>
                <div class="text-green-600">+     [id]</div>
                <div class="text-green-600">+   )</div>
                <div class="text-green-600">+   return user</div>
                <div>}</div>
            </div>
            <div class="mt-3 px-3 py-2 bg-green-50 border border-green-200 text-green-700 text-xs font-bold">
                ✓ Parameterized Query (Secure)
            </div>
        </div>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-3 gap-4 mb-10">
        <div class="bg-white border border-stone-200 p-4 text-center code-shadow">
            <div class="font-bold text-2xl text-red-600">-8</div>
            <div class="font-mono text-xs text-stone-500 uppercase">Lines Removed</div>
        </div>
        <div class="bg-white border border-stone-200 p-4 text-center code-shadow">
            <div class="font-bold text-2xl text-green-600">+8</div>
            <div class="font-mono text-xs text-stone-500 uppercase">Lines Added</div>
        </div>
        <div class="bg-white border border-stone-200 p-4 text-center code-shadow">
            <div class="font-bold text-2xl text-primary-container">100%</div>
            <div class="font-mono text-xs text-stone-500 uppercase">Issue Fixed</div>
        </div>
    </div>

    <!-- Apply Fix Section -->
    <div class="bg-white border border-stone-200 p-6 code-shadow">
        <h3 class="font-headline font-bold uppercase mb-4">Apply This Fix</h3>
        <p class="text-sm text-stone-600 mb-4">This fix prevents SQL injection vulnerabilities by using parameterized queries.</p>
        <div class="grid grid-cols-2 gap-4">
            <button class="px-6 py-3 bg-primary-container text-on-primary-fixed font-bold text-sm uppercase hover:bg-primary transition">
                Apply Fix Automatically
            </button>
            <button class="px-6 py-3 border border-stone-200 text-stone-600 font-bold text-sm uppercase hover:bg-stone-50 transition">
                Review & Apply Manually
            </button>
        </div>
    </div>
</div>
    `;
}
