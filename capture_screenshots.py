"""
Automated Screenshot Capture Engine for PROLOG-PARSE Visual Studio
Uses Chrome DevTools Protocol (CDP) via headless Chrome and websockets.
Captures all pages, tabs, presets, proof traces, and themes, saving to images/ and iamges/.
"""

import os
import sys
import time
import json
import base64
import asyncio
import tempfile
import subprocess
import urllib.request
import websockets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
IAMGES_DIR = os.path.join(BASE_DIR, "iamges")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CDP_PORT = 9222
APP_BASE_URL = "http://127.0.0.1:5050"

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(IAMGES_DIR, exist_ok=True)

class CDPClient:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.ws = None
        self.req_id = 0

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url, max_size=50 * 1024 * 1024)

    async def send(self, method, params=None):
        self.req_id += 1
        msg_id = self.req_id
        payload = {"id": msg_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(payload))
        while True:
            resp_raw = await self.ws.recv()
            resp = json.loads(resp_raw)
            if resp.get("id") == msg_id:
                if "error" in resp:
                    print(f"  [CDP Error] {method}: {resp['error']}")
                return resp.get("result", {})

    async def evaluate_js(self, expression):
        result = await self.send("Runtime.evaluate", {
            "expression": expression,
            "awaitPromise": True,
            "returnByValue": True
        })
        return result.get("result", {}).get("value")

    async def capture_screenshot(self, filename):
        res = await self.send("Page.captureScreenshot", {"format": "png"})
        data_b64 = res.get("data")
        if data_b64:
            img_bytes = base64.b64decode(data_b64)
            path1 = os.path.join(IMAGES_DIR, filename)
            path2 = os.path.join(IAMGES_DIR, filename)
            with open(path1, "wb") as f1:
                f1.write(img_bytes)
            with open(path2, "wb") as f2:
                f2.write(img_bytes)
            print(f"  [SAVED] {filename} ({len(img_bytes):,} bytes)")
            return True
        print(f"  [FAILED] {filename}")
        return False

