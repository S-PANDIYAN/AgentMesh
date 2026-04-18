// ============================================
// File Browser - Uploaded Files Navigator
// ============================================

function render_file_browser() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">File Browser</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Explore uploaded project files</p>
        </div>
        <div class="flex gap-2">
            <button class="px-4 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">
                Upload More
            </button>
        </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
        <!-- File Tree -->
        <div class="col-span-1 bg-white border border-stone-200 p-4 code-shadow max-h-96 overflow-y-auto">
            <div class="font-bold uppercase text-xs mb-4">Project Structure</div>
            
            <!-- Folder Example -->
            <div class="space-y-2 font-mono text-xs">
                <div class="cursor-pointer hover:bg-stone-50 p-2 rounded">
                    <span class="text-primary-container">▼</span> src/
                </div>
                <div class="ml-4 space-y-2">
                    <div class="cursor-pointer hover:bg-stone-50 p-2 rounded">
                        <span class="text-primary-container">▼</span> auth/
                    </div>
                    <div class="ml-4 space-y-2">
                        <div class="cursor-pointer hover:bg-stone-50 p-2 rounded text-stone-600">
                            📄 auth.py
                        </div>
                        <div class="cursor-pointer hover:bg-stone-50 p-2 rounded text-stone-600">
                            📄 login.ts
                        </div>
                    </div>
                    
                    <div class="cursor-pointer hover:bg-stone-50 p-2 rounded">
                        <span class="text-primary-container">▼</span> database/
                    </div>
                    <div class="ml-4 space-y-2">
                        <div class="cursor-pointer hover:bg-stone-50 p-2 rounded text-stone-600">
                            📄 database.js
                        </div>
                        <div class="cursor-pointer hover:bg-stone-50 p-2 rounded text-primary-container font-bold bg-primary-container/10 p-2 rounded">
                            📄 connection.py ← Selected
                        </div>
                    </div>

                    <div class="cursor-pointer hover:bg-stone-50 p-2 rounded">
                        <span class="text-primary-container">▼</span> utils/
                    </div>
                    <div class="ml-4 space-y-2">
                        <div class="cursor-pointer hover:bg-stone-50 p-2 rounded text-stone-600">
                            📄 helpers.ts
                        </div>
                    </div>
                </div>
                
                <div class="cursor-pointer hover:bg-stone-50 p-2 rounded">
                    <span class="text-primary-container">▼</span> tests/
                </div>
                <div class="ml-4">
                    <div class="cursor-pointer hover:bg-stone-50 p-2 rounded text-stone-600">
                        📄 test_auth.py
                    </div>
                </div>
            </div>
        </div>

        <!-- File Details -->
        <div class="col-span-2 space-y-6">
            <!-- Selected File Info -->
            <div class="bg-white border border-stone-200 p-6 code-shadow">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <div class="font-headline font-bold text-2xl uppercase">connection.py</div>
                        <div class="font-mono text-xs text-stone-500 mt-2 space-y-1">
                            <div>📍 src/database/connection.py</div>
                            <div>📊 Size: 3.2 KB</div>
                            <div>📅 Last modified: 2 days ago</div>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        <button class="px-3 py-2 bg-primary-container text-on-primary-fixed font-bold text-xs uppercase hover:bg-primary transition">
                            View
                        </button>
                        <button class="px-3 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">
                            Download
                        </button>
                    </div>
                </div>

                <!-- Analysis Stats -->
                <div class="grid grid-cols-3 gap-3">
                    <div class="border border-stone-200 p-3">
                        <div class="font-bold">2</div>
                        <div class="font-mono text-xs text-stone-600">Issues Found</div>
                    </div>
                    <div class="border border-stone-200 p-3">
                        <div class="font-bold">142</div>
                        <div class="font-mono text-xs text-stone-600">Lines of Code</div>
                    </div>
                    <div class="border border-stone-200 p-3">
                        <div class="font-bold">78%</div>
                        <div class="font-mono text-xs text-stone-600">Quality Score</div>
                    </div>
                </div>
            </div>

            <!-- File Preview -->
            <div class="bg-white border border-stone-200 p-6 code-shadow">
                <div class="font-bold uppercase text-sm mb-4 flex justify-between items-center">
                    <span>File Preview</span>
                    <span class="font-mono text-xs text-stone-400">(First 20 lines)</span>
                </div>
                <div class="bg-stone-50 border border-stone-200 p-4 font-mono text-[10px] leading-relaxed overflow-x-auto">
                    <div><span class="text-stone-400">1</span>  <span class="text-purple-600">import</span> psycopg2</div>
                    <div><span class="text-stone-400">2</span>  <span class="text-purple-600">from</span> contextlib <span class="text-purple-600">import</span> contextmanager</div>
                    <div><span class="text-stone-400">3</span>  </div>
                    <div><span class="text-stone-400">4</span>  <span class="text-blue-600">class</span> <span class="text-green-600">DatabaseConnection</span>:</div>
                    <div><span class="text-stone-400">5</span>      <span class="text-purple-600">def</span> <span class="text-blue-600">__init__</span>(self, conn_string):</div>
                    <div><span class="text-stone-400">6</span>          <span class="text-red-600">self.conn_str = conn_string</span></div>
                    <div><span class="text-stone-400">7</span>          <span class="text-red-600">self.connection = None</span></div>
                    <div><span class="text-stone-400">8</span>  </div>
                    <div><span class="text-stone-400">9</span>      <span class="text-purple-600">def</span> <span class="text-blue-600">connect</span>(self):</div>
                    <div><span class="text-stone-400">10</span>         <span class="text-green-600">\"\"\"Establish database connection\"\"\"</span></div>
                    <div><span class="text-stone-400">11</span>         <span class="text-red-600">self.connection = psycopg2.connect(</span></div>
                    <div><span class="text-stone-400">12</span>             <span class="text-green-600">self.conn_str</span></div>
                    <div><span class="text-stone-400">13</span>         <span class="text-red-600">)</span></div>
                    <div><span class="text-stone-400">14</span>  </div>
                    <div><span class="text-stone-400">15</span>     <span class="text-purple-600">def</span> <span class="text-blue-600">query</span>(self, sql, params):</div>
                    <div><span class="text-stone-400">16</span>         <span class="text-green-600">\"\"\"Execute parameterized query\"\"\"</span></div>
                    <div><span class="text-stone-400">17</span>         cursor = self.connection.cursor()</div>
                    <div><span class="text-stone-400">18</span>         cursor.execute(sql, params)</div>
                    <div><span class="text-stone-400">19</span>         <span class="text-red-600">return</span> cursor.fetchall()</div>
                    <div><span class="text-stone-400">20</span>  </div>
                </div>
            </div>

            <!-- Issues in File -->
            <div class="bg-white border border-stone-200 p-6 code-shadow">
                <div class="font-bold uppercase text-sm mb-4">Issues in This File</div>
                <div class="space-y-3">
                    <div class="flex gap-3 items-start border-b border-stone-100 pb-3">
                        <span class="text-red-600 font-bold">🔴</span>
                        <div class="flex-1">
                            <div class="font-bold text-sm">No error handling in connect()</div>
                            <div class="font-mono text-xs text-stone-600">Line 11-13: Connection failures not caught</div>
                        </div>
                        <a href="#issue-details" class="px-3 py-1 bg-stone-50 hover:bg-stone-100 text-xs font-bold uppercase">View</a>
                    </div>
                    <div class="flex gap-3 items-start">
                        <span class="text-yellow-600 font-bold">🟡</span>
                        <div class="flex-1">
                            <div class="font-bold text-sm">Missing connection timeout</div>
                            <div class="font-mono text-xs text-stone-600">Line 11: Could hang indefinitely</div>
                        </div>
                        <a href="#issue-details" class="px-3 py-1 bg-stone-50 hover:bg-stone-100 text-xs font-bold uppercase">View</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    `;
}
