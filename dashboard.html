<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hunter Pro CRM AI | النظام الذكي المتكامل</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    
    <style>
        * { font-family: 'Tajawal', sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        
        .glass {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        
        .glow { box-shadow: 0 0 30px rgba(102, 126, 234, 0.5); }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .float-animation { animation: float 3s ease-in-out infinite; }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .slide-up { animation: slideUp 0.6s ease-out forwards; }
        
        .chat-bubble {
            max-width: 80%;
            padding: 12px 18px;
            border-radius: 18px;
            margin: 8px 0;
            word-wrap: break-word;
        }
        
        .chat-bubble.user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-right: auto;
            border-bottom-right-radius: 4px;
        }
        
        .chat-bubble.ai {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin-left: auto;
            border-bottom-left-radius: 4px;
        }
        
        .typing-indicator {
            display: flex;
            gap: 4px;
            padding: 12px;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            animation: blink 1.4s infinite both;
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes blink {
            0%, 80%, 100% { opacity: 0; }
            40% { opacity: 1; }
        }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; }
        
        .nav-item { transition: all 0.3s ease; }
        .nav-item:hover { transform: translateX(-5px); }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body class="overflow-hidden">

    <!-- Login Screen -->
    <div id="login-screen" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="glass rounded-3xl p-10 max-w-md w-full mx-4 slide-up">
            <div class="text-center mb-8">
                <div class="w-24 h-24 bg-gradient-to-br from-purple-600 to-blue-600 rounded-3xl flex items-center justify-center mx-auto mb-6 glow float-animation">
                    <i class="fas fa-brain text-white text-5xl"></i>
                </div>
                <h1 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600 mb-2">
                    Hunter Pro AI
                </h1>
                <p class="text-gray-600">نظام CRM الذكي المتكامل</p>
            </div>
            
            <form onsubmit="login(event)" class="space-y-4">
                <div class="relative">
                    <i class="fas fa-envelope absolute right-4 top-4 text-gray-400"></i>
                    <input type="email" id="login-email" value="admin@example.com" 
                        class="w-full pr-12 pl-4 py-4 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition"
                        placeholder="البريد الإلكتروني">
                </div>
                
                <div class="relative">
                    <i class="fas fa-lock absolute right-4 top-4 text-gray-400"></i>
                    <input type="password" id="login-password" value="admin123"
                        class="w-full pr-12 pl-4 py-4 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition"
                        placeholder="كلمة المرور">
                </div>
                
                <button type="submit" class="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-2xl transform hover:scale-105 transition">
                    <i class="fas fa-sign-in-alt ml-2"></i> دخول
                </button>
            </form>
        </div>
    </div>

    <!-- Main Dashboard -->
    <div id="dashboard" class="hidden flex h-screen">
        
        <!-- Sidebar -->
        <aside class="w-72 glass p-6 hidden lg:block overflow-y-auto">
            <div class="flex items-center gap-3 mb-10">
                <div class="w-12 h-12 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center glow">
                    <i class="fas fa-brain text-white text-2xl"></i>
                </div>
                <div>
                    <h1 class="text-xl font-black text-gray-800">Hunter Pro AI</h1>
                    <span class="text-xs bg-gradient-to-r from-purple-600 to-blue-600 text-white px-2 py-1 rounded-full">v5.0</span>
                </div>
            </div>

            <nav class="space-y-2">
                <a href="#" onclick="showSection('dashboard')" class="nav-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-purple-100 hover:text-purple-700 transition">
                    <i class="fas fa-chart-line w-5"></i> لوحة التحكم
                </a>
                <a href="#" onclick="showSection('hunt')" class="nav-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-purple-100 hover:text-purple-700 transition">
                    <i class="fas fa-search w-5"></i> محرك البحث
                </a>
                <a href="#" onclick="showSection('leads')" class="nav-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-purple-100 hover:text-purple-700 transition">
                    <i class="fas fa-users w-5"></i> إدارة العملاء
                </a>
                <a href="#" onclick="showSection('ai-chat')" class="nav-item flex items-center gap-3 px-4 py-3 rounded-xl bg-gradient-to-r from-purple-100 to-blue-100 text-purple-700 transition">
                    <i class="fas fa-robot w-5"></i> المحاور الذكي
                </a>
                <a href="#" onclick="showSection('campaigns')" class="nav-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-purple-100 hover:text-purple-700 transition">
                    <i class="fab fa-whatsapp w-5"></i> الحملات
                </a>
                <a href="#" onclick="showSection('admin-ai')" class="nav-item flex items-center gap-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-purple-100 hover:text-purple-700 transition">
                    <i class="fas fa-cog w-5"></i> شات الأدمن
                </a>
            </nav>

            <div class="mt-auto pt-6 border-t border-gray-200">
                <button onclick="logout()" class="w-full bg-red-50 text-red-600 py-3 rounded-xl hover:bg-red-100 transition font-bold">
                    <i class="fas fa-sign-out-alt ml-2"></i> تسجيل خروج
                </button>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto p-8 bg-gradient-to-br from-blue-50 to-purple-50">
            
            <!-- Dashboard Section -->
            <section id="section-dashboard" class="section">
                <div class="mb-8">
                    <h2 class="text-4xl font-black text-gray-800 mb-2">مرحباً بك 👋</h2>
                    <p class="text-gray-600">إليك ملخص النظام اليوم</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div class="stat-card rounded-2xl p-6 text-white" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <div class="flex items-center justify-between mb-4">
                            <i class="fas fa-users text-4xl opacity-80"></i>
                            <span class="text-5xl font-black" id="stat-leads">0</span>
                        </div>
                        <p class="text-sm opacity-90">إجمالي العملاء</p>
                    </div>

                    <div class="stat-card rounded-2xl p-6 text-white" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <div class="flex items-center justify-between mb-4">
                            <i class="fab fa-whatsapp text-4xl opacity-80"></i>
                            <span class="text-5xl font-black" id="stat-messages">0</span>
                        </div>
                        <p class="text-sm opacity-90">رسائل مرسلة</p>
                    </div>

                    <div class="stat-card rounded-2xl p-6 text-white" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        <div class="flex items-center justify-between mb-4">
                            <i class="fas fa-fire text-4xl opacity-80"></i>
                            <span class="text-5xl font-black" id="stat-excellent">0</span>
                        </div>
                        <p class="text-sm opacity-90">عملاء ممتازين</p>
                    </div>

                    <div class="stat-card rounded-2xl p-6 text-white" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                        <div class="flex items-center justify-between mb-4">
                            <i class="fas fa-search text-4xl opacity-80"></i>
                            <span class="text-5xl font-black" id="stat-hunts">0</span>
                        </div>
                        <p class="text-sm opacity-90">عمليات بحث</p>
                    </div>
                </div>

                <div class="glass rounded-3xl p-8">
                    <h3 class="text-2xl font-bold text-gray-800 mb-6">تحليل الأداء</h3>
                    <canvas id="performanceChart" class="w-full" height="100"></canvas>
                </div>
            </section>

            <!-- Hunt Section -->
            <section id="section-hunt" class="section hidden">
                <div class="glass rounded-3xl p-8 mb-6">
                    <h2 class="text-3xl font-black text-gray-800 mb-6">محرك البحث الذكي 🔍</h2>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">نية البحث</label>
                            <input type="text" id="hunt-query" 
                                placeholder="مثال: مطلوب شقة في التجمع الخامس"
                                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition">
                        </div>

                        <div>
                            <label class="block text-sm font-bold text-gray-700 mb-2">المدينة</label>
                            <select id="hunt-city" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition">
                                <option value="القاهرة">القاهرة</option>
                                <option value="الجيزة">الجيزة</option>
                                <option value="الإسكندرية">الإسكندرية</option>
                            </select>
                        </div>

                        <button onclick="startHunt()" class="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-2xl transform hover:scale-105 transition">
                            <i class="fas fa-rocket ml-2"></i> ابدأ البحث
                        </button>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <button onclick="openExtractModal()" class="glass rounded-2xl p-6 hover:shadow-2xl transition transform hover:scale-105">
                        <i class="fas fa-file-lines text-4xl text-purple-600 mb-3"></i>
                        <h4 class="font-bold text-gray-800">استخراج من نص</h4>
                    </button>

                    <button onclick="exportData()" class="glass rounded-2xl p-6 hover:shadow-2xl transition transform hover:scale-105">
                        <i class="fas fa-download text-4xl text-green-600 mb-3"></i>
                        <h4 class="font-bold text-gray-800">تصدير Excel</h4>
                    </button>
                </div>
            </section>

            <!-- Leads Section -->
            <section id="section-leads" class="section hidden">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-3xl font-black text-gray-800">قاعدة العملاء</h2>
                    <button onclick="openAddLeadModal()" class="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-xl font-bold hover:shadow-2xl transition">
                        <i class="fas fa-plus ml-2"></i> إضافة عميل
                    </button>
                </div>

                <div class="glass rounded-3xl overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
                                <tr>
                                    <th class="px-6 py-4 text-right">العميل</th>
                                    <th class="px-6 py-4 text-right">الجودة</th>
                                    <th class="px-6 py-4 text-right">المصدر</th>
                                    <th class="px-6 py-4 text-right">الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody id="leads-table" class="divide-y divide-gray-200">
                                <tr><td colspan="4" class="text-center py-8 text-gray-500">جاري التحميل...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- AI Chat Section (للعميل) -->
            <section id="section-ai-chat" class="section hidden">
                <div class="glass rounded-3xl p-8">
                    <div class="flex items-center gap-4 mb-6">
                        <div class="w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl flex items-center justify-center glow">
                            <i class="fas fa-robot text-white text-3xl"></i>
                        </div>
                        <div>
                            <h2 class="text-3xl font-black text-gray-800">المحاور الذكي</h2>
                            <p class="text-gray-600">تحدث مع عملائك بذكاء اصطناعي</p>
                        </div>
                    </div>

                    <div class="mb-4">
                        <label class="block text-sm font-bold text-gray-700 mb-2">رقم العميل</label>
                        <input type="text" id="customer-phone" 
                            placeholder="01012345678"
                            class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition">
                    </div>

                    <div id="ai-chat-messages" class="bg-gray-50 rounded-2xl p-6 h-96 overflow-y-auto mb-4 space-y-3">
                        <!-- Messages here -->
                    </div>

                    <div class="flex gap-3">
                        <input type="text" id="customer-message" 
                            placeholder="اكتب رسالة العميل..."
                            class="flex-1 px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition"
                            onkeypress="if(event.key==='Enter') sendCustomerMessage()">
                        <button onclick="sendCustomerMessage()" class="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:shadow-2xl transition">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </section>

            <!-- Admin AI Section -->
            <section id="section-admin-ai" class="section hidden">
                <div class="glass rounded-3xl p-8">
                    <div class="flex items-center gap-4 mb-6">
                        <div class="w-16 h-16 bg-gradient-to-br from-red-600 to-pink-600 rounded-2xl flex items-center justify-center glow">
                            <i class="fas fa-crown text-white text-3xl"></i>
                        </div>
                        <div>
                            <h2 class="text-3xl font-black text-gray-800">شات الأدمن الذكي</h2>
                            <p class="text-gray-600">تحكم كامل بالنظام عبر الذكاء الاصطناعي</p>
                        </div>
                    </div>

                    <div id="admin-chat-messages" class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-6 h-96 overflow-y-auto mb-4 space-y-3">
                        <!-- Admin messages here -->
                    </div>

                    <div class="flex gap-3">
                        <input type="text" id="admin-command" 
                            placeholder="مثال: اعرض إحصائيات اليوم | أضف مستخدم جديد"
                            class="flex-1 px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition"
                            onkeypress="if(event.key==='Enter') sendAdminCommand()">
                        <button onclick="sendAdminCommand()" class="bg-gradient-to-r from-red-600 to-pink-600 text-white px-8 py-3 rounded-xl font-bold hover:shadow-2xl transition">
                            <i class="fas fa-magic"></i>
                        </button>
                    </div>

                    <div class="mt-4 p-4 bg-yellow-50 border-2 border-yellow-200 rounded-xl">
                        <h4 class="font-bold text-yellow-800 mb-2">💡 أمثلة الأوامر:</h4>
                        <ul class="text-sm text-yellow-700 space-y-1">
                            <li>• "اعرض إحصائيات العملاء الجدد اليوم"</li>
                            <li>• "أضف مستخدم جديد اسمه أحمد"</li>
                            <li>• "أنشئ حملة واتساب للعملاء الممتازين"</li>
                            <li>• "حلل أداء البحث في آخر أسبوع"</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Campaigns Section -->
            <section id="section-campaigns" class="section hidden">
                <h2 class="text-3xl font-black text-gray-800 mb-6">الحملات التسويقية</h2>
                
                <div class="glass rounded-3xl p-8 mb-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-4">إنشاء حملة جديدة</h3>
                    <form onsubmit="createCampaign(event)" class="space-y-4">
                        <input name="name" placeholder="اسم الحملة" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition">
                        <textarea name="message" rows="3" placeholder="نص الرسالة" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition"></textarea>
                        <button type="submit" class="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-xl font-bold hover:shadow-2xl transition">
                            <i class="fas fa-rocket ml-2"></i> إنشاء الحملة
                        </button>
                    </form>
                </div>

                <div id="campaigns-list" class="space-y-4">
                    <!-- Campaigns here -->
                </div>
            </section>

        </main>
    </div>

    <!-- Extract Modal -->
    <div id="extract-modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass rounded-3xl w-full max-w-2xl p-8 slide-up">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gray-800">استخراج الأرقام</h3>
                <button onclick="closeExtractModal()" class="w-10 h-10 rounded-full bg-gray-100 hover:bg-gray-200 transition">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <textarea id="extract-text" class="w-full h-48 px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition mb-4" placeholder="الصق النص هنا..."></textarea>
            <button onclick="extractPhones()" class="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-xl font-bold hover:shadow-2xl transition">
                <i class="fas fa-magic ml-2"></i> استخراج
            </button>
            <div id="extract-result" class="mt-4 hidden p-4 bg-green-50 border-2 border-green-200 rounded-xl"></div>
        </div>
    </div>

    <script>
        const API = window.location.origin;
        let currentUser = 'admin';
        let chatHistory = [];
        let chartInstance = null;

        // Login
        async function login(e) {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const res = await fetch(`${API}/api/login`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email, password})
                });

                if (res.ok) {
                    const data = await res.json();
                    localStorage.setItem('token', data.access_token);
                    document.getElementById('login-screen').classList.add('hidden');
                    document.getElementById('dashboard').classList.remove('hidden');
                    loadDashboard();
                    Swal.fire({icon: 'success', title: 'مرحباً بك!', timer: 1500, showConfirmButton: false});
                } else {
                    Swal.fire('خطأ', 'بيانات الدخول غير صحيحة', 'error');
                }
            } catch (e) {
                Swal.fire('خطأ', 'فشل الاتصال بالخادم', 'error');
            }
        }

        function logout() {
            localStorage.clear();
            location.reload();
        }

        // Load Dashboard
        async function loadDashboard() {
            try {
                // Load stats
                const stats = await (await fetch(`${API}/api/admin-stats`)).json();
                document.getElementById('stat-leads').innerText = stats.total_leads || 0;
                document.getElementById('stat-messages').innerText = stats.total_messages || 0;
                document.getElementById('stat-excellent').innerText = Math.floor((stats.total_leads || 0) * 0.3);
                document.getElementById('stat-hunts').innerText = Math.floor(Math.random() * 50) + 10;

                // Load leads
                const leads = await (await fetch(`${API}/api/leads`)).json();
                renderLeads(leads.leads || []);

                // Init chart
                initChart(stats.total_leads || 0);
            } catch (e) {
                console.error('Load error:', e);
            }
        }

        function renderLeads(leads) {
            const tbody = document.getElementById('leads-table');
            if (!leads.length) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center py-8 text-gray-500">لا توجد بيانات</td></tr>';
                return;
            }

            tbody.innerHTML = leads.slice(0, 50).map(l => `
                <tr class="hover:bg-purple-50 transition">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 text-white flex items-center justify-center font-bold">
                                ${l.phone_number.slice(-2)}
                            </div>
                            <span class="font-bold text-gray-800">${l.phone_number}</span>
                        </div>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-3 py-1 rounded-full text-xs font-bold ${l.quality?.includes('ممتاز') ? 'bg-purple-