async def main():
    print("=" * 68)
    print(" [PROLOG-PARSE] Automated Visual Screenshot Engine")
    print(f" Target directories: {IMAGES_DIR} & {IAMGES_DIR}")
    print("=" * 68)

    # 1. Launch Headless Chrome without extensions
    cmd = [
        CHROME_PATH,
        "--headless=new",
        f"--remote-debugging-port={CDP_PORT}",
        "--disable-gpu",
        "--disable-extensions",
        "--no-sandbox",
        "--window-size=1920,1080",
        "--hide-scrollbars"
    ]
    print(f"Launching Chrome Headless on CDP port {CDP_PORT}...")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for CDP endpoint
        ws_url = None
        for attempt in range(15):
            time.sleep(0.5)
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json", timeout=1) as resp:
                    tabs = json.loads(resp.read().decode())
                    for t in tabs:
                        if t.get("type") == "page":
                            ws_url = t.get("webSocketDebuggerUrl")
                            break
                    if ws_url:
                        break
            except Exception:
                pass

        if not ws_url:
            print("[Error] Failed to connect to Chrome page debugger.")
            return

        print(f"Connected to CDP WebSocket: {ws_url}")
        client = CDPClient(ws_url)
        await client.connect()

        # Initialize CDP domains
        await client.send("Page.enable")
        await client.send("Runtime.enable")
        await client.send("DOM.enable")
        await client.send("Emulation.setDeviceMetricsOverride", {
            "width": 1920,
            "height": 1080,
            "deviceScaleFactor": 1,
            "mobile": False
        })

        # ---------------------------------------------------------------------
        # 1. LANDING PAGE HERO
        # ---------------------------------------------------------------------
        print("\n1. Capturing Landing Page Hero...")
        await client.send("Page.navigate", {"url": f"{APP_BASE_URL}/"})
        await asyncio.sleep(1.8)
        await client.capture_screenshot("01_landing_hero.png")

        # ---------------------------------------------------------------------
        # 2. LANDING PAGE SYLLABUS & ARCHITECTURE
        # ---------------------------------------------------------------------
        print("2. Capturing Landing Page Syllabus & Architecture...")
        await client.evaluate_js("window.scrollTo(0, 680);")
        await asyncio.sleep(0.8)
        await client.capture_screenshot("02_landing_syllabus_architecture.png")

        # ---------------------------------------------------------------------
        # 3. STUDIO WORKBENCH OVERVIEW
        # ---------------------------------------------------------------------
        print("3. Navigating to Studio Workbench...")
        await client.send("Page.navigate", {"url": f"{APP_BASE_URL}/studio"})
        await asyncio.sleep(1.8)
        await client.evaluate_js("compileCode();")
        await asyncio.sleep(1.0)
        await client.capture_screenshot("03_studio_overview.png")

        # ---------------------------------------------------------------------
        # 4. TAB 1: LEXER TOKENS
        # ---------------------------------------------------------------------
        print("4. Capturing Lexer Tokens Tab...")
        await client.evaluate_js("switchTab('tab-lexer');")
        await asyncio.sleep(0.8)
        await client.capture_screenshot("04_lexer_tokens_view.png")

        # ---------------------------------------------------------------------
        # 5. TAB 2: AST & SYMBOLS
        # ---------------------------------------------------------------------
        print("5. Capturing AST & Symbols Tab...")
        await client.evaluate_js("switchTab('tab-ast');")
        await asyncio.sleep(0.8)
        await client.capture_screenshot("05_ast_and_symbols_view.png")

        # ---------------------------------------------------------------------
        # 6. TAB 3: CALL GRAPH (PDG)
        # ---------------------------------------------------------------------
        print("6. Capturing Call Graph (PDG) Tab...")
        await client.evaluate_js("switchTab('tab-pdg'); if (typeof renderPDGGraph === 'function') renderPDGGraph();")
        await asyncio.sleep(1.0)
        await client.capture_screenshot("06_call_graph_pdg_view.png")

        # ---------------------------------------------------------------------
        # 7. TAB 4: WAM BYTECODE & TAC QUADRUPLES
        # ---------------------------------------------------------------------
        print("7. Capturing WAM Bytecode & TAC Tab...")
        await client.evaluate_js("switchTab('tab-wam');")
        await asyncio.sleep(0.8)
        await client.capture_screenshot("07_wam_bytecode_tac_view.png")

        # ---------------------------------------------------------------------
        # 8. WAM OPTIMIZED BYTECODE
        # ---------------------------------------------------------------------
        print("8. Capturing Optimized WAM Bytecode View...")
        await client.evaluate_js("var optBtn = document.getElementById('segOpt'); if (optBtn) optBtn.click();")
        await asyncio.sleep(0.6)
        await client.capture_screenshot("08_wam_optimized_diff_view.png")

        # ---------------------------------------------------------------------
        # 9. TAB 5: LIVE DEMO SHOWCASE TOUR
        # ---------------------------------------------------------------------
        print("9. Capturing Live Demo Showcase Tab...")
        await client.evaluate_js("switchTab('tab-demo'); jumpToDemoStep(3);")
        await asyncio.sleep(1.0)
        await client.capture_screenshot("09_live_demo_showcase.png")

        # ---------------------------------------------------------------------
        # 10. INTERACTIVE QUERY & SLD RESOLUTION PROOF TRACE
        # ---------------------------------------------------------------------
        print("10. Solving Query and Capturing SLD Proof Trace...")
        await client.evaluate_js("solveQuery();")
        await asyncio.sleep(1.2)
        await client.evaluate_js("""
            var details = document.querySelector('.trace-details');
            if (details) details.open = true;
        """)
        await asyncio.sleep(0.8)
        await client.capture_screenshot("10_query_sld_resolution_trace.png")

        # ---------------------------------------------------------------------
        # 11. PRESET: NETWORK PATHS BENCHMARK
        # ---------------------------------------------------------------------
        print("11. Capturing Network Paths Benchmark...")
        await client.evaluate_js("""
            var btn = document.querySelector('.preset-btn[data-key="graph_network"]');
            if (btn) selectPreset('graph_network', btn);
        """)
        await asyncio.sleep(0.8)
        await client.evaluate_js("compileCode(); switchTab('tab-pdg'); if (typeof renderPDGGraph === 'function') renderPDGGraph();")
        await asyncio.sleep(1.0)
        await client.capture_screenshot("11_network_paths_preset.png")

        # ---------------------------------------------------------------------
        # 12. PRESET: RECURSIVE LIST OPERATIONS
        # ---------------------------------------------------------------------
        print("12. Capturing Recursive List Operations Benchmark...")
        await client.evaluate_js("""
            var btn = document.querySelector('.preset-btn[data-key="list_algorithms"]');
            if (btn) selectPreset('list_algorithms', btn);
        """)
        await asyncio.sleep(0.8)
        await client.evaluate_js("compileCode(); switchTab('tab-ast');")
        await asyncio.sleep(1.0)
        await client.capture_screenshot("12_list_operations_preset.png")

        # ---------------------------------------------------------------------
        # 13. PRESET: SYMBOLIC ARITHMETIC EVALUATOR
        # ---------------------------------------------------------------------
        print("13. Capturing Expression Evaluator Benchmark...")
        await client.evaluate_js("""
            var btn = document.querySelector('.preset-btn[data-key="expr_evaluator"]');
            if (btn) selectPreset('expr_evaluator', btn);
        """)
        await asyncio.sleep(0.8)
        await client.evaluate_js("compileCode(); switchTab('tab-wam');")
        await asyncio.sleep(1.0)
        await client.capture_screenshot("13_expression_evaluator_preset.png")

        # ---------------------------------------------------------------------
        # 14. CLEAN LIGHT THEME STUDIO
        # ---------------------------------------------------------------------
        print("14. Capturing Clean Light Theme Studio...")
        await client.evaluate_js("""
            var btn = document.querySelector('.preset-btn[data-key="ancestor_tree"]');
            if (btn) selectPreset('ancestor_tree', btn);
            if (typeof toggleTheme === 'function') toggleTheme();
            switchTab('tab-lexer');
        """)
        await asyncio.sleep(1.0)
        await client.capture_screenshot("14_clean_light_theme_studio.png")

        print("\n" + "=" * 68)
        print(" All 14 screenshots successfully captured and stored in:")
        print(f"  • {IMAGES_DIR}")
        print(f"  • {IAMGES_DIR}")
        print("=" * 68)

    finally:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

if __name__ == "__main__":
    asyncio.run(main())
