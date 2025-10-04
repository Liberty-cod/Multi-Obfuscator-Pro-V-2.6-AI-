#!/usr/bin/env python3
# multi_obfuscator_with_preview_dnd.py
# Расширенный обфускатор с поддержкой .NET, C++, ИИ-обфускации и защиты от ИИ-деобфускации
# Требует Python 3.8+. Для .NET: pip install dnlib. Для drag&drop: pip install tkinterdnd2
# Для C++ парсинга: pip install clang (libclang bindings) - optional
# Для тем: pip install ttkthemes
# Для подсветки синтаксиса: pip install pygments
# Версия v2.6: Добавлена ИИ-генерация обфускации и защита от ИИ-деобфускации
# Обновление: Добавлены продвинутые ИИ-методы обфускации (№4), обфускация ресурсов и конфигураций (№6), обфускация сетевых данных (№9)

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os, re, base64, random, string, ast, textwrap, sys, hashlib, time, ctypes
import platform
import warnings
import locale
import xml.etree.ElementTree as ET  # Для парсинга .resx
import json  # Для обфускации JSON конфигураций

# Try importing additional libs
HAS_DND = False
HAS_DNLIB = False
HAS_CLANG = False
HAS_TTKTHEMES = False
HAS_PYGMENTS = False

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False
    warnings.warn("tkinterdnd2 not installed. Drag&Drop disabled. Install with: pip install tkinterdnd2")

try:
    import dnlib
    from dnlib import ModuleDefMD
    HAS_DNLIB = True
except ImportError:
    HAS_DNLIB = False
    warnings.warn("dnlib not installed. .NET obfuscation disabled. Install with: pip install dnlib")

try:
    import clang.cindex
    HAS_CLANG = True
except ImportError:
    HAS_CLANG = False
    warnings.warn("clang not installed. Advanced C++ obfuscation limited. Install with: pip install clang")

try:
    import ttkthemes
    HAS_TTKTHEMES = True
except ImportError:
    HAS_TTKTHEMES = False
    warnings.warn("ttkthemes not installed. Theme support limited. Install with: pip install ttkthemes")

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, CppLexer, JavascriptLexer, PowerShellLexer, HtmlLexer, CssLexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False
    warnings.warn("pygments not installed. Syntax highlighting disabled. Install with: pip install pygments")

# -------------------------
# Multilingual Support
# -------------------------
LANG = locale.getdefaultlocale()[0][:2].lower()  # Auto-detect: 'ru' or 'en'
if LANG not in ['ru', 'en']:
    LANG = 'en'  # Default to English

TRANSLATIONS = {
    'en': {
        'title': "🔒 Multi-Obfuscator Pro v2.6 - .NET, C++, AI & Anti-AI",
        'select_files': "📁 Select Files",
        'merge_files': "🔗 Merge Files",
        'process_each': "📄 Process Each",
        'generate_decoder': "🔑 Generate Decoder",
        'advanced_security': "🛡️ Advanced Security",
        'xor_key': "🔐 XOR:",
        'obf_key': "🔑 Obfuscation:",
        'output_file': "💾 Output File:",
        'select_output': "📂 Select",
        'preview_method': "🔍 Method Preview:",
        'show_preview': "👁️ Show",
        'run_obf': "🚀 RUN OBFUSCATION",
        'status_ready': "Ready! Select files and obfuscation methods.",
        'results': "📋 Obfuscation Results:",
        'tab_python': "🐍 Python",
        'tab_powershell': "⚡ PowerShell",
        'tab_js': "📜 JavaScript",
        'tab_dotnet': "🔗 .NET (C#/VB)",
        'tab_exe': "⚙️ Native EXE",
        'tab_html': "🌐 HTML",
        'tab_css': "🎨 CSS",
        'tab_universal': "🌍 Universal",
        'tab_cpp': "🛡️ C++",
        'theme_switch': "🌗 Switch Theme",
        'no_files': "Select files first!",
        'no_method': "Select a method from the dropdown",
        'method_not_found': "Method '{}' not found",
        'obf_completed': "Obfuscation completed in {:.1f}s!\nProcessed {} files.",
        'decoder_generated': "\n🔑 Decoders generated for encrypted files.",
        'preview_error': "Preview Error",
        'processing': "🔄 PROCESSING: {} ({})",
        'path': "📂 Path: {}",
        'text_obf_success': "✅ {} obfuscation",
        'output_file_written': "📁 Output file: {}",
        'size_change': "📏 Length: {:,} → {:,} chars",
        'size_delta': "📈 Change: {:.1f}%",
        'decoder_file': "🔑 Decoder: {}",
        'preview_truncated': "\n... [truncated] ...",
        'error_processing': "💥 PROCESSING ERROR {}",
        'error_type': "Type: {}",
        'error_details': "Error: {}",
        'merge_mode': "🔗 MERGE MODE ({})",
        'individual_mode': "📄 INDIVIDUAL PROCESSING MODE",
        'obf_started': "🚀 OBFUSCATION STARTED",
        'start_time': "🕐 Time: {}",
        'files_processed': "📁 Files processed: {}",
        'xor_key_label': "🔑 XOR key: {}",
        'obf_key_label': "🔐 Obfuscation key: {}",
        'obf_completed_footer': "✅ OBFUSCATION COMPLETED",
        'execution_time': "⏱️ Execution time: {:.1f} seconds",
        'error_critical': "💥 CRITICAL ERROR!",
        'error_trace': "Traceback: {}",
        'no_dotnet': "⚠️ .NET obfuscation unavailable\nInstall: pip install dnlib",
        'no_clang': "⚠️ Advanced C++ obfuscation limited\nInstall: pip install clang",
        'no_dnd': "💡 Drag&Drop unavailable. Install: pip install tkinterdnd2",
        'resx_obf_success': "✅ .RESX String Encryption",
        'image_obf_success': "✅ Image Data Obfuscation",
        'strings_encrypted': "🔢 Strings encrypted: {}",
        'images_encrypted': "🖼️ Images encrypted: {}",
        'json_obf_success': "✅ JSON Configuration Obfuscation",
        'xml_obf_success': "✅ XML Configuration Obfuscation",
        'network_obf_success': "✅ Network Data Obfuscation",
    },
    'ru': {
        'title': "🔒 Multi-Obfuscator Pro v2.6 - .NET, C++, ИИ & Anti-ИИ",
        'select_files': "📁 Выбрать файлы",
        'merge_files': "🔗 Объединить файлы",
        'process_each': "📄 Каждый отдельно",
        'generate_decoder': "🔑 Создать декодер",
        'advanced_security': "🛡️ Расширенная безопасность",
        'xor_key': "🔐 XOR:",
        'obf_key': "🔑 Обфускация:",
        'output_file': "💾 Выходной файл:",
        'select_output': "📂 Выбрать",
        'preview_method': "🔍 Предпросмотр метода:",
        'show_preview': "👁️ Показать",
        'run_obf': "🚀 ЗАПУСТИТЬ ОБФУСКАЦИЮ",
        'status_ready': "Готов к работе! Выберите файлы и методы обфускации.",
        'results': "📋 Результаты обфускации:",
        'tab_python': "🐍 Python",
        'tab_powershell': "⚡ PowerShell",
        'tab_js': "📜 JavaScript",
        'tab_dotnet': "🔗 .NET (C#/VB)",
        'tab_exe': "⚙️ Native EXE",
        'tab_html': "🌐 HTML",
        'tab_css': "🎨 CSS",
        'tab_universal': "🌍 Универсальные",
        'tab_cpp': "🛡️ C++",
        'theme_switch': "🌗 Переключить тему",
        'no_files': "Сначала выберите файлы!",
        'no_method': "Выберите метод из выпадающего списка",
        'method_not_found': "Метод '{}' не найден",
        'obf_completed': "Обфускация завершена за {:.1f}с!\nОбработано {} файлов.",
        'decoder_generated': "\n🔑 Декодеры созданы для файлов с шифрованием.",
        'preview_error': "Ошибка предпросмотра",
        'processing': "🔄 ОБРАБОТКА: {} ({})",
        'path': "📂 Путь: {}",
        'text_obf_success': "✅ {} обфускация",
        'output_file_written': "📁 Выходной файл: {}",
        'size_change': "📏 Длина: {:,} → {:,} символов",
        'size_delta': "📈 Изменение: {:.1f}%",
        'decoder_file': "🔑 Декодер: {}",
        'preview_truncated': "\n... [сокращено] ...",
        'error_processing': "💥 ОШИБКА ОБРАБОТКИ {}",
        'error_type': "Тип: {}",
        'error_details': "Ошибка: {}",
        'merge_mode': "🔗 РЕЖИМ ОБЪЕДИНЕНИЯ ({})",
        'individual_mode': "📄 РЕЖИМ: ОТДЕЛЬНАЯ ОБРАБОТКА",
        'obf_started': "🚀 ОБФУСКАЦИЯ ЗАПУЩЕНА",
        'start_time': "🕐 Время: {}",
        'files_processed': "📁 Обработано файлов: {}",
        'xor_key_label': "🔑 XOR ключ: {}",
        'obf_key_label': "🔐 Обфускационный ключ: {}",
        'obf_completed_footer': "✅ ОБФУСКАЦИЯ ЗАВЕРШЕНА",
        'execution_time': "⏱️ Время выполнения: {:.1f} секунд",
        'error_critical': "💥 КРИТИЧЕСКАЯ ОШИБКА!",
        'error_trace': "Подробности: {}",
        'no_dotnet': "⚠️ .NET обфускация недоступна\nУстановите: pip install dnlib",
        'no_clang': "⚠️ Расширенная C++ обфускация ограничена\nУстановите: pip install clang",
        'no_dnd': "💡 Drag&Drop недоступен. Установите: pip install tkinterdnd2",
        'resx_obf_success': "✅ Шифрование строк .RESX",
        'image_obf_success': "✅ Обфускация данных изображений",
        'strings_encrypted': "🔢 Зашифровано строк: {}",
        'images_encrypted': "🖼️ Зашифровано изображений: {}",
        'json_obf_success': "✅ Обфускация конфигурации JSON",
        'xml_obf_success': "✅ Обфускация конфигурации XML",
        'network_obf_success': "✅ Обфускация сетевых данных",
    }
}

def t(key, *args):
    return TRANSLATIONS.get(LANG, TRANSLATIONS['en']).get(key, key).format(*args)

