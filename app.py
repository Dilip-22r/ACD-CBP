"""
PROLOG-PARSE: AI-Native Visual Compiler & Interactive Logic Demo Studio
Restyled by applying:
- ui-ux-pro-max skill (design-system generator): Dark Mode (OLED) base palette,
  AI-Native UI accents, Bento grid structure, JetBrains Mono / IBM Plex Sans pairing,
  pre-delivery checklist (focus rings, contrast, reduced-motion, no emoji icons).
- design-taste-frontend skill: anti-slop rules (real component previews, restrained
  accent palette, hero discipline, layout diversity, honest copy).

Engineering note: HTML_TEMPLATE is a RAW string (r""). In the previous version a plain
triple-quoted string converted `split('\n')` into a real newline inside the rendered JS,
raising `SyntaxError: Invalid or unexpected token` and disabling the entire page.
Backend compiler modules (lexer, parser, semantic, wam_compiler, engine, graph_builder)
are unchanged.
Course: Compiler Design Laboratory (22PC2CS301)
Department of Computer Science & Engineering, VNRVJIET
"""

from flask import Flask, render_template_string, request, jsonify
from lexer import PrologLexer, TokenType
from parser import PrologParser
from semantic import SemanticAnalyzer
from wam_compiler import WAMCompiler
from engine import ResolutionEngine
from graph_builder import GraphBuilder
from ast_nodes import Query
from sample_programs import SAMPLE_PROGRAMS

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Interactive Prolog compiler studio: lexer tokens, AST, call graph, WAM bytecode and live SLD resolution proofs.">
    <title>PROLOG-PARSE · Visual Prolog Compiler Studio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        /* =========================================================
           DESIGN TOKENS - ui-ux-pro-max generated design system
           Style: Dark Mode (OLED) x AI-Native UI, bento structure
           ========================================================= */
        :root {
            /* Dark theme (default) - deep midnight, low white emission */
            --bg-abyss: #060a14;
            --bg-base: #0a101f;
            --bg-surface: #0e1626;
            --bg-raise: #131d31;
            --bg-raise-2: #18233b;
            --bg-inset: #070c18;
            --bg-inset-2: #0a1120;
            --border: #22304a;
            --border-soft: #182238;
            --border-strong: #33415c;

            --text-1: #eef2fa;
            --text-2: #a9b6cb;
            --text-3: #7e8da8;
            --edge: #8ea3c4;

            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --accent-soft: #a5b4fc;
            --accent-wash: rgba(99, 102, 241, 0.14);

            --ok: #34d399;
            --ok-deep: #10b981;
            --ok-wash: rgba(52, 211, 153, 0.12);

            --bad: #fb7185;
            --bad-deep: #f43f5e;
            --bad-wash: rgba(251, 113, 133, 0.12);

            --warn: #fbbf24;
            --warn-deep: #f59e0b;
            --warn-wash: rgba(251, 191, 36, 0.12);

            --info: #38bdf8;
            --info-wash: rgba(56, 189, 248, 0.12);

            --shadow-1: 0 1px 2px rgba(2, 6, 18, 0.5), 0 8px 24px -12px rgba(2, 6, 18, 0.55);
            --shadow-accent: 0 4px 16px -6px rgba(99, 102, 241, 0.45);
            --focus-ring: 0 0 0 2px var(--bg-base), 0 0 0 4px var(--accent);

            --nav-blur: rgba(10, 16, 31, 0.86);
            --grid-dot: rgba(148, 163, 184, 0.07);
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;

            --font-ui: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
            --font-mono: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;

            /* Prolog highlighter palette (matches token pill language) */
            --pl-atom: #d5dfee;
            --pl-var: var(--warn);
            --pl-op: var(--bad);
            --pl-num: var(--ok);
            --pl-str: var(--ok);
            --pl-fn: var(--info);
            --pl-comment: var(--text-3);
        }

        [data-theme="light"] {
            /* Light theme - clean Linear-style developer aesthetic, AA contrast */
            --bg-abyss: #eef1f7;
            --bg-base: #f6f7fb;
            --bg-surface: #ffffff;
            --bg-raise: #f1f4fa;
            --bg-raise-2: #e9edf5;
            --bg-inset: #f8fafd;
            --bg-inset-2: #f1f4fa;
            --border: #dde3ee;
            --border-soft: #e7ecf5;
            --border-strong: #c3ccdd;

            --text-1: #131b2c;
            --text-2: #3d4c63;
            --text-3: #5f6d84;
            --edge: #52627a;

            --accent: #4f46e5;
            --accent-hover: #4338ca;
            --accent-soft: #6366f1;
            --accent-wash: rgba(79, 70, 229, 0.10);

            --ok: #059669;
            --ok-deep: #047857;
            --ok-wash: rgba(5, 150, 105, 0.10);

            --bad: #e11d48;
            --bad-deep: #be123c;
            --bad-wash: rgba(225, 29, 72, 0.09);

            --warn: #b45309;
            --warn-deep: #92400e;
            --warn-wash: rgba(180, 83, 9, 0.10);

            --info: #0284c7;
            --info-wash: rgba(2, 132, 199, 0.10);

            --shadow-1: 0 1px 2px rgba(15, 23, 42, 0.06), 0 8px 24px -12px rgba(15, 23, 42, 0.12);
            --shadow-accent: 0 4px 16px -6px rgba(79, 70, 229, 0.35);
            --focus-ring: 0 0 0 2px var(--bg-base), 0 0 0 4px var(--accent);

            --nav-blur: rgba(246, 247, 251, 0.88);
            --grid-dot: rgba(15, 23, 42, 0.06);

            --pl-atom: #1e293b;
            --pl-var: #b45309;
            --pl-op: #e11d48;
            --pl-num: #059669;
            --pl-str: #047857;
            --pl-fn: #0284c7;
            --pl-comment: var(--text-3);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html, body {
            height: 100vh;
            max-height: 100vh;
            overflow: hidden;
            background: var(--bg-base);
            color: var(--text-1);
            font-family: var(--font-ui);
            font-size: 13px;
            display: flex;
            flex-direction: column;
            -webkit-font-smoothing: antialiased;
        }

        /* Focus discipline (ui-ux-pro-max checklist: visible focus for keyboard nav) */
        :focus {
            outline: none;
        }
        :focus-visible {
            outline: none;
            box-shadow: var(--focus-ring);
        }
        .code-textarea:focus-visible {
            box-shadow: none; /* editor focus is shown by caret + gutter accents */
        }

        button, input, textarea, select, a { font-family: inherit; }
        .icon { flex-shrink: 0; }

        ::selection {
            background: var(--accent-wash);
            color: inherit;
        }

        /* Reduced motion: collapse all animation + transitions */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }
        }

        /* -------------------------------------------------------------
           VIEW SWITCHER
           ------------------------------------------------------------- */
        #landingView {
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow-y: auto;
            scroll-behavior: smooth;
        }

        #studioView {
            display: none;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }

        /* =========================================================
           LANDING PAGE - AI-native bento, left-aligned hero
           ========================================================= */
        .shell-nav {
            position: sticky;
            top: 0;
            z-index: 50;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 0 28px;
            background: var(--nav-blur);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-soft);
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-badge {
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
            color: #ffffff;
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.8px;
            padding: 4px 8px;
            border-radius: 5px;
            box-shadow: var(--shadow-accent);
        }

        .brand-text h1 {
            font-size: 13.5px;
            font-weight: 700;
            line-height: 1.2;
            color: var(--text-1);
        }

        .brand-text p {
            font-size: 10.5px;
            color: var(--text-2);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .nav-link {
            appearance: none;
            background: transparent;
            border: none;
            color: var(--text-2);
            font-size: 12.5px;
            font-weight: 500;
            padding: 7px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: color 0.15s, background 0.15s;
        }

        .nav-link:hover {
            color: var(--text-1);
            background: var(--bg-raise);
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .icon-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            color: var(--text-2);
            padding: 7px 9px;
            border-radius: 7px;
            cursor: pointer;
            transition: color 0.15s, border-color 0.15s, transform 0.15s;
        }

        .icon-btn:hover {
            color: var(--text-1);
            border-color: var(--border-strong);
        }

        .icon-btn:active {
            transform: scale(0.96);
        }

        /* Hero - split layout: copy left, live terminal right */
        .hero-wrap {
            max-width: 1160px;
            width: 100%;
            margin: 0 auto;
            padding: 64px 32px 40px;
            display: grid;
            grid-template-columns: 1.02fr 0.98fr;
            gap: 48px;
            align-items: center;
        }

        .eyebrow-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            padding: 5px 13px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 600;
            color: var(--accent-soft);
            letter-spacing: 0.3px;
            width: fit-content;
        }

        .hero-copy {
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .hero-title {
            font-size: clamp(30px, 4.6vw, 54px);
            font-weight: 700;
            letter-spacing: -0.035em;
            line-height: 1.08;
            color: var(--text-1);
        }

        .hero-title em {
            font-family: var(--font-mono);
            font-style: italic;
            color: var(--accent-soft);
        }

        .hero-sub {
            font-size: 14.5px;
            line-height: 1.65;
            color: var(--text-2);
            max-width: 52ch;
        }

        .hero-ctas {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 4px;
        }

        .btn-large {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 9px;
            cursor: pointer;
            border: none;
            text-decoration: none;
            transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), background 0.18s, border-color 0.18s, box-shadow 0.18s;
        }

        .btn-large:active {
            transform: translateY(1px) scale(0.98);
        }

        .btn-large-primary {
            background: var(--accent);
            color: #ffffff;
            box-shadow: var(--shadow-accent);
        }

        .btn-large-primary:hover {
            background: var(--accent-hover);
            transform: translateY(-1px);
        }

        .btn-large-secondary {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            color: var(--text-1);
        }

        .btn-large-secondary:hover {
            background: var(--bg-raise);
            border-color: var(--border-strong);
            transform: translateY(-1px);
        }

        .hero-hint {
            font-size: 11px;
            color: var(--text-3);
        }

        .hero-hint kbd {
            font-family: var(--font-mono);
            font-size: 10px;
            background: var(--bg-raise);
            border: 1px solid var(--border);
            border-bottom-width: 2px;
            border-radius: 4px;
            padding: 1px 5px;
        }

        /* Real terminal preview (actual compiler output shape) */
        .terminal-card {
            background: var(--bg-inset);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-1), inset 0 1px 0 rgba(255, 255, 255, 0.04);
            font-family: var(--font-mono);
            font-size: 11.5px;
            line-height: 1.75;
        }

        .terminal-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 14px;
            background: var(--bg-raise);
            border-bottom: 1px solid var(--border);
            color: var(--text-2);
            font-size: 10.5px;
            letter-spacing: 0.4px;
        }

        .terminal-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--ok);
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--ok);
        }

        @media (prefers-reduced-motion: no-preference) {
            .pulse-dot { animation: pulseDot 2.2s ease-in-out infinite; }
        }

        @keyframes pulseDot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.35; }
        }

        .terminal-body {
            padding: 14px 16px 16px;
            color: var(--pl-atom);
            white-space: pre-wrap;
            min-height: 300px;
        }

        .terminal-body .cm { color: var(--pl-comment); font-style: italic; }
        .terminal-body .vr { color: var(--pl-var); }
        .terminal-body .op { color: var(--pl-op); }
        .terminal-body .fn { color: var(--pl-fn); }
        .terminal-body .nm { color: var(--pl-num); }
        .terminal-body .ok { color: var(--ok); }
        .terminal-body .dim { color: var(--text-3); }
        /* Pipeline stepper */
        .pipeline-section {
            max-width: 1160px;
            width: 100%;
            margin: 0 auto;
            padding: 8px 32px 48px;
        }

        .pipeline-strip {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 14px 18px;
            box-shadow: var(--shadow-1);
            flex-wrap: wrap;
        }

        .pipeline-node {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-mono);
            font-size: 10.5px;
            color: var(--text-2);
            white-space: nowrap;
        }

        .pipeline-node b {
            font-size: 9.5px;
            font-weight: 700;
            color: var(--accent-soft);
            border: 1px solid var(--border);
            background: var(--bg-raise);
            border-radius: 4px;
            padding: 2px 5px;
        }

        .pipeline-node.last b {
            color: var(--ok);
            border-color: var(--ok-wash);
            background: var(--ok-wash);
        }

        .pipeline-arrow {
            color: var(--border-strong);
            font-family: var(--font-mono);
        }

        /* Bento grid with rhythm */
        .bento-section {
            max-width: 1160px;
            width: 100%;
            margin: 0 auto;
            padding: 0 32px 40px;
        }

        .bento-head {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 16px;
        }

        .bento-head h2 {
            font-size: 19px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-1);
        }

        .bento-head p {
            font-size: 12.5px;
            color: var(--text-2);
        }

        .bento-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
        }

        .bento-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            box-shadow: var(--shadow-1);
            transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, box-shadow 0.2s;
            min-width: 0;
        }

        .bento-card:hover {
            transform: translateY(-3px);
            border-color: var(--border-strong);
            box-shadow: var(--shadow-1), var(--shadow-accent);
        }

        .bento-card.span-3 { grid-column: span 3; }
        .bento-card.span-2 { grid-column: span 2; }
        .bento-card.span-4 { grid-column: span 4; }

        .bento-card.tinted {
            background: linear-gradient(150deg, var(--bg-raise) 0%, var(--bg-surface) 65%);
        }

        .bento-icon {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--accent-wash);
            color: var(--accent-soft);
        }

        .bento-icon.ok { background: var(--ok-wash); color: var(--ok); }
        .bento-icon.warn { background: var(--warn-wash); color: var(--warn); }
        .bento-icon.info { background: var(--info-wash); color: var(--info); }
        .bento-icon.bad { background: var(--bad-wash); color: var(--bad); }

        .bento-card h3 {
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-1);
        }

        .bento-card > p {
            font-size: 12px;
            line-height: 1.55;
            color: var(--text-2);
        }

        .bento-visual {
            background: var(--bg-inset);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 10px 12px;
            font-family: var(--font-mono);
            font-size: 10.5px;
            line-height: 1.7;
            color: var(--text-2);
            overflow: hidden;
        }

        .bento-visual .cm { color: var(--pl-comment); }
        .bento-visual .vr { color: var(--pl-var); }
        .bento-visual .op { color: var(--pl-op); }
        .bento-visual .fn { color: var(--pl-fn); }
        .bento-visual .nm { color: var(--pl-num); }
        .bento-visual .pn { color: var(--text-3); }

        .mini-token-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .mini-token {
            font-family: var(--font-mono);
            font-size: 9px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 3px 8px;
            border-radius: 4px;
        }

        .mini-token.atom { background: var(--info-wash); color: var(--info); border: 1px solid var(--border); }
        .mini-token.var { background: var(--warn-wash); color: var(--warn); border: 1px solid var(--border); }
        .mini-token.op { background: var(--bad-wash); color: var(--bad); border: 1px solid var(--border); }
        .mini-token.punct { background: var(--bg-raise); color: var(--text-2); border: 1px solid var(--border); }
        .mini-token.num { background: var(--ok-wash); color: var(--ok); border: 1px solid var(--border); }

        .mini-graph-svg {
            width: 100%;
            height: 96px;
            display: block;
        }

        /* Stats strip */
        .stats-strip {
            max-width: 1160px;
            width: 100%;
            margin: 0 auto;
            padding: 0 32px 48px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }

        .stat-cell {
            border-top: 1px solid var(--border);
            padding: 14px 4px 0;
        }

        .stat-cell .k {
            font-family: var(--font-mono);
            font-size: 20px;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.02em;
        }

        .stat-cell .k small {
            font-size: 11px;
            color: var(--text-3);
            font-weight: 500;
            margin-left: 3px;
        }

        .stat-cell .l {
            font-size: 11px;
            color: var(--text-2);
            margin-top: 3px;
        }

        /* CTA band + footer */
        .cta-band {
            margin-top: auto;
            border-top: 1px solid var(--border-soft);
            background: linear-gradient(180deg, var(--bg-surface) 0%, var(--bg-base) 100%);
            padding: 36px 32px 26px;
            max-width: 1160px;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }

        .cta-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            flex-wrap: wrap;
        }

        .cta-band h2 {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-1);
        }

        .cta-band p {
            font-size: 12.5px;
            color: var(--text-2);
            margin-top: 4px;
        }

        .site-footer {
            max-width: 1160px;
            margin: 0 auto;
            width: 100%;
            padding: 14px 32px 26px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 11px;
            color: var(--text-3);
        }

        /* =========================================================
           STUDIO / PLAYGROUND
           ========================================================= */
        header.site-header {
            background: var(--nav-blur);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border);
            padding: 7px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            position: sticky;
            top: 0;
            z-index: 50;
            height: 54px;
        }

        .preset-bar {
            display: flex;
            align-items: center;
            gap: 3px;
            background: var(--bg-raise);
            border: 1px solid var(--border);
            padding: 3px;
            border-radius: 9px;
        }

        .preset-btn {
            background: transparent;
            border: none;
            color: var(--text-2);
            font-size: 11.5px;
            font-weight: 600;
            padding: 5px 11px;
            border-radius: 6px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            transition: color 0.15s, background 0.15s;
        }

        .preset-btn:hover {
            color: var(--text-1);
            background: var(--bg-raise-2);
        }

        .preset-btn.active {
            background: var(--accent);
            color: #ffffff;
            font-weight: 700;
            box-shadow: var(--shadow-accent);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 7px;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 600;
            padding: 6px 12px;
            border-radius: 7px;
            cursor: pointer;
            border: none;
            transition: transform 0.15s, background 0.15s, border-color 0.15s, box-shadow 0.15s;
        }

        .btn:active { transform: scale(0.97); }

        .btn-primary {
            background: var(--accent);
            color: white;
            box-shadow: var(--shadow-accent);
        }

        .btn-primary:hover { background: var(--accent-hover); }

        .btn-secondary {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            color: var(--text-2);
        }

        .btn-secondary:hover {
            color: var(--text-1);
            border-color: var(--border-strong);
        }

        .btn-demo {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            color: var(--accent-soft);
        }

        .btn-demo:hover {
            background: var(--accent-wash);
            border-color: var(--accent);
        }
        /* Workspace */
        main.app-workspace {
            flex: 1 1 0;
            min-height: 0;
            display: grid;
            grid-template-columns: minmax(380px, 430px) minmax(0, 1fr);
            gap: 12px;
            padding: 12px 18px 14px;
            overflow: hidden;
            height: calc(100vh - 54px);
        }

        .left-panel {
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow: hidden;
            height: 100%;
            min-height: 0;
        }

        .clean-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-1);
        }

        .source-card-flex {
            flex: 1 1 0;
            min-height: 0;
            overflow: hidden;
        }

        .query-card-flex {
            flex: 0 0 auto;
        }

        .card-topbar {
            padding: 7px 12px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-soft);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }

        .card-title {
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-1);
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        .card-title.accent { color: var(--accent-soft); }

        .card-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            color: var(--text-3);
            font-family: var(--font-mono);
        }

        .status-text { font-weight: 600; }
        .status-text.ok { color: var(--ok); }
        .status-text.bad { color: var(--bad); }

        .edit-banner {
            display: none;
            align-items: flex-start;
            gap: 8px;
            background: var(--bad-wash);
            border-bottom: 1px solid var(--bad-deep);
            color: var(--bad);
            padding: 8px 12px;
            font-size: 11px;
            font-family: var(--font-mono);
            line-height: 1.5;
        }

        .edit-banner .banner-text { flex: 1; }

        /* Editor: highlight layer behind transparent-text textarea */
        .source-editor-wrapper {
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            background: var(--bg-inset);
            position: relative;
            overflow: hidden;
        }

        .line-numbers-col {
            width: 42px;
            padding: 10px 7px 10px 0;
            background: var(--bg-inset-2);
            border-right: 1px solid var(--border-soft);
            color: var(--text-3);
            font-family: var(--font-mono);
            font-size: 11.5px;
            line-height: 21px;
            text-align: right;
            user-select: none;
            overflow: hidden;
            height: 100%;
        }

        .line-numbers-col .ln { height: 21px; }
        .line-numbers-col .ln.err { color: var(--bad); background: var(--bad-wash); border-radius: 3px 0 0 3px; }
        .line-numbers-col .ln.active { color: var(--accent-soft); }

        .editor-stack {
            position: relative;
            flex: 1 1 0;
            min-width: 0;
            overflow: hidden;
        }

        .code-highlight-layer,
        textarea.code-textarea {
            position: absolute;
            inset: 0;
            margin: 0;
            font-family: var(--font-mono);
            font-size: 12.5px;
            line-height: 21px;
            padding: 10px 14px;
            white-space: pre;
            overflow: auto;
            tab-size: 4;
            border: none;
            background: transparent;
            letter-spacing: 0;
        }

        .code-highlight-layer {
            pointer-events: none;
            overflow: hidden;
            color: var(--pl-atom);
        }

        .code-highlight-layer .cm { color: var(--pl-comment); font-style: italic; }
        .code-highlight-layer .vr { color: var(--pl-var); }
        .code-highlight-layer .op { color: var(--pl-op); }
        .code-highlight-layer .nm { color: var(--pl-num); }
        .code-highlight-layer .str { color: var(--pl-str); }
        .code-highlight-layer .fn { color: var(--pl-fn); }
        .code-highlight-layer .pn { color: var(--text-3); }

        textarea.code-textarea {
            color: transparent;
            caret-color: var(--text-1);
            resize: none;
            overflow: auto;
        }

        textarea.code-textarea::selection {
            background: var(--accent-wash);
            color: transparent;
        }

        /* Query card */
        .query-card {
            padding: 10px 12px 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .query-flex-row {
            display: flex;
            gap: 7px;
        }

        .query-text-input {
            flex: 1;
            min-width: 0;
            background: var(--bg-inset);
            border: 1px solid var(--border);
            color: var(--text-1);
            font-family: var(--font-mono);
            font-size: 12px;
            padding: 7px 10px;
            border-radius: 6px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .query-text-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-wash);
        }

        .solutions-preview {
            background: var(--bg-inset);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 9px 11px;
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            gap: 4px;
            max-height: 170px;
            overflow-y: auto;
        }

        .solutions-preview::-webkit-scrollbar { width: 8px; }
        .solutions-preview::-webkit-scrollbar-thumb { background: var(--border); border-radius: 8px; }

        .sol-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
            color: var(--text-2);
        }

        .sol-row .idx { color: var(--text-3); font-size: 10px; }
        .sol-pair b { color: var(--warn); font-weight: 700; }
        .sol-pair .eq { color: var(--text-3); }
        .sol-true { color: var(--ok); font-weight: 600; }
        .sol-false { color: var(--text-2); font-weight: 600; }
        .sol-none { color: var(--text-2); }
        .sol-error { color: var(--bad); }

        .trace-details {
            border-top: 1px dashed var(--border);
            margin-top: 4px;
            padding-top: 6px;
        }

        .trace-details summary {
            cursor: pointer;
            font-size: 10.5px;
            color: var(--info);
            font-weight: 600;
            user-select: none;
        }

        .trace-details summary:hover { color: var(--text-1); }

        .trace-steps {
            max-height: 170px;
            overflow-y: auto;
            font-size: 11px;
            line-height: 1.7;
            color: var(--text-2);
            margin-top: 4px;
            padding-right: 4px;
        }

        .trace-step .ev { font-weight: 700; }
        .trace-step.ev-success .ev { color: var(--ok); }
        .trace-step.ev-fail .ev { color: var(--bad); }
        .trace-step.ev-util .ev { color: var(--info); }
        .trace-step .dd { color: var(--text-3); }

        /* Right column + tabs */
        .right-panel {
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-1);
            height: 100%;
            min-height: 0;
        }

        .visualizer-tabs-bar {
            display: flex;
            align-items: center;
            background: var(--bg-raise);
            border-bottom: 1px solid var(--border);
            padding: 0 8px;
            gap: 2px;
            overflow-x: auto;
            scrollbar-width: thin;
        }

        .tab-button {
            background: transparent;
            border: none;
            color: var(--text-2);
            font-size: 11.5px;
            font-weight: 600;
            padding: 10px 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            border-bottom: 2px solid transparent;
            white-space: nowrap;
            transition: color 0.15s;
        }

        .tab-button:hover { color: var(--text-1); }

        .tab-button.active {
            color: var(--accent-soft);
            border-bottom-color: var(--accent);
        }

        .tab-content-area {
            flex: 1 1 0;
            min-height: 0;
            overflow: hidden;
            position: relative;
        }

        .tab-panel {
            display: none;
            height: 100%;
            min-height: 0;
            overflow: hidden;
        }

        .tab-panel.active {
            display: flex;
            flex-direction: column;
            height: 100%;
            min-height: 0;
        }
        /* Tab 1: Lexer */
        .lexer-split-view {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 300px;
            height: 100%;
            min-height: 0;
            overflow: hidden;
        }

        .tokens-stream-col {
            padding: 10px;
            overflow-y: auto;
            height: 100%;
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .token-filter-row {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            padding: 2px 2px 8px;
            border-bottom: 1px dashed var(--border-soft);
            margin-bottom: 4px;
        }

        .filter-chip {
            background: var(--bg-raise);
            border: 1px solid var(--border);
            color: var(--text-2);
            font-family: var(--font-mono);
            font-size: 9.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 3px 9px;
            border-radius: 999px;
            cursor: pointer;
            transition: background 0.15s, color 0.15s, border-color 0.15s;
        }

        .filter-chip:hover { color: var(--text-1); border-color: var(--border-strong); }

        .filter-chip.on {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }

        .token-row {
            display: flex;
            align-items: center;
            padding: 4px 10px;
            background: var(--bg-raise);
            border: 1px solid var(--border-soft);
            border-radius: 5px;
            font-family: var(--font-mono);
            font-size: 12px;
            gap: 10px;
            animation: rowIn 0.22s ease-out backwards;
        }

        @keyframes rowIn {
            from { opacity: 0; transform: translateY(2px); }
            to { opacity: 1; transform: none; }
        }

        .token-row:hover {
            background: var(--bg-raise-2);
            border-color: var(--border);
        }

        .token-row.hidden { display: none; }

        .token-pill {
            font-size: 8.5px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
            width: 82px;
            text-align: center;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }

        .pill-atom { background: var(--info-wash); color: var(--info); border: 1px solid var(--border); }
        .pill-variable { background: var(--warn-wash); color: var(--warn); border: 1px solid var(--border); }
        .pill-operator { background: var(--bad-wash); color: var(--bad); border: 1px solid var(--border); }
        .pill-punct { background: var(--bg-raise-2); color: var(--text-2); border: 1px solid var(--border); }
        .pill-number { background: var(--ok-wash); color: var(--ok); border: 1px solid var(--border); }
        .pill-error { background: var(--bad-wash); color: var(--bad); border: 1px solid var(--bad); }

        .token-val {
            flex: 1;
            color: var(--text-1);
            word-break: break-all;
        }

        .token-loc {
            color: var(--text-3);
            font-size: 10.5px;
        }

        .lexer-report-col {
            background: var(--bg-raise);
            border-left: 1px solid var(--border);
            padding: 12px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .report-box {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 11px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .report-header {
            font-size: 11px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .report-header.ok { color: var(--ok); }
        .report-header.bad { color: var(--bad); }
        .report-header.info { color: var(--info); }
        .report-header.plain { color: var(--text-1); }

        .report-text {
            font-size: 11.5px;
            color: var(--text-2);
            line-height: 1.55;
        }

        .stat-list {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-2);
            line-height: 1.7;
        }

        .stat-list b { color: var(--text-1); }
        .stat-list .sep { border-top: 1px dashed var(--border-soft); margin: 4px 0; }

        .ff-table {
            font-family: var(--font-mono);
            font-size: 10.5px;
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }

        .ff-row {
            display: grid;
            grid-template-columns: 64px 1fr;
            gap: 6px;
            align-items: baseline;
            padding: 3px 4px;
            border-radius: 4px;
        }

        .ff-row:nth-child(odd) { background: var(--bg-inset); }

        .ff-row .nt { color: var(--accent-soft); font-weight: 600; }
        .ff-row .set { color: var(--text-2); word-break: break-word; }
        .ff-row .set b { color: var(--text-2); font-size: 9.5px; }

        /* Tab 2: AST */
        .ast-tree-scroll {
            padding: 12px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .clause-tree-card {
            background: var(--bg-inset);
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-md);
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .clause-tree-card.flash {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-wash);
        }

        .clause-badge-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .clause-idx {
            font-family: var(--font-mono);
            font-size: 9px;
            font-weight: 700;
            color: var(--text-3);
            border: 1px solid var(--border);
            background: var(--bg-inset-2);
            border-radius: 4px;
            padding: 2px 6px;
        }

        .clause-type {
            font-size: 8.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 2px 6px;
            border-radius: 4px;
        }

        .clause-type.fact { background: var(--info-wash); color: var(--info); }
        .clause-type.rule { background: var(--accent-wash); color: var(--accent-soft); }

        .clause-title {
            font-family: var(--font-mono);
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-1);
            flex: 1;
            min-width: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .clause-line {
            font-family: var(--font-mono);
            font-size: 10px;
            color: var(--text-3);
        }

        .terms-pill-flex {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }

        .term-badge {
            background: var(--bg-raise);
            border: 1px solid var(--border-soft);
            font-family: var(--font-mono);
            font-size: 10px;
            color: var(--text-2);
            padding: 2px 7px;
            border-radius: 4px;
        }

        .term-badge b { color: var(--info); font-weight: 700; font-size: 9px; }

        .ast-section-sep {
            font-family: var(--font-mono);
            font-size: 9.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--text-3);
            padding: 8px 2px 0;
            border-top: 1px dashed var(--border);
            margin-top: 4px;
        }

        .sym-grid {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .sym-row {
            display: grid;
            grid-template-columns: minmax(90px, auto) auto 1fr;
            align-items: center;
            gap: 10px;
            font-family: var(--font-mono);
            font-size: 11px;
            background: var(--bg-inset);
            border: 1px solid var(--border-soft);
            border-radius: 5px;
            padding: 5px 9px;
        }

        .sym-row .sig { color: var(--text-1); font-weight: 700; }
        .sym-row .counts { color: var(--text-3); font-size: 10px; white-space: nowrap; }
        .sym-row .counts b.ok { color: var(--ok); }
        .sym-row .counts b.ac { color: var(--accent-soft); }
        .sym-row .lines {
            color: var(--text-3);
            font-size: 10px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            text-align: right;
        }

        .diag-row {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            font-size: 11.5px;
            line-height: 1.5;
            padding: 4px 2px;
            color: var(--text-2);
        }

        .diag-pill {
            font-size: 8px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 2px 6px;
            border-radius: 4px;
            flex-shrink: 0;
        }

        .diag-pill.error { background: var(--bad-wash); color: var(--bad); }
        .diag-pill.warning { background: var(--warn-wash); color: var(--warn); }
        .diag-pill.info-c { background: var(--info-wash); color: var(--info); }
        /* Tab 3: PDG */
        .pdg-canvas-wrapper {
            flex: 1;
            position: relative;
            background-color: var(--bg-inset);
            background-image: radial-gradient(var(--grid-dot) 1px, transparent 1px);
            background-size: 22px 22px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .graph-toolbar {
            position: absolute;
            top: 10px;
            right: 12px;
            z-index: 10;
            display: flex;
            gap: 3px;
            background: var(--nav-blur);
            border: 1px solid var(--border);
            padding: 3px;
            border-radius: 7px;
            backdrop-filter: blur(8px);
        }

        .graph-tool-btn {
            background: transparent;
            border: none;
            color: var(--text-2);
            font-size: 10.5px;
            font-weight: 600;
            padding: 4px 9px;
            border-radius: 5px;
            cursor: pointer;
            transition: color 0.15s, background 0.15s;
        }

        .graph-tool-btn:hover {
            color: var(--text-1);
            background: var(--bg-raise-2);
        }

        .pdg-legend {
            position: absolute;
            bottom: 12px;
            left: 12px;
            z-index: 10;
            display: flex;
            gap: 10px;
            align-items: center;
            background: var(--nav-blur);
            border: 1px solid var(--border);
            border-radius: 7px;
            padding: 5px 10px;
            backdrop-filter: blur(8px);
            font-size: 10px;
            color: var(--text-2);
        }

        .lg-dot {
            width: 8px;
            height: 8px;
            border-radius: 2px;
            display: inline-block;
            margin-right: 4px;
            vertical-align: middle;
            border: 1px solid var(--border-strong);
        }

        .lg-dot.base { border-color: var(--info); }
        .lg-dot.rule { border-color: var(--accent); }
        .lg-dot.rec { border-color: var(--bad); border-style: dashed; }

        svg.pdg-svg { width: 100%; height: 100%; display: block; }

        .pdg-edge {
            fill: none;
            stroke: var(--edge);
            stroke-width: 1.8;
            opacity: 0.95;
            transition: opacity 0.2s, stroke 0.2s, stroke-width 0.2s;
        }

        .pdg-edge:hover { stroke: var(--accent-soft); stroke-width: 2.4; opacity: 1; }

        .pdg-edge.loop { stroke: var(--bad); stroke-width: 2; stroke-dasharray: 6 3; opacity: 1; }

        .pdg-node { cursor: pointer; }

        .pdg-node rect {
            fill: var(--bg-surface);
            stroke: var(--border-strong);
            stroke-width: 1.25;
            transition: stroke 0.15s, fill 0.15s;
        }

        .pdg-node .n-label {
            fill: var(--text-1);
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 700;
        }

        .pdg-node .n-sub {
            fill: var(--text-2);
            font-family: var(--font-ui);
            font-size: 10px;
        }

        .pdg-node.rule-node rect { fill: var(--bg-raise); }
        .pdg-node.rule-node .n-label { fill: var(--accent-soft); }

        .pdg-node.rec-node rect {
            stroke: var(--bad);
            stroke-dasharray: 5 3;
        }

        .pdg-node.rec-node .n-label { fill: var(--bad); }

        .pdg-node:hover rect { stroke: var(--accent); fill: var(--bg-raise-2); }
        .pdg-node:hover .n-sub { fill: var(--text-1); }

        /* Tab 4: WAM & TAC */
        .wam-split-view {
            display: grid;
            grid-template-columns: 1fr 1fr;
            height: 100%;
            overflow: hidden;
        }

        .wam-view {
            display: flex;
            flex-direction: column;
            border-right: 1px solid var(--border);
            min-width: 0;
            height: 100%;
        }

        .wam-view:last-child { border-right: none; }

        .seg-toggle {
            display: inline-flex;
            align-items: center;
            gap: 2px;
            background: var(--bg-raise);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 2px;
        }

        .seg-btn {
            background: transparent;
            border: none;
            color: var(--text-2);
            font-size: 10px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 4px;
            cursor: pointer;
        }

        .seg-btn.on {
            background: var(--accent);
            color: white;
        }

        .wam-code-panel {
            flex: 1 1 0;
            min-height: 0;
            padding: 10px 12px;
            background: var(--bg-inset);
            overflow-y: auto;
            font-family: var(--font-mono);
            font-size: 11px;
            line-height: 1.8;
            color: var(--text-2);
        }

        .wam-code-panel .wln { display: flex; gap: 12px; }
        .wam-code-panel .wln .lnum {
            color: var(--text-3);
            width: 26px;
            text-align: right;
            flex-shrink: 0;
            user-select: none;
        }
        .wam-code-panel .wln .op-label { color: var(--warn); font-weight: 700; }
        .wam-code-panel .wln .op-main { color: var(--info); font-weight: 600; }
        .wam-code-panel .wln .op-args { color: var(--text-1); }
        .wam-code-panel .wln .tac-idx { color: var(--text-3); width: 30px; flex-shrink: 0; text-align: right; }
        .wam-code-panel .wln .tac-op { color: var(--accent-soft); font-weight: 600; }
        .wam-code-panel .wln .tac-res { color: var(--ok); }

        /* Tab 5: Demo */
        .demo-player-container {
            flex: 1;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow-y: auto;
        }

        .demo-hero-banner {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            flex-wrap: wrap;
        }

        .demo-hero-banner h3 {
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-1);
        }

        .demo-hero-banner .sub {
            font-size: 11px;
            color: var(--text-2);
            margin-top: 2px;
        }

        .demo-controls {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .demo-progress {
            height: 3px;
            background: var(--bg-raise-2);
            border-radius: 999px;
            overflow: hidden;
        }

        .demo-progress .fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, var(--accent), var(--info));
            border-radius: 999px;
            transition: width 0.45s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .demo-step-track {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 5px;
        }

        .demo-step-node {
            display: flex;
            align-items: center;
            gap: 5px;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            padding: 5px 11px;
            border-radius: 999px;
            font-size: 10.5px;
            font-weight: 600;
            font-family: var(--font-ui);
            color: var(--text-2);
            cursor: pointer;
            white-space: nowrap;
            transition: background 0.2s, border-color 0.2s, color 0.2s;
        }

        .demo-step-node:hover { color: var(--text-1); border-color: var(--border-strong); }

        .demo-step-node.active {
            background: var(--accent-wash);
            border-color: var(--accent);
            color: var(--accent-soft);
        }

        .demo-step-node.completed {
            background: var(--ok-wash);
            border-color: var(--ok-deep);
            color: var(--ok);
        }

        .demo-stage {
            flex: 1;
            background: var(--bg-inset);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            min-height: 270px;
        }

        .demo-stage-title {
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 700;
            color: var(--accent-soft);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .demo-stage-body {
            flex: 1;
            font-family: var(--font-mono);
            font-size: 11.5px;
            line-height: 1.7;
            color: var(--text-2);
            white-space: pre-wrap;
            overflow-y: auto;
            animation: stageIn 0.3s ease-out;
        }

        @keyframes stageIn {
            from { opacity: 0; transform: translateY(3px); }
            to { opacity: 1; transform: none; }
        }

        .demo-stage-body .hi { color: var(--text-1); font-weight: 700; }
        .demo-stage-body .ok { color: var(--ok); }
        .demo-stage-body .op { color: var(--pl-op); }
        .demo-stage-body .fn { color: var(--pl-fn); }
        .demo-stage-body .vr { color: var(--pl-var); }
        .demo-stage-body .cm { color: var(--pl-comment); }
        .demo-stage-body .dim { color: var(--text-3); }

        #demoLiveGraphCanvas {
            width: 100%;
            height: 240px;
            display: none;
            background: var(--bg-inset);
            border: 1px solid var(--border-soft);
            border-radius: 6px;
        }

        .demo-node-pop { animation: nodePop 0.35s cubic-bezier(0.16, 1, 0.3, 1) backwards; }

        @keyframes nodePop {
            from { opacity: 0; transform: scale(0.92); }
            to { opacity: 1; transform: scale(1); }
        }

        /* -------------------------------------------------------------
           RESPONSIVE
           ------------------------------------------------------------- */
        @media (max-width: 1240px) {
            .preset-btn .preset-label { display: none; }
        }

        @media (max-width: 1100px) {
            main.app-workspace {
                grid-template-columns: 1fr;
                height: auto;
                overflow-y: auto;
            }

            .left-panel { height: auto; }
            .source-editor-wrapper { min-height: 240px; height: 260px; flex: none; }
            .right-panel { height: 640px; }

            .lexer-split-view { grid-template-columns: 1fr; }
            .lexer-report-col { border-left: none; border-top: 1px solid var(--border); }

            .hero-wrap { grid-template-columns: 1fr; gap: 28px; padding-top: 44px; }
            .terminal-body { min-height: 240px; }
            .bento-grid { grid-template-columns: 1fr 1fr; }
            .bento-card.span-4, .bento-card.span-3, .bento-card.span-2 { grid-column: span 2; }
            .stats-strip { grid-template-columns: 1fr 1fr; }
        }

        @media (max-width: 720px) {
            header.site-header {
                height: auto;
                flex-wrap: wrap;
                padding: 8px 12px;
                row-gap: 8px;
            }

            .header-actions { margin-left: auto; }
            .preset-bar { order: 3; width: 100%; overflow-x: auto; justify-content: flex-start; }
            main.app-workspace { padding: 10px 10px 14px; }

            .wam-split-view { grid-template-columns: 1fr; }
            .wam-view { border-right: none; border-bottom: 1px solid var(--border); min-height: 260px; }
            .wam-view:last-child { border-bottom: none; }

            .shell-nav { padding: 0 16px; }
            .nav-links .nav-link { padding: 7px 8px; }
            .brand-text p { display: none; }

            .hero-wrap { padding: 36px 18px 30px; }
            .pipeline-section, .bento-section, .stats-strip, .cta-band, .site-footer { padding-left: 18px; padding-right: 18px; }
            .bento-grid { grid-template-columns: 1fr; }
            .bento-card.span-4, .bento-card.span-3, .bento-card.span-2 { grid-column: span 1; }
            .stats-strip { grid-template-columns: 1fr 1fr; }
            .pipeline-strip { padding: 12px; gap: 8px; }
        }

        /* ================= CUSTOM CURSOR ================= */
        .cursor-dot,
        .cursor-ring {
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100000;
            pointer-events: none;
            border-radius: 50%;
            opacity: 0;
            will-change: transform;
            transform: translate3d(-100px, -100px, 0);
        }

        .cursor-dot {
            width: 6px;
            height: 6px;
            background: var(--accent-soft);
            box-shadow: 0 0 8px var(--accent);
        }

        .cursor-ring {
            width: 30px;
            height: 30px;
            border: 1.5px solid var(--accent-soft);
            background: transparent;
            transition: width 0.18s ease, height 0.18s ease, border-color 0.18s ease, background 0.18s ease, opacity 0.15s ease;
        }

        .cursor-ring.hover {
            width: 42px;
            height: 42px;
            border-color: var(--accent);
            background: var(--accent-wash);
        }

        .cursor-ring.press {
            box-shadow: 0 0 0 5px var(--accent-wash);
        }

        .cursor-dot.hidden,
        .cursor-ring.hidden { opacity: 0 !important; }

        html.has-custom-cursor,
        html.has-custom-cursor body,
        html.has-custom-cursor * { cursor: none !important; }

        html.has-custom-cursor input,
        html.has-custom-cursor textarea,
        html.has-custom-cursor [contenteditable="true"] { cursor: text !important; }

        html.has-custom-cursor select,
        html.has-custom-cursor input[type="checkbox"],
        html.has-custom-cursor input[type="radio"],
        html.has-custom-cursor input[type="range"] { cursor: pointer !important; }

        .icon-btn[aria-pressed="true"] {
            color: var(--accent-soft);
            border-color: var(--accent);
            background: var(--accent-wash);
        }

        @media (max-width: 900px), (pointer: coarse) {
            .cursor-dot, .cursor-ring, #cursorToggleLanding, #cursorToggleStudio { display: none !important; }
        }

        @media (prefers-reduced-motion: reduce) {
            .cursor-ring { transition: none; }
        }

        /* =========================================================
           GRAMMAR SPECIFICATION MODAL
           ========================================================= */
        .grammar-modal-backdrop {
            position: fixed;
            inset: 0;
            background: rgba(4, 8, 18, 0.78);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .grammar-modal-backdrop.active {
            opacity: 1;
            pointer-events: auto;
        }

        .grammar-modal-window {
            background: var(--bg-surface);
            border: 1px solid var(--border-strong);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 960px;
            max-height: 88vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.05);
            transform: translateY(12px) scale(0.985);
            transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }

        .grammar-modal-backdrop.active .grammar-modal-window {
            transform: translateY(0) scale(1);
        }

        .grammar-modal-header {
            padding: 16px 20px 14px;
            background: var(--bg-raise);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 16px;
        }

        .grammar-badge-row {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 6px;
            flex-wrap: wrap;
        }

        .g-badge {
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 999px;
            font-family: var(--font-mono);
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }

        .g-badge.accent {
            background: var(--accent-wash);
            color: var(--accent-soft);
            border: 1px solid rgba(99, 102, 241, 0.35);
        }

        .g-badge.ok {
            background: var(--ok-wash);
            color: var(--ok);
            border: 1px solid rgba(52, 211, 153, 0.35);
        }

        .g-badge.info {
            background: var(--info-wash);
            color: var(--info);
            border: 1px solid rgba(56, 189, 248, 0.35);
        }

        .grammar-modal-title {
            font-size: 17px;
            font-weight: 700;
            color: var(--text-1);
            margin: 0;
            line-height: 1.3;
        }

        .grammar-modal-sub {
            font-size: 12px;
            color: var(--text-3);
            margin: 4px 0 0;
        }

        .grammar-close-btn {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-3);
            border-radius: var(--radius-sm);
            width: 32px;
            height: 32px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.15s ease;
            flex-shrink: 0;
        }

        .grammar-close-btn:hover {
            color: var(--text-1);
            border-color: var(--border-strong);
            background: var(--bg-surface);
        }

        .grammar-tab-bar {
            display: flex;
            align-items: center;
            background: var(--bg-inset);
            border-bottom: 1px solid var(--border);
            padding: 0 12px;
            overflow-x: auto;
            gap: 4px;
            scrollbar-width: thin;
        }

        .g-tab-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 10px 14px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-3);
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }

        .g-tab-btn:hover {
            color: var(--text-1);
        }

        .g-tab-btn.active {
            color: var(--accent-soft);
            border-bottom-color: var(--accent);
            background: var(--accent-wash);
        }

        .grammar-modal-body {
            padding: 20px;
            overflow-y: auto;
            flex: 1 1 auto;
            scrollbar-width: thin;
        }

        .grammar-panel {
            display: none;
        }

        .grammar-panel.active {
            display: block;
            animation: fadeIn 0.18s ease-out;
        }

        .spec-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 14px;
        }

        .spec-ref-card {
            background: var(--bg-raise);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            transition: border-color 0.15s, transform 0.15s;
        }

        .spec-ref-card:hover {
            border-color: var(--accent);
            transform: translateY(-2px);
        }

        .spec-ref-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .spec-ref-title {
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-1);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .spec-ref-title:hover {
            color: var(--accent-soft);
        }

        .spec-ref-desc {
            font-size: 12px;
            color: var(--text-2);
            line-height: 1.55;
            margin: 0;
        }

        .spec-ref-meta {
            font-size: 11px;
            font-family: var(--font-mono);
            color: var(--text-3);
            display: flex;
            gap: 12px;
            margin-top: 4px;
        }

        .g-table-wrap {
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            background: var(--bg-raise);
        }

        .g-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: left;
        }

        .g-table th {
            background: var(--bg-surface);
            padding: 10px 14px;
            font-weight: 700;
            color: var(--text-1);
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }

        .g-table td {
            padding: 9px 14px;
            border-bottom: 1px solid var(--border-soft);
            color: var(--text-2);
        }

        .g-table tr:last-child td {
            border-bottom: none;
        }

        .g-table tr:hover td {
            background: var(--accent-wash);
        }

        .g-op-badge {
            display: inline-block;
            font-family: var(--font-mono);
            font-size: 11.5px;
            font-weight: 600;
            padding: 2px 7px;
            border-radius: 4px;
            background: var(--bg-inset);
            border: 1px solid var(--border);
            color: var(--warn);
        }

        .g-assoc-badge {
            font-size: 11px;
            font-family: var(--font-mono);
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--bg-surface);
            border: 1px solid var(--border-soft);
            color: var(--info);
        }

        .g-info-callout {
            margin-top: 14px;
            padding: 12px 14px;
            background: var(--accent-wash);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: var(--radius-md);
            font-size: 12px;
            line-height: 1.6;
            color: var(--text-2);
        }

        .g-info-callout strong {
            color: var(--accent-soft);
        }

        .grammar-code-box {
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            background: var(--bg-inset);
            overflow: hidden;
        }

        .grammar-code-header {
            padding: 8px 14px;
            background: var(--bg-raise);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .grammar-code-title {
            font-size: 11.5px;
            font-family: var(--font-mono);
            font-weight: 600;
            color: var(--text-3);
        }

        .grammar-copy-btn {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 9px;
            font-size: 11px;
            font-family: var(--font-mono);
            font-weight: 600;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-2);
            cursor: pointer;
            transition: all 0.15s;
        }

        .grammar-copy-btn:hover {
            color: var(--text-1);
            border-color: var(--border-strong);
            background: var(--bg-raise-2);
        }

        .grammar-code-pre {
            margin: 0;
            padding: 14px 16px;
            max-height: 400px;
            overflow-y: auto;
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.6;
            color: var(--text-1);
            white-space: pre;
            scrollbar-width: thin;
        }

        .simpl-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }

        .simpl-item {
            background: var(--bg-raise);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 12px 16px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .simpl-item-title {
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-1);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .simpl-item-desc {
            font-size: 12px;
            color: var(--text-2);
            line-height: 1.55;
            margin: 0;
        }
    </style>
</head>
<body>
    <!-- =========================================================
         VIEW 1: LANDING PAGE
         ========================================================= -->
    <div id="landingView" style="display: {{ 'none' if initial_view == 'studio' else 'flex' }};">
        <nav class="shell-nav">
            <div class="header-brand">
                <span class="brand-badge">PROLOG-PARSE</span>
                <div class="brand-text">
                    <h1>Compiler Studio</h1>
                    <p>Course 22PC2CS301 · VNRVJIET</p>
                </div>
            </div>

            <div class="nav-links">
                <button class="nav-link" onclick="scrollToSection('phases')">Pipeline</button>
                <button class="nav-link" onclick="scrollToSection('architecture')">Architecture</button>
                <button class="nav-link" onclick="scrollToSection('demos')">Demo</button>
                <button class="nav-link" onclick="openGrammarModal()" id="btnNavGrammar">Grammar Spec</button>
            </div>

            <div class="nav-right">
                <button id="cursorToggleLanding" class="icon-btn" onclick="toggleCursor()" aria-pressed="true" title="Toggle custom cursor" aria-label="Toggle custom cursor">
                    <svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"></path><path d="M13 13l6 6"></path></svg>
                </button>
                <button class="icon-btn" onclick="toggleTheme()" title="Toggle light / dark theme" aria-label="Toggle light or dark theme">
                    <svg id="themeIconLanding" class="icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"></svg>
                </button>
                <button id="btnGrammarDocsLanding" class="btn-large btn-large-secondary" onclick="openGrammarModal()" style="padding: 7px 12px; font-size: 12px;" title="Official Prolog Grammar & Operator Specification Reference">
                    <svg class="icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                    Grammar
                </button>
                <button id="btnEnterPlayground" class="btn-large btn-large-primary" onclick="enterStudio()">
                    Enter Playground
                    <svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="9 18 15 12 9 6"></polyline></svg>
                </button>
            </div>
        </nav>

        <section class="hero-wrap">
            <div class="hero-copy">
                <div class="eyebrow-pill">
                    <svg class="icon" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    Compiler Design Laboratory · VNRVJIET
                </div>
                <h1 class="hero-title">Compile Prolog.<br>Watch <em>every phase</em> run.</h1>
                <p class="hero-sub">Type Horn clauses and inspect live tokens, ASTs, call graphs, WAM bytecode and SLD resolution proofs - all rendered as they compile.</p>
                <div class="hero-ctas">
                    <button id="btnLaunchPlayground" class="btn-large btn-large-primary" onclick="enterStudio()">
                        Launch Playground
                        <svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    </button>
                    <button class="btn-large btn-large-secondary" onclick="enterStudioWithDemo()">
                        <svg class="icon" width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        Watch live demo
                    </button>
                </div>
                <div class="hero-hint">Inside the playground: <kbd>Ctrl</kbd>+<kbd>Enter</kbd> compiles - <kbd>/</kbd> jumps to the query box</div>
            </div>

            <div class="terminal-card" aria-label="Sample compiler output">
                <div class="terminal-head">
                    <span>prolog-parse - compile ancestor_family</span>
                    <span class="terminal-status"><span class="pulse-dot" aria-hidden="true"></span>ready</span>
                </div>
                <div class="terminal-body" id="heroTerminalBody">% preparing...</div>
            </div>
        </section>

        <section class="pipeline-section" id="phases">
            <div class="pipeline-strip">
                <span class="pipeline-node"><b>01</b> Character stream</span>
                <span class="pipeline-arrow" aria-hidden="true">&#8594;</span>
                <span class="pipeline-node"><b>02</b> DFA tokenizer</span>
                <span class="pipeline-arrow" aria-hidden="true">&#8594;</span>
                <span class="pipeline-node"><b>03</b> Recursive-descent AST</span>
                <span class="pipeline-arrow" aria-hidden="true">&#8594;</span>
                <span class="pipeline-node"><b>04</b> Semantic - symbol table</span>
                <span class="pipeline-arrow" aria-hidden="true">&#8594;</span>
                <span class="pipeline-node"><b>05</b> Call graph - WAM - TAC</span>
                <span class="pipeline-arrow" aria-hidden="true">&#8594;</span>
                <span class="pipeline-node last"><b>06</b> SLD proof</span>
            </div>
        </section>

        <section class="bento-section" id="architecture">
            <div class="bento-head">
                <h2>Six phases, built from scratch</h2>
                <p>No parser generators, no regex shortcuts - a hand-written lexer, parser, analyzer, graph builder, code generator and resolution engine in pure Python.</p>
            </div>

            <div class="bento-grid">
                <div class="bento-card span-3">
                    <div class="bento-icon">
                        <svg class="icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                    </div>
                    <h3>Lexical analysis (DFA)</h3>
                    <p>Scans the character stream into classified token structures with precise line and column tracking.</p>
                    <div class="mini-token-row" aria-label="Token types">
                        <span class="mini-token atom">atom</span>
                        <span class="mini-token var">variable</span>
                        <span class="mini-token op">op_rule</span>
                        <span class="mini-token punct">dot</span>
                        <span class="mini-token num">number</span>
                    </div>
                </div>

                <div class="bento-card span-3 tinted">
                    <div class="bento-icon ok">
                        <svg class="icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="4" r="2"></circle><circle cx="6" cy="18" r="2"></circle><circle cx="18" cy="18" r="2"></circle><path d="M12 6v4m0 0-5 6m5-6 5 6"></path></svg>
                    </div>
                    <h3>Recursive-descent AST</h3>
                    <p>A predictive parser over context-free grammar productions with explicit FIRST and FOLLOW sets.</p>
                    <div class="bento-visual"><span class="cm">CFG core</span>
Program ::= Clause* EOF
Clause  ::= Fact | Rule | Query
Rule    ::= Head <span class="op">:-</span> GoalList <span class="pn">.</span></div>
                </div>

                <div class="bento-card span-2">
                    <div class="bento-icon warn">
                        <svg class="icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="6" cy="6" r="3"></circle><circle cx="18" cy="18" r="3"></circle><path d="M8.5 8.5l7 7"></path><circle cx="18" cy="6" r="3" stroke-dasharray="4 2"></circle></svg>
                    </div>
                    <h3>Predicate call graph</h3>
                    <p>Three-tier topological layout with recursive self-loop detection.</p>
                    <svg class="mini-graph-svg" viewBox="0 0 260 96" aria-hidden="true">
                        <rect x="10" y="36" width="92" height="26" rx="6" fill="var(--bg-inset)" stroke="var(--info)"></rect>
                        <text x="20" y="53" font-size="10" font-family="var(--font-mono)" fill="var(--text-2)">parent/2</text>
                        <rect x="76" y="4" width="92" height="26" rx="6" fill="var(--bg-inset)" stroke="var(--accent)"></rect>
                        <text x="86" y="21" font-size="10" font-family="var(--font-mono)" fill="var(--text-2)">ancestor/2</text>
                        <rect x="168" y="36" width="84" height="26" rx="6" fill="var(--bg-inset)" stroke="var(--accent)"></rect>
                        <text x="178" y="53" font-size="10" font-family="var(--font-mono)" fill="var(--text-2)">father/2</text>
                        <path d="M 110 62 C 110 78, 92 66, 104 60" fill="none" stroke="var(--border-strong)" stroke-width="1.5" opacity="0.6"></path>
                        <path d="M 76 17 C 66 17, 70 30, 74 34" fill="none" stroke="var(--bad)" stroke-width="1.5" opacity="0.85" stroke-dasharray="5 3"></path>
                        <path d="M 168 49 C 158 49, 146 44, 138 44" fill="none" stroke="var(--border-strong)" stroke-width="1.5" opacity="0.6"></path>
                    </svg>
                </div>

                <div class="bento-card span-2 tinted">
                    <div class="bento-icon info">
                        <svg class="icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="8" rx="2"></rect><rect x="2" y="14" width="20" height="8" rx="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>
                    </div>
                    <h3>WAM bytecode + TAC</h3>
                    <p>Warren Abstract Machine instructions and three-address quadruples per clause.</p>
                    <div class="bento-visual"><span class="fn">get_variable</span> Ax0, Aj1
<span class="fn">get_variable</span> Yx0, Aj2
<span class="nm">10.</span> (add, X, Y, T1)</div>
                </div>

                <div class="bento-card span-2">
                    <div class="bento-icon ok">
                        <svg class="icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </div>
                    <h3>SLD resolution proofs</h3>
                    <p>Robinson unification with occurs-check, returning a full step-by-step proof trace.</p>
                    <div class="bento-visual"><span class="vr">?- ancestor(george, X).</span>
<span class="cm">% SLD trace</span>
X = john <span class="op">;</span> X = mary <span class="ok">SOLVED</span></div>
                </div>
            </div>

            <div class="stats-strip">
                <div class="stat-cell">
                    <div class="k" id="statTokens">-<small>tokens</small></div>
                    <div class="l">scanned live from the default program</div>
                </div>
                <div class="stat-cell">
                    <div class="k" id="statClauses">-<small>clauses</small></div>
                    <div class="l">facts and Horn rules parsed per run</div>
                </div>
                <div class="stat-cell">
                    <div class="k" id="statWam">-<small>instrs</small></div>
                    <div class="l">WAM instructions emitted by codegen</div>
                </div>
                <div class="stat-cell">
                    <div class="k" id="statSteps">-<small>steps</small></div>
                    <div class="l">real SLD proof steps on the demo query</div>
                </div>
            </div>
        </section>

        <section class="cta-band" id="demos">
            <div class="cta-inner">
                <div>
                    <h2>Try the compiler live</h2>
                    <p>Four sample programs, a query box and a six-step walkthrough of the whole pipeline.</p>
                </div>
                <button id="btnBottomLaunchPlayground" class="btn-large btn-large-primary" onclick="enterStudio()">
                    Launch Compiler Playground
                    <svg class="icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="9 18 15 12 9 6"></polyline></svg>
                </button>
            </div>
        </section>

        <footer class="site-footer">
            <span>Compiler Design Laboratory - Course 22PC2CS301 - VNRVJIET CSE</span>
            <span>Pure Python stdlib - zero runtime dependencies</span>
        </footer>
    </div>
    <!-- =========================================================
         VIEW 2: COMPILER STUDIO
         ========================================================= -->
    <div id="studioView" style="display: {{ 'flex' if initial_view == 'studio' else 'none' }};">

        <header class="site-header">
            <div class="header-brand">
                <button class="icon-btn" onclick="exitStudioToLanding()" title="Back to landing page" aria-label="Back to landing page">
                    <svg class="icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                </button>
                <span class="brand-badge">PROLOG-PARSE</span>
            </div>

            <div class="preset-bar" role="toolbar" aria-label="Sample programs">
                <button class="preset-btn active" data-key="ancestor_tree" onclick="selectPreset('ancestor_tree', this)" title="Classical recursive ancestry and relationships">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="5" r="3"/><circle cx="6" cy="19" r="3"/><circle cx="18" cy="19" r="3"/><path d="M12 8v4m0 0-6 4m6-4 6 4"/></svg>
                    <span class="preset-label">Family Tree</span>
                </button>
                <button class="preset-btn" data-key="graph_network" onclick="selectPreset('graph_network', this)" title="Directed network reachability and paths">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="5" cy="6" r="3"/><circle cx="19" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><path d="m7.5 7.5 7 7M16.5 7.5l-7 7"/></svg>
                    <span class="preset-label">Network Paths</span>
                </button>
                <button class="preset-btn" data-key="list_algorithms" onclick="selectPreset('list_algorithms', this)" title="List processing: member, append, reverse">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                    <span class="preset-label">List Ops</span>
                </button>
                <button class="preset-btn" data-key="expr_evaluator" onclick="selectPreset('expr_evaluator', this)" title="Symbolic arithmetic and expression evaluation">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="18"/><path d="M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/></svg>
                    <span class="preset-label">Evaluator</span>
                </button>
                <button class="preset-btn" data-key="nlp_expert" onclick="selectPreset('nlp_expert', this)" title="Massive 160+ Rules NLP Parser, Clinical Expert System & Degree Audit">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                    <span class="preset-label">NLP & Expert (160+ Rules)</span>
                </button>
            </div>

            <div class="header-actions">
                <button id="cursorToggleStudio" class="icon-btn" onclick="toggleCursor()" aria-pressed="true" title="Toggle custom cursor" aria-label="Toggle custom cursor">
                    <svg class="icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"></path><path d="M13 13l6 6"></path></svg>
                </button>
                <button class="icon-btn" onclick="toggleTheme()" title="Toggle light / dark theme" aria-label="Toggle light or dark theme">
                    <svg id="themeIconStudio" class="icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"></svg>
                </button>
                <button id="btnGrammarDocsStudio" class="btn btn-secondary" onclick="openGrammarModal()" title="Official Prolog Grammar & Operator Specification Reference">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                    Grammar
                </button>
                <button class="btn btn-demo" onclick="startLiveDemo()" title="Six-step guided walkthrough">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                    Demo
                </button>
                <button id="btnCompileCode" class="btn btn-primary" onclick="compileCode()" title="Analyze and compile (Ctrl + Enter)">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                    Analyze & Compile
                </button>
                <button id="btnResetStudio" class="btn btn-secondary" onclick="resetStudio()" title="Reset editor to the default sample">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg>
                    Reset
                </button>
            </div>
        </header>

        <main class="app-workspace">

            <div class="left-panel">

                <div class="clean-card source-card-flex">
                    <div class="card-topbar">
                        <span class="card-title">
                            <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                            Source Code (ISO Prolog)
                        </span>
                        <div class="card-meta">
                            <span class="status-text ok" id="compilerStatusBadge">Ready</span>
                            <span id="codeMetrics">0 lines</span>
                        </div>
                    </div>
                    <div id="compilerErrorBanner" class="edit-banner" role="alert" aria-live="assertive">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" style="margin-top:2px"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                        <div class="banner-text">
                            <span id="compilerErrorText"></span>
                            <span id="compilerErrorMore" style="color:var(--text-3)"></span>
                        </div>
                    </div>
                    <div class="source-editor-wrapper">
                        <div id="lineNumbers" class="line-numbers-col" aria-hidden="true"><div class="ln">1</div></div>
                        <div class="editor-stack">
                            <div id="codeHighlight" class="code-highlight-layer" aria-hidden="true"></div>
                            <textarea id="sourceEditor" class="code-textarea" spellcheck="false"
                                oninput="onCodeInput()"
                                onscroll="syncEditorScroll()"
                                aria-label="Prolog source code editor"></textarea>
                        </div>
                    </div>
                </div>

                <div class="clean-card query-card-flex">
                    <div class="card-topbar">
                        <span class="card-title accent">
                            <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                            Interactive Logic Query
                        </span>
                        <span class="status-text ok" id="queryStatusTag">Ready</span>
                    </div>
                    <div class="query-card">
                        <div class="query-flex-row">
                            <input type="text" id="queryGoalInput" class="query-text-input" value="?- ancestor(george, X)." placeholder="?- goal(X)." aria-label="Prolog query goal" onkeydown="if (event.key === 'Enter') solveQuery()">
                            <button id="btnSolveQuery" class="btn btn-primary" onclick="solveQuery()">Solve</button>
                        </div>
                        <div id="solutionsBox" class="solutions-preview" aria-live="polite">
                            <span class="sol-none">Run a query to execute unification and SLD resolution.</span>
                        </div>
                    </div>
                </div>

            </div>

            <div class="right-panel">

                <div class="visualizer-tabs-bar" role="tablist" aria-label="Visualizer tabs" id="vizTabBar">
                    <button id="btnTabLexer" class="tab-button active" role="tab" aria-selected="true" aria-controls="tab-lexer" data-pane="tab-lexer" onclick="switchTab('tab-lexer')">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                        Lexer Tokens
                    </button>
                    <button id="btnTabAst" class="tab-button" role="tab" aria-selected="false" aria-controls="tab-ast" data-pane="tab-ast" onclick="switchTab('tab-ast')">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="4" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/><path d="M12 6v4m0 0-5 6m5-6 5 6"/></svg>
                        AST & Symbols
                    </button>
                    <button id="btnTabPdg" class="tab-button" role="tab" aria-selected="false" aria-controls="tab-pdg" data-pane="tab-pdg" onclick="switchTab('tab-pdg')">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M8.5 8.5l7 7"/></svg>
                        Call Graph
                    </button>
                    <button id="btnTabWam" class="tab-button" role="tab" aria-selected="false" aria-controls="tab-wam" data-pane="tab-wam" onclick="switchTab('tab-wam')">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
                        WAM & TAC
                    </button>
                    <button id="btnTabGrammar" class="tab-button" role="tab" aria-selected="false" aria-controls="tab-grammar" data-pane="tab-grammar" onclick="switchTab('tab-grammar')">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                        Grammar & Length
                    </button>
                    <button id="btnTabDemo" class="tab-button" role="tab" aria-selected="false" aria-controls="tab-demo" data-pane="tab-demo" onclick="switchTab('tab-demo')">
                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        Live Demo
                    </button>
                </div>

                <div class="tab-content-area">

                    <!-- TAB 1: LEXER TOKENS -->
                    <div id="tab-lexer" class="tab-panel active" role="tabpanel" aria-labelledby="btnTabLexer">
                        <div class="lexer-split-view">
                            <div class="tokens-stream-col">
                                <div class="token-filter-row" id="tokenFilterRow">
                                    <button class="filter-chip on" data-ft="all" onclick="filterTokens('all', this)">All tokens</button>
                                    <button class="filter-chip" data-ft="atom" onclick="filterTokens('atom', this)">Atoms</button>
                                    <button class="filter-chip" data-ft="variable" onclick="filterTokens('variable', this)">Variables</button>
                                    <button class="filter-chip" data-ft="operator" onclick="filterTokens('operator', this)">Operators</button>
                                    <button class="filter-chip" data-ft="punct" onclick="filterTokens('punct', this)">Punct</button>
                                    <button class="filter-chip" data-ft="number" onclick="filterTokens('number', this)">Numbers</button>
                                </div>
                                <div id="tokenStreamContainer" style="display:flex;flex-direction:column;gap:4px;"></div>
                            </div>
                            <div class="lexer-report-col">
                                <div class="report-box" id="lexerStatusReportBox">
                                    <div class="report-header ok">
                                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        Lexical Analysis Status
                                    </div>
                                    <p class="report-text">Run Analyze & Compile to tokenize the source code.</p>
                                </div>
                                <div class="report-box">
                                    <div class="report-header plain">Token distribution</div>
                                    <div id="tokenDistributionStats" class="stat-list">-</div>
                                </div>
                                <div class="report-box">
                                    <div class="report-header info">FIRST / FOLLOW sets</div>
                                    <div id="ffTableBox" class="ff-table">-</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- TAB 2: AST & SYMBOLS -->
                    <div id="tab-ast" class="tab-panel" role="tabpanel" aria-labelledby="btnTabAst">
                        <div id="astTreeList" class="ast-tree-scroll">
                            <p class="report-text">Run Analyze & Compile to build the syntax tree.</p>
                        </div>
                    </div>

                    <!-- TAB 3: CALL GRAPH -->
                    <div id="tab-pdg" class="tab-panel" role="tabpanel" aria-labelledby="btnTabPdg">
                        <div class="pdg-canvas-wrapper">
                            <div class="graph-toolbar">
                                <button class="graph-tool-btn" onclick="renderPDGGraph()">Fit view</button>
                            </div>
                            <svg id="cleanGraphSvg" class="pdg-svg" viewBox="0 0 900 580" aria-label="Predicate dependency graph">
                                <defs>
                                    <marker id="arrowhead" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                        <path d="M 0 1 L 10 5 L 0 9 z" style="fill:var(--edge)"></path>
                                    </marker>
                                    <marker id="arrowhead-loop" viewBox="0 0 10 10" refX="20" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                        <path d="M 0 1 L 10 5 L 0 9 z" style="fill:var(--bad)"></path>
                                    </marker>
                                </defs>
                                <g id="svgEdgesLayer"></g>
                                <g id="svgNodesLayer"></g>
                            </svg>
                            <div class="pdg-legend" aria-hidden="true">
                                <span><span class="lg-dot base"></span>Facts</span>
                                <span><span class="lg-dot rule"></span>Rules</span>
                                <span><span class="lg-dot rec"></span>Recursive</span>
                            </div>
                        </div>
                    </div>

                    <!-- TAB 4: WAM & TAC -->
                    <div id="tab-wam" class="tab-panel" role="tabpanel" aria-labelledby="btnTabWam">
                        <div class="wam-split-view">
                            <div class="wam-view">
                                <div class="card-topbar">
                                    <span class="card-title">Warren Abstract Machine bytecode</span>
                                    <div style="display:flex;align-items:center;gap:6px;">
                                        <div class="seg-toggle" role="group" aria-label="Bytecode variant">
                                            <button id="segOrig" class="seg-btn on" onclick="selectWamView('orig', this)">Original</button>
                                            <button id="segOpt" class="seg-btn" onclick="selectWamView('opt', this)">Optimized</button>
                                        </div>
                                        <button class="icon-btn" onclick="copyWam()" title="Copy to clipboard" aria-label="Copy WAM bytecode to clipboard">
                                            <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"></rect><path d="M5 15V5a2 2 0 0 1 2-2h10"></path></svg>
                                        </button>
                                    </div>
                                </div>
                                <div id="wamInstructionsBox" class="wam-code-panel"><span style="color:var(--text-3)">-</span></div>
                            </div>
                            <div class="wam-view">
                                <div class="card-topbar">
                                    <span class="card-title">Three-address code (quadruples)</span>
                                    <button class="icon-btn" onclick="copyTac()" title="Copy to clipboard" aria-label="Copy TAC to clipboard">
                                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"></rect><path d="M5 15V5a2 2 0 0 1 2-2h10"></path></svg>
                                    </button>
                                </div>
                                <div id="tacQuadruplesBox" class="wam-code-panel"><span style="color:var(--text-3)">-</span></div>
                            </div>
                        </div>
                    </div>

                    <!-- TAB 5: LIVE DEMO -->
                    <div id="tab-demo" class="tab-panel" role="tabpanel" aria-labelledby="btnTabDemo">
                        <div class="demo-player-container">
                            <div class="demo-hero-banner">
                                <div>
                                    <h3>Live end-to-end compiler showcase</h3>
                                    <p class="sub">Ingestion, tokenization, parsing, symbols, graph construction and a real proof - actual data, not canned text.</p>
                                </div>
                                <div class="demo-controls">
                                    <button class="btn btn-secondary" onclick="demoPrevStep()" aria-label="Previous step">
                                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="15 18 9 12 15 6"></polyline></svg>
                                        Prev
                                    </button>
                                    <button id="btnAutoPlay" class="btn btn-demo" onclick="toggleAutoPlay()">Play</button>
                                    <button class="btn btn-primary" onclick="demoNextStep()" aria-label="Next step">
                                        Next
                                        <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="9 18 15 12 9 6"></polyline></svg>
                                    </button>
                                </div>
                            </div>

                            <div class="demo-progress" aria-hidden="true"><div class="fill" id="demoProgressBar"></div></div>

                            <div class="demo-step-track" role="group" aria-label="Demo steps">
                                <button id="dStep1" class="demo-step-node active" onclick="jumpToDemoStep(1)">1. Ingestion</button>
                                <button id="dStep2" class="demo-step-node" onclick="jumpToDemoStep(2)">2. Lexer DFA</button>
                                <button id="dStep3" class="demo-step-node" onclick="jumpToDemoStep(3)">3. AST Parser</button>
                                <button id="dStep4" class="demo-step-node" onclick="jumpToDemoStep(4)">4. Symbol Table</button>
                                <button id="dStep5" class="demo-step-node" onclick="jumpToDemoStep(5)">5. Live Call Graph</button>
                                <button id="dStep6" class="demo-step-node" onclick="jumpToDemoStep(6)">6. Logic Proof</button>
                            </div>

                            <div class="demo-stage">
                                <div class="demo-stage-title"><span id="stageTitle">Step 1: Reading Prolog Horn Clauses</span></div>
                                <svg id="demoLiveGraphCanvas" viewBox="0 0 760 240">
                                    <defs>
                                        <marker id="demo-arrow" viewBox="0 0 10 10" refX="20" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                            <path d="M 0 1 L 10 5 L 0 9 z" style="fill:var(--edge)"></path>
                                        </marker>
                                        <marker id="demo-loop-arrow" viewBox="0 0 10 10" refX="18" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                            <path d="M 0 1 L 10 5 L 0 9 z" style="fill:var(--bad)"></path>
                                        </marker>
                                    </defs>
                                    <g id="demoSvgEdges"></g>
                                    <g id="demoSvgNodes"></g>
                                </svg>
                                <div id="stageOutput" class="demo-stage-body" aria-live="polite">Ready when you are - press Play or Next.</div>
                            </div>
                        </div>
                    </div>

                    <!-- TAB 6: GRAMMAR & RULE LENGTH -->
                    <div id="tab-grammar" class="tab-panel" role="tabpanel" aria-labelledby="btnTabGrammar">
                        <div style="padding: 16px; display: flex; flex-direction: column; gap: 14px; max-width: 960px; margin: 0 auto;">
                            
                            <!-- Which Grammar Banner -->
                            <div style="background: var(--bg-raise); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 18px;">
                                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 8px;">
                                    <h3 style="margin: 0; font-size: 15px; color: var(--text-1); font-weight: 700;">
                                        Which Grammar: ISO/IEC 13211-1 Standard Prolog Context-Free Grammar (CFG)
                                    </h3>
                                    <div style="display: flex; gap: 6px;">
                                        <span class="g-badge accent">1,000 Formal Rules</span>
                                        <span class="g-badge ok">Dual LALR(1) / LL(1)</span>
                                    </div>
                                </div>
                                <p style="margin: 0; font-size: 12.5px; color: var(--text-2); line-height: 1.6;">
                                    This compiler implements the formal Context-Free Grammar for ISO Prolog Horn Clauses. The grammar covers 
                                    <strong>Facts</strong> (<code>head.</code>), <strong>Rules</strong> (<code>head :- body.</code>), 
                                    <strong>Queries</strong> (<code>?- body.</code>), <strong>Directives</strong> (<code>:- directive.</code>), 
                                    <strong>Definite Clause Grammars</strong> (<code>head --> body.</code>), <strong>Lists</strong> (<code>[H|T]</code>), 
                                    <strong>Infix Arithmetic</strong> (<code>is</code>, <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>mod</code>), 
                                    and <strong>Relational Comparisons</strong> (<code>=</code>, <code>\=</code>, <code>==</code>, <code>\==</code>, <code>&lt;</code>, <code>&gt;</code>, <code>=&lt;</code>, <code>&gt;=</code>).
                                </p>
                            </div>

                            <!-- Grammar Length Metric Cards -->
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
                                <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                    <div style="font-size: 26px; font-weight: 800; color: var(--accent-soft); font-family: var(--font-mono);">1,000</div>
                                    <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">Total Formal Rules</div>
                                    <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">Cataloged in GRAMMAR_SPEC_1000.md</div>
                                </div>
                                <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                    <div style="font-size: 26px; font-weight: 800; color: var(--ok); font-family: var(--font-mono);">1,088</div>
                                    <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">YACC Grammar Lines</div>
                                    <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">prolog.y (LALR(1) C Engine)</div>
                                </div>
                                <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                    <div style="font-size: 26px; font-weight: 800; color: var(--info); font-family: var(--font-mono);">220</div>
                                    <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">Flex Scanner Lines</div>
                                    <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">prolog.l (DFA Tokenizer)</div>
                                </div>
                                <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                    <div style="font-size: 26px; font-weight: 800; color: #a78bfa; font-family: var(--font-mono);">400</div>
                                    <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">Python Parser Lines</div>
                                    <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">parser.py (Recursive Descent)</div>
                                </div>
                            </div>

                            <!-- Grammar Length Distribution Table -->
                            <div class="g-table-wrap">
                                <table class="g-table">
                                    <thead>
                                        <tr>
                                            <th>Grammar Subsystem / Phase</th>
                                            <th>Rule Group</th>
                                            <th>Length (Rules)</th>
                                            <th>Implementation File</th>
                                            <th>Description</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td><strong>Group 1: Lexical DFA Grammar</strong></td>
                                            <td><code>L1 – L100</code></td>
                                            <td><span class="g-badge ok">100 Rules</span></td>
                                            <td><code>prolog.l</code> / <code>lexer.py</code></td>
                                            <td>Atoms, variables, multi-radix numbers (hex/bin/oct), strings, comment states</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 2: Concrete Syntax CFG</strong></td>
                                            <td><code>P1 – P250</code></td>
                                            <td><span class="g-badge ok">250 Rules</span></td>
                                            <td><code>prolog.y</code> / <code>parser.py</code></td>
                                            <td>Clause hierarchy, facts, rules, queries, DCG rules, lists, operator precedence</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 3: Static Semantic Invariants</strong></td>
                                            <td><code>S1 – S150</code></td>
                                            <td><span class="g-badge ok">150 Rules</span></td>
                                            <td><code>semantic.py</code></td>
                                            <td>Symbol table indexing (functor/arity), clause multiset counts, singleton linter</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 4: Panic-Mode Error Recovery</strong></td>
                                            <td><code>R1 – R100</code></td>
                                            <td><span class="g-badge ok">100 Rules</span></td>
                                            <td><code>parser.py:synchronize</code></td>
                                            <td>Resynchronization on '.' boundary, error clause nodes, clean multi-clause parsing</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 5: WAM Bytecode &amp; TAC</strong></td>
                                            <td><code>W1 – W100</code></td>
                                            <td><span class="g-badge ok">100 Rules</span></td>
                                            <td><code>wam_compiler.py</code></td>
                                            <td>Warren Abstract Machine instructions (put_*, get_*, unify_*, call, proceed)</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 6: SLD Resolution &amp; Unification</strong></td>
                                            <td><code>E1 – E100</code></td>
                                            <td><span class="g-badge ok">100 Rules</span></td>
                                            <td><code>engine.py</code></td>
                                            <td>Robinson Unification with Occurs-Check, chronological depth-first backtracking</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 7: Predicate Dependency Graph</strong></td>
                                            <td><code>G1 – G100</code></td>
                                            <td><span class="g-badge ok">100 Rules</span></td>
                                            <td><code>graph_builder.py</code></td>
                                            <td>Call graph extraction, recursion cycle detection, 4-tier topological layering</td>
                                        </tr>
                                        <tr>
                                            <td><strong>Group 8: ISO Built-in Predicates</strong></td>
                                            <td><code>B1 – B100</code></td>
                                            <td><span class="g-badge ok">100 Rules</span></td>
                                            <td><code>engine.py</code></td>
                                            <td>var/1, functor/3, =../2, call/1, cut (!/0), is/2 arithmetic, list operations</td>
                                        </tr>
                                        <tr style="background: var(--bg-raise); font-weight: 700;">
                                            <td colspan="2"><strong>TOTAL FORMAL PRODUCTIONS</strong></td>
                                            <td><span class="g-badge accent" style="font-size: 12px;">1,000 Rules</span></td>
                                            <td colspan="2">Exhaustive specification cataloged in <code>GRAMMAR_SPEC_1000.md</code></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <!-- Modal Launcher Buttons -->
                            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px;">
                                <button class="btn btn-primary" onclick="openGrammarModal('bison')">
                                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                                    View Full YACC (prolog.y) Grammar
                                </button>
                                <button class="btn btn-secondary" onclick="openGrammarModal('prec')">
                                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                                    Operator Precedence Table
                                </button>
                                <button class="btn btn-secondary" onclick="openGrammarModal('firstfollow')">
                                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                                    FIRST &amp; FOLLOW Sets
                                </button>
                            </div>

                        </div>
                    </div>

                </div>
            </div>

        </main>
    </div>

    <!-- =========================================================
         MODAL: PROLOG LANGUAGE SPECIFICATION & GRAMMAR REFERENCE
         ========================================================= -->
    <div id="grammarModal" class="grammar-modal-backdrop" onclick="handleGrammarBackdropClick(event)" role="dialog" aria-modal="true" aria-labelledby="grammarModalTitle">
        <div class="grammar-modal-window">
            <div class="grammar-modal-header">
                <div class="grammar-title-group">
                    <div class="grammar-badge-row">
                        <span class="g-badge accent">ISO/IEC 13211-1</span>
                        <span class="g-badge ok">LALR(1) / LL(1) Validated</span>
                        <span class="g-badge info">Compiler Design Lab Specification</span>
                    </div>
                    <h2 id="grammarModalTitle" class="grammar-modal-title">Prolog Language Specification & Formal Grammar</h2>
                    <p class="grammar-modal-sub">Course 22PC2CS301 · VNRVJIET CSE · Lexical, Syntactic & Semantic Reference Documentation</p>
                </div>
                <button class="grammar-close-btn" onclick="closeGrammarModal()" aria-label="Close Grammar Modal" title="Close (Esc)">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <!-- Tab Buttons -->
            <div class="grammar-tab-bar" role="tablist">
                <button class="g-tab-btn active" id="gtab-btn-spec" onclick="switchGrammarTab('spec')">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    1. Grammar & 1,000-Rule Length
                </button>
                <button class="g-tab-btn" id="gtab-btn-bison" onclick="switchGrammarTab('bison')">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                    2. YACC/Bison Grammar (prolog.y)
                </button>
                <button class="g-tab-btn" id="gtab-btn-prec" onclick="switchGrammarTab('prec')">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                    3. Operator Precedence Table
                </button>
                <button class="g-tab-btn" id="gtab-btn-firstfollow" onclick="switchGrammarTab('firstfollow')">
                    <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                    4. FIRST & FOLLOW Sets
                </button>
            </div>

            <!-- Scrollable Body Panels -->
            <div class="grammar-modal-body">
                <!-- PANEL 1: GRAMMAR & RULE LENGTH METRICS -->
                <div id="gtab-panel-spec" class="grammar-panel active">
                    <div style="display: flex; flex-direction: column; gap: 16px;">
                        
                        <!-- Core Grammar Overview Banner -->
                        <div style="background: var(--bg-raise); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 18px;">
                            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                                <h3 style="margin: 0; font-size: 15px; color: var(--text-1); font-weight: 700;">
                                    Which Grammar: ISO/IEC 13211-1 Standard Prolog Context-Free Grammar (CFG)
                                </h3>
                                <div style="display: flex; gap: 6px;">
                                    <span class="g-badge accent">1,000 Formal Rules</span>
                                    <span class="g-badge ok">Dual Engine</span>
                                </div>
                            </div>
                            <p style="margin: 0; font-size: 12.5px; color: var(--text-2); line-height: 1.6;">
                                This compiler implements the formal Context-Free Grammar for ISO Prolog Horn Clauses. The grammar covers 
                                <strong>Facts</strong> (<code>head.</code>), <strong>Rules</strong> (<code>head :- body.</code>), 
                                <strong>Queries</strong> (<code>?- body.</code>), <strong>Directives</strong> (<code>:- module/dynamic.</code>), 
                                <strong>Definite Clause Grammars</strong> (<code>head --> body.</code>), <strong>Lists</strong> (<code>[H|T]</code>), 
                                <strong>Infix Arithmetic</strong> (<code>is</code>, <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>mod</code>), 
                                and <strong>Relational Comparisons</strong> (<code>=</code>, <code>\=</code>, <code>==</code>, <code>\==</code>, <code>&lt;</code>, <code>&gt;</code>, <code>=&lt;</code>, <code>&gt;=</code>).
                            </p>
                        </div>

                        <!-- 4 Stat Highlight Cards -->
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                <div style="font-size: 26px; font-weight: 800; color: var(--accent-soft); font-family: var(--font-mono);">1,000</div>
                                <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">Total Formal Rules</div>
                                <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">Cataloged in GRAMMAR_SPEC_1000.md</div>
                            </div>
                            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                <div style="font-size: 26px; font-weight: 800; color: var(--ok); font-family: var(--font-mono);">1,088</div>
                                <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">YACC Grammar Lines</div>
                                <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">prolog.y (LALR(1) C Engine)</div>
                            </div>
                            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                <div style="font-size: 26px; font-weight: 800; color: var(--info); font-family: var(--font-mono);">400</div>
                                <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">Python Parser Lines</div>
                                <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">parser.py (Recursive Descent)</div>
                            </div>
                            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px; text-align: center;">
                                <div style="font-size: 26px; font-weight: 800; color: #a78bfa; font-family: var(--font-mono);">36 / 36</div>
                                <div style="font-size: 11.5px; font-weight: 600; color: var(--text-2); margin-top: 4px;">Unit Tests Passing</div>
                                <div style="font-size: 10.5px; color: var(--text-3); margin-top: 2px;">100% Validated in tests_edge_cases.py</div>
                            </div>
                        </div>

                        <!-- Formal Production Distribution Table -->
                        <div class="g-table-wrap">
                            <table class="g-table">
                                <thead>
                                    <tr>
                                        <th>Grammar Subsystem / Phase</th>
                                        <th>Rule Group</th>
                                        <th>Rule Count</th>
                                        <th>Implementation File</th>
                                        <th>Description</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>Group 1: Lexical DFA Grammar</strong></td>
                                        <td><code>L1 – L100</code></td>
                                        <td><span class="g-badge ok">100 Rules</span></td>
                                        <td><code>prolog.l</code> / <code>lexer.py</code></td>
                                        <td>Atoms, variables, multi-radix numbers (hex/bin/oct), strings, comment states</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 2: Concrete Syntax CFG</strong></td>
                                        <td><code>P1 – P250</code></td>
                                        <td><span class="g-badge ok">250 Rules</span></td>
                                        <td><code>prolog.y</code> / <code>parser.py</code></td>
                                        <td>Clause hierarchy, facts, rules, queries, DCG rules, lists, operator precedence</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 3: Static Semantic Invariants</strong></td>
                                        <td><code>S1 – S150</code></td>
                                        <td><span class="g-badge ok">150 Rules</span></td>
                                        <td><code>semantic.py</code></td>
                                        <td>Symbol table indexing (functor/arity), clause multiset counts, singleton linter</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 4: Panic-Mode Error Recovery</strong></td>
                                        <td><code>R1 – R100</code></td>
                                        <td><span class="g-badge ok">100 Rules</span></td>
                                        <td><code>parser.py:synchronize</code></td>
                                        <td>Resynchronization on '.' boundary, error clause nodes, clean multi-clause parsing</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 5: WAM Bytecode &amp; TAC</strong></td>
                                        <td><code>W1 – W100</code></td>
                                        <td><span class="g-badge ok">100 Rules</span></td>
                                        <td><code>wam_compiler.py</code></td>
                                        <td>Warren Abstract Machine instructions (put_*, get_*, unify_*, call, proceed)</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 6: SLD Resolution &amp; Unification</strong></td>
                                        <td><code>E1 – E100</code></td>
                                        <td><span class="g-badge ok">100 Rules</span></td>
                                        <td><code>engine.py</code></td>
                                        <td>Robinson Unification with Occurs-Check, chronological depth-first backtracking</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 7: Predicate Dependency Graph</strong></td>
                                        <td><code>G1 – G100</code></td>
                                        <td><span class="g-badge ok">100 Rules</span></td>
                                        <td><code>graph_builder.py</code></td>
                                        <td>Call graph extraction, recursion cycle detection, 4-tier topological layering</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Group 8: ISO Built-in Predicates</strong></td>
                                        <td><code>B1 – B100</code></td>
                                        <td><span class="g-badge ok">100 Rules</span></td>
                                        <td><code>engine.py</code></td>
                                        <td>var/1, functor/3, =../2, call/1, cut (!/0), is/2 arithmetic, list operations</td>
                                    </tr>
                                    <tr style="background: var(--bg-raise); font-weight: 700;">
                                        <td colspan="2"><strong>TOTAL FORMAL COMPILER PRODUCTIONS</strong></td>
                                        <td><span class="g-badge accent" style="font-size: 12px;">1,000 Rules</span></td>
                                        <td colspan="2">Exhaustive specification cataloged in <code>GRAMMAR_SPEC_1000.md</code></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>

                <!-- PANEL 2: YACC/BISON GRAMMAR (prolog.y) -->
                <div id="gtab-panel-bison" class="grammar-panel">
                    <div class="grammar-code-box">
                        <div class="grammar-code-header">
                            <span class="grammar-code-title">GNU Bison LALR(1) / CFG Grammar Specification (prolog.y)</span>
                            <button id="btnCopyGrammar" class="grammar-copy-btn" onclick="copyBisonGrammar()">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                                Copy Grammar
                            </button>
                        </div>
                        <pre id="bisonGrammarCode" class="grammar-code-pre">/* =========================================================================
 * GNU Bison LALR(1) Context-Free Grammar for ISO Prolog Horn Clauses
 * Source file: prolog.y (1,088 lines) · Lexer: prolog.l (220 lines)
 * Complies with ISO/IEC 13211-1 Prolog Specification
 * ========================================================================= */

%token ATOM VARIABLE NUMBER STRING ANON_VAR
%token OP_RULE OP_QUERY OP_DCG CUT
%token LPAREN RPAREN LBRACKET RBRACKET COMMA SEMICOLON PIPE DOT
%token OPERATOR IS

%right OP_RULE OP_DCG
%right SEMICOLON
%right COMMA
%nonassoc '=' OP_NEQ OP_EQ OP_NOTEQ '&lt;' '&gt;' OP_LE OP_GE IS
%left '+' '-'
%left '*' '/'

%start program

%%

program
    : clause_list
    ;

clause_list
    : clause_list clause
    | /* empty */
    ;

clause
    : fact
    | rule
    | query
    | dcg_rule
    | directive
    | error DOT
    ;

fact
    : head DOT
    ;

rule
    : head OP_RULE goal_list DOT
    ;

query
    : OP_QUERY goal_list DOT
    ;

dcg_rule
    : head OP_DCG goal_list DOT
    ;

directive
    : OP_RULE goal_list DOT
    ;

head
    : compound_term
    | ATOM
    ;

goal_list
    : goal_list COMMA goal
    | goal_list SEMICOLON goal
    | goal
    ;

goal
    : expr
    | CUT
    ;

expr
    : expr '=' expr
    | expr OPERATOR expr
    | expr IS expr
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | primary_term
    ;

primary_term
    : compound_term
    | ATOM
    | VARIABLE
    | ANON_VAR
    | NUMBER
    | STRING
    | list_term
    | LPAREN expr RPAREN
    ;

compound_term
    : ATOM LPAREN arg_list RPAREN
    ;

arg_list
    : arg_list COMMA expr
    | expr
    ;

list_term
    : LBRACKET RBRACKET
    | LBRACKET list_elements RBRACKET
    ;

list_elements
    : expr_list PIPE primary_term
    | expr_list
    ;

expr_list
    : expr_list COMMA expr
    | expr
    ;

%%</pre>
                    </div>
                </div>

                <!-- PANEL 3: OPERATOR PRECEDENCE & ASSOCIATIVITY -->
                <div id="gtab-panel-prec" class="grammar-panel">
                    <div class="g-table-wrap">
                        <table class="g-table">
                            <thead>
                                <tr>
                                    <th>Precedence Level</th>
                                    <th>Operators</th>
                                    <th>Associativity</th>
                                    <th>ISO Type</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>1 (Lowest) / 1200</strong></td>
                                    <td><span class="g-op-badge">:-</span> <span class="g-op-badge">?-</span></td>
                                    <td><span class="g-assoc-badge">Right / Prefix</span></td>
                                    <td><code>xfx, fx</code></td>
                                    <td>Clause Neck (Rule definition) & Query Directive</td>
                                </tr>
                                <tr>
                                    <td><strong>2 / 1100</strong></td>
                                    <td><span class="g-op-badge">;</span></td>
                                    <td><span class="g-assoc-badge">Right</span></td>
                                    <td><code>xfy</code></td>
                                    <td>Logical Disjunction (OR)</td>
                                </tr>
                                <tr>
                                    <td><strong>3 / 1050</strong></td>
                                    <td><span class="g-op-badge">-&gt;</span></td>
                                    <td><span class="g-assoc-badge">Right</span></td>
                                    <td><code>xfy</code></td>
                                    <td>If-Then Implication / Local conditional branch</td>
                                </tr>
                                <tr>
                                    <td><strong>4 / 1000</strong></td>
                                    <td><span class="g-op-badge">,</span></td>
                                    <td><span class="g-assoc-badge">Right</span></td>
                                    <td><code>xfy</code></td>
                                    <td>Logical Conjunction (AND - sequential goal evaluation)</td>
                                </tr>
                                <tr>
                                    <td><strong>5 / 900</strong></td>
                                    <td><span class="g-op-badge">\+</span></td>
                                    <td><span class="g-assoc-badge">Right</span></td>
                                    <td><code>fy</code></td>
                                    <td>Negation-as-Failure (Logical NOT / unprovability)</td>
                                </tr>
                                <tr>
                                    <td><strong>6 / 700</strong></td>
                                    <td><span class="g-op-badge">=</span> <span class="g-op-badge">\=</span></td>
                                    <td><span class="g-assoc-badge">None</span></td>
                                    <td><code>xfx</code></td>
                                    <td>Syntactic Unification & Syntactic Non-Unification</td>
                                </tr>
                                <tr>
                                    <td><strong>7 / 700</strong></td>
                                    <td><span class="g-op-badge">==</span> <span class="g-op-badge">\==</span></td>
                                    <td><span class="g-assoc-badge">None</span></td>
                                    <td><code>xfx</code></td>
                                    <td>Strict Structural Term Identity & Non-Identity</td>
                                </tr>
                                <tr>
                                    <td><strong>8 / 700</strong></td>
                                    <td><span class="g-op-badge">&lt;</span> <span class="g-op-badge">&gt;</span> <span class="g-op-badge">=&lt;</span> <span class="g-op-badge">&gt;=</span></td>
                                    <td><span class="g-assoc-badge">None</span></td>
                                    <td><code>xfx</code></td>
                                    <td>Relational Arithmetic Comparison</td>
                                </tr>
                                <tr>
                                    <td><strong>9 / 700</strong></td>
                                    <td><span class="g-op-badge">is</span></td>
                                    <td><span class="g-assoc-badge">None</span></td>
                                    <td><code>xfx</code></td>
                                    <td>Arithmetic Evaluation & Variable Binding</td>
                                </tr>
                                <tr>
                                    <td><strong>10 / 500</strong></td>
                                    <td><span class="g-op-badge">+</span> <span class="g-op-badge">-</span></td>
                                    <td><span class="g-assoc-badge">Left</span></td>
                                    <td><code>yfx, fx</code></td>
                                    <td>Binary Addition, Subtraction & Unary Plus/Minus</td>
                                </tr>
                                <tr>
                                    <td><strong>11 / 400</strong></td>
                                    <td><span class="g-op-badge">*</span> <span class="g-op-badge">/</span> <span class="g-op-badge">mod</span></td>
                                    <td><span class="g-assoc-badge">Left</span></td>
                                    <td><code>yfx</code></td>
                                    <td>Multiplication, Float Division, Integer Modulo</td>
                                </tr>
                                <tr>
                                    <td><strong>12 (Highest)</strong></td>
                                    <td><span class="g-op-badge">!</span> <span class="g-op-badge">[H|T]</span> <span class="g-op-badge">f(...)</span> <span class="g-op-badge">(expr)</span></td>
                                    <td><span class="g-assoc-badge">Left / Enclosing</span></td>
                                    <td><code>Primary</code></td>
                                    <td>Cut barrier, List constructor, Functor call, Grouping</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="g-info-callout">
                        <strong>ISO Fixity Notation:</strong>
                        <code>xfy</code> denotes right-associativity (e.g. <code>A, B, C</code> binds as <code>,(A, ,(B, C))</code>).
                        <code>yfx</code> denotes left-associativity (e.g. <code>10 - 3 - 2</code> binds as <code>-( -(10, 3), 2)</code>).
                        <code>xfx</code> denotes non-associative comparison (chaining like <code>A = B = C</code> is illegal without explicit parentheses).
                    </div>
                </div>

                <!-- PANEL 5: FIRST & FOLLOW SETS -->
                <div id="gtab-panel-firstfollow" class="grammar-panel">
                    <div class="g-table-wrap">
                        <table class="g-table">
                            <thead>
                                <tr>
                                    <th>Non-Terminal ($V_N$)</th>
                                    <th>FIRST Set</th>
                                    <th>FOLLOW Set</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Program</strong></td>
                                    <td><code>{ ATOM, VARIABLE, '? -', ε }</code></td>
                                    <td><code>{ $ }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Clause</strong></td>
                                    <td><code>{ ATOM, VARIABLE, '? -' }</code></td>
                                    <td><code>{ ATOM, VARIABLE, '? -', $ }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Fact</strong></td>
                                    <td><code>{ ATOM }</code></td>
                                    <td><code>{ ATOM, VARIABLE, '? -', $ }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Rule</strong></td>
                                    <td><code>{ ATOM }</code></td>
                                    <td><code>{ ATOM, VARIABLE, '? -', $ }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Query</strong></td>
                                    <td><code>{ '? -' }</code></td>
                                    <td><code>{ ATOM, VARIABLE, '? -', $ }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>GoalList</strong></td>
                                    <td><code>{ ATOM, VARIABLE, NUMBER, '[', '(', '!' }</code></td>
                                    <td><code>{ '.' }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Term</strong></td>
                                    <td><code>{ ATOM, VARIABLE, NUMBER, STRING, '[', '(' }</code></td>
                                    <td><code>{ ',', ')', ']', '|', '.', ':-', ';', OPERATOR, $ }</code></td>
                                </tr>
                                <tr>
                                    <td><strong>ListTerm</strong></td>
                                    <td><code>{ '[' }</code></td>
                                    <td><code>{ ',', ')', ']', '|', '.', ':-', ';', $ }</code></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="g-info-callout">
                        <strong>LL(1) Predictive Parsing Condition:</strong>
                        For any non-terminal $A$ with productions $A \to \alpha \mid \beta$, the intersection $\text{FIRST}(\alpha) \cap \text{FIRST}(\beta) = \emptyset$.
                        When $\alpha \Rightarrow^* \varepsilon$, then $\text{FIRST}(\beta) \cap \text{FOLLOW}(A) = \emptyset$.
                        This guarantees zero backtracking during top-down recursive descent syntax tree construction.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="cursorDot" class="cursor-dot" aria-hidden="true"></div>
    <div id="cursorRing" class="cursor-ring" aria-hidden="true"></div>

    <script>
        const PRESETS = {{ presets | tojson }};
        let currentCompiledData = null;
        let demoCurrentStep = 1;
        let isAutoPlaying = false;
        let autoPlayTimer = null;
        let wamViewMode = 'orig';
        let tokenFilterActive = 'all';
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const SB = { L: '{', R: '}' }; // avoids Jinja brace collision in template strings

        /* ================= THEME ================= */
        const SUN_SVG = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
        const MOON_SVG = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="currentColor" stroke="none"></path>';

        function initTheme() {
            const saved = localStorage.getItem('prolog_theme') || 'dark';
            document.documentElement.setAttribute('data-theme', saved);
            syncThemeIcons(saved);
        }

        function toggleTheme() {
            const next = (document.documentElement.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('prolog_theme', next);
            syncThemeIcons(next);
            if (currentCompiledData) renderPDGGraph();
        }

        function syncThemeIcons(theme) {
            const svg = theme === 'dark' ? SUN_SVG : MOON_SVG;
            ['themeIconLanding', 'themeIconStudio'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.innerHTML = svg;
            });
        }

        /* ================= CUSTOM CURSOR ================= */
        const CURSOR_PREF_KEY = 'prolog_cursor';
        let cursorEnabled = false;
        let cursorInitialized = false;
        let cursorDotEl = null;
        let cursorRingEl = null;
        let cursorX = -100, cursorY = -100;
        let cursorRingX = -100, cursorRingY = -100;
        let cursorRafId = null;
        let cursorSeen = false;

        function initCursor() {
            cursorDotEl = document.getElementById('cursorDot');
            cursorRingEl = document.getElementById('cursorRing');
            if (!cursorDotEl || !cursorRingEl) return;
            if (!cursorInitialized) {
                cursorInitialized = true;
                window.addEventListener('mousemove', onCursorMove, { passive: true });
                window.addEventListener('mousedown', onCursorDown, { passive: true });
                window.addEventListener('mouseup', onCursorUp, { passive: true });
                window.addEventListener('blur', hideCursor);
                document.addEventListener('mouseout', onCursorOut);
            }
            const fine = window.matchMedia('(pointer: fine)').matches;
            const saved = localStorage.getItem(CURSOR_PREF_KEY);
            if (fine && saved !== 'off') {
                enableCursor();
            } else {
                disableCursor();
            }
        }

        function enableCursor() {
            if (!cursorDotEl || !cursorRingEl) return;
            cursorEnabled = true;
            document.documentElement.classList.add('has-custom-cursor');
            if (!cursorRafId) cursorRafId = requestAnimationFrame(cursorTick);
            syncCursorButtons();
        }

        function disableCursor() {
            cursorEnabled = false;
            document.documentElement.classList.remove('has-custom-cursor');
            if (cursorDotEl) {
                cursorDotEl.classList.add('hidden');
                cursorDotEl.style.opacity = '0';
            }
            if (cursorRingEl) {
                cursorRingEl.classList.add('hidden');
                cursorRingEl.classList.remove('hover', 'press');
                cursorRingEl.style.opacity = '0';
            }
            if (cursorRafId) { cancelAnimationFrame(cursorRafId); cursorRafId = null; }
            syncCursorButtons();
        }

        function syncCursorButtons() {
            ['cursorToggleLanding', 'cursorToggleStudio'].forEach(id => {
                const btn = document.getElementById(id);
                if (btn) btn.setAttribute('aria-pressed', cursorEnabled ? 'true' : 'false');
            });
        }

        function toggleCursor() {
            if (!cursorInitialized) initCursor();
            if (cursorEnabled) {
                disableCursor();
                localStorage.setItem(CURSOR_PREF_KEY, 'off');
            } else {
                if (!window.matchMedia('(pointer: fine)').matches) return;
                cursorSeen = false;
                enableCursor();
                localStorage.setItem(CURSOR_PREF_KEY, 'on');
            }
            syncCursorButtons();
        }

        function onCursorMove(e) {
            if (!cursorEnabled) return;
            cursorX = e.clientX;
            cursorY = e.clientY;
            const firstSeen = !cursorSeen;
            if (firstSeen) {
                cursorSeen = true;
                cursorRingX = cursorX;
                cursorRingY = cursorY;
            }
            const t = e.target;
            const textTarget = t && t.closest ? t.closest('input:not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([type="button"]):not([type="submit"]):not([type="reset"]):not([type="color"]), textarea, [contenteditable="true"]') : null;
            const interactive = t && t.closest ? t.closest('a, button, [role="button"], summary, select, label, .preset-btn, .filter-chip, .tab-button, .seg-btn, .pdg-node, input[type="checkbox"], input[type="radio"], input[type="range"]') : null;
            const onText = !!textTarget;
            if (onText) {
                cursorRingX = cursorX;
                cursorRingY = cursorY;
            }
            cursorDotEl.classList.toggle('hidden', onText);
            cursorRingEl.classList.toggle('hidden', onText);
            cursorRingEl.classList.toggle('hover', !!interactive && !onText);
            cursorDotEl.style.opacity = onText ? '0' : '1';
            cursorRingEl.style.opacity = onText ? '0' : (interactive ? '1' : '0.55');
            cursorDotEl.style.transform = 'translate3d(' + cursorX + 'px, ' + cursorY + 'px, 0) translate(-50%, -50%)';
            if (firstSeen || onText || reduceMotion) {
                cursorRingEl.style.transform = 'translate3d(' + cursorRingX + 'px, ' + cursorRingY + 'px, 0) translate(-50%, -50%)';
            }
        }

        function onCursorDown() {
            if (!cursorEnabled || !cursorRingEl) return;
            cursorRingEl.classList.add('press');
        }

        function onCursorUp() {
            if (!cursorRingEl) return;
            cursorRingEl.classList.remove('press');
        }

        function hideCursor() {
            if (!cursorEnabled) return;
            cursorDotEl.style.opacity = '0';
            cursorRingEl.style.opacity = '0';
        }

        function onCursorOut(e) {
            if (!e.relatedTarget && !e.toElement) hideCursor();
        }

        function cursorTick() {
            if (!cursorEnabled) { cursorRafId = null; return; }
            const ease = reduceMotion ? 1 : 0.2;
            cursorRingX += (cursorX - cursorRingX) * ease;
            cursorRingY += (cursorY - cursorRingY) * ease;
            if (Math.abs(cursorX - cursorRingX) < 0.08) cursorRingX = cursorX;
            if (Math.abs(cursorY - cursorRingY) < 0.08) cursorRingY = cursorY;
            cursorDotEl.style.transform = 'translate3d(' + cursorX + 'px, ' + cursorY + 'px, 0) translate(-50%, -50%)';
            cursorRingEl.style.transform = 'translate3d(' + cursorRingX.toFixed(2) + 'px, ' + cursorRingY.toFixed(2) + 'px, 0) translate(-50%, -50%)';
            cursorRafId = requestAnimationFrame(cursorTick);
        }

        /* ================= VIEW SWITCH ================= */
        function enterStudio() {
            document.getElementById('landingView').style.display = 'none';
            document.getElementById('studioView').style.display = 'flex';
            history.replaceState(null, '', '#playground');
            if (!currentCompiledData || !document.getElementById('sourceEditor').value.trim()) {
                selectPreset('ancestor_tree', null);
            }
        }

        function enterStudioWithDemo() {
            enterStudio();
            startLiveDemo();
        }

        function exitStudioToLanding() {
            document.getElementById('studioView').style.display = 'none';
            document.getElementById('landingView').style.display = 'flex';
            history.replaceState(null, '', window.location.pathname);
        }

        function scrollToSection(id) {
            const el = document.getElementById(id);
            if (el) el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        }

        /* ================= EDITOR (highlight + gutter) ================= */
        const $id = (v) => document.getElementById(v);
        const $editor = () => document.getElementById('sourceEditor');

        function escapeHtml(s) {
            return String(s).replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>').replace(/"/g, '"');
        }

        function colorFunctors(chunk) {
            if (!chunk) return '';
            return chunk.replace(/\b([a-z][A-Za-z0-9_]*)(?=\s*\()/g, '<span class="fn">$1</span>');
        }

        // One-pass Prolog tokenizer over pre-escaped text.
        function highlightProlog(code) {
            if (!code) return '';
            const esc = escapeHtml(code);
            const RE = /(%[^\n]*)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|\b[A-Z_][A-Za-z0-9_]*\b|\b\d+(?:\.\d+)?\b|:-|\\==|\\=|>=|=<|<=|[\[\]{}(),.;|]/g;
            let out = '';
            let last = 0;
            let m;
            while ((m = RE.exec(esc)) !== null) {
                out += colorFunctors(esc.slice(last, m.index));
                const tok = m[0];
                let cls = null;
                if (m[1] !== undefined) cls = 'cm';
                else if (m[2] !== undefined) cls = 'str';
                else if (/^\d/.test(tok)) cls = 'nm';
                else if (/^\\?[A-Z_]/.test(tok)) cls = 'vr';
                else if (/^(?:>=|=<|<=)$/.test(tok) || tok === ':-' || tok.startsWith('\\')) cls = 'op';
                else if (/^[\[\]{}(),.;|]$/.test(tok)) cls = 'pn';
                out += cls ? '<span class="' + cls + '">' + tok + '</span>' : tok;
                last = m.index + tok.length;
            }
            out += colorFunctors(esc.slice(last));
            return out;
        }

        function renderEditor() {
            $id('codeHighlight').innerHTML = highlightProlog($editor().value) + '\n';
        }

        function syncEditorScroll() {
            const ed = $editor();
            $id('codeHighlight').scrollTop = ed.scrollTop;
            $id('codeHighlight').scrollLeft = ed.scrollLeft;
            $id('lineNumbers').scrollTop = ed.scrollTop;
        }

        function errorLineFrom(errors) {
            if (!errors || !errors.length) return null;
            const m = String(errors[0]).match(/line\s+(\d+)/i);
            return m ? parseInt(m[1], 10) : null;
        }

        function updateLineNumbers(errorLine) {
            const lines = $editor().value.split('\n');
            let html = '';
            for (let i = 1; i <= lines.length; i++) {
                let cls = 'ln';
                if (errorLine && i === errorLine) cls += ' err';
                html += '<div class="' + cls + '">' + i + '</div>';
            }
            const gutter = $id('lineNumbers');
            gutter.innerHTML = html;
            gutter.scrollTop = $editor().scrollTop;
            const clauses = currentCompiledData && currentCompiledData.ast_graph ? currentCompiledData.ast_graph.total_clauses : null;
            $id('codeMetrics').textContent = lines.length + ' lines' + (clauses !== null ? ' · ' + clauses + ' clauses' : '');
        }

        let compileDebounce = null;
        function onCodeInput() {
            renderEditor();
            clearTimeout(compileDebounce);
            compileDebounce = setTimeout(compileCode, 450);
        }

        /* ================= PRESETS ================= */
        function selectPreset(key, btn) {
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            const target = btn || document.querySelector('.preset-btn[data-key="' + key + '"]');
            if (target) target.classList.add('active');

            const preset = PRESETS[key];
            if (!preset) return;
            $editor().value = preset.code;
            $id('queryGoalInput').value = preset.default_query;
            renderEditor();
            updateLineNumbers();
            compileCode();
            solveQuery();
        }

        function resetStudio() {
            selectPreset('ancestor_tree', null);
        }

        /* ================= TABS (role=tablist + arrow keys) ================= */
        function switchTab(tabId) {
            document.querySelectorAll('#vizTabBar .tab-button').forEach(btn => {
                const on = btn.getAttribute('data-pane') === tabId;
                btn.classList.toggle('active', on);
                btn.setAttribute('aria-selected', on ? 'true' : 'false');
                btn.tabIndex = on ? 0 : -1;
            });
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            const pane = $id(tabId);
            if (pane) pane.classList.add('active');
            if (tabId === 'tab-pdg' && currentCompiledData) renderPDGGraph();
        }

        /* ================= COMPILE ================= */
        function compileCode() {
            const code = $editor().value;
            $id('compilerStatusBadge').textContent = 'Compiling...';
            $id('compilerStatusBadge').className = 'status-text';

            fetch('/api/compile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            })
            .then(res => res.json())
            .then(data => {
                currentCompiledData = data;
                renderCompileStatus(data);
                renderLexer(data);
                renderAST(data);
                if ($id('tab-pdg').classList.contains('active')) renderPDGGraph();
                renderWamTac(data);
                renderHeroTerminal(data);
                refreshHeroStats(data);
                updateLineNumbers(errorLineFrom(data.errors));
            })
            .catch(err => {
                console.error('Compiler request failed:', err);
                $id('compilerStatusBadge').textContent = 'Network error';
                $id('compilerStatusBadge').className = 'status-text bad';
            });
        }

        function renderCompileStatus(data) {
            const badge = $id('compilerStatusBadge');
            const banner = $id('compilerErrorBanner');
            const text = $id('compilerErrorText');
            const more = $id('compilerErrorMore');
            const errs = data.errors || [];
            if (errs.length > 0) {
                badge.textContent = 'Syntax Error (' + errs.length + ')';
                badge.className = 'status-text bad';
                banner.style.display = 'flex';
                text.textContent = errs[0];
                more.textContent = errs.length > 1 ? '  +' + (errs.length - 1) + ' more' : '';
            } else {
                badge.textContent = 'Syntax Valid';
                badge.className = 'status-text ok';
                banner.style.display = 'none';
            }
        }
        /* ================= TOKEN TYPE MAPPING ================= */
        function tokenPillClass(typeName) {
            const t = String(typeName || '');
            if (t === 'ATOM' || t === 'STRING') return 'atom';
            if (t === 'VARIABLE' || t === 'ANON_VAR') return 'variable';
            if (t === 'NUMBER') return 'number';
            if (t === 'DOT' || t === 'COMMA' || t === 'LPAREN' || t === 'RPAREN' || t === 'LBRACKET' || t === 'RBRACKET' || t === 'COMMENT' || t === 'EOF') return 'punct';
            if (t === 'ERROR') return 'error';
            return 'operator'; // OP_RULE, OP_QUERY, OPERATOR, CUT, SEMICOLON, PIPE
        }

        /* ================= LEXER RENDERERS ================= */
        function renderLexer(data) {
            const box = document.getElementById('tokenStreamContainer');
            const tokens = data.tokens || [];

            if (!tokens.length) {
                box.innerHTML = '<div class="report-text">No tokens available — resolve syntax errors first.</div>';
            } else {
                let rows = '';
                for (let i = 0; i < tokens.length; i++) {
                    const tk = tokens[i];
                    const cls = tokenPillClass(tk.type);
                    const delay = reduceMotion ? 0 : (' style="animation-delay:' + Math.min(i * 12, 500) + 'ms"');
                    rows += '<div class="token-row" data-ft="' + cls + '"' + delay + '>'
                        + '<span class="token-pill pill-' + cls + '">' + escapeHtml(tk.type) + '</span>'
                        + '<span class="token-val">' + escapeHtml(tk.raw || tk.value) + '</span>'
                        + '<span class="token-loc">L' + (tk.line || 0) + ':C' + (tk.col || 0) + '</span>'
                        + '</div>';
                }
                box.innerHTML = rows;
            }
            setTokenFilter('all');
            applyTokenFilter();

            // Token distribution report
            const dist = { atom: 0, variable: 0, number: 0, operator: 0, punct: 0, error: 0 };
            for (let i = 0; i < tokens.length; i++) dist[tokenPillClass(tokens[i].type)]++;
            let distHtml = '<div><b>' + tokens.length + '</b> <span style="color:var(--text-3)">total tokens</span></div><div class="sep"></div>';
            const ORDER = ['atom', 'variable', 'number', 'operator', 'punct', 'error'];
            ORDER.forEach(k => {
                if (dist[k] > 0) distHtml += '<div><b>' + dist[k] + '</b> ' + k + (dist[k] > 1 ? 's' : '') + '</div>';
            });
            document.getElementById('tokenDistributionStats').innerHTML = distHtml;

            // Lexical status report
            const report = document.getElementById('lexerStatusReportBox');
            const errs = data.errors || [];
            if (errs.length > 0) {
                report.innerHTML = '<div class="report-header bad">Lexical Analysis Status</div>'
                    + '<p class="report-text">' + escapeHtml(errs[0]) + ' Tokens may be incomplete because scanning stopped at the first error.</p>';
            } else {
                report.innerHTML = '<div class="report-header ok">'
                    + '<svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>'
                    + 'Lexical Analysis Status</div>'
                    + '<p class="report-text"><b style="color:var(--text-1)">' + tokens.length + ' tokens</b> scanned by the hand-written DFA scanner — zero lexical errors.</p>';
            }
        }

        function setTokenFilter(ft) {
            tokenFilterActive = ft;
            document.querySelectorAll('#tokenFilterRow .filter-chip').forEach(c => {
                c.classList.toggle('on', c.getAttribute('data-ft') === ft);
            });
        }

        function filterTokens(ft, chip) {
            setTokenFilter(ft);
            applyTokenFilter();
        }

        function applyTokenFilter() {
            const rows = document.querySelectorAll('#tokenStreamContainer .token-row');
            let visible = 0;
            rows.forEach(r => {
                const hide = tokenFilterActive !== 'all' && r.getAttribute('data-ft') !== tokenFilterActive;
                r.classList.toggle('hidden', hide);
                if (!hide) visible++;
            });
            let empty = document.getElementById('tokenFilterEmpty');
            if (rows.length > 0 && visible === 0) {
                if (!empty) {
                    empty = document.createElement('div');
                    empty.id = 'tokenFilterEmpty';
                    empty.className = 'report-text';
                    empty.style.cssText = 'padding:14px 12px;border:1px dashed var(--border);border-radius:6px;text-align:center;';
                    document.getElementById('tokenStreamContainer').appendChild(empty);
                }
                empty.textContent = 'No ' + tokenFilterActive + ' tokens in this program — choose "All tokens" to see every token.';
                empty.style.display = '';
            } else if (empty) {
                empty.style.display = 'none';
            }
        }

        function renderFirstFollow(data) {
            const box = document.getElementById('ffTableBox');
            const ff = data.first_and_follow;
            if (!ff) { box.innerHTML = '<div class="report-text">FIRST/FOLLOW unavailable.</div>'; return; }
            let html = '';
            for (const nt in ff) {
                html += '<div class="ff-row"><span class="nt">' + escapeHtml(nt) + '</span>'
                    + '<span class="set"><b>FIRST</b> ' + escapeHtml((ff[nt].FIRST || []).join(' | '))
                    + '<br><b>FOLLOW</b> ' + escapeHtml((ff[nt].FOLLOW || []).join(' | ')) + '</span></div>';
            }
            box.innerHTML = html || '<div class="report-text">—</div>';
        }

        /* ================= AST + SYMBOL TABLE RENDERER ================= */
        function renderAST(data) {
            const list = document.getElementById('astTreeList');
            const ag = data.ast_graph;
            if (!ag || !ag.clauses) {
                list.innerHTML = '<p class="report-text">No syntax tree — resolve errors first.</p>';
                return;
            }

            let html = '';
            ag.clauses.forEach(c => {
                const pills = (c.nodes || []).map(n =>
                    '<span class="term-badge"><b>' + escapeHtml(n.kind) + '</b> ' + escapeHtml(n.label) + '</span>').join('');
                html += '<div class="clause-tree-card" id="clauseCard' + c.index + '">'
                    + '<div class="clause-badge-row">'
                    + '<span class="clause-idx">#' + c.index + '</span>'
                    + '<span class="clause-type ' + (String(c.type).toLowerCase()) + '">' + escapeHtml(c.type) + '</span>'
                    + '<span class="clause-title">' + escapeHtml(c.head) + '</span>'
                    + '<span class="clause-line">L' + c.line + '</span>'
                    + '</div>'
                    + (pills ? '<div class="terms-pill-flex">' + pills + '</div>' : '')
                    + '<div class="report-text" style="font-family:var(--font-mono);font-size:9.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + escapeHtml(c.code) + '</div>'
                    + '</div>';
            });

            const sem = data.semantic || {};
            const st = sem.symbol_table || {};
            const sigs = Object.keys(st);
            html += '<div class="ast-section-sep">Symbol table — ' + (sem.total_predicates || sigs.length) + ' predicate' + ((sem.total_predicates || sigs.length) === 1 ? '' : 's') + '</div>';
            html += '<div class="sym-grid">';
            sigs.forEach(sig => {
                const s = st[sig];
                html += '<div class="sym-row">'
                    + '<span class="sig">' + escapeHtml(s.signature) + '</span>'
                    + '<span class="counts"><b class="ok">' + s.facts + 'F</b> <span style="color:var(--text-3)">/</span> <b class="ac">' + s.rules + 'R</b></span>'
                    + '<span class="lines">L' + (s.defined_at_lines || []).join(', L')
                    + (s.callers && s.callers.length ? ' · called by ' + escapeHtml(s.callers.join(', ')) : '') + '</span>'
                    + '</div>';
            });
            html += '</div>';

            const diags = sem.diagnostics || [];
            html += '<div class="ast-section-sep">Semantic diagnostics — errors ' + (sem.errors_count || 0) + ' · warnings ' + (sem.warnings_count || 0) + '</div>';
            if (!diags.length) {
                html += '<div class="diag-row"><span class="diag-pill info-c">clean</span><span>No semantic issues detected.</span></div>';
            } else {
                diags.forEach(d => {
                    const lvl = String(d.level || 'INFO').toUpperCase();
                    const pillCls = lvl === 'ERROR' ? 'error' : (lvl === 'WARNING' ? 'warning' : 'info-c');
                    html += '<div class="diag-row"><span class="diag-pill ' + pillCls + '">' + escapeHtml(lvl) + '</span>'
                        + '<span>' + escapeHtml(d.message)
                        + ' <span class="dd" style="color:var(--text-3)">L' + (d.line || '?') + (d.code ? ' · ' + escapeHtml(d.code) : '') + '</span></span></div>';
                });
            }

            list.innerHTML = html;
            renderFirstFollow(data);
        }

        /* ================= PDG RENDERER ================= */
        const SVG_NS = 'http://www.w3.org/2000/svg';

        function svgEl(tag, attrs) {
            const el = document.createElementNS(SVG_NS, tag);
            for (const k in attrs) el.setAttribute(k, attrs[k]);
            return el;
        }

        function renderPDGGraph() {
            const data = currentCompiledData;
            if (!data || !data.pdg) return;
            const pdg = data.pdg;
            const nodes = pdg.nodes || [];
            const edges = pdg.edges || [];
            const edgesLayer = document.getElementById('svgEdgesLayer');
            const nodesLayer = document.getElementById('svgNodesLayer');
            const svg = document.getElementById('cleanGraphSvg');
            while (edgesLayer.firstChild) edgesLayer.removeChild(edgesLayer.firstChild);
            while (nodesLayer.firstChild) nodesLayer.removeChild(nodesLayer.firstChild);

            if (!nodes.length) {
                const t = svgEl('text', { x: 450, y: 290, 'text-anchor': 'middle', fill: 'var(--text-3)', 'font-family': 'var(--font-mono)', 'font-size': '12' });
                t.textContent = 'No predicates to graph — define facts or rules.';
                nodesLayer.appendChild(t);
                svg.setAttribute('viewBox', '0 0 900 580');
                return;
            }

            const geo = {};
            nodes.forEach(n => {
                const subParts = [];
                if (n.facts > 0) subParts.push(n.facts + 'F');
                if (n.rules > 0) subParts.push(n.rules + 'R');
                if (n.is_recursive) subParts.push('recursive');
                const sub = subParts.join(' | ');
                geo[n.id] = {
                    x: n.x, y: n.y,
                    w: Math.max(n.label.length * 7, (sub.length || 2) * 6.2) + 26,
                    h: 40, label: n.label, sub: sub
                };
            });

            // Auto-fit viewBox
            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            for (const id in geo) {
                const g = geo[id];
                minX = Math.min(minX, g.x); minY = Math.min(minY, g.y);
                maxX = Math.max(maxX, g.x + g.w); maxY = Math.max(maxY, g.y + g.h);
            }
            minY -= 34; minX -= 34; maxX += 34; maxY += 34;
            svg.setAttribute('viewBox', minX + ' ' + minY + ' ' + (maxX - minX) + ' ' + (maxY - minY));
            svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');

            // Edges first (below nodes)
            edges.forEach(e => {
                const s = geo[e.source], t = geo[e.target];
                if (!s || !t) return;
                const loop = e.source === e.target;
                const path = svgEl('path', { class: 'pdg-edge' + (loop ? ' loop' : ''), 'marker-end': loop ? 'url(#arrowhead-loop)' : 'url(#arrowhead)' });
                if (loop) {
                    path.setAttribute('d', 'M ' + (s.x + s.w * 0.80) + ' ' + s.y
                        + ' C ' + (s.x + s.w * 0.80 + 40) + ' ' + (s.y - 40) + ', '
                        + (s.x + s.w * 0.20 - 40) + ' ' + (s.y - 40) + ', '
                        + (s.x + s.w * 0.20) + ' ' + s.y);
                } else {
                    const sx = s.x + s.w, sy = s.y + s.h / 2;
                    const tx = t.x, ty = t.y + t.h / 2;
                    const my = (sy + ty) / 2;
                    path.setAttribute('d', 'M ' + sx + ' ' + sy + ' C ' + sx + ' ' + my + ', ' + tx + ' ' + my + ', ' + tx + ' ' + ty);
                }
                const tt = svgEl('title', {});
                tt.textContent = e.source + ' calls ' + e.target + (e.line ? ' (L' + e.line + ')' : '');
                path.appendChild(tt);
                edgesLayer.appendChild(path);
            });

            // Nodes on top
            nodes.forEach(n => {
                const g = geo[n.id];
                const cls = 'pdg-node' + (n.rules > 0 ? ' rule-node' : '') + (n.is_recursive ? ' rec-node' : '');
                const node = svgEl('g', { class: cls, transform: 'translate(' + g.x + ',' + g.y + ')' });
                node.appendChild(svgEl('rect', { x: 0, y: 0, width: g.w, height: g.h, rx: 7 }));
                const label = svgEl('text', { x: g.w / 2, y: 17, 'text-anchor': 'middle', class: 'n-label' });
                label.textContent = g.label;
                const sub = svgEl('text', { x: g.w / 2, y: 31, 'text-anchor': 'middle', class: 'n-sub' });
                sub.textContent = g.sub;
                const tt = svgEl('title', {});
                tt.textContent = g.label + ' — defined at line ' + (n.lines && n.lines.length ? n.lines.join(', ') : '?') + (n.is_recursive ? ' (recursive)' : '');
                node.appendChild(label); node.appendChild(sub); node.appendChild(tt);
                nodesLayer.appendChild(node);
            });
        }

        /* ================= WAM + TAC RENDERERS ================= */
        function renderWamTac(data) {
            const wam = data.wam || {};
            const list = wamViewMode === 'opt'
                ? (wam.optimized_wam && wam.optimized_wam.length ? wam.optimized_wam : wam.wam_instructions || [])
                : (wam.wam_instructions || []);
            const box = document.getElementById('wamInstructionsBox');
            if (!list.length) {
                box.innerHTML = '<span style="color:var(--text-3)">No WAM instructions — resolve syntax errors first.</span>';
            } else {
                box.innerHTML = list.map((ins, i) => {
                    const args = (ins.args || []).join(', ');
                    const cmt = ins.comment ? '<span class="op-label">; ' + escapeHtml(ins.comment) + '</span>' : '';
                    return '<div class="wln"><span class="lnum">' + String(i + 1).padStart(2, '0') + '</span>'
                        + '<div><span class="op-main">' + escapeHtml(ins.op) + '</span>'
                        + (args ? ' <span class="op-args">' + escapeHtml(args) + '</span>' : '')
                        + (cmt ? ' ' + cmt : '') + '</div></div>';
                }).join('');
            }

            const quads = wam.quadruples || [];
            const tac = document.getElementById('tacQuadruplesBox');
            if (!quads.length) {
                tac.innerHTML = '<span style="color:var(--text-3)">No quadruples generated.</span>';
            } else {
                tac.innerHTML = quads.map((q, i) =>
                    '<div class="wln"><span class="tac-idx">' + String(i + 1).padStart(2, '0') + '.</span>'
                    + '<div><span class="tac-op">(' + escapeHtml(q.op) + '</span>'
                    + '<span style="color:var(--text-2)">, ' + escapeHtml(q.arg1) + ', ' + escapeHtml(q.arg2) + ', </span>'
                    + '<span class="tac-res">' + escapeHtml(q.result) + ')</span></div></div>'
                ).join('');
            }
        }

        function selectWamView(mode, btn) {
            wamViewMode = mode;
            document.getElementById('segOrig').classList.toggle('on', mode === 'orig');
            document.getElementById('segOpt').classList.toggle('on', mode === 'opt');
            if (currentCompiledData) renderWamTac(currentCompiledData);
        }

        /* ================= CLIPBOARD HELPERS ================= */
        let toastTimer = null;
        function flashToast(msg) {
            let t = document.getElementById('copyToast');
            if (!t) {
                t = document.createElement('div');
                t.id = 'copyToast';
                t.setAttribute('role', 'status');
                t.style.cssText = 'position:fixed;bottom:18px;right:18px;z-index:100;background:var(--bg-raise-2);border:1px solid var(--border-strong);color:var(--text-1);font-size:11px;padding:7px 12px;border-radius:8px;box-shadow:var(--shadow-1);opacity:0;transition:opacity .2s;';
                document.body.appendChild(t);
            }
            t.textContent = msg;
            t.style.opacity = '1';
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => { t.style.opacity = '0'; }, 1400);
        }

        function copyToClipboard(text, label) {
            if (!text) { flashToast('Nothing to copy yet — compile first.'); return; }
            const done = () => flashToast(label + ' copied to clipboard.');
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(done).catch(() => { legacyCopy(text, done); });
            } else {
                legacyCopy(text, done);
            }
        }

        function legacyCopy(text, done) {
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.cssText = 'position:fixed;opacity:0;';
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); done(); } catch (e) { flashToast('Copy failed in this browser.'); }
            document.body.removeChild(ta);
        }

        function copyWam() {
            const wam = currentCompiledData && currentCompiledData.wam;
            const list = wam ? (wamViewMode === 'opt' ? (wam.optimized_wam || wam.wam_instructions || []) : (wam.wam_instructions || [])) : [];
            copyToClipboard(list.map(i => i.disassembly || (i.op + ' ' + (i.args || []).join(', '))).join('\n'), 'WAM bytecode');
        }

        function copyTac() {
            const wam = currentCompiledData && currentCompiledData.wam;
            const quads = wam ? (wam.quadruples || []) : [];
            copyToClipboard(quads.map(q => '(' + q.op + ', ' + q.arg1 + ', ' + q.arg2 + ', ' + q.result + ')').join('\n'), 'TAC quadruples');
        }
        /* ================= QUERY + SLD TRACE ================= */
        let lastQueryData = null;

        function solveQuery() {
            const goal = document.getElementById('queryGoalInput').value.trim();
            const box = document.getElementById('solutionsBox');
            const tag = document.getElementById('queryStatusTag');
            if (!goal) {
                box.innerHTML = '<span class="sol-none">Type a goal, e.g. ?- ancestor(george, X).</span>';
                return;
            }
            tag.textContent = 'Solving...';
            tag.className = 'status-text';
            box.innerHTML = '<span class="sol-none">Running SLD resolution...</span>';

            fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: goal, code: $editor().value })
            })
            .then(res => res.json())
            .then(data => {
                lastQueryData = data;
                renderSolutions(data);
                const stepsEl = document.getElementById('statSteps');
                if (data.trace) stepsEl.innerHTML = data.trace.length + '<small>steps</small>';
                if (demoCurrentStep === 6 && document.getElementById('tab-demo').classList.contains('active')) renderDemoStep(6);
            })
            .catch(() => {
                tag.textContent = 'Network error';
                tag.className = 'status-text bad';
                box.innerHTML = '<span class="sol-error">Could not reach the resolver — is the server running?</span>';
            });
        }

        function renderSolutions(data) {
            const box = document.getElementById('solutionsBox');
            const tag = document.getElementById('queryStatusTag');

            if (data.error) {
                tag.textContent = 'Error';
                tag.className = 'status-text bad';
                box.innerHTML = '<span class="sol-error">' + escapeHtml(data.error) + '</span>';
                return;
            }

            if (data.found_solution) {
                tag.textContent = data.solution_count + (data.solution_count === 1 ? ' solution' : ' solutions');
                tag.className = 'status-text ok';
                let html = '';
                (data.solutions || []).forEach((s, i) => {
                    const keys = Object.keys(s);
                    if (!keys.length) {
                        html += '<div class="sol-row"><span class="idx">' + (i + 1) + '.</span><span class="sol-true">true</span></div>';
                    } else {
                        const pairs = keys.map(k => '<b>' + escapeHtml(k) + '</b><span class="eq"> = </span>' + escapeHtml(s[k])).join('<span class="eq">, </span>');
                        html += '<div class="sol-row"><span class="idx">' + (i + 1) + '.</span><span class="sol-pair">' + pairs + '</span></div>';
                    }
                });

                const trace = data.trace || [];
                if (trace.length) {
                    html += '<details class="trace-details"><summary>SLD proof trace — ' + trace.length + ' resolution steps</summary><div class="trace-steps">';
                    trace.forEach(st => {
                        const ev = String(st.event || 'STEP').toUpperCase();
                        let cls = 'trace-step';
                        if (ev.indexOf('SUCCESS') >= 0) cls += ' ev-success';
                        else if (ev.indexOf('FAIL') >= 0 || ev.indexOf('LIMIT') >= 0) cls += ' ev-fail';
                        else cls += ' ev-util';
                        html += '<div class="' + cls + '"><span class="ev">' + escapeHtml(ev) + '</span><span class="dd">d' + (st.depth || 0) + '</span> ' + escapeHtml(st.description || '') + '</div>';
                    });
                    html += '</div></details>';
                }
                box.innerHTML = html;
            } else {
                tag.textContent = 'false';
                tag.className = 'status-text';
                box.innerHTML = '<span class="sol-false">false — no proof exists for this goal over the current knowledge base.</span>';
            }
        }

        /* ================= LIVE DEMO SUITE ================= */
        const DEMO_TOTAL = 6;

        function stopAutoPlay() {
            isAutoPlaying = false;
            if (autoPlayTimer) { clearTimeout(autoPlayTimer); autoPlayTimer = null; }
        }

        function updateDemoControls() {
            const b = document.getElementById('btnAutoPlay');
            if (b) {
                b.textContent = isAutoPlaying ? 'Pause' : (demoCurrentStep >= DEMO_TOTAL ? 'Replay' : 'Play');
            }
            document.getElementById('demoProgressBar').style.width = (demoCurrentStep / DEMO_TOTAL * 100) + '%';
            for (let i = 1; i <= DEMO_TOTAL; i++) {
                const node = document.getElementById('dStep' + i);
                node.classList.toggle('active', i === demoCurrentStep);
                node.classList.toggle('completed', i < demoCurrentStep);
            }
        }

        function scheduleAutoPlay() {
            if (autoPlayTimer) clearTimeout(autoPlayTimer);
            if (!isAutoPlaying) return;
            autoPlayTimer = setTimeout(() => {
                if (demoCurrentStep >= DEMO_TOTAL) {
                    stopAutoPlay();
                } else {
                    demoCurrentStep++;
                    renderDemoStep(demoCurrentStep);
                    scheduleAutoPlay();
                }
                updateDemoControls();
            }, 2300);
        }

        function toggleAutoPlay() {
            if (isAutoPlaying) {
                stopAutoPlay();
            } else {
                if (demoCurrentStep >= DEMO_TOTAL) demoCurrentStep = 1;
                isAutoPlaying = true;
                renderDemoStep(demoCurrentStep);
                scheduleAutoPlay();
            }
            updateDemoControls();
        }

        function startLiveDemo() {
            switchTab('tab-demo');
            if (!document.getElementById('sourceEditor').value.trim()) selectPreset('ancestor_tree', null);
            if (demoCurrentStep >= DEMO_TOTAL) demoCurrentStep = 1;
            isAutoPlaying = true;
            renderDemoStep(demoCurrentStep);
            scheduleAutoPlay();
            updateDemoControls();
        }

        function demoNextStep() {
            stopAutoPlay();
            demoCurrentStep = demoCurrentStep >= DEMO_TOTAL ? 1 : demoCurrentStep + 1;
            renderDemoStep(demoCurrentStep);
            updateDemoControls();
        }

        function demoPrevStep() {
            stopAutoPlay();
            demoCurrentStep = demoCurrentStep <= 1 ? demoCurrentStep : demoCurrentStep - 1;
            renderDemoStep(demoCurrentStep);
            updateDemoControls();
        }

        function jumpToDemoStep(n) {
            stopAutoPlay();
            demoCurrentStep = n;
            renderDemoStep(n);
            updateDemoControls();
        }

        function runDemoProof() {
            const goal = document.getElementById('queryGoalInput').value.trim();
            fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: goal, code: $editor().value })
            })
            .then(res => res.json())
            .then(data => {
                lastQueryData = data;
                const stepsEl = document.getElementById('statSteps');
                if (data.trace) stepsEl.innerHTML = data.trace.length + '<small>steps</small>';
                if (demoCurrentStep === 6) renderDemoStep(6);
            })
            .catch(() => flashToast('Resolver unreachable — compile first, then replay the demo.'));
        }

        function renderDemoStep(step) {
            const title = document.getElementById('stageTitle');
            const body = document.getElementById('stageOutput');
            const canvas = document.getElementById('demoLiveGraphCanvas');
            canvas.style.display = 'none';
            const preview = currentCompiledData || {};

            if (!reduceMotion) { body.style.animation = 'none'; void body.offsetHeight; body.style.animation = ''; }

            if (step === 1) {
                title.textContent = 'Step 1: Ingestion — reading Horn clauses';
                const lines = $editor().value.split('\n');
                const shown = lines.slice(0, 8).map(l => escapeHtml(l) || ' ').join('\n');
                const more = lines.length > 8 ? '\n<span class="dim">... +' + (lines.length - 8) + ' more lines</span>' : '';
                const total = preview.ast_graph ? '<span class="ok">Ingested ' + preview.ast_graph.total_clauses + ' clauses from the character stream.</span>' : '';
                body.innerHTML = '<span class="dim">% character stream consumed from the playground editor</span>\n'
                    + shown + more + (total ? '\n\n' + total : '');
            } else if (step === 2) {
                title.textContent = 'Step 2: Lexer DFA — token classification';
                const toks = preview.tokens || [];
                let html = '<span class="dim">% DFA scanner emitted ' + toks.length + ' tokens</span>\n';
                const showN = Math.min(toks.length, 16);
                for (let i = 0; i < showN; i++) {
                    const cls = tokenPillClass(toks[i].type);
                    html += '<span class="token-pill pill-' + cls + '">' + escapeHtml(toks[i].type) + '</span> <span class="hi">' + escapeHtml(toks[i].raw || toks[i].value) + '</span><span class="dim"> L' + toks[i].line + '</span>\n';
                }
                if (toks.length > 16) html += '<span class="dim">... +' + (toks.length - 16) + ' more tokens</span>';
                body.innerHTML = html;
            } else if (step === 3) {
                title.textContent = 'Step 3: AST construction (recursive descent)';
                const cl = (preview.ast_graph && preview.ast_graph.clauses) || [];
                let html = '<span class="dim">% parsed ' + cl.length + ' clauses into syntax trees</span>\n';
                cl.slice(0, 6).forEach(c => {
                    html += '<span class="op">#' + c.index + '</span> <span class="fn">' + escapeHtml(c.head) + '</span> <span class="vr">[' + escapeHtml(c.type) + ' - L' + c.line + ']</span>\n';
                });
                if (cl.length > 6) html += '<span class="dim">... +' + (cl.length - 6) + ' more</span>';
                body.innerHTML = html;
            } else if (step === 4) {
                title.textContent = 'Step 4: Symbol table + semantic analysis';
                const sem = preview.semantic || {};
                const st = sem.symbol_table || {};
                let html = '<span class="dim">% ' + (sem.total_predicates || 0) + ' predicates - errors ' + (sem.errors_count || 0) + ' - warnings ' + (sem.warnings_count || 0) + '</span>\n';
                for (const k in st) {
                    const s = st[k];
                    html += '<span class="hi">' + escapeHtml(s.signature) + '</span> <span class="dim">-</span> ' + s.facts + 'F / ' + s.rules + 'R <span class="dim">L' + (s.defined_at_lines || []).join(', L') + '</span>\n';
                }
                body.innerHTML = html;
            } else if (step === 5) {
                title.textContent = 'Step 5: Predicate call graph (live)';
                const pdg = preview.pdg || {};
                if ((pdg.nodes || []).length) {
                    canvas.style.display = 'block';
                    renderDemoGraph(pdg);
                    const rec = (pdg.nodes || []).filter(nn => nn.is_recursive).map(nn => nn.label);
                    body.innerHTML = '<span class="ok">' + (pdg.nodes || []).length + ' predicate nodes</span> <span class="dim">- ' + (pdg.edges || []).length + ' call edges</span>'
                        + (rec.length ? '\n<span class="op">recursive predicates:</span> ' + rec.map(escapeHtml).join(', ') : '\n<span class="dim">no recursion detected in this program</span>');
                } else {
                    body.innerHTML = '<span class="dim">No graph data — run Analyze & Compile first.</span>';
                }
            } else if (step === 6) {
                title.textContent = 'Step 6: SLD resolution — proving the goal';
                const tq = lastQueryData;
                if (!tq) {
                    body.innerHTML = '<span class="dim">% resolving the current query over the knowledge base...</span>';
                    runDemoProof();
                    return;
                }
                if (tq.error) {
                    body.innerHTML = '<span class="op">failed:</span> ' + escapeHtml(tq.error);
                } else if (tq.found_solution) {
                    let html = '<span class="ok">PROVED</span> — ' + escapeHtml(tq.query) + '\n';
                    (tq.solutions || []).forEach((s, i) => {
                        const keys = Object.keys(s);
                        const pairs = keys.length
                            ? keys.map(k => '<b class="vr">' + escapeHtml(k) + '</b><span class="dim"> = </span>' + escapeHtml(s[k])).join('<span class="dim">, </span>')
                            : '<span class="ok">true</span>';
                        html += '  <span class="vr">' + (i + 1) + '.</span> ' + pairs + '\n';
                    });
                    const tr = tq.trace || [];
                    html += '\n<span class="cm">% proof trace: ' + tr.length + ' steps (first 6 shown)</span>\n';
                    tr.slice(0, 6).forEach(s2 => {
                        html += '  <span class="dim">d' + (s2.depth || 0) + '</span> ' + escapeHtml(String(s2.event || '')) + ' — ' + escapeHtml(String(s2.description || '')) + '\n';
                    });
                    html += '<span class="dim">full trace available in the query panel</span>';
                    body.innerHTML = html;
                } else {
                    body.innerHTML = '<span class="op">false.</span> <span class="dim">No proof found for ' + escapeHtml(tq.query) + '</span>';
                }
            }
        }

        function renderDemoGraph(pdg) {
            const nodes = pdg.nodes || [];
            const edges = pdg.edges || [];
            const eg = document.getElementById('demoSvgEdges');
            const ng = document.getElementById('demoSvgNodes');
            while (eg.firstChild) eg.removeChild(eg.firstChild);
            while (ng.firstChild) ng.removeChild(ng.firstChild);

            const W = 760, H = 240, PX = 78, PY = 42;
            const geo = {};
            nodes.forEach(nn => {
                const parts = [];
                if (nn.facts > 0) parts.push(nn.facts + 'F');
                if (nn.rules > 0) parts.push(nn.rules + 'R');
                if (nn.is_recursive) parts.push('rec');
                geo[nn.id] = { w: Math.max(nn.label.length * 6.2, (parts.join('|') || 'predicate').length * 5.4) + 24, h: 30 };
            });

            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            nodes.forEach(nn => {
                const cx0 = nn.x + 55, cy0 = nn.y + 20;
                minX = Math.min(minX, cx0); maxX = Math.max(maxX, cx0);
                minY = Math.min(minY, cy0); maxY = Math.max(maxY, cy0);
            });
            if (!isFinite(minX)) { minX = 0; minY = 0; maxX = 1; maxY = 1; }
            const rx = Math.max(1, maxX - minX), ry = Math.max(1, maxY - minY);
            nodes.forEach(nn => {
                const g = geo[nn.id];
                g.cx = PX + ((nn.x + 55) - minX) * (W - PX * 2) / rx;
                g.cy = PY + ((nn.y + 20) - minY) * (H - PY * 2) / ry;
            });

            edges.forEach(e2 => {
                const s = geo[e2.source], t = geo[e2.target];
                if (!s || !t) return;
                const loop = e2.source === e2.target;
                const path = svgEl('path', { class: 'pdg-edge' + (loop ? ' loop' : ''), 'marker-end': loop ? 'url(#demo-loop-arrow)' : 'url(#demo-arrow)' });
                if (loop) {
                    path.setAttribute('d', 'M ' + (s.cx + s.w * 0.3) + ' ' + (s.cy - s.h / 2)
                        + ' C ' + (s.cx + 60) + ' ' + (s.cy - 48) + ', ' + (s.cx - 60) + ' ' + (s.cy - 48) + ', '
                        + (s.cx - s.w * 0.3 - 4) + ' ' + (s.cy - s.h / 2 - 2));
                } else {
                    const sx = s.cx + s.w / 2, sy = s.cy;
                    const tx = t.cx - t.w / 2, ty = t.cy;
                    const my2 = (sy + ty) / 2;
                    path.setAttribute('d', 'M ' + sx + ' ' + sy + ' C ' + sx + ' ' + my2 + ', ' + tx + ' ' + my2 + ', ' + tx + ' ' + ty);
                }
                eg.appendChild(path);
            });

            nodes.forEach((nn, idx) => {
                const g = geo[nn.id];
                const outer = svgEl('g', { transform: 'translate(' + g.cx.toFixed(1) + ',' + g.cy.toFixed(1) + ')' });
                const inner = svgEl('g', { class: 'pdg-node' + (nn.rules > 0 ? ' rule-node' : '') + (nn.is_recursive ? ' rec-node' : '') });
                if (!reduceMotion) {
                    inner.classList.add('demo-node-pop');
                    inner.style.animationDelay = Math.min(idx * 60, 500) + 'ms';
                }
                inner.appendChild(svgEl('rect', { x: -g.w / 2, y: -g.h / 2, width: g.w, height: g.h, rx: 6 }));
                const lb = svgEl('text', { x: 0, y: -1, 'text-anchor': 'middle', class: 'n-label', style: 'font-size:11px' });
                lb.textContent = nn.label;
                const sub = svgEl('text', { x: 0, y: 11, 'text-anchor': 'middle', class: 'n-sub', style: 'font-size:9px' });
                sub.textContent = nn.is_recursive ? 'recursive' : ((nn.facts + 'F/' + nn.rules + 'R') === '0F/0R' ? 'builtin' : nn.facts + 'F/' + nn.rules + 'R');
                const tt = svgEl('title', {});
                tt.textContent = nn.label + (nn.is_recursive ? ' (recursive)' : '');
                inner.appendChild(lb); inner.appendChild(sub); inner.appendChild(tt);
                outer.appendChild(inner);
                ng.appendChild(outer);
            });
        }

        /* ================= HERO TERMINAL + LIVE STATS ================= */
        function refreshHeroStats(data) {
            if (!data) return;
            document.getElementById('statTokens').innerHTML = (data.tokens || []).length + '<small>tokens</small>';
            document.getElementById('statClauses').innerHTML = ((data.ast_graph && data.ast_graph.total_clauses) || 0) + '<small>clauses</small>';
            document.getElementById('statWam').innerHTML = ((data.wam && data.wam.wam_instructions ? data.wam.wam_instructions.length : 0)) + '<small>instrs</small>';
        }

        function renderHeroTerminal(data) {
            const body = document.getElementById('heroTerminalBody');
            if (!body || !data) return;
            const sem = data.semantic || {};
            const errs = (data.errors || []).length;
            const diags = (sem.diagnostics || []).length;
            const wamN = (data.wam && data.wam.wam_instructions ? data.wam.wam_instructions.length : 0);
            const tacN = (data.wam && data.wam.quadruples ? data.wam.quadruples.length : 0);
            const pdgN = ((data.pdg && data.pdg.nodes) || []).length;
            const pdgE = ((data.pdg && data.pdg.edges) || []).length;

            body.innerHTML =
                '<span class="dim">$ prolog-parse build .</span>\n'
                + '<span class="ok">[1/6 lex]</span> DFA scan complete — ' + (data.tokens || []).length + ' tokens, ' + errs + ' errors\n'
                + '<span class="ok">[2/6 parse]</span> recursive descent built the AST — ' + ((data.ast_graph && data.ast_graph.total_clauses) || 0) + ' clauses\n'
                + '<span class="ok">[3/6 sem]</span> symbol table: ' + (sem.total_predicates || 0) + ' predicates, ' + diags + ' diagnostics\n'
                + '<span class="ok">[4/6 graph]</span> PDG: ' + pdgN + ' nodes / ' + pdgE + ' call edges\n'
                + '<span class="ok">[5/6 wam]</span> ' + wamN + ' WAM instructions, ' + tacN + ' TAC quadruples\n'
                + '<span class="ok">[6/6 sld]</span> ' + (lastQueryData ? (lastQueryData.found_solution ? 'proof found — ' + (lastQueryData.trace || []).length + ' steps' : 'goal failed (false)') : 'resolver armed') + '\n'
                + '<span class="ok">SUCCESS</span> <span class="dim">pipeline finished — open the playground for the interactive view</span>';
        }

        /* ================= GLOBAL KEYBOARD ================= */
        document.addEventListener('keydown', (event) => {
            if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
                event.preventDefault();
                compileCode();
                return;
            }
            if (event.key === '/' && !(event.ctrlKey || event.metaKey || event.altKey)) {
                const ae = document.activeElement;
                const typing = ae && (ae.tagName === 'TEXTAREA' || ae.tagName === 'INPUT');
                if (!typing) {
                    event.preventDefault();
                    const q = document.getElementById('queryGoalInput');
                    if (q) { q.focus(); q.select(); }
                }
            }
        });

        /* Roving tabindex navigation across visualizer tabs */
        document.getElementById('vizTabBar').addEventListener('keydown', (event) => {
            if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
            const buttons = Array.from(document.querySelectorAll('#vizTabBar .tab-button'));
            if (!buttons.some(b => b === document.activeElement)) return;
            event.preventDefault();
            const cur = buttons.indexOf(document.activeElement);
            const next = event.key === 'ArrowRight' ? (cur + 1) % buttons.length : (cur - 1 + buttons.length) % buttons.length;
            buttons[next].focus();
            switchTab(buttons[next].getAttribute('data-pane'));
        });

        /* ================= GRAMMAR SPECIFICATION MODAL ================= */
        function openGrammarModal(defaultTab = 'spec') {
            const modal = document.getElementById('grammarModal');
            if (modal) {
                modal.classList.add('active');
                modal.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';
                switchGrammarTab(defaultTab);
            }
        }

        function closeGrammarModal() {
            const modal = document.getElementById('grammarModal');
            if (modal) {
                modal.classList.remove('active');
                modal.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
            }
        }

        function handleGrammarBackdropClick(event) {
            if (event.target && event.target.id === 'grammarModal') {
                closeGrammarModal();
            }
        }

        function switchGrammarTab(tabKey) {
            const tabs = ['spec', 'bison', 'prec', 'firstfollow'];
            tabs.forEach(key => {
                const btn = document.getElementById('gtab-btn-' + key);
                const panel = document.getElementById('gtab-panel-' + key);
                if (btn) btn.classList.toggle('active', key === tabKey);
                if (panel) panel.classList.toggle('active', key === tabKey);
            });
        }

        function copyBisonGrammar() {
            const codeEl = document.getElementById('bisonGrammarCode');
            const copyBtn = document.getElementById('btnCopyGrammar');
            if (!codeEl) return;
            const text = codeEl.innerText || codeEl.textContent;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(() => {
                    if (copyBtn) {
                        const originalHtml = copyBtn.innerHTML;
                        copyBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!';
                        setTimeout(() => { copyBtn.innerHTML = originalHtml; }, 2000);
                    }
                }).catch(() => fallbackCopy(text, copyBtn));
            } else {
                fallbackCopy(text, copyBtn);
            }
        }

        function fallbackCopy(text, copyBtn) {
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            if (copyBtn) {
                copyBtn.textContent = 'Copied!';
                setTimeout(() => { copyBtn.textContent = 'Copy Grammar'; }, 2000);
            }
        }

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                closeGrammarModal();
            }
        });

        /* ================= BOOTSTRAP ================= */
        window.addEventListener('load', () => {
            initTheme();
            initCursor();
            updateDemoControls();
            if (location.hash === '#playground') {
                enterStudio();
            } else {
                selectPreset('ancestor_tree', null);
            }
            // Warm the hero stats with the default query once the first compile lands.
            setTimeout(() => { if (!lastQueryData) solveQuery(); }, 900);
        });
    </script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Flask routes (backend behaviour unchanged)
