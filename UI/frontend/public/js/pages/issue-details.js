// ============================================
// Issue Details Page - Deep Dive Analysis
// ============================================

function render_issue_details() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-5xl mx-auto">
    <div class="mb-10">
        <a href="#results" class="text-primary-container hover:text-primary font-bold text-sm mb-4 inline-flex items-center gap-2">
            <span class="material-symbols-outlined text-lg">arrow_back</span> Back to Results
        </a>
        <div class="bg-white border-l-4 border-red-500 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h1 class="font-headline text-3xl font-black uppercase mb-2">SQL Injection Vulnerability</h1>
                    <div class="font-mono text-xs text-stone-600 space-y-1">
                        <div>📎 CVE-2024-12345 • CWE-89</div>
                        <div>🔍 Found in: auth.py (Line 145)</div>
                        <div>🗓️ Discovered: 2 hours ago</div>
                    </div>
                </div>
                <div class="bg-red-50 border border-red-200 px-6 py-4 text-center">
                    <div class="font-bold text-3xl text-red-600 mb-1">9.1</div>
                    <div class="font-mono text-xs text-red-600 font-bold">CVSS Score</div>
                    <div class="font-mono text-xs text-red-600 mt-2">CRITICAL</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabs -->
    <div class="mb-8 border-b border-stone-200">
        <div class="flex gap-0">
            <button class="px-6 py-4 font-bold text-sm uppercase border-b-2 border-primary-container text-on-primary-fixed">Overview</button>
            <button class="px-6 py-4 font-bold text-sm uppercase text-stone-500 hover:text-on-surface">Code</button>
            <button class="px-6 py-4 font-bold text-sm uppercase text-stone-500 hover:text-on-surface">Fix</button>
            <button class="px-6 py-4 font-bold text-sm uppercase text-stone-500 hover:text-on-surface">References</button>
        </div>
    </div>

    <div class="space-y-6">
        <!-- Description -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">Description</h3>
            <p class="text-sm text-stone-700 leading-relaxed mb-4">
                The application constructs SQL queries by directly concatenating user input without proper parameterization. 
                An attacker can inject malicious SQL code through the userId parameter to manipulate database queries, 
                potentially leading to unauthorized data access, modification, or deletion.
            </p>
            <div class="bg-red-50 border border-red-200 p-4 rounded font-mono text-xs text-red-800">
                <div class="font-bold mb-2">Attack Vector Example:</div>
                <div>userId = "1 OR 1=1 --"</div>
                <div class="mt-2 text-red-600">Result: Bypasses authentication and returns all users</div>
            </div>
        </div>

        <!-- Vulnerable Code -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">Vulnerable Code</h3>
            <div class="bg-stone-50 border border-stone-200 p-4 font-mono text-xs leading-relaxed overflow-x-auto">
                <div class="text-stone-400">1</div>
                <div class="text-red-600">database.query(\`</div>
                <div class="text-red-600">  SELECT * FROM users</div>
                <div class="text-red-600">  WHERE id = \${userId}  ← Dangerous concatenation</div>
                <div class="text-red-600">\`)</div>
            </div>
            <div class="mt-3 p-3 bg-red-50 border border-red-200 text-red-700 text-xs font-bold">
                ❌ Direct string interpolation allows SQL injection
            </div>
        </div>

        <!-- Impact -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">Impact Assessment</h3>
            <div class="grid grid-cols-2 gap-4">
                <div class="border border-stone-200 p-4">
                    <div class="font-bold text-sm mb-2">Confidentiality</div>
                    <div class="w-full bg-stone-200 h-2 mb-1"><div class="bg-red-500 h-full" style="width: 100%"></div></div>
                    <div class="font-mono text-xs text-stone-600">HIGH - All user data at risk</div>
                </div>
                <div class="border border-stone-200 p-4">
                    <div class="font-bold text-sm mb-2">Integrity</div>
                    <div class="w-full bg-stone-200 h-2 mb-1"><div class="bg-red-500 h-full" style="width: 100%"></div></div>
                    <div class="font-mono text-xs text-stone-600">HIGH - Data can be modified</div>
                </div>
                <div class="border border-stone-200 p-4">
                    <div class="font-bold text-sm mb-2">Availability</div>
                    <div class="w-full bg-stone-200 h-2 mb-1"><div class="bg-orange-500 h-full" style="width: 90%"></div></div>
                    <div class="font-mono text-xs text-stone-600">HIGH - Database could be destroyed</div>
                </div>
                <div class="border border-stone-200 p-4">
                    <div class="font-bold text-sm mb-2">Difficulty</div>
                    <div class="w-full bg-stone-200 h-2 mb-1"><div class="bg-green-500 h-full" style="width: 20%"></div></div>
                    <div class="font-mono text-xs text-stone-600">LOW - Easy to exploit</div>
                </div>
            </div>
        </div>

        <!-- Recommended Fix -->
        <div class="bg-green-50 border-l-4 border-green-500 p-6 code-shadow">
            <h3 class="font-headline font-bold uppercase mb-4">✓ Recommended Fix</h3>
            <p class="text-sm text-stone-700 mb-4">Use parameterized queries (prepared statements) to safely handle user input:</p>
            <div class="bg-white border border-stone-200 p-4 font-mono text-xs leading-relaxed overflow-x-auto">
                <div class="text-green-600">database.query(</div>
                <div class="text-green-600">  'SELECT * FROM users WHERE id = ?',</div>
                <div class="text-green-600">  [userId]  ← Parameter passed separately</div>
                <div class="text-green-600">)</div>
            </div>
            <div class="mt-3 p-3 bg-green-100 border border-green-300 text-green-800 text-xs font-bold">
                ✓ Parameterized queries prevent SQL injection
            </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 pt-4">
            <a href="#diff-viewer" class="flex-1 px-6 py-3 bg-primary-container text-on-primary-fixed font-bold text-sm uppercase text-center hover:bg-primary transition">
                View Diff
            </a>
            <button class="flex-1 px-6 py-3 border border-stone-200 text-stone-600 font-bold text-sm uppercase hover:bg-stone-50 transition">
                Mark as Fixed
            </button>
            <button class="flex-1 px-6 py-3 border border-stone-200 text-stone-600 font-bold text-sm uppercase hover:bg-stone-50 transition">
                Ignore Issue
            </button>
        </div>
    </div>
</div>
    `;
}