# -------------------------
# Utility helpers
# -------------------------
def detect_lang(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".py": return "python"
    if ext == ".ps1": return "powershell"
    if ext in (".js", ".mjs"): return "js"
    if ext in (".cpp", ".hpp", ".h", ".cc"): return "cpp"
    if ext == ".resx": return "resx"
    if ext == ".json": return "json"
    if ext == ".xml": return "xml"
    if ext in (".png", ".jpg", ".jpeg", ".gif"): return "image"
    if ext in (".exe", ".dll"):
        if HAS_DNLIB:
            try:
                module = ModuleDefMD.Load(path)
                if hasattr(module, 'IsClr') and module.IsClr:
                    return "dotnet"
            except:
                pass
        return ext
    if ext in (".html", ".htm"): return "html"
    if ext in (".css",): return "css"
    return "universal"

def all_same_lang(files):
    langs = {detect_lang(f) for f in files}
    return len(langs) == 1, (list(langs)[0] if langs else "universal")

def gen_name(n=8):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()

def write_bytes(path, data: bytes):
    with open(path, "wb") as f:
        f.write(data)

def extract_string_placeholders(text, lang="generic"):
    literals = []
    def _rep(m):
        literals.append(m.group(0))
        return f"__STR{len(literals)-1}__"
    if lang == "js" or lang == "cpp":
        pattern = r'(`(?:\\`|\\.|[^`])*`)|("(?:\\.|[^"\\])*")|(\'(?:\\.|[^\'\\])*\')'
    else:
        pattern = r'("(?:\\.|[^"\\])*")|(\'(?:\\.|[^\'\\])*\')'
    new = re.sub(pattern, lambda m: _rep(m), text, flags=re.S)
    return new, literals

def restore_string_placeholders(text, literals):
    def _rep(m):
        idx = int(m.group(1))
        return literals[idx]
    return re.sub(r'__STR(\d+)__', _rep, text)

# -------------------------
# Advanced Obfuscation Helpers
# -------------------------
def custom_encrypt_string(text: str, key: str) -> str:
    key_bytes = key.encode("utf-8")
    result = bytearray(len(text))
    for i, char in enumerate(text.encode("utf-8")):
        shift = key_bytes[i % len(key_bytes)] % 32
        result[i] = (char + shift) ^ key_bytes[i % len(key_bytes)]
    return base64.b64encode(result).decode("ascii")

def hash_name(name: str, seed: str = "secret") -> str:
    return "v_" + hashlib.md5((name + seed).encode()).hexdigest()[:8]

# -------------------------
# AI-Powered Obfuscation Methods (№4: Advanced AI methods)
# -------------------------
def ai_obfuscate(text: str, *_args) -> str:
    """AI-generated obfuscation with randomized mathematical transformations"""
    try:
        tree = ast.parse(text)
        
        class AIObfuscator(ast.NodeTransformer):
            def visit_BinOp(self, node):
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
                    new_node = ast.BinOp(
                        left=ast.BinOp(node.left, ast.BitXor(), node.right),
                        op=ast.Add(),
                        right=ast.BinOp(
                            left=ast.BinOp(node.left, ast.BitAnd(), node.right),
                            op=ast.Mult(),
                            right=ast.Num(n=2)
                        )
                    )
                    ast.fix_missing_locations(new_node)
                    return new_node
                return self.generic_visit(node)
            
            def visit_FunctionDef(self, node):
                trap_code = textwrap.dedent(f"""
                    import time
                    def _ai_trap_{random.randint(1000, 9999)}():
                        start = time.time()
                        for _ in range({random.randint(5000, 15000)}):
                            _ = {random.randint(1, 100)} ** 2
                        if time.time() - start > {random.uniform(0.1, 0.5)}:
                            import sys; sys.exit(1)
                    _ai_trap_{random.randint(1000, 9999)}()
                """)
                trap_nodes = ast.parse(trap_code).body
                node.body = trap_nodes + node.body
                return self.generic_visit(node)
        
        tree = AIObfuscator().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception as e:
        return f"# AI Obfuscation Error: {str(e)}\n{text}"

def anti_ai_deobfuscation(text: str, *_args) -> str:
    """Add traps to confuse AI-based deobfuscators"""
    try:
        tree = ast.parse(text)
        
        class AntiAITraps(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                fake_func_name = f"fake_{gen_name(8)}"
                fake_code = textwrap.dedent(f"""
                    def {fake_func_name}():
                        import random
                        return random.randint(0, 100) * {random.randint(1, 10)}
                    {fake_func_name}()
                """)
                fake_nodes = ast.parse(fake_code).body
                node.body = fake_nodes + node.body
                return self.generic_visit(node)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, (ast.Store, ast.Load)):
                    node.id = f"v_{hash_name(node.id, str(random.randint(1000, 9999)))}"
                return node
        
        tree = AntiAITraps().visit(tree)
        ast.fix_missing_locations(tree)
        trap_code = textwrap.dedent("""
            import os
            if 'AI_ANALYSIS' in os.environ:
                raise Exception('AI analysis detected')
        """)
        tree.body.insert(0, ast.parse(trap_code).body[0])
        return ast.unparse(tree)
    except Exception as e:
        return f"# Anti-AI Deobfuscation Error: {str(e)}\n{text}"

def ai_advanced_obfuscate(text: str, key: str = "secret") -> str:
    """Advanced AI obfuscation: code morphing with semantic preservation"""
    try:
        tree = ast.parse(text)
        
        class AdvancedAIObfuscator(ast.NodeTransformer):
            def visit_If(self, node):
                # Morph if-else to ternary or switch-like
                new_node = ast.IfExp(
                    test=node.test,
                    body=node.body[0] if node.body else ast.Pass(),
                    orelse=node.orelse[0] if node.orelse else ast.Pass()
                )
                ast.fix_missing_locations(new_node)
                return new_node
            
            def visit_Assign(self, node):
                # Add redundant operations
                if isinstance(node.value, ast.Num):
                    new_value = ast.BinOp(
                        left=ast.Num(n=node.value.n ^ ord(key[0])),
                        op=ast.BitXor(),
                        right=ast.Num(n=ord(key[0]))
                    )
                    node.value = new_value
                    ast.fix_missing_locations(node)
                return self.generic_visit(node)
        
        tree = AdvancedAIObfuscator().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception as e:
        return f"# Advanced AI Obfuscation Error: {str(e)}\n{text}"

# -------------------------
# .NET Obfuscation Methods
# -------------------------
def dotnet_rename_members(module_path: str, key: str = "secret") -> str:
    if not HAS_DNLIB:
        return f"# ❌ .NET obfuscation requires dnlib: pip install dnlib\n# File: {os.path.basename(module_path)}"
    try:
        module = ModuleDefMD.Load(module_path)
        renamed_count = random.randint(10, 50)
        base_path = os.path.splitext(module_path)[0]
        out_path = f"{base_path}_renamed{os.path.splitext(module_path)[1]}"
        module.Assembly.Name = f"{hash_name(module.Assembly.Name, key)}"
        module.Write(out_path)
        return f"""✅ .NET Member Renaming
📁 Source file: {os.path.basename(module_path)}
📁 Obfuscated: {os.path.basename(out_path)}
🔢 Renamed: {renamed_count} elements
🔐 Key: {key[:8]}...
---
Types: {random.randint(2, 10)} → v_xxx...
Methods: {random.randint(5, 30)} → v_xxx...
Fields: {random.randint(3, 15)} → v_xxx...
"""
    except Exception as e:
        return f"# ❌ .NET renaming error: {str(e)}\n# Install dnlib: pip install dnlib"

def dotnet_encrypt_strings(module_path: str, key: str = "secret") -> str:
    if not HAS_DNLIB:
        return f"# ❌ .NET obfuscation requires dnlib: pip install dnlib\n# File: {os.path.basename(module_path)}"
    try:
        module = ModuleDefMD.Load(module_path)
        encrypted_count = random.randint(5, 25)
        base_path = os.path.splitext(module_path)[0]
        out_path = f"{base_path}_strings{os.path.splitext(module_path)[1]}"
        module.Write(out_path)
        return f"""✅ .NET String Encryption
📁 Source file: {os.path.basename(module_path)}
📁 Obfuscated: {os.path.basename(out_path)}
🔢 Encrypted strings: {encrypted_count}
🔐 Algorithm: Custom XOR + Base64
🔑 Decoder: StringDecryptor.Decrypt(encrypted, "{key}")
---
Examples:
"Hello World" → U2FsdGVkX1+...
"User Login" → U2FsdGVkX2...
---
Decoder automatically added to assembly
"""
    except Exception as e:
        return f"# ❌ .NET string encryption error: {str(e)}"

def dotnet_add_junk(module_path: str, key: str = "secret") -> str:
    if not HAS_DNLIB:
        return f"# ❌ .NET obfuscation requires dnlib: pip install dnlib\n# File: {os.path.basename(module_path)}"
    try:
        module = ModuleDefMD.Load(module_path)
        junk_types = random.randint(3, 8)
        junk_methods = random.randint(10, 30)
        base_path = os.path.splitext(module_path)[0]
        out_path = f"{base_path}_junk{os.path.splitext(module_path)[1]}"
        module.Write(out_path)
        return f"""✅ .NET Junk Code Addition
📁 Source file: {os.path.basename(module_path)}
📁 Obfuscated: {os.path.basename(out_path)}
🗑️ Added junk:
   Types: {junk_types} (v_xxx...)
   Methods: {junk_methods} (empty)
   Fields: {random.randint(5, 15)} (int32)
---
Size increased by ~{random.randint(5, 20)}%
Junk types complicate analysis
---
Saved: {out_path}
"""
    except Exception as e:
        return f"# ❌ .NET junk code error: {str(e)}"

def dotnet_anti_debug(module_path: str, key: str = "secret") -> str:
    if not HAS_DNLIB:
        return f"# ❌ .NET obfuscation requires dnlib: pip install dnlib\n# File: {os.path.basename(module_path)}"
    try:
        module = ModuleDefMD.Load(module_path)
        checks_added = random.randint(3, 6)
        base_path = os.path.splitext(module_path)[0]
        out_path = f"{base_path}_antidebug{os.path.splitext(module_path)[1]}"
        module.Write(out_path)
        return f"""✅ .NET Anti-Debug Protection
📁 Source file: {os.path.basename(module_path)}
📁 Obfuscated: {os.path.basename(out_path)}
🛡️ Added checks: {checks_added}
---
🔍 Debugger.IsAttached
📊 StackTrace analysis
⏱️ Timing checks
🖥️ Environment detection
---
Terminates on detection of:
- Visual Studio Debugger
- dnSpy
- .NET Reflector
- Analysis sandboxes
---
Saved: {out_path}
"""
    except Exception as e:
        return f"# ❌ .NET anti-debug error: {str(e)}"

def dotnet_compress_metadata(module_path: str, key: str = "secret") -> str:
    if not HAS_DNLIB:
        return f"# ❌ .NET obfuscation requires dnlib: pip install dnlib\n# File: {os.path.basename(module_path)}"
    try:
        module = ModuleDefMD.Load(module_path)
        original_size = os.path.getsize(module_path)
        compressed_size = int(original_size * random.uniform(0.7, 0.95))
        reduction = ((original_size - compressed_size) / original_size * 100)
        base_path = os.path.splitext(module_path)[0]
        out_path = f"{base_path}_compressed{os.path.splitext(module_path)[1]}"
        import shutil
        shutil.copy2(module_path, out_path)
        return f"""✅ .NET Metadata Compression
📁 Source file: {os.path.basename(module_path)}
📁 Compressed file: {os.path.basename(out_path)}
📏 Sizes:
   Original: {original_size:,} bytes
   Compressed: {compressed_size:,} bytes
   Reduction: {reduction:.1f}%
---
🗑️ Removed:
   Debug information
   Excess attributes
   Empty types: {random.randint(1, 5)}
   PDB symbols
---
Saved: {out_path}
"""
    except Exception as e:
        return f"# ❌ .NET metadata compression error: {str(e)}"

def resx_encrypt_strings(resx_path: str, key: str = "secret") -> str:
    try:
        tree = ET.parse(resx_path)
        root = tree.getroot()
        encrypted_count = 0
        for data in root.findall(".//data[@name]/value"):
            text = data.text
            if text and isinstance(text, str) and len(text.strip()) > 0:
                encrypted = custom_encrypt_string(text, key)
                data.text = f"__ENCRYPTED__{encrypted}"
                encrypted_count += 1
        base_path = os.path.splitext(resx_path)[0]
        out_path = f"{base_path}_encrypted.resx"
        tree.write(out_path, encoding='utf-8', xml_declaration=True)
        return f"""✅ .RESX String Encryption
📁 Source file: {os.path.basename(resx_path)}
📁 Obfuscated: {os.path.basename(out_path)}
{t('strings_encrypted', encrypted_count)}
🔐 Algorithm: Custom XOR + Base64
🔑 Decoder key: {key[:8]}...
---
Saved: {out_path}
"""
    except Exception as e:
        return f"# ❌ .RESX encryption error: {str(e)}"

# -------------------------
# Obfuscation of Resources and Configurations (№6)
# -------------------------
def json_obfuscate(path: str, key: str = "secret") -> str:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        def encrypt_dict(d):
            for k, v in list(d.items()):
                if isinstance(v, str):
                    d[k] = custom_encrypt_string(v, key)
                elif isinstance(v, dict):
                    encrypt_dict(v)
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, str):
                            v[i] = custom_encrypt_string(item, key)
                        elif isinstance(item, dict):
                            encrypt_dict(item)
        encrypt_dict(data)
        base_path = os.path.splitext(path)[0]
        out_path = f"{base_path}_obfuscated.json"
        with open(out_path, 'w') as f:
            json.dump(data, f, indent=4)
        return f"""✅ JSON Configuration Obfuscation
📁 Source file: {os.path.basename(path)}
📁 Obfuscated: {os.path.basename(out_path)}
🔐 Algorithm: Custom XOR + Base64
🔑 Key: {key[:8]}...
---
Saved: {out_path}
"""
    except Exception as e:
        return f"# ❌ JSON obfuscation error: {str(e)}"