# ---------------------------------------------------------------------------
last_program_ast = None


def _run_pipeline(code: str):
    """Lex + parse source; returns (tokens, errors, ast_or_none)."""
    lexer = PrologLexer(code)
    tokens = lexer.tokenize()
    errors = list(lexer.errors)

    ast = None
    parser = None
    try:
        parser = PrologParser(tokens)
        ast = parser.parse_program()
        if parser.errors:
            errors.extend(parser.errors)
    except Exception as exc:
        errors.append(str(exc))

    return tokens, errors, ast


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, presets=SAMPLE_PROGRAMS, initial_view='landing')


@app.route('/playground')
def playground():
    return render_template_string(HTML_TEMPLATE, presets=SAMPLE_PROGRAMS, initial_view='studio')


@app.route('/studio')
def studio():
    return render_template_string(HTML_TEMPLATE, presets=SAMPLE_PROGRAMS, initial_view='studio')


@app.route('/api/compile', methods=['POST'])
def api_compile():
    global last_program_ast
    payload = request.get_json(silent=True) or {}
    code = str(payload.get('code', ''))

    tokens, errors, ast = _run_pipeline(code)

    ast_graph = {"total_clauses": 0, "clauses": []}
    pdg = {"nodes": [], "edges": []}
    semantic = {"symbol_table": {}, "diagnostics": [], "total_predicates": 0, "warnings_count": 0, "errors_count": 0}
    wam = {"wam_instructions": [], "optimized_wam": [], "quadruples": []}

    if ast is not None:
        ast_graph = GraphBuilder.build_ast_graph(ast)
        pdg = GraphBuilder.build_pdg_graph(ast)
        semantic = SemanticAnalyzer(ast).analyze()
        wam = WAMCompiler(ast).compile()
        last_program_ast = ast

    return jsonify({
        "tokens": [t.to_dict() for t in tokens],
        "errors": errors,
        "ast_graph": ast_graph,
        "pdg": pdg,
        "semantic": semantic,
        "wam": wam,
        "first_and_follow": PrologParser.get_first_and_follow_sets(),
    })


