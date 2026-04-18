// ============================================
// Analysis History - Historical Trend Tracking
// ============================================

function render_analysis_history() {
    const app = document.getElementById('app');
    app.innerHTML = `
<div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-start mb-10">
        <div>
            <h1 class="font-headline text-4xl font-black uppercase tracking-tighter mb-2">Analysis History</h1>
            <p class="font-mono text-sm text-stone-600 uppercase tracking-widest">Track your improvements over time</p>
        </div>
        <div class="flex gap-2">
            <button class="px-4 py-2 border border-stone-200 text-stone-600 font-bold text-xs uppercase hover:bg-stone-50 transition">
                Export Report
            </button>
        </div>
    </div>

    <!-- Trend Summary -->
    <div class="grid grid-cols-4 gap-4 mb-10">
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-mono text-xs text-stone-600 uppercase tracking-widest mb-2">Total Analyses</div>
            <div class="font-headline text-3xl font-black">24</div>
            <div class="font-mono text-xs text-green-600 mt-2">↑ 4 this month</div>
        </div>
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-mono text-xs text-stone-600 uppercase tracking-widest mb-2">Issues Resolved</div>
            <div class="font-headline text-3xl font-black text-green-600">47</div>
            <div class="font-mono text-xs text-green-600 mt-2">↑ 65% improvement</div>
        </div>
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-mono text-xs text-stone-600 uppercase tracking-widest mb-2">Avg Quality Score</div>
            <div class="font-headline text-3xl font-black">82%</div>
            <div class="font-mono text-xs text-green-600 mt-2">↑ up from 64%</div>
        </div>
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-mono text-xs text-stone-600 uppercase tracking-widest mb-2">Security Threats</div>
            <div class="font-headline text-3xl font-black text-orange-600">3</div>
            <div class="font-mono text-xs text-green-600 mt-2">↓ 84% reduction</div>
        </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
        <!-- Metrics Trend Chart -->
        <div class="col-span-2 bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-bold uppercase text-sm mb-6">Quality Score Trend (Last 60 days)</div>
            
            <!-- Simple chart representation -->
            <div class="flex items-end justify-between h-48 gap-1 mb-4">
                <div class="flex-1 bg-stone-100 rounded" style="height: 30%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 35%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 40%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 45%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 48%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 52%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 58%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 62%;"></div>
                <div class="flex-1 bg-stone-100 rounded" style="height: 65%;"></div>
                <div class="flex-1 bg-primary-container rounded" style="height: 82%;"></div>
            </div>
            
            <div class="font-mono text-xs text-stone-600 grid grid-cols-2">
                <div>30 days ago: 48% → 10 issues</div>
                <div>Today: 82% → 3 issues</div>
            </div>
        </div>

        <!-- Analysis Summary -->
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-bold uppercase text-sm mb-4">Latest Analyses</div>
            <div class="space-y-3">
                <div class="border-b border-stone-100 pb-3">
                    <div class="font-bold text-sm">Today 2:45 PM</div>
                    <div class="font-mono text-xs text-stone-600">backend/api.py</div>
                    <div class="flex gap-2 mt-2">
                        <span class="px-2 py-1 bg-green-100 text-green-600 text-xs font-bold">82%</span>
                        <span class="px-2 py-1 bg-stone-100 text-stone-600 text-xs">-3 issues</span>
                    </div>
                </div>
                <div class="border-b border-stone-100 pb-3">
                    <div class="font-bold text-sm">Yesterday 11:20 AM</div>
                    <div class="font-mono text-xs text-stone-600">frontend/components.tsx</div>
                    <div class="flex gap-2 mt-2">
                        <span class="px-2 py-1 bg-yellow-100 text-orange-600 text-xs font-bold">71%</span>
                        <span class="px-2 py-1 bg-stone-100 text-stone-600 text-xs">-2 issues</span>
                    </div>
                </div>
                <div>
                    <div class="font-bold text-sm">Wed, Mar 13</div>
                    <div class="font-mono text-xs text-stone-600">Full project scan</div>
                    <div class="flex gap-2 mt-2">
                        <span class="px-2 py-1 bg-red-100 text-red-600 text-xs font-bold">64%</span>
                        <span class="px-2 py-1 bg-stone-100 text-stone-600 text-xs">-5 issues</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Detailed History Table -->
    <div class="mt-10 bg-white border border-stone-200 p-6 code-shadow">
        <div class="font-bold uppercase text-sm mb-6">Complete Analysis History</div>
        
        <table class="w-full font-mono text-xs">
            <thead>
                <tr class="border-b border-stone-200">
                    <th class="text-left py-3 font-bold uppercase">Date</th>
                    <th class="text-left py-3 font-bold uppercase">File/Scope</th>
                    <th class="text-left py-3 font-bold uppercase">Quality</th>
                    <th class="text-left py-3 font-bold uppercase">Issues</th>
                    <th class="text-left py-3 font-bold uppercase">Security</th>
                    <th class="text-left py-3 font-bold uppercase">Performance</th>
                    <th class="text-left py-3 font-bold uppercase">Change</th>
                    <th class="text-left py-3 font-bold uppercase">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr class="border-b border-stone-100 hover:bg-stone-50">
                    <td class="py-3">Mar 15, 2:45 PM</td>
                    <td class="text-stone-600">backend/api.py</td>
                    <td class="font-bold">82%</td>
                    <td><span class="px-2 py-1 bg-green-100 text-green-600 text-xs">3</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">1</span></td>
                    <td><span class="px-1 bg-yellow-100 text-orange-600">2</span></td>
                    <td class="text-green-600">+8%</td>
                    <td><button class="text-primary-container hover:underline">Compare</button></td>
                </tr>
                <tr class="border-b border-stone-100 hover:bg-stone-50">
                    <td class="py-3">Mar 14, 11:20 AM</td>
                    <td class="text-stone-600">frontend/components.tsx</td>
                    <td class="font-bold">71%</td>
                    <td><span class="px-2 py-1 bg-yellow-100 text-orange-600 text-xs">5</span></td>
                    <td><span class="px-1 bg-yellow-100 text-orange-600">2</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">3</span></td>
                    <td class="text-green-600">+7%</td>
                    <td><button class="text-primary-container hover:underline">Compare</button></td>
                </tr>
                <tr class="border-b border-stone-100 hover:bg-stone-50">
                    <td class="py-3">Mar 13, 9:15 AM</td>
                    <td class="text-stone-600">Full project scan</td>
                    <td class="font-bold">64%</td>
                    <td><span class="px-2 py-1 bg-red-100 text-red-600 text-xs">12</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">5</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">7</span></td>
                    <td>—</td>
                    <td><button class="text-primary-container hover:underline">View</button></td>
                </tr>
                <tr class="border-b border-stone-100 hover:bg-stone-50">
                    <td class="py-3">Mar 12, 3:30 PM</td>
                    <td class="text-stone-600">database/queries.sql</td>
                    <td class="font-bold">58%</td>
                    <td><span class="px-2 py-1 bg-red-100 text-red-600 text-xs">8</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">3</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">5</span></td>
                    <td>+15%</td>
                    <td><button class="text-primary-container hover:underline">Compare</button></td>
                </tr>
                <tr class="border-b border-stone-100 hover:bg-stone-50">
                    <td class="py-3">Mar 11, 10:00 AM</td>
                    <td class="text-stone-600">utils/helpers.py</td>
                    <td class="font-bold">43%</td>
                    <td><span class="px-2 py-1 bg-red-100 text-red-600 text-xs">15</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">4</span></td>
                    <td><span class="px-1 bg-red-100 text-red-600">6</span></td>
                    <td>—</td>
                    <td><button class="text-primary-container hover:underline">View</button></td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Before/After Comparison Preview -->
    <div class="mt-10 grid grid-cols-2 gap-6">
        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-bold uppercase text-sm mb-4">First Analysis (Mar 11)</div>
            <div class="space-y-2">
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Quality Score</span>
                    <span class="font-bold">43%</span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Total Issues</span>
                    <span class="font-bold">15</span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Security Threats</span>
                    <span class="font-bold text-red-600">4</span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Performance Issues</span>
                    <span class="font-bold">6</span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Code Quality Issues</span>
                    <span class="font-bold">5</span>
                </div>
            </div>
        </div>

        <div class="bg-white border border-stone-200 p-6 code-shadow">
            <div class="font-bold uppercase text-sm mb-4">Latest Analysis (Mar 15)</div>
            <div class="space-y-2 border-l-4 border-green-500 pl-4">
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Quality Score</span>
                    <span class="font-bold text-green-600">82% <span class="text-xs">+39%</span></span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Total Issues</span>
                    <span class="font-bold text-green-600">3 <span class="text-xs">-80%</span></span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Security Threats</span>
                    <span class="font-bold text-green-600">1 <span class="text-xs">-75%</span></span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Performance Issues</span>
                    <span class="font-bold text-green-600">1 <span class="text-xs">-83%</span></span>
                </div>
                <div class="flex justify-between">
                    <span class="font-mono text-sm">Code Quality Issues</span>
                    <span class="font-bold text-green-600">1 <span class="text-xs">-80%</span></span>
                </div>
            </div>
        </div>
    </div>
</div>
    `;
}
