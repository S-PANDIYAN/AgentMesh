// ============================================
// Security Page Renderer
// ============================================

function render_security() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Security Analysis</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">3 Critical Issues Found</p>
        </div>
    </div>

    <div class="space-y-6">
        <!-- CVE-1 -->
        <div class="bg-white border-l-4 border-red-500 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="font-headline font-bold text-lg uppercase text-red-600 mb-2">SQL Injection Vulnerability</h3>
                    <div class="font-mono text-xs text-stone-600 mb-2">CVE-2024-12345 • CVSS 9.1 • CWE-89</div>
                </div>
                <div class="bg-red-50 border border-red-200 px-4 py-2 text-center">
                    <div class="font-bold text-2xl text-red-600">9.1</div>
                    <div class="font-mono text-xs text-red-600">CRITICAL</div>
                </div>
            </div>
            <div class="bg-stone-50 p-4 mb-4 border border-stone-200">
                <div class="font-mono text-xs text-stone-600">
                    <div class="text-red-600">❌ Vulnerable Code:</div>
                    <div class="mt-2">database.query(\`SELECT * FROM users WHERE id = \${userId}\`)</div>
                </div>
            </div>
            <div class="grid grid-cols-3 gap-4 text-sm">
                <div><span class="font-bold">Location:</span> <span class="font-mono text-xs">auth.py:145</span></div>
                <div><span class="font-bold">Severity:</span> <span class="text-red-600">CRITICAL</span></div>
                <div><span class="font-bold">Fix Priority:</span> <span class="text-red-600">IMMEDIATE</span></div>
            </div>
        </div>

        <!-- CVE-2 -->
        <div class="bg-white border-l-4 border-red-500 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="font-headline font-bold text-lg uppercase text-red-600 mb-2">Hardcoded Secrets & API Keys</h3>
                    <div class="font-mono text-xs text-stone-600 mb-2">CWE-798 • CVSS 8.8 • Secret Exposure</div>
                </div>
                <div class="bg-red-50 border border-red-200 px-4 py-2 text-center">
                    <div class="font-bold text-2xl text-red-600">8.8</div>
                    <div class="font-mono text-xs text-red-600">CRITICAL</div>
                </div>
            </div>
            <div class="bg-stone-50 p-4 mb-4 border border-stone-200">
                <div class="font-mono text-xs text-stone-600">
                    <div class="text-red-600">❌ Found Secrets:</div>
                    <div class="mt-2">const API_KEY = "sk-abc123xyz"</div>
                    <div>const DB_PASSWORD = "p@ssw0rd123"</div>
                </div>
            </div>
            <div class="grid grid-cols-3 gap-4 text-sm">
                <div><span class="font-bold">Location:</span> <span class="font-mono text-xs">config.py:23-24</span></div>
                <div><span class="font-bold">Severity:</span> <span class="text-red-600">CRITICAL</span></div>
                <div><span class="font-bold">Action:</span> <span class="text-red-600">ROTATE KEYS</span></div>
            </div>
        </div>

        <!-- CVE-3 -->
        <div class="bg-white border-l-4 border-orange-500 p-6 code-shadow">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="font-headline font-bold text-lg uppercase text-orange-600 mb-2">Missing Input Validation</h3>
                    <div class="font-mono text-xs text-stone-600 mb-2">CWE-20 • CVSS 7.5 • Input Sanitization</div>
                </div>
                <div class="bg-orange-50 border border-orange-200 px-4 py-2 text-center">
                    <div class="font-bold text-2xl text-orange-600">7.5</div>
                    <div class="font-mono text-xs text-orange-600">HIGH</div>
                </div>
            </div>
            <div class="bg-stone-50 p-4 mb-4 border border-stone-200">
                <div class="font-mono text-xs text-stone-600">
                    <div class="text-orange-600">⚠️ No Validation:</div>
                    <div class="mt-2">function processUserInput(input) &#123;</div>
                    <div class="ml-4">// Directly using user input without sanitization</div>
                    <div class="ml-4">database.store(input);</div>
                    <div>&#125;</div>
                </div>
            </div>
            <div class="grid grid-cols-3 gap-4 text-sm">
                <div><span class="font-bold">Location:</span> <span class="font-mono text-xs">utils.js:89</span></div>
                <div><span class="font-bold">Severity:</span> <span class="text-orange-600">HIGH</span></div>
                <div><span class="font-bold">Recommendation:</span> <span>Add input sanitization</span></div>
            </div>
        </div>
    </div>
</div>
    `;
}