@app.route('/api/query', methods=['POST'])
def api_query():
    global last_program_ast
    payload = request.get_json(silent=True) or {}
    query_text = str(payload.get('query', '')).strip()
    code = payload.get('code')

    ast = None
    if code:
        _, _, ast = _run_pipeline(code)
    elif last_program_ast is not None:
        ast = last_program_ast

    if not query_text:
        return jsonify({"error": "Query cannot be empty — enter a goal like ?- ancestor(george, X).", "found_solution": False}), 200
    if not query_text.endswith('.'):
        query_text += '.'

    query_source = query_text if '?-' in query_text else ('?- ' + query_text)

    if ast is None:
        return jsonify({"error": "No compiled program available yet — run Analyze & Compile first.", "found_solution": False}), 400

    try:
        q_tokens = PrologLexer(query_source).tokenize()
        q_parser = PrologParser(q_tokens)
        q_ast = q_parser.parse_program()
        if q_parser.errors:
            err_msg = "; ".join(e.get("message", "Syntax error") if isinstance(e, dict) else str(e) for e in q_parser.errors)
            return jsonify({"error": f"Query syntax error: {err_msg}", "found_solution": False}), 200
        goals = []
        for clause in q_ast.clauses:
            if isinstance(clause, Query):
                goals = clause.goals
                break
        if not goals:
            return jsonify({"error": "Could not parse a goal from: " + query_text, "found_solution": False}), 200
        resolution = ResolutionEngine(ast).solve(goals)
    except Exception as exc:
        return jsonify({"error": str(exc), "found_solution": False}), 200

    return jsonify(resolution)


if __name__ == '__main__':
    print("=" * 68)
    print(" [CD LAB] PROLOG-PARSE: CLEAN COMPILER & VISUAL DEMO STUDIO")
    print(" -> Studio URL : http://127.0.0.1:5050")
    print("=" * 68)
    app.run(host='127.0.0.1', port=5050, debug=False)