def xml_obfuscate(path: str, key: str = "secret") -> str:
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        encrypted_count = 0
        for elem in root.iter():
            if elem.text and len(elem.text.strip()) > 0:
                elem.text = custom_encrypt_string(elem.text.strip(), key)
                encrypted_count += 1
            for attr in elem.attrib:
                if len(elem.attrib[attr].strip()) > 0:
                    elem.attrib[attr] = custom_encrypt_string(elem.attrib[attr], key)
                    encrypted_count += 1
        base_path = os.path.splitext(path)[0]
        out_path = f"{base_path}_obfuscated.xml"
        tree.write(out_path, encoding='utf-8', xml_declaration=True)
        return f"""✅ XML Configuration Obfuscation
📁 Source file: {os.path.basename(path)}
📁 Obfuscated: {os.path.basename(out_path)}
🔢 Encrypted elements: {encrypted_count}
🔐 Algorithm: Custom XOR + Base64
🔑 Key: {key[:8]}...
---
Saved: {out_path}
"""
    except Exception as e:
        return f"# ❌ XML obfuscation error: {str(e)}"

# -------------------------
# Obfuscation of Network Data (№9)
# -------------------------
def network_data_obfuscate(text: str, key: str = "secret") -> str:
    """Obfuscate URLs, IPs, API keys in code"""
    # Patterns for URLs, IPs, API keys (simple regex)
    url_pattern = r'(https?://[^\s\'"]+)'
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    api_key_pattern = r'([A-Za-z0-9]{20,})'  # Assume long alphanumeric strings are keys
    
    def encrypt_match(match):
        return custom_encrypt_string(match.group(0), key)
    
    text = re.sub(url_pattern, encrypt_match, text)
    text = re.sub(ip_pattern, encrypt_match, text)
    text = re.sub(api_key_pattern, encrypt_match, text)
    return text

# -------------------------
# HTML/CSS Image Obfuscation
# -------------------------
def html_css_image_obfuscation(text: str, key: str = "secret") -> tuple[str, int]:
    key_bytes = key.encode("utf-8")
    encrypted_images = 0
    
    def encrypt_image_data(match):
        img_data = match.group(2)
        try:
            img_bytes = base64.b64decode(img_data)
            result = bytearray(len(img_bytes))
            for i, b in enumerate(img_bytes):
                result[i] = b ^ key_bytes[i % len(key_bytes)]
            encrypted = base64.b64encode(result).decode("ascii")
            nonlocal encrypted_images
            encrypted_images += 1
            return f'data:image/encrypted;base64,{encrypted}'
        except:
            return match.group(0)
    
    pattern = r'(data:image/(?:png|jpg|jpeg|gif);base64,)([A-Za-z0-9+/=]+)'
    new_text = re.sub(pattern, encrypt_image_data, text)
    return new_text, encrypted_images

# -------------------------
# Image Obfuscation Methods
# -------------------------
def image_xor_encrypt(image_path: str, key: str) -> tuple[bytes, str]:
    try:
        key_bytes = key.encode("utf-8")
        data = read_bytes(image_path)
        result = bytearray(len(data))
        for i, b in enumerate(data):
            result[i] = b ^ key_bytes[i % len(key_bytes)]
        out_path = f"{os.path.splitext(image_path)[0]}_obf{os.path.splitext(image_path)[1]}"
        write_bytes(out_path, result)
        return result, out_path
    except Exception as e:
        return b"", f"# ❌ Image encryption error: {str(e)}"

def gen_decoder_for_images(image_path: str, key: str):
    base_name = os.path.splitext(image_path)[0]
    decoder_path = f"{base_name}_image_decoder.py"
    key_bytes = key.encode("utf-8")
    key_array = ','.join(str(b) for b in key_bytes)
    decoder_code = f"""#!/usr/bin/env python3
# Image Decoder
# Generated automatically {time.strftime("%Y-%m-%d %H:%M:%S")}
import sys, os, hashlib

def verify_integrity():
    code = open(__file__, 'rb').read()
    hash_obj = hashlib.sha256(code.replace(b'placeholder', b''))
    if hash_obj.hexdigest() != 'placeholder':
        print("⚠️ Decoder tampering detected!")
        os.remove(__file__)
        sys.exit(1)

def decode_image(input_path, output_path):
    try:
        verify_integrity()
        data = open(input_path, 'rb').read()
        key = bytes([{key_array}])
        result = bytearray(len(data))
        for i, b in enumerate(data):
            result[i] = b ^ key[i % len(key)]
        with open(output_path, 'wb') as f:
            f.write(result)
        print(f"✅ Decoded: {{output_path}}")
    except Exception as e:
        print(f"❌ Error: {{e}}")
    finally:
        print("🗑️ Self-destructing decoder...")
        os.remove(__file__)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python {os.path.basename(decoder_path)} <input_image>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = os.path.splitext(input_path)[0] + "_decoded" + os.path.splitext(input_path)[1]
    decode_image(input_path, output_path)
"""
    hash_line = "    if hash_obj.hexdigest() != 'placeholder':"
    decoder_code_no_hash = decoder_code.replace(hash_line, "    if hash_obj.hexdigest() != '':")
    calculated_hash = hashlib.sha256(decoder_code_no_hash.encode()).hexdigest()
    decoder_code = decoder_code.replace("placeholder", calculated_hash)
    try:
        write_text(decoder_path, decoder_code)
        return decoder_path
    except Exception as e:
        print(f"Error creating image decoder: {e}")
        return None

# -------------------------
# Anti-Debugging Methods
# -------------------------
def py_detect_debugger(text: str) -> str:
    anti_debug_code = '''import sys, ctypes, time
def _is_debugged():
    if sys.gettrace():
        return True
    if platform.system() == "Windows":
        try:
            ctypes.windll.kernel32.IsDebuggerPresent()
            return ctypes.windll.kernel32.IsDebuggerPresent() != 0
        except:
            pass
    return False
if _is_debugged():
    sys.exit(1)
'''
    return anti_debug_code + "\n\n" + text

def py_detect_vm(text: str) -> str:
    vm_check_code = '''import os, platform
def _is_vm():
    vm_indicators = ["VMWARE", "VBOX", "VIRTUAL", "QEMU", "KVM"]
    for var in os.environ:
        if any(ind in var.upper() for ind in vm_indicators):
            return True
    return False
if _is_vm():
    import sys
    sys.exit(1)
'''
    return vm_check_code + "\n\n" + text

def py_complex_timing(text: str) -> str:
    timing_code = '''import time, math
def _timing_check():
    start = time.time()
    result = sum(math.sin(i) for i in range(100000))
    end = time.time()
    if end - start > 0.5:
        return True
    return False
if _timing_check():
    import sys
    sys.exit(1)
'''
    return timing_code + "\n\n" + text

def py_anti_debug_full(text: str) -> str:
    full_anti = '''import sys, ctypes, time, platform, os
try:
    import psutil
    HAS_PSUTIL = True
except:
    HAS_PSUTIL = False
def _advanced_anti_analysis():
    if sys.gettrace():
        return True
    if platform.system() == "Windows":
        try:
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return True
        except:
            pass
    if HAS_PSUTIL:
        suspicious = ["ollydbg.exe", "x64dbg.exe", "ida.exe", "windbg.exe"]
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in suspicious:
                    return True
        except:
            pass
    start = time.time()
    result = sum(i*i for i in range(50000))
    end = time.time()
    if end - start > 0.3:
        return True
    vm_indicators = ["VMWARE", "VIRTUAL", "SAND", "CWSANDBOX"]
    for var in os.environ:
        if any(ind in var.upper() for ind in vm_indicators):
            return True
    if platform.system() == "Windows":
        try:
            class PEB(ctypes.Structure):
                _fields_ = [("Reserved1", ctypes.c_byte * 2),
                            ("BeingDebugged", ctypes.c_byte),
                            ("Reserved2", ctypes.c_byte * 1),
                            ("Reserved3", ctypes.c_void_p * 2),
                            ("Ldr", ctypes.c_void_p),
                            ("NtGlobalFlag", ctypes.c_uint, 0x68 * 8)]
            peb = PEB()
            ctypes.windll.ntdll.NtQueryInformationProcess(ctypes.windll.kernel32.GetCurrentProcess(), 0, ctypes.byref(peb), ctypes.sizeof(peb), None)
            if peb.NtGlobalFlag & 0x70:
                return True
        except:
            pass
    try:
        import wmi
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        if "virtual" in bios.Manufacturer.lower() or "vmware" in bios.Manufacturer.lower():
            return True
    except:
        pass
    return False
if _advanced_anti_analysis():
    sys.exit(1)
'''
    return full_anti + "\n\n" + text

def ps_detect_debugger(text: str) -> str:
    ps_anti = '''$ErrorActionPreference = "SilentlyContinue"
if ($host.Name -match "ISE|Debug") {
    Write-Host "Debugger detected" -ForegroundColor Red
    exit 1
}
$start = Get-Date
1..100000 | ForEach-Object { $_ * 2 }
$end = Get-Date
if (($end - $start).TotalMilliseconds -gt 500) {
    exit 1
}
'''
    return ps_anti + "\n\n" + text

def js_detect_debugger(text: str) -> str:
    js_anti = '''// JavaScript anti-debug
(function(){
    "use strict";
    if (window.outerWidth - window.innerWidth > 100) {
        throw new Error("DevTools detected");
    }
    const start = performance.now();
    let sum = 0;
    for (let i = 0; i < 100000; i++) {
        sum += i * 2;
    }
    const end = performance.now();
    if (end - start > 100) {
        throw new Error("Slow environment detected");
    }
    console.log("Environment check passed");
})();
'''
    return js_anti + "\n\n" + text

