# My Second Brain Sync (Obsidian + AI Agent Automation)

Welcome to your personalized **Second Brain & Zettelkasten Knowledge System**. This project is a highly sophisticated, semi-automated personal knowledge management (PKM) vault powered by **Obsidian** and a customized **AI Multi-Agent Automation Pipeline** running locally via PowerShell and the Antigravity (`agy`) CLI.

---

## 📖 Second Brain Visual Reader & Mind-Map Companion (HTML5 SPA)
Located under the `reader-app/` folder, this premium Single Page Web Application (SPA) is designed to solve visual fatigue when reading long notes and visualize knowledge graphs seamlessly.

### ✨ Key Features:
1.  **Space-Theme Glassmorphism UI:** Built on a customized HSL space palette, using premium typography (Outfit & IBM Plex Sans Thai), smooth micro-animations, and full dark-theme layouts.
2.  **Local-First Vault Connection:** Utilizes the modern HTML5 File System Access API (`showDirectoryPicker`) to let you open your vault directory directly in the browser. It runs 100% locally with zero internet data leakage.
3.  **Contrarian Ingestion Callout:** Automatically detects and extracts the **Contrarian Analysis & Trade-offs** section, rendering it inside a custom styled coral warning box.
4.  **Wikilink Parser:** Automatically converts Obsidian `[[Note Name]]` syntaxes inside your notes into clickable, active interactive links.
5.  **Interactive Mind-Map Visualizer:** Dynamically renders a force-directed spring physics network graph of all connected notes on a HTML5 Canvas. You can drag nodes, watch them interact, and click any node to load the note instantly.

### 🚀 How to Run:
1.  Navigate to [reader-app/index.html](file:///D:/Boss/3%29%20Hobby/3.13%29%20AI/AI%20Agent/Second%20Brain/My%20Second%20Brain%20Sync/reader-app/index.html).
2.  Double-click to open it in any modern browser (Chrome, Edge, or Opera recommended).
3.  Click the **"เชื่อมต่อ Obsidian Vault"** button at the top-left, select the main `My Second Brain Sync` vault directory, and grant permission.
4.  Enjoy your beautifully rendered notes and mind graph!

---

## 📂 The Idea Pipeline Folder Structure

Information enters as raw capture and flows through a structured refinement process into high-quality output:

```text
My Second Brain Sync/
├── 01_INBOX/              # Raw captures, scratch files, and YouTube URLs to process.
├── 02_SOURCE/             # High-level overview summaries of external books, articles, or videos.
├── 03_ZETTEL/             # Atomic "Zettel" Notes (1 note = 1 core concept/idea), highly interlinked.
├── 04_MOC/                # Maps of Content. Concept directories linking and contextualizing Zettels.
├── 05_OUTPUT/             # Draft deliverables (articles, blueprints, scripts) ready to be published.
├── reader-app/            # HTML5 Visual Reader & Mind-Map Companion Web App.
└── SECOND_BRAIN_PRINCIPLE/# Core vault principles, domain definitions, and system guidelines.
```

---

## 👥 The AI Automation Agent Suite

Custom prompts and behaviors are configured under the `.agents/` folder and triggered via PowerShell entry-point scripts:

### 1. The Standard Distiller (`.agents/Distiller/`)
Processes standard plain-text or Markdown files in `01_INBOX` and refines them into standard Obsidian notes in `02_SOURCE` or `03_ZETTEL` according to strict templates.

### 2. The YouTube Multi-Agent Ingestion Pipeline (`.agents/YouTubeManager/`)
An advanced, multi-step pipeline engineered to fetch transcripts and distill YouTube videos without confirmation bias or marketing hype:
*   **Subtitles Extraction:** A lightweight Python script automatically scrapes Thai or English subtitles from the video ID.
*   **The Summarizer Sub-Agent:** Captures the core thesis, framework diagrams, and actionable steps.
*   **The Contrarian Sub-Agent (Devil's Advocate):** Specifically looks for logical fallacies, survivorship biases, limitations, and failure modes (`#concept/trade-off`).
*   **The Verifier Sub-Agent:** Separates facts/empirical data from opinions and noise (`#concept/signal-vs-noise`).
*   **The Orchestrator:** Synthesizes their debates into a highly objective, balanced review note inside the vault.

### 3. The Architect (`.agents/Architect/`)
Analyzes, clusters, and formats your Zettels in `03_ZETTEL` into thematic **Maps of Content (MOCs)** in `04_MOC`.

### 4. The Builder (`.agents/Builder/`)
Synthesizes material from MOCs and Zettels to draft publication-ready articles or plans in `05_OUTPUT`.

---

## 🛠️ Getting Started & Execution

All automated workflows are driven by PowerShell scripts. Both scripts are pre-formatted in **UTF-8 with BOM** for perfect support of Thai text in Windows PowerShell.

### A. Processing the Inbox (Ingest & Distill)
To process raw text notes or YouTube URLs in `01_INBOX`, open PowerShell in the project directory and run:
```powershell
.\run-distiller.ps1
```
You will be prompted with three options:
1.  **Extract into 03_ZETTEL only:** Best for short ideas/atomic concepts.
2.  **Summarize into 02_SOURCE + Extract into 03_ZETTEL:** Best for deep, comprehensive knowledge mapping.
3.  **Summarize into 02_SOURCE only:** Best for quick video/article updates where atomic concept notes are not required.
4.  **Skip.**

### B. Organizing Tags & Formats
To automatically scan, format, and organize tags in your Source or Zettel directories:
```powershell
.\run-architect.ps1
```

---

## 🔒 Version Control & Backups (Git + GitHub)

This repository is fully under local Git version control with a strict `.gitignore` to protect personal layout state (`workspace.json`) and temporary scraping cache (`temp_transcript.txt`).

To manually backup your updates to your private GitHub repository:
```powershell
git add .
git commit -m "Update notes and structure"
git push
```

If any file is accidentally corrupted or deleted during automation, recover your entire state instantly with:
```powershell
git reset --hard HEAD
```