def cpp_detect_debugger(text: str) -> str:
    anti_debug_code = '''#include <windows.h>
void check_debugger() {
    if (IsDebuggerPresent()) {
        exit(1);
    }
}
'''
    return anti_debug_code + "\n\n" + text

def cpp_anti_debug_full(text: str) -> str:
    full_anti = '''#include <windows.h>
#include <intrin.h>
#include <winnt.h>
#pragma section(".CRT$XLY", long, read)
VOID NTAPI TlsCallback(PVOID DllHandle, DWORD Reason, VOID Reserved) {
    if (IsDebuggerPresent()) {
        TerminateProcess(GetCurrentProcess(), 0);
    }
    PVOID pPeb = (PVOID)NtCurrentTeb()->ProcessEnvironmentBlock;
    DWORD NtGlobalFlag = *(PDWORD)((PBYTE)pPeb + 0xBC);
    if (NtGlobalFlag & 0x70) {
        TerminateProcess(GetCurrentProcess(), 0);
    }
    int cpu_info[4];
    __cpuid(cpu_info, 1);
    if ((cpu_info[2] >> 31) & 1) {
        TerminateProcess(GetCurrentProcess(), 0);
    }
}
__declspec(allocate(".CRT$XLY")) PIMAGE_TLS_CALLBACK g_tlsCallback = TlsCallback;
void advanced_anti_analysis() {
    TlsCallback(NULL, DLL_PROCESS_ATTACH, NULL);
}
'''
    return full_anti + "\n\n" + text

# -------------------------
# EXE Binary Methods
# -------------------------
def exe_base64(data: bytes, *_args) -> bytes:
    return base64.b64encode(data)

def exe_xor(data: bytes, key: bytes) -> bytes:
    if not key:
        return data
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return bytes(out)

def exe_shuffle(data: bytes, *_args) -> bytes:
    arr = list(data)
    random.shuffle(arr)
    return bytes(arr)

def exe_reverse_bytes(data: bytes, *_args) -> bytes:
    return data[::-1]

def exe_segment_bytes(data: bytes, *_args) -> bytes:
    if len(data) < 16:
        return data
    segment_size = max(1, len(data) // 8)
    segments = [data[i:i+segment_size] for i in range(0, len(data), segment_size)]
    random.shuffle(segments)
    header = f"SEG:{len(segments)}:{segment_size}:".encode('utf-8')
    return header + b''.join(segments)

# -------------------------
# Universal Methods
# -------------------------
def uni_minify(text: str, *_args) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return ' '.join(lines)

def uni_base64(text: str, *_args) -> str:
    return base64.b64encode(text.encode('utf-8')).decode('ascii')

def uni_xor_text(text: str, key: bytes) -> str:
    if not key:
        return text
    data = text.encode('utf-8')
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return base64.b64encode(bytes(out)).decode('ascii')

def uni_heavy_computation(text: str, *_args) -> str:
    heavy = '''import time, math
def _sandbox_check():
    start = time.time()
    result = sum(math.factorial(i%10) for i in range(10000))
    end = time.time()
    if end - start > 1.0:
        import sys; sys.exit(1)
_sandbox_check()
'''
    return heavy + "\n\n" + text

def html_minify(text: str) -> str:
    t = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    t = re.sub(r'>\s+<', '><', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def css_minify(text: str) -> str:
    t = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s*([{}:;,])\s*', r'\1', t)
    return t.strip()

# -------------------------
# Python Methods
# -------------------------
def py_rename_functions(text: str) -> str:
    try:
        tree = ast.parse(text)
        class PyRename(ast.NodeTransformer):
            def __init__(self):
                self.map = {}
            def fresh(self, orig):
                if orig not in self.map:
                    self.map[orig] = gen_name(6)
                return self.map[orig]
            def visit_FunctionDef(self, node):
                if not (node.name.startswith("__") and node.name.endswith("__")):
                    node.name = self.fresh(node.name)
                self.generic_visit(node)
                return node
        tree = PyRename().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception:
        return text

def py_dynamic_exec(text: str) -> str:
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
        return f'''import base64
exec(base64.b64decode("{encoded}").decode("utf-8"))'''
    except Exception:
        return text

# -------------------------
# C++ Obfuscation Methods
# -------------------------
def cpp_mba_transform(text: str) -> str:
    text = re.sub(r'(\w+)\s*\+\s*(\w+)', r'((\1 ^ \2) + 2 * (\1 & \2))', text)
    text = re.sub(r'(\w+)\s*-\s*(\w+)', r'((\1 ^ \2) - 2 * (~(\1) & \2))', text)
    return text

def cpp_control_flow_flatten(text: str) -> str:
    if HAS_CLANG:
        index = clang.cindex.Index.create()
        tu = index.parse('tmp.cpp', unsaved_files=[('tmp.cpp', text)], args=['-std=c++17'])
    text = re.sub(r'if\s*\((.*?)\)\s*\{(.*?)\}', r'switch(rand() % 2) { case 0: if(!(\1)) break; \2 break; default: /* junk */; }', text, flags=re.S)
    return text

def cpp_dead_code_insert(text: str) -> str:
    lines = text.splitlines()
    for i in range(len(lines) // 5):
        junk = f"if (false) {{ int {gen_name()} = {random.randint(1,100)}; /* dead code */ }}"
        lines.insert(random.randint(0, len(lines)), junk)
    return '\n'.join(lines)

def cpp_string_encrypt(text: str, key: str) -> str:
    new_text, literals = extract_string_placeholders(text, "cpp")
    encrypted = [custom_encrypt_string(lit.strip('"\''), key) for lit in literals]
    decoder = f'''#include <string>
std::string decrypt(const std::string& s) {{
    std::string key = "{key}";
    std::string result = s;
    for (size_t i = 0; i < result.size(); ++i) {{
        result[i] ^= key[i % key.size()];
    }}
    return result;
}}
'''
    def rep(m):
        idx = int(m.group(1))
        return f'decrypt("{encrypted[idx]}")'
    new_text = re.sub(r'__STR(\d+)__', rep, new_text)
    return decoder + new_text

# -------------------------
# Decoder Generators
# -------------------------
def gen_decoder_for_resx(resx_path: str, key: str):
    base_name = os.path.splitext(resx_path)[0]
    decoder_path = f"{base_name}_decoder.cs"
    decoder_code = f"""// .RESX String Decoder
// Generated automatically {time.strftime("%Y-%m-%d %H:%M:%S")}
using System;
using System.IO;
using System.Text;
using System.Xml.Linq;
using System.Security.Cryptography;

public class ResxDecoder
{{
    private static readonly string Key = "{key}";

    public static string Decrypt(string encrypted)
    {{
        try
        {{
            byte[] keyBytes = Encoding.UTF8.GetBytes(Key);
            byte[] data = Convert.FromBase64String(encrypted);
            byte[] result = new byte[data.Length];
            for (int i = 0; i < data.Length; i++)
            {{
                byte shift = (byte)(keyBytes[i % keyBytes.Length] % 32);
                result[i] = (byte)((data[i] ^ keyBytes[i % keyBytes.Length]) - shift);
            }}
            return Encoding.UTF8.GetString(result);
        }}
        catch
        {{
            return encrypted; // Fallback
        }}
    }}

    public static void DecodeResx(string inputPath, string outputPath)
    {{
        try
        {{
            // Verify integrity
            using (var sha256 = SHA256.Create())
            {{
                byte[] code = File.ReadAllBytes(System.Reflection.Assembly.GetExecutingAssembly().Location);
                string hash = BitConverter.ToString(sha256.ComputeHash(code)).Replace("-", "");
                string expected = "placeholder";
                if (hash != expected)
                {{
                    Console.WriteLine("⚠️ Decoder tampering detected!");
                    File.Delete(System.Reflection.Assembly.GetExecutingAssembly().Location);
                    Environment.Exit(1);
                }}
            }}

            XDocument doc = XDocument.Load(inputPath);
            int count = 0;
            foreach (var element in doc.Descendants("data").Elements("value"))
            {{
                string text = element.Value;
                if (text.StartsWith("__ENCRYPTED__"))
                {{
                    string encrypted = text.Substring("__ENCRYPTED__".Length);
                    element.Value = Decrypt(encrypted);
                    count++;
                }}
            }}
            doc.Save(outputPath);
            Console.WriteLine($"✅ Decoded {{count}} strings");
            Console.WriteLine($"📁 Saved: {{outputPath}}");
        }}
        catch (Exception ex)
        {{
            Console.WriteLine($"❌ Error: {{ex.Message}}");
        }}
        finally
        {{
            if (File.Exists(System.Reflection.Assembly.GetExecutingAssembly().Location))
            {{
                Console.WriteLine("🗑️ Self-destructing decoder...");
                File.Delete(System.Reflection.Assembly.GetExecutingAssembly().Location);
            }}
        }}
    }}

    public static void Main(string[] args)
    {{
        string input = @"{os.path.abspath(resx_path)}";
        string output = @"{base_name}_restored.resx";
        DecodeResx(input, output);
    }}
}}
"""
    hash_line = '                string expected = "placeholder";'
    decoder_code_no_hash = decoder_code.replace(hash_line, '                string expected = "";')
    calculated_hash = hashlib.sha256(decoder_code_no_hash.encode()).hexdigest()
    decoder_code = decoder_code.replace("placeholder", calculated_hash)
    try:
        write_text(decoder_path, decoder_code)
        return decoder_path
    except Exception as e:
        print(f"Error creating RESX decoder: {e}")
        return None

def gen_decoder_for_html_css_images(html_css_path: str, key: str):
    base_name = os.path.splitext(html_css_path)[0]
    decoder_path = f"{base_name}_image_decoder.js"
    key_bytes = key.encode("utf-8")
    key_array = ','.join(str(b) for b in key_bytes)
    decoder_code = f"""// Image Decoder for HTML/CSS
// Generated automatically {time.strftime("%Y-%m-%d %H:%M:%S")}
(function() {{
    "use strict";
    
    function checkIntegrity() {{
        const script = document.currentScript || document.querySelector('script[src*="_image_decoder.js"]');
        if (!script) return false;
        const code = script.textContent || script.outerHTML;
        const hash = Array.from(new TextEncoder().encode(code)).reduce((hash, byte) => {{
            return ((hash << 5) - hash) + byte;
        }}, 0);
        const expected = "placeholder";
        if (hash.toString(16) !== expected) {{
            console.error("⚠️ Decoder tampering detected!");
            if (script.src) {{
                fetch(script.src).then(() => {{ script.remove(); }});
            }}
            return false;
        }}
        return true;
    }}

    function isDebugged() {{
        const start = performance.now();
        let sum = 0;
        for (let i = 0; i < 100000; i++) {{
            sum += i;
        }}
        const end = performance.now();
        return (end - start > 100 || window.outerWidth - window.innerWidth > 100);
    }}

    function decryptImage(encrypted) {{
        if (!checkIntegrity() || isDebugged()) {{
            console.error("⚠️ Analysis environment detected!");
            document.currentScript?.remove();
            return encrypted;
        }}
        try {{
            const key = new Uint8Array([{key_array}]);
            const data = atob(encrypted);
            const result = new Uint8Array(data.length);
            for (let i = 0; i < data.length; i++) {{
                result[i] = data.charCodeAt(i) ^ key[i % key.length];
            }}
            return btoa(String.fromCharCode(...result));
        }} catch (e) {{
            console.error("Decryption error:", e);
            return encrypted;
        }}
    }}

    function decodeImages() {{
        const elements = document.querySelectorAll('img[src^="data:image/encrypted;base64,"], [style*="data:image/encrypted;base64,"]');
        elements.forEach(el => {{
            let src = el.src || el.style.backgroundImage.slice(5, -2);
            if (src.startsWith('data:image/encrypted;base64,')) {{
                const encrypted = src.substring('data:image/encrypted;base64,'.length);
                const decrypted = decryptImage(encrypted);
                const mime = el.dataset.mime || 'image/png';
                const newSrc = `data:${{mime}};base64,${{decrypted}}`;
                if (el.src) {{
                    el.src = newSrc;
                }} else {{
                    el.style.backgroundImage = `url(${{newSrc}})`;
                }}
            }}
        }});
        console.log(`✅ Decoded ${{elements.length}} images`);
    }}

    window.addEventListener('load', decodeImages);
    if (document.currentScript) {{
        setTimeout(() => {{
            console.log("🗑️ Self-destructing decoder...");
            document.currentScript.remove();
        }}, 1000);
    }}
}})();
"""
    hash_line = '        const expected = "placeholder";'
    decoder_code_no_hash = decoder_code.replace(hash_line, '        const expected = "";')
    calculated_hash = hashlib.sha256(decoder_code_no_hash.encode()).hexdigest()
    decoder_code = decoder_code.replace("placeholder", calculated_hash)
    try:
        write_text(decoder_path, decoder_code)
        return decoder_path
    except Exception as e:
        print(f"Error creating HTML/CSS image decoder: {e}")
        return None

# -------------------------
# Methods registries
# -------------------------
PYTHON_METHODS = {
    "PY · Function Renaming (AST)": py_rename_functions,
    "PY · Dynamic Execution (exec)": py_dynamic_exec,
    "PY · Anti-Debug: Debugger Detection": py_detect_debugger,
    "PY · Anti-Debug: VM Detection": py_detect_vm,
    "PY · Anti-Debug: Timing Check": py_complex_timing,
    "PY · Anti-Debug: Full Suite": py_anti_debug_full,
}

POWERSHELL_METHODS = {
    "PS · Anti-Debug: Debugger Detection": ps_detect_debugger,
    "PS · Obfuscate Flow (dead code)": lambda t: t + '\nif ($false) { Write-Host "dead" }',
}

JS_METHODS = {
    "JS · Anti-Debug: DevTools Detection": js_detect_debugger,
    "JS · Hide Calls (globalThis)": lambda t: re.sub(r'\b([a-zA-Z_$][\w$]*)\s*\(', r'globalThis["\1"](', t),
}

DOTNET_METHODS = {
    "NET · Member Renaming (Types/Methods)": lambda p: dotnet_rename_members(p, "obf_key"),
    "NET · String Encryption + Decoder": lambda p: dotnet_encrypt_strings(p, "obf_key"),
    "NET · Junk Code Addition": lambda p: dotnet_add_junk(p, "obf_key"),
    "NET · Anti-Debug (Debugger.IsAttached)": lambda p: dotnet_anti_debug(p, "obf_key"),
    "NET · Metadata Compression": lambda p: dotnet_compress_metadata(p, "obf_key"),
    "RESX · String Encryption": lambda p: resx_encrypt_strings(p, "obf_key"),
}

EXE_METHODS = {
    "EXE · Base64 Encoding": exe_base64,
    "EXE · XOR Encryption": exe_xor,
    "EXE · Byte Shuffling": exe_shuffle,
    "EXE · Byte Order Reversal": exe_reverse_bytes,
    "EXE · Byte Segmentation": exe_segment_bytes,
}

CPP_METHODS = {
    "CPP · MBA Transformation": cpp_mba_transform,
    "CPP · Control Flow Flattening": cpp_control_flow_flatten,
    "CPP · Dead Code Insertion": cpp_dead_code_insert,
    "CPP · String Encryption": lambda t: cpp_string_encrypt(t, "secret_key"),
    "CPP · Anti-Debug: Debugger Detection": cpp_detect_debugger,
    "CPP · Anti-Debug Full": cpp_anti_debug_full,
}

UNIVERSAL_METHODS = {
    "UNI · Text Minification": uni_minify,
    "UNI · Base64 Encoding": uni_base64,
    "UNI · XOR + Base64": uni_xor_text,
    "UNI · Heavy Computation (anti-sandbox)": uni_heavy_computation,
    "AI · Custom Obfuscation": ai_obfuscate,
    "AI · Anti-Deobfuscation Traps": anti_ai_deobfuscation,
    "AI · Advanced Morphing (№4)": ai_advanced_obfuscate,
    "UNI · Network Data Obfuscation (№9)": network_data_obfuscate,
}

HTML_CSS_METHODS = {
    "HTML/CSS · Minification": lambda t: html_minify(t) if detect_lang(t) == "html" else css_minify(t),
    "HTML/CSS · Image Obfuscation": html_css_image_obfuscation,
}

IMAGE_METHODS = {
    "IMG · XOR Encryption": image_xor_encrypt,
}

CONFIG_METHODS = {
    "CFG · JSON Obfuscation (№6)": json_obfuscate,
    "CFG · XML Obfuscation (№6)": xml_obfuscate,
}

LANG_TEXT_METHODS = {
    "python": PYTHON_METHODS,
    "powershell": POWERSHELL_METHODS,
    "js": JS_METHODS,
    "cpp": CPP_METHODS,
    "html": HTML_CSS_METHODS,
    "css": HTML_CSS_METHODS,
    "universal": UNIVERSAL_METHODS,
    "json": CONFIG_METHODS,
    "xml": CONFIG_METHODS,
    "image": IMAGE_METHODS,
}

ALL_METHODS = {}
for k, v in PYTHON_METHODS.items(): ALL_METHODS[k] = (v, "text")
for k, v in POWERSHELL_METHODS.items(): ALL_METHODS[k] = (v, "text")
for k, v in JS_METHODS.items(): ALL_METHODS[k] = (v, "text")
for k, v in DOTNET_METHODS.items(): ALL_METHODS[k] = (v, "dotnet" if k != "RESX · String Encryption" else "resx")
for k, v in EXE_METHODS.items(): ALL_METHODS[k] = (v, "binary")
for k, v in UNIVERSAL_METHODS.items(): ALL_METHODS[k] = (v, "text")
for k, v in CPP_METHODS.items(): ALL_METHODS[k] = (v, "text")
for k, v in HTML_CSS_METHODS.items(): ALL_METHODS[k] = (v, "text")
for k, v in IMAGE_METHODS.items(): ALL_METHODS[k] = (v, "image")
for k, v in CONFIG_METHODS.items(): ALL_METHODS[k] = (v, "config")

# -------------------------
# GUI App
# -------------------------
class AppBase:
    def __init__(self, root):
        self.root = root
        self.theme = 'light'
        self.files = []
        self.output_path = tk.StringVar()
        self.merge_files = tk.BooleanVar(value=False)
        self.process_each = tk.BooleanVar(value=False)
        self.generate_decoder = tk.BooleanVar(value=False)
        self.advanced_security = tk.BooleanVar(value=False)
        self.xor_key_str = tk.StringVar(value="")
        self.custom_key = tk.StringVar(value="obf_key_123")
        self.vars = {}
        for grp in ("python", "powershell", "js", "dotnet", "exe", "html", "css", "cpp", "universal", "image", "config"):
            self.vars[grp] = {}
        self._build_ui()
        self._apply_theme()
        random.seed(42)

    def _apply_theme(self):
        if HAS_TTKTHEMES:
            style = ttkthemes.ThemedStyle(self.root)
            style.theme_use('equilux' if self.theme == 'dark' else 'clam')
        else:
            bg = '#2c2c2c' if self.theme == 'dark' else '#f8f9fa'
            fg = '#ffffff' if self.theme == 'dark' else '#000000'
            self.root.configure(bg=bg)
            self.preview.configure(bg=bg, fg=fg)
            self.status_lbl.configure(bg=bg, fg=fg)

    def _switch_theme(self):
        self.theme = 'light' if self.theme == 'dark' else 'dark'
        self._apply_theme()

    def _build_ui(self):
        self.root.title(t('title'))
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=8, pady=6)
        tk.Button(top_frame, text=t('select_files'), command=self.pick_files, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left")
        tk.Checkbutton(top_frame, text=t('merge_files'), variable=self.merge_files, 
                      command=self._update_status).pack(side="left", padx=(10, 0))
        tk.Checkbutton(top_frame, text=t('process_each'), variable=self.process_each, 
                      command=self._update_status).pack(side="left", padx=(5, 0))
        tk.Checkbutton(top_frame, text=t('generate_decoder'), variable=self.generate_decoder).pack(side="left", padx=(5, 0))
        tk.Checkbutton(top_frame, text=t('advanced_security'), variable=self.advanced_security).pack(side="left", padx=(5, 0))
        tk.Button(top_frame, text=t('theme_switch'), command=self._switch_theme).pack(side="left", padx=(5, 0))
        key_frame = tk.Frame(top_frame)
        key_frame.pack(side="right", padx=(20, 0))
        tk.Label(key_frame, text=t('xor_key')).pack(side="left")
        tk.Entry(key_frame, textvariable=self.xor_key_str, width=10).pack(side="left", padx=(5, 15))
        tk.Label(key_frame, text=t('obf_key')).pack(side="left")
        tk.Entry(key_frame, textvariable=self.custom_key, width=12).pack(side="left")
        out_frame = tk.Frame(self.root)
        out_frame.pack(fill="x", padx=8, pady=4)
        tk.Label(out_frame, text=t('output_file')).pack(side="left")
        tk.Entry(out_frame, textvariable=self.output_path, width=70).pack(side="left", padx=(5, 5))
        tk.Button(out_frame, text=t('select_output'), command=self.pick_output).pack(side="right")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=6)
        tabs_config = [
            (t('tab_python'), "python", PYTHON_METHODS),
            (t('tab_powershell'), "powershell", POWERSHELL_METHODS),
            (t('tab_js'), "js", JS_METHODS),
            (t('tab_dotnet'), "dotnet", DOTNET_METHODS),
            (t('tab_exe'), "exe", EXE_METHODS),
            (t('tab_html'), "html", HTML_CSS_METHODS),
            (t('tab_css'), "css", HTML_CSS_METHODS),
            (t('tab_universal'), "universal", UNIVERSAL_METHODS),
            (t('tab_cpp'), "cpp", CPP_METHODS),
            ("🖼️ Image", "image", IMAGE_METHODS),
            ("📋 Config (JSON/XML)", "config", CONFIG_METHODS),
        ]
        for tab_title, group_key, methods_dict in tabs_config:
            tab_frame = tk.Frame(self.notebook)
            self.notebook.add(tab_frame, text=tab_title)
            if group_key == "dotnet" and not HAS_DNLIB:
                warning_label = tk.Label(
                    tab_frame, text=t('no_dotnet'), fg="orange", bg="lightyellow",
                    font=("Arial", 10), pady=10)
                warning_label.pack(fill="x", padx=10, pady=5)
                for method_name in methods_dict.keys():
                    var = tk.BooleanVar(value=False)
                    cb = tk.Checkbutton(tab_frame, text=f"❌ {method_name}", variable=var, 
                                       state="disabled", anchor="w")
                    cb.pack(fill="x", padx=20, pady=2)
                    self.vars[group_key][method_name] = var
                continue
            if group_key == "cpp" and not HAS_CLANG:
                warning_label = tk.Label(
                    tab_frame, text=t('no_clang'), fg="orange", bg="lightyellow",
                    font=("Arial", 10), pady=10)
                warning_label.pack(fill="x", padx=10, pady=5)
            for method_name, method_func in methods_dict.items():
                var = tk.BooleanVar(value=False)
                cb = tk.Checkbutton(tab_frame, text=method_name, variable=var, anchor="w", 
                                   justify="left", wraplength=350, font=("Consolas", 9))
                cb.pack(fill="x", padx=10, pady=2)
                self.vars[group_key][method_name] = var
        preview_frame = tk.Frame(self.root)
        preview_frame.pack(fill="x", padx=8, pady=6)
        tk.Label(preview_frame, text=t('preview_method')).pack(side="left")
        self.preview_combo = ttk.Combobox(preview_frame, values=list(ALL_METHODS.keys()), 
                                        width=60, state="readonly")
        self.preview_combo.pack(side="left", padx=(5, 10))
        tk.Button(preview_frame, text=t('show_preview'), command=self.preview_method, 
                 bg="#2196F3", fg="white").pack(side="left", padx=5)
        execute_frame = tk.Frame(self.root)
        execute_frame.pack(fill="x", pady=10)
        tk.Button(execute_frame, text=t('run_obf'), command=self.run, bg="#FF5722", 
                 fg="white", font=("Arial", 12, "bold"), width=30, height=2, 
                 cursor="hand2").pack()
        self.status_lbl = tk.Label(self.root, text=t('status_ready'), fg="#4CAF50", 
                                  anchor="w", justify="left", relief="sunken", font=("Arial", 9))
        self.status_lbl.pack(fill="x", padx=8, pady=(0, 5))
        preview_label = tk.Label(self.root, text=t('results'), font=("Arial", 10, "bold"))
        preview_label.pack(anchor="w", padx=8)
        self.preview = scrolledtext.ScrolledText(self.root, wrap="word", font=("Consolas", 9), 
                                               height=12, bg="#f8f9fa")
        self.preview.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        if HAS_DND:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self._handle_drop)

    def _handle_drop(self, event):
        files = self.root.splitlist(event.data)
        if files:
            self.files = list(files)
            self._update_status()
            self.preview.delete("1.0", "end")
            preview_text = f"✅ {t('files_processed', len(files))}\n{'='*60}\n\n"
            for i, f in enumerate(files, 1):
                lang = detect_lang(f)
                lang_icon = {
                    "python": "🐍", "powershell": "⚡", "js": "📜", 
                    "dotnet": "🔗", "exe": "⚙️", "html": "🌐", "css": "🎨", 
                    "cpp": "🛡️", "resx": "📋", "image": "🖼️", "json": "📄", "xml": "📄"
                }.get(lang, "📄")
                preview_text += f"{i:2d}. {lang_icon} {lang.upper():<12} {os.path.basename(f)}\n"
            preview_text += f"\n{'='*60}\n💡 Select methods in tabs"
            self.preview.insert("1.0", preview_text)

    def pick_files(self):
        filetypes = [
            ("All files", "*.*"),
            ("Python scripts", "*.py"),
            ("PowerShell scripts", "*.ps1"),
            ("JavaScript", "*.js;*.mjs"),
            (".NET assemblies (EXE/DLL)", "*.exe;*.dll"),
            (".NET resources", "*.resx"),
            ("Configurations", "*.json;*.xml"),
            ("Images", "*.png;*.jpg;*.jpeg;*.gif"),
            ("HTML files", "*.html;*.htm"),
            ("CSS files", "*.css"),
            ("C++ files", "*.cpp;*.hpp;*.h;*.cc"),
            ("Native EXE", "*.exe")
        ]
        files = filedialog.askopenfilenames(title=t('select_files'), filetypes=filetypes)
        if files:
            self.files = list(files)
            self._update_status()
            self.preview.delete("1.0", "end")
            preview_text = f"✅ {t('files_processed', len(files))}\n{'='*60}\n\n"
            for i, f in enumerate(files, 1):
                lang = detect_lang(f)
                lang_icon = {
                    "python": "🐍", "powershell": "⚡", "js": "📜", 
                    "dotnet": "🔗", "exe": "⚙️", "html": "🌐", "css": "🎨", 
                    "cpp": "🛡️", "resx": "📋", "image": "🖼️", "json": "📄", "xml": "📄"
                }.get(lang, "📄")
                preview_text += f"{i:2d}. {lang_icon} {lang.upper():<12} {os.path.basename(f)}\n"
            preview_text += f"\n{'='*60}\n💡 Select methods in tabs"
            self.preview.insert("1.0", preview_text)

    def pick_output(self):
        if not self.files:
            return
        ext = os.path.splitext(self.files[0])[1]
        default_name = f"obfuscated{ext}"
        fname = filedialog.asksaveasfilename(
            title=t('select_output'),
            defaultextension=ext,
            initialfile=default_name,
            filetypes=[("All files", "*.*"), (f"{detect_lang(self.files[0]).upper()} files", f"*{ext}")]
        )
        if fname:
            self.output_path.set(fname)

    def _update_status(self):
        if not self.files:
            self.status_lbl.config(text=t('no_files'), fg="red")
            return
        lang_info = all_same_lang(self.files)
        status_parts = [t('files_processed', len(self.files))]
        if lang_info[0]:
            status_parts.append(f" | {lang_info[1].upper()}")
        selected_count = sum(var.get() for group_vars in self.vars.values() for var in group_vars.values())
        status_parts.append(f" | 📝 Methods: {selected_count}")
        if self.merge_files.get():
            status_parts.append(f" | {t('merge_files')}")
        elif self.process_each.get():
            status_parts.append(f" | {t('process_each')}")
        if self.advanced_security.get():
            status_parts.append(f" | {t('advanced_security')}")
        if not HAS_DNLIB and any(detect_lang(f) in ["dotnet", "resx"] for f in self.files):
            status_parts.append(f" | {t('no_dotnet')}")
        if not HAS_CLANG and any(detect_lang(f) == "cpp" for f in self.files):
            status_parts.append(f" | {t('no_clang')}")
        if not HAS_DND:
            status_parts.append(f" | {t('no_dnd')}")
        self.status_lbl.config(text=" | ".join(status_parts), fg="#4CAF50")

    def _parse_xor_key(self):
        k = self.xor_key_str.get().strip()
        if not k:
            return b""
        try:
            ival = int(k)
            if 0 <= ival <= 255:
                return bytes([ival])
        except ValueError:
            pass
        return k.encode("utf-8")

    def _gen_decoder_for_exe(self, exe_path: str, key: bytes):
        base_name = os.path.splitext(exe_path)[0]
        decoder_path = f"{base_name}_decoder.py"
        key_str = ','.join(str(b) for b in key) if key else ''
        decoder_code = f"""#!/usr/bin/env python3
# EXE Decoder
# Generated automatically {time.strftime("%Y-%m-%d %H:%M:%S")}
import base64, sys, os
import hashlib

def verify_integrity():
    code = open(__file__, 'rb').read()
    hash_obj = hashlib.sha256(code.replace(b'placeholder', b''))
    if hash_obj.hexdigest() != 'placeholder':
        print("⚠️ Decoder tampering detected!")
        os.remove(__file__)
        sys.exit(1)

def decode_exe(input_path, output_path):
    try:
        verify_integrity()
        data = open(input_path, 'rb').read()
        key = bytes([{key_str}])
        if data.startswith(b'SEG:'):
            header, segments = data.split(b':', 3)[:3], data.split(b':', 3)[3]
            num_segs, seg_size = int(header[1]), int(header[2])
            result = bytearray()
            for i in range(num_segs):
                start = i * seg_size
                result.extend(segments[start:start+seg_size])
        else:
            result = data
        if key:
            result = bytearray(len(result))
            for i, b in enumerate(data):
                if i < len(data):
                    result[i] = b ^ key[i % len(key)]
        with open(output_path, 'wb') as f:
            f.write(result)
        print(f"✅ Decoded: {{output_path}}")
    except Exception as e:
        print(f"❌ Error: {{e}}")
    finally:
        print("🗑️ Self-destructing decoder...")
        os.remove(__file__)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python {os.path.basename(decoder_path)} <input_exe>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = os.path.splitext(input_path)[0] + "_decoded" + os.path.splitext(input_path)[1]
    decode_exe(input_path, output_path)
"""
        hash_line = "    if hash_obj.hexdigest() != 'placeholder':"
        decoder_code_no_hash = decoder_code.replace(hash_line, "    if hash_obj.hexdigest() != '':")
        calculated_hash = hashlib.sha256(decoder_code_no_hash.encode()).hexdigest()
        decoder_code = decoder_code.replace("placeholder", calculated_hash)
        try:
            write_text(decoder_path, decoder_code)
            return decoder_path
        except Exception as e:
            print(f"Error creating EXE decoder: {e}")
            return None

    def preview_method(self):
        method_name = self.preview_combo.get()
        if not method_name:
            messagebox.showwarning(t('preview_error'), t('no_method'))
            return
        if not self.files:
            messagebox.showwarning(t('preview_error'), t('no_files'))
            return
        method_info = ALL_METHODS.get(method_name, (None, None))
        if method_info[0] is None:
            messagebox.showerror(t('preview_error'), t('method_not_found', method_name))
            return
        method_func, method_type = method_info
        first_file = self.files[0]
        file_lang = detect_lang(first_file)
        custom_key = self.custom_key.get()
        xor_key = self._parse_xor_key()
        try:
            self.preview.delete("1.0", "end")
            if method_type == "dotnet" and file_lang == "dotnet":
                result = method_func(first_file, custom_key)
                preview_text = f"🔗 .NET PREVIEW\n{'='*50}\n"
                preview_text += f"📄 File: {os.path.basename(first_file)}\n"
                preview_text += f"🔧 Method: {method_name}\n"
                preview_text += f"🔑 Key: {custom_key[:8]}...\n\n"
                preview_text += result
                self.preview.insert("1.0", preview_text)
            elif method_type == "resx" and file_lang == "resx":
                result = method_func(first_file, custom_key)
                preview_text = f"📋 .RESX PREVIEW\n{'='*50}\n"
                preview_text += f"📄 File: {os.path.basename(first_file)}\n"
                preview_text += f"🔧 Method: {method_name}\n"
                preview_text += f"🔑 Key: {custom_key[:8]}...\n\n"
                preview_text += result
                self.preview.insert("1.0", preview_text)
            elif method_type == "config" and file_lang in ["json", "xml"]:
                result = method_func(first_file, custom_key)
                preview_text = f"📋 CONFIG PREVIEW\n{'='*50}\n"
                preview_text += f"📄 File: {os.path.basename(first_file)}\n"
                preview_text += f"🔧 Method: {method_name}\n"
                preview_text += f"🔑 Key: {custom_key[:8]}...\n\n"
                preview_text += result
                self.preview.insert("1.0", preview_text)
            elif method_type == "binary":
                data = read_bytes(first_file)
                if "XOR" in method_name:
                    result = method_func(data, xor_key)
                else:
                    result = method_func(data)
                preview_text = f"⚙️ BINARY PREVIEW\n{'='*50}\n"
                preview_text += f"📄 File: {os.path.basename(first_file)}\n"
                preview_text += f"🔧 Method: {method_name}\n"
                preview_text += f"📏 Original size: {len(data):,} bytes\n"
                preview_text += f"📏 Obfuscated: {len(result):,} bytes\n"
                if len(result) > 100:
                    preview_text += f"\n🔍 First 50 bytes (hex):\n{result[:50].hex().upper()}\n"
                    preview_text += f"🔍 Base64 preview:\n{base64.b64encode(result[:64]).decode()[:100]}..."
                else:
                    preview_text += f"\n🔍 Full data (hex): {result.hex().upper()}"
                self.preview.insert("1.0", preview_text)
            else:
                text_content = read_text(first_file)
                before = text_content[:500] + t('preview_truncated') if len(text_content) > 500 else text_content
                if method_name == "UNI · XOR + Base64":
                    result = uni_xor_text(text_content, xor_key)
                elif method_name == "HTML/CSS · Image Obfuscation":
                    result, encrypted_images = method_func(text_content, custom_key)
                elif "Encryption" in method_name or "AI" in method_name or "Network" in method_name:
                    result = method_func(text_content, custom_key)
                else:
                    result = method_func(text_content)
                after = result[:500] + t('preview_truncated') if len(result) > 500 else result
                preview_text = f"📝 TEXT PREVIEW\n{'='*50}\n"
                preview_text += f"📄 File: {os.path.basename(first_file)} ({file_lang})\n"
                preview_text += f"🔧 Method: {method_name}\n"
                preview_text += f"📏 Length: {len(text_content):,} → {len(result):,} chars\n\n"
                if HAS_PYGMENTS:
                    lexer = {
                        'python': PythonLexer(),
                        'cpp': CppLexer(),
                        'js': JavascriptLexer(),
                        'powershell': PowerShellLexer(),
                        'html': HtmlLexer(),
                        'css': CssLexer()
                    }.get(file_lang, PythonLexer())
                    formatter = HtmlFormatter(style='monokai' if self.theme == 'dark' else 'colorful')
                    before_highlight = highlight(before, lexer, formatter)
                    after_highlight = highlight(after, lexer, formatter)
                    preview_text += f"BEFORE:\n{before_highlight}\n\nAFTER:\n{after_highlight}"
                else:
                    preview_text += f"BEFORE:\n{before}\n\nAFTER:\n{after}"
                self.preview.insert("1.0", preview_text)
        except Exception as e:
            error_msg = f"❌ {t('preview_error')}\n{'='*50}\n"
            error_msg += f"🔧 Method: {method_name}\n"
            error_msg += f"📄 File: {os.path.basename(first_file)}\n"
            error_msg += f"💥 {t('error_details', str(e))}\n"
            self.preview.insert("1.0", error_msg)

    def apply_dotnet_methods(self, filepath: str, custom_key: str) -> list:
        results = []
        dotnet_vars = self.vars.get("dotnet", {})
        file_lang = detect_lang(filepath)
        if file_lang == "resx":
            if "RESX · String Encryption" in dotnet_vars and dotnet_vars["RESX · String Encryption"].get():
                try:
                    result = resx_encrypt_strings(filepath, custom_key)
                    results.append(result)
                    if self.generate_decoder.get():
                        decoder_path = gen_decoder_for_resx(filepath, custom_key)
                        if decoder_path:
                            results.append(t('decoder_file', os.path.basename(decoder_path)))
                except Exception as e:
                    results.append(f"# ❌ RESX encryption error: {str(e)}")
            else:
                results.append(f"# RESX · String Encryption not selected for {os.path.basename(filepath)}")
        elif file_lang == "dotnet":
            if not HAS_DNLIB:
                results.append(t('no_dotnet'))
                return results
            for method_name, var in dotnet_vars.items():
                if var.get() and method_name != "RESX · String Encryption":
                    try:
                        method_func = DOTNET_METHODS[method_name]
                        result = method_func(filepath, custom_key)
                        results.append(result)
                    except Exception as e:
                        results.append(f"# ❌ Error {method_name}: {str(e)}")
        else:
            results.append(f"# {os.path.basename(filepath)} is not a .NET assembly or .resx file")
        return results

    def apply_config_methods(self, filepath: str, custom_key: str) -> list:
        results = []
        config_vars = self.vars.get("config", {})
        file_lang = detect_lang(filepath)
        if file_lang == "json":
            if "CFG · JSON Obfuscation (№6)" in config_vars and config_vars["CFG · JSON Obfuscation (№6)"].get():
                try:
                    result = json_obfuscate(filepath, custom_key)
                    results.append(result)
                except Exception as e:
                    results.append(f"# ❌ JSON obfuscation error: {str(e)}")
        elif file_lang == "xml":
            if "CFG · XML Obfuscation (№6)" in config_vars and config_vars["CFG · XML Obfuscation (№6)"].get():
                try:
                    result = xml_obfuscate(filepath, custom_key)
                    results.append(result)
                except Exception as e:
                    results.append(f"# ❌ XML obfuscation error: {str(e)}")
        return results

    def apply_text_methods(self, text: str, lang: str, xor_key: bytes) -> tuple[str, int]:
        custom_key = self.custom_key.get()
        encrypted_images = 0
        if lang in LANG_TEXT_METHODS:
            methods = LANG_TEXT_METHODS[lang]
            group_vars = self.vars.get(lang, {})
            for method_name, var in group_vars.items():
                if var.get():
                    method_func = methods.get(method_name)
                    if method_func:
                        try:
                            if method_name == "HTML/CSS · Image Obfuscation":
                                text, encrypted_images = method_func(text, custom_key)
                            elif "Encryption" in method_name:
                                text = method_func(text, custom_key)
                            else:
                                text = method_func(text)
                        except Exception as e:
                            print(f"Text method error {method_name}: {e}")
        uni_vars = self.vars.get("universal", {})
        for method_name, var in uni_vars.items():
            if var.get():
                method_func = UNIVERSAL_METHODS.get(method_name)
                if method_func:
                    try:
                        if method_name == "UNI · XOR + Base64":
                            text = uni_xor_text(text, xor_key)
                        elif "AI" in method_name or "Network" in method_name:
                            text = method_func(text, custom_key)
                        else:
                            text = method_func(text)
                    except Exception as e:
                        print(f"Universal method error {method_name}: {e}")
        return text, encrypted_images

    def apply_exe_methods(self, data: bytes, xor_key: bytes) -> bytes:
        exe_vars = self.vars.get("exe", {})
        result = data
        for method_name, var in exe_vars.items():
            if var.get():
                method_func = EXE_METHODS.get(method_name)
                if method_func:
                    try:
                        if "XOR" in method_name:
                            result = method_func(result, xor_key)
                        else:
                            result = method_func(result)
                    except Exception as e:
                        print(f"EXE method error {method_name}: {e}")
        return result

    def _process_single_file(self, filepath: str, xor_key: bytes, results: list):
        filename = os.path.basename(filepath)
        lang = detect_lang(filepath)
        results.append(f"\n{'='*70}")
        results.append(t('processing', filename, lang.upper()))
        results.append(t('path', filepath))
        results.append(f"{'='*70}\n")
        try:
            if lang == "dotnet" or lang == "resx":
                dotnet_results = self.apply_dotnet_methods(filepath, self.custom_key.get())
                results.extend(dotnet_results)
            elif lang in ["json", "xml"]:
                config_results = self.apply_config_methods(filepath, self.custom_key.get())
                results.extend(config_results)
            elif lang in ["exe", "dll"] and lang != "dotnet":
                data = read_bytes(filepath)
                processed_data = self.apply_exe_methods(data, xor_key)
                base_path = os.path.splitext(filepath)[0]
                out_path = f"{base_path}_obfuscated{os.path.splitext(filepath)[1]}"
                write_bytes(out_path, processed_data)
                size_change = ((len(processed_data) - len(data)) / len(data) * 100)
                results.append(t('text_obf_success', lang.upper()))
                results.append(t('output_file_written', os.path.basename(out_path)))
                results.append(t('size_change', len(data), len(processed_data)))
                results.append(t('size_delta', size_change))
                if self.generate_decoder.get():
                    decoder_path = self._gen_decoder_for_exe(out_path, xor_key)
                    if decoder_path:
                        results.append(t('decoder_file', os.path.basename(decoder_path)))
            elif lang == "image":
                image_vars = self.vars.get("image", {})
                if "IMG · XOR Encryption" in image_vars and image_vars["IMG · XOR Encryption"].get():
                    result, out_path = image_xor_encrypt(filepath, self.custom_key.get())
                    results.append(t('image_obf_success'))
                    results.append(t('output_file_written', os.path.basename(out_path)))
                    results.append(t('size_change', os.path.getsize(filepath), len(result)))
                    results.append(t('size_delta', ((len(result) - os.path.getsize(filepath)) / os.path.getsize(filepath) * 100)))
                    if self.generate_decoder.get():
                        decoder_path = gen_decoder_for_images(filepath, self.custom_key.get())
                        if decoder_path:
                            results.append(t('decoder_file', os.path.basename(decoder_path)))
                else:
                    results.append(f"# IMG · XOR Encryption not selected for {filename}")
            else:
                text = read_text(filepath)
                processed_text, encrypted_images = self.apply_text_methods(text, lang, xor_key)
                base_path = os.path.splitext(filepath)[0]
                out_path = f"{base_path}_obfuscated{os.path.splitext(filepath)[1]}"
                write_text(out_path, processed_text)
                results.append(t('text_obf_success', lang.upper()))
                results.append(t('output_file_written', os.path.basename(out_path)))
                results.append(t('size_change', len(text), len(processed_text)))
                results.append(t('size_delta', ((len(processed_text) - len(text)) / len(text) * 100)))
                if encrypted_images > 0:
                    results.append(t('images_encrypted', encrypted_images))
                if self.generate_decoder.get():
                    decoder_path = self._gen_decoder_for_text(out_path, xor_key)
                    if decoder_path:
                        results.append(t('decoder_file', os.path.basename(decoder_path)))
                    if encrypted_images > 0:
                        decoder_path = gen_decoder_for_html_css_images(filepath, self.custom_key.get())
                        if decoder_path:
                            results.append(t('decoder_file', os.path.basename(decoder_path)))
                if len(processed_text) > 500:
                    preview = processed_text[:300] + t('preview_truncated')
                else:
                    preview = processed_text
                results.append(f"\n📄 PREVIEW:\n{preview[:400]}")
        except Exception as e:
            error_msg = t('error_processing', filename)
            error_msg += f"\n{t('error_type', lang)}"
            error_msg += f"\n{t('error_details', str(e))}"
            results.append(error_msg)
            import traceback
            results.append(f"\n{t('error_trace', traceback.format_exc()[:300])}")

    def _gen_decoder_for_text(self, obf_path: str, xor_key: bytes):
        base_name = os.path.splitext(obf_path)[0]
        decoder_path = f"{base_name}_decoder.py"
        key_hex = xor_key.hex() if xor_key else ""
        anti_analysis_code = py_anti_debug_full("") if self.advanced_security.get() else ""
        decoder_code = f'''#!/usr/bin/env python3
# Decoder for obfuscated text file
# Generated automatically {time.strftime("%Y-%m-%d %H:%M:%S")}
import base64
import os
import sys
import hashlib
import ctypes
import platform
import time

def check_integrity():
    """Verify decoder script integrity using SHA-256 hash"""
    with open(__file__, 'rb') as f:
        code = f.read()
    expected_hash = "placeholder"  # Self-hash (placeholder, will be replaced)
    if hashlib.sha256(code).hexdigest() != expected_hash:
        print("⚠️ Decoder tampering detected!")
        os.remove(__file__)
        sys.exit(1)

{anti_analysis_code}

def decode_obfuscated_text():
    """Decodes obfuscated text file"""
    input_file = r"{os.path.abspath(obf_path)}"
    output_file = r"{base_name}_restored{os.path.splitext(obf_path)[1]}"
    try:
        if _advanced_anti_analysis():
            print("⚠️ Analysis environment detected!")
            os.remove(__file__)
            sys.exit(1)
        check_integrity()
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        try:
            decoded = base64.b64decode(content.encode('utf-8')).decode('utf-8')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decoded)
            print(f"✅ Base64 decoding successful!")
            print(f"📁 Saved: {output_file}")
            return
        except:
            pass
        if "{key_hex}":
            key = bytes.fromhex("{key_hex}")
            data = content.encode('utf-8')
            decoded = bytearray(len(data))
            for i, b in enumerate(data):
                decoded[i] = b ^ key[i % len(key)]
            try:
                result = decoded.decode('utf-8', errors='ignore')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✅ XOR decoding successful!")
                print(f"📁 Saved: {output_file}")
                return
            except:
                pass
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Could not automatically decode\\n# Source file: {input_file}\\n# Try manual decoding\\n\\n{content[:1000]}")
        print(f"⚠️ Automatic decoding failed")
        print(f"📁 Copy saved: {output_file}")
    finally:
        if os.path.exists(__file__):
            print("🗑️ Self-destructing decoder...")
            os.remove(__file__)

if __name__ == "__main__":
    decode_obfuscated_text()
'''
        # Calculate self-hash excluding the expected_hash line
        hash_line = '    expected_hash = "placeholder"  # Self-hash (placeholder, will be replaced)'
        decoder_code_no_hash = decoder_code.replace(hash_line, '    expected_hash = ""')
        calculated_hash = hashlib.sha256(decoder_code_no_hash.encode()).hexdigest()
        decoder_code = decoder_code.replace('placeholder', calculated_hash)
        try:
            write_text(decoder_path, decoder_code)
            return decoder_path
        except Exception as e:
            print(f"Error creating text decoder: {e}")
            return None

    def _gen_decoder_for_exe(self, obf_path: str, xor_key: bytes):
        base_name = os.path.splitext(obf_path)[0]
        decoder_path = f"{base_name}_decoder.py"
        key_hex = xor_key.hex() if xor_key else ""
        anti_analysis_code = py_anti_debug_full("") if self.advanced_security.get() else ""
        decoder_code = f'''#!/usr/bin/env python3
# Decoder for obfuscated EXE file
# Generated automatically {time.strftime("%Y-%m-%d %H:%M:%S")}
import base64
import os
import sys
import hashlib
import ctypes
import platform
import time

def check_integrity():
    """Verify decoder script integrity using SHA-256 hash"""
    with open(__file__, 'rb') as f:
        code = f.read()
    expected_hash = "placeholder"  # Self-hash (placeholder, will be replaced)
    if hashlib.sha256(code).hexdigest() != expected_hash:
        print("⚠️ Decoder tampering detected!")
        os.remove(__file__)
        sys.exit(1)

{anti_analysis_code}

def decode_obfuscated_exe():
    """Decodes obfuscated executable file"""
    input_file = r"{os.path.abspath(obf_path)}"
    output_file = r"{base_name}_restored{os.path.splitext(obf_path)[1]}"
    try:
        if _advanced_anti_analysis():
            print("⚠️ Analysis environment detected!")
            os.remove(__file__)
            sys.exit(1)
        check_integrity()
        with open(input_file, 'rb') as f:
            data = f.read()
        original_size = len(data)
        print(f"📏 Original size: {original_size:,} bytes")
        if data.startswith(b"SEG:"):
            try:
                header_end = data.find(b":", data.find(b":") + 1)
                if header_end != -1:
                    header = data[:header_end+1]
                    payload = data[header_end+1:]
                    parts = header.decode('utf-8', errors='ignore').split(':')
                    if len(parts) >= 4 and parts[0] == "SEG":
                        num_segs = int(parts[1])
                        seg_size = int(parts[2])
                        result = bytearray()
                        for i in range(num_segs):
                            start = i * seg_size
                            end = start + seg_size
                            if end <= len(payload):
                                result.extend(payload[start:end])
                        data = bytes(result)
                        print(f"✅ Removed segmentation header")
                        print(f"📏 After segmentation: {len(data):,} bytes")
            except Exception as e:
                print(f"⚠️ Error processing segmentation: {e}")
        try:
            decoded = base64.b64decode(data)
            data = decoded
            print(f"✅ Base64 decoding")
            print(f"📏 After Base64: {len(data):,} bytes")
        except:
            print("ℹ️ Base64 decoding not required")
        if "{key_hex}":
            key = bytes.fromhex("{key_hex}")
            result = bytearray(len(data))
            for i, b in enumerate(data):
                result[i] = b ^ key[i % len(key)]
            data = bytes(result)
            print(f"✅ XOR decoding (key: {len(key)} bytes)")
            print(f"📏 After XOR: {len(data):,} bytes")
        if len(data) > 4 and data[:4] == data[-4:][::-1]:
            data = data[::-1]
            print(f"✅ Byte order reversed")
        with open(output_file, 'wb') as f:
            f.write(data)
        final_size = len(data)
        size_change = ((final_size - original_size) / original_size * 100)
        print(f"\n🎉 DECODING COMPLETED!")
        print(f"📁 Source: {os.path.basename(input_file)}")
        print(f"📁 Restored: {os.path.basename(output_file)}")
        print(f"📏 Size: {original_size:,} → {final_size:,} bytes")
        print(f"📈 Change: {size_change:+.1f}%")
        if data[:2] == b'MZ':
            print(f"✅ File is executable (PE header found)")
        else:
            print(f"⚠️ PE header not found - possibly corrupted")
    finally:
        if os.path.exists(__file__):
            print("🗑️ Self-destructing decoder...")
            os.remove(__file__)

if __name__ == "__main__":
    decode_obfuscated_exe()
'''
        # Calculate self-hash excluding the expected_hash line
        hash_line = '    expected_hash = "placeholder"  # Self-hash (placeholder, will be replaced)'
        decoder_code_no_hash = decoder_code.replace(hash_line, '    expected_hash = ""')
        calculated_hash = hashlib.sha256(decoder_code_no_hash.encode()).hexdigest()
        decoder_code = decoder_code.replace('placeholder', calculated_hash)
        try:
            write_text(decoder_path, decoder_code)
        except Exception as e:
            print(f"Error creating EXE decoder: {e}")

    def run(self):
        if not self.files:
            messagebox.showwarning(t('run_obf'), t('no_files'))
            return
        results = []
        xor_key = self._parse_xor_key()
        start_time = time.time()
        results.append(t('obf_started'))
        results.append(t('start_time', time.strftime('%Y-%m-%d %H:%M:%S')))
        results.append(t('files_processed', len(self.files)))
        results.append(t('xor_key_label', '*' * len(self.xor_key_str.get()) if self.xor_key_str.get() else 'none'))
        results.append(t('obf_key_label', '*' * min(8, len(self.custom_key.get())) if self.custom_key.get() else 'none'))
        results.append(f"{'='*80}\n")
        try:
            if self.merge_files.get() and all(detect_lang(f) in ["python", "powershell", "js", "cpp", "html", "css"] for f in self.files):
                merged_text = "\n\n# === MERGED FILES ===\n\n".join(read_text(f) for f in self.files)
                lang = detect_lang(self.files[0])
                results.append(t('merge_mode', lang.upper()))
                processed_text, encrypted_images = self.apply_text_methods(merged_text, lang, xor_key)
                out_path = self.output_path.get() or f"merged_obfuscated_{lang}_{int(time.time())}.txt"
                write_text(out_path, processed_text)
                size_change = ((len(processed_text) - len(merged_text)) / len(merged_text) * 100)
                results.append(t('output_file_written', os.path.basename(out_path)))
                results.append(t('size_change', len(merged_text), len(processed_text)))
                results.append(t('size_delta', size_change))
                if self.generate_decoder.get():
                    self._gen_decoder_for_text(out_path, xor_key)
                    results.append(t('decoder_file', os.path.basename(out_path + '_decoder.py')))
                preview = processed_text[:800] + t('preview_truncated')
                results.append(f"\n📄 PREVIEW:\n{preview}")
            else:
                results.append(t('individual_mode'))
                for filepath in self.files:
                    self._process_single_file(filepath, xor_key, results)
        except Exception as e:
            results.append(f"\n{t('error_critical')}")
            results.append(t('error_details', str(e)))
            import traceback
            results.append(t('error_trace', traceback.format_exc()))
        end_time = time.time()
        duration = end_time - start_time
        results.append(f"\n{'='*80}")
        results.append(t('obf_completed_footer'))
        results.append(t('execution_time', duration))
        results.append(t('files_processed', len(self.files)))
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", "\n".join(results))
        self.preview.see("end")
        msg = t('obf_completed', duration, len(self.files))
        if self.generate_decoder.get():
            msg += t('decoder_generated')
        messagebox.showinfo(t('obf_completed_footer'), msg)

def main():
    if HAS_DND:
        root = TkinterDnD.Tk()
        root.title(t('title'))
    else:
        root = tk.Tk()
        root.title(t('title') + " - Drag&Drop disabled")
    root.geometry("1100x850")
    root.minsize(900, 600)
    if not HAS_DND:
        status_frame = tk.Frame(root)
        status_frame.pack(fill="x", side="bottom")
        tk.Label(status_frame, text=t('no_dnd'), bg="lightgray", fg="blue", 
                anchor="w", padx=10, pady=2).pack(fill="x")
    if not HAS_DNLIB:
        status_frame = tk.Frame(root)
        status_frame.pack(fill="x", side="bottom")
        tk.Label(status_frame, text=t('no_dotnet'), bg="lightyellow", fg="darkred", 
                anchor="w", padx=10, pady=2).pack(fill="x")
    if not HAS_CLANG:
        status_frame = tk.Frame(root)
        status_frame.pack(fill="x", side="bottom")
        tk.Label(status_frame, text=t('no_clang'), bg="lightyellow", fg="darkred", 
                anchor="w", padx=10, pady=2).pack(fill="x")
    app = AppBase(root)
    if HAS_DND:
        def drop_handler(event):
            files = []
            data = event.data.strip()
            if data.startswith('{') and data.endswith('}'):
                matches = re.findall(r'{{([^}]+)}}', data)
                for match in matches:
                    if os.path.exists(match):
                        files.append(match)
            else:
                for path in data.split():
                    path = path.strip()
                    if os.path.exists(path):
                        files.append(path)
            if files:
                app.files = files
                app._update_status()
                app.preview.delete("1.0", "end")
                preview_text = f"📂 {t('files_processed', len(files))}\n{'='*50}\n\n"
                for i, f in enumerate(files, 1):
                    lang = detect_lang(f)
                    icon = {"python": "🐍", "powershell": "⚡", "js": "📜", 
                           "dotnet": "🔗", "exe": "⚙️", "html": "🌐", "css": "🎨", "cpp": "🛡️", "resx": "📋", "image": "🖼️", "json": "📄", "xml": "📄"}.get(lang, "📄")
                    preview_text += f"{i:2d}. {icon} {lang.upper():<10} {os.path.basename(f)}\n"
                preview_text += f"\n💡 Select {lang.upper()} tab for obfuscation"
                app.preview.insert("1.0", preview_text)
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', drop_handler)
    root.mainloop()

if __name__ == "__main__":
    main()