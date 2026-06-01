// Global App State
let vaultFiles = {}; // Dictionary of: { "FileName.md": { name, folder, path, content, tags, creators } }
let selectedNoteKey = null;
let activeTagsFilter = new Set();
let searchQuery = "";
let graphSimulation = null;

// DOM Elements
const btnConnect = document.getElementById("btn-connect");
const searchInput = document.getElementById("search-input");
const tagsCloud = document.getElementById("tags-cloud");
const filesList = document.getElementById("files-list");
const welcomeState = document.getElementById("welcome-state");
const readerState = document.getElementById("reader-state");

// Active Note DOM Elements
const noteFolderBadge = document.getElementById("note-folder-badge");
const noteCreators = document.getElementById("note-creators");
const noteTitle = document.getElementById("note-title");
const noteTags = document.getElementById("note-tags");
const noteBody = document.getElementById("note-body");
const contrarianHighlight = document.getElementById("contrarian-highlight");
const contrarianBody = document.getElementById("contrarian-body");

// Tabs DOM Elements
const tabBtns = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");

/* ==========================================
   1. Directory Parsing (File System Access)
   ========================================== */
btnConnect.addEventListener("click", async () => {
    try {
        // Request folder access from the user
        const dirHandle = await window.showDirectoryPicker();
        vaultFiles = {};
        
        // Show loading state
        filesList.innerHTML = `<div class="empty-explorer"><i class="fa-solid fa-spinner fa-spin"></i><p>กำลังโหลดและอ่านไฟล์ข้อมูล...</p></div>`;
        
        // Recursively read the folder
        await readDirectoryRecursive(dirHandle, "");
        
        // Setup Search and UI States
        searchInput.disabled = false;
        renderSidebar();
        renderTagsCloud();
        
        // Notify user of success
        const fileCount = Object.keys(vaultFiles).length;
        btnConnect.innerHTML = `<i class="fa-solid fa-circle-check" style="color:var(--color-accent-emerald);"></i> โหลดแล้ว ${fileCount} โน้ต`;
        btnConnect.style.boxShadow = "0 4px 15px rgba(76, 175, 80, 0.2)";
        btnConnect.style.backgroundColor = "var(--bg-card-hover)";
        btnConnect.style.borderColor = "var(--color-accent-emerald)";
        btnConnect.style.border = "1px solid var(--color-accent-emerald)";
        
    } catch (err) {
        console.error("Error accessing folder: ", err);
        if (err.name !== "AbortError") {
            filesList.innerHTML = `<div class="empty-explorer"><i class="fa-solid fa-triangle-exclamation" style="color:var(--color-accent-coral);"></i><p>เกิดข้อผิดพลาดในการเปิดโฟลเดอร์ กรุณาลองใหม่อีกครั้ง</p></div>`;
        }
    }
});

// Recursive folder scanner
async function readDirectoryRecursive(dirHandle, relativePath) {
    // We only want to scan core Obsidian folders and ignore system or config folders
    const ignoredFolders = [".git", ".obsidian", ".antigravitycli", ".agents", "scratch"];
    
    for await (const entry of dirHandle.values()) {
        if (entry.kind === "directory") {
            if (ignoredFolders.includes(entry.name)) continue;
            
            const nextRelativePath = relativePath ? `${relativePath}/${entry.name}` : entry.name;
            await readDirectoryRecursive(entry, nextRelativePath);
        } else if (entry.kind === "file" && entry.name.endsWith(".md") && entry.name !== "README.md" && entry.name !== "ANTIGRAVITY.md") {
            const file = await entry.getFile();
            const content = await file.text();
            
            // Extract folder name
            const folder = relativePath.split("/")[0] || "Root";
            
            // Extract tags and creators
            const tags = extractTags(content);
            const creators = extractCreators(content);
            
            vaultFiles[entry.name] = {
                name: entry.name.replace(".md", ""),
                fileName: entry.name,
                folder: folder,
                path: relativePath ? `${relativePath}/${entry.name}` : entry.name,
                content: content,
                tags: tags,
                creators: creators
            };
        }
    }
}

// Extract tags from body (e.g. #concept/leverage, #domain/tech)
function extractTags(content) {
    const regex = /#([a-zA-Z0-9\-\/]+)/g;
    const tags = [];
    let match;
    while ((match = regex.exec(content)) !== null) {
        const tag = match[1].toLowerCase();
        // Ignore creator and type/status tags for general tagging
        if (!tag.startsWith("creator/") && !tag.startsWith("type/") && !tag.startsWith("status/")) {
            tags.push(tag);
        }
    }
    return [...new Set(tags)];
}

// Extract creators (e.g. #creator/ai, #creator/me)
function extractCreators(content) {
    const creators = [];
    if (content.includes("#creator/ai")) creators.push("ai");
    if (content.includes("#creator/me")) creators.push("me");
    if (creators.length === 0) creators.push("me"); // Default to user if not specified
    return creators;
}

/* ==========================================
   2. UI Rendering & Filters
   ========================================== */
function renderSidebar() {
    filesList.innerHTML = "";
    
    // Group files by folder
    const folders = {};
    
    Object.values(vaultFiles).forEach(file => {
        // Filter by Search Query
        if (searchQuery) {
            const matchesName = file.name.toLowerCase().includes(searchQuery);
            const matchesContent = file.content.toLowerCase().includes(searchQuery);
            const matchesTags = file.tags.some(tag => tag.includes(searchQuery));
            if (!matchesName && !matchesContent && !matchesTags) return;
        }
        
        // Filter by Active Tags
        if (activeTagsFilter.size > 0) {
            const hasMatchingTag = file.tags.some(tag => activeTagsFilter.has(tag));
            if (!hasMatchingTag) return;
        }
        
        if (!folders[file.folder]) {
            folders[file.folder] = [];
        }
        folders[file.folder].push(file);
    });
    
    const folderKeys = Object.keys(folders).sort();
    
    if (folderKeys.length === 0) {
        filesList.innerHTML = `<div class="empty-explorer"><i class="fa-solid fa-magnifying-glass-minus"></i><p>ไม่พบไฟล์โน้ตที่ตรงตามเงื่อนไขค้นหา</p></div>`;
        return;
    }
    
    folderKeys.forEach(folder => {
        const folderDiv = document.createElement("div");
        folderDiv.className = "explorer-folder";
        
        const titleDiv = document.createElement("div");
        titleDiv.className = "folder-title";
        
        // Choose folder icon
        let folderIcon = "fa-folder-closed";
        if (folder === "01_INBOX") folderIcon = "fa-inbox";
        else if (folder === "02_SOURCE") folderIcon = "fa-book";
        else if (folder === "03_ZETTEL") folderIcon = "fa-tags";
        else if (folder === "04_MOC") folderIcon = "fa-sitemap";
        else if (folder === "05_OUTPUT") folderIcon = "fa-file-export";
        else if (folder === "SECOND_BRAIN_PRINCIPLE") folderIcon = "fa-sliders";
        
        titleDiv.innerHTML = `<i class="fa-solid ${folderIcon}"></i> ${folder}`;
        folderDiv.appendChild(titleDiv);
        
        folders[folder].sort((a, b) => a.name.localeCompare(b.name)).forEach(file => {
            const noteDiv = document.createElement("div");
            noteDiv.className = `note-item ${selectedNoteKey === file.fileName ? 'active' : ''}`;
            noteDiv.innerHTML = `<i class="fa-regular fa-file-lines"></i> <span>${file.name}</span>`;
            noteDiv.addEventListener("click", () => selectNote(file.fileName));
            folderDiv.appendChild(noteDiv);
        });
        
        filesList.appendChild(folderDiv);
    });
}

function renderTagsCloud() {
    tagsCloud.innerHTML = "";
    
    // Count tag frequencies
    const tagCounts = {};
    Object.values(vaultFiles).forEach(file => {
        file.tags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
    });
    
    const sortedTags = Object.keys(tagCounts).sort((a, b) => tagCounts[b] - tagCounts[a]).slice(0, 15);
    
    if (sortedTags.length === 0) {
        tagsCloud.innerHTML = `<span class="no-tags">ไม่มีแท็กทั่วไป</span>`;
        return;
    }
    
    sortedTags.forEach(tag => {
        const tagBtn = document.createElement("span");
        tagBtn.className = `tag-badge-btn ${activeTagsFilter.has(tag) ? 'active' : ''}`;
        tagBtn.innerHTML = `#${tag} <span style="opacity:0.6; font-weight:normal;">(${tagCounts[tag]})</span>`;
        tagBtn.addEventListener("click", () => {
            if (activeTagsFilter.has(tag)) {
                activeTagsFilter.delete(tag);
            } else {
                activeTagsFilter.add(tag);
            }
            renderTagsCloud();
            renderSidebar();
        });
        tagsCloud.appendChild(tagBtn);
    });
}

// Search Input Listener
searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderSidebar();
});

/* ==========================================
   3. Note Parsing & Viewer
   ========================================== */
function selectNote(fileName) {
    selectedNoteKey = fileName;
    
    // Refresh Sidebar to highlight the active item
    renderSidebar();
    
    // Render the note content
    const file = vaultFiles[fileName];
    if (!file) return;
    
    welcomeState.classList.add("hidden");
    readerState.classList.remove("hidden");
    
    // Render Header Info
    noteFolderBadge.innerHTML = `<i class="fa-solid fa-folder"></i> ${file.folder}`;
    
    // Render Creator badges
    noteCreators.innerHTML = "";
    file.creators.forEach(creator => {
        const span = document.createElement("span");
        span.className = `creator-badge ${creator}`;
        span.innerText = creator === "ai" ? "AI Crafted" : "Personal";
        noteCreators.appendChild(span);
    });
    
    noteTitle.innerText = file.name;
    
    // Render Tags pills
    noteTags.innerHTML = "";
    file.tags.forEach(tag => {
        const span = document.createElement("span");
        span.className = "tag-pill";
        span.innerText = `#${tag}`;
        noteTags.appendChild(span);
    });
    
    // Parse Note Body & Contrarian
    parseAndRenderBody(file.content);
    
    // Initialize Mind Graph for this note
    setTimeout(() => {
        initMindGraph(fileName);
    }, 100);
}

// Robust parsing of Note body
function parseAndRenderBody(content) {
    let cleanBody = content;
    
    // 1. Remove all top-level Tag lines from the printed body text to prevent clutter
    cleanBody = cleanBody.replace(/^#[a-zA-Z0-9\-\/]+\s*$/gm, "");
    
    // 2. Extract Contrarian Box if it exists
    // Look for various formats of contrarian/trade-off headers
    const contrarianRegexPatterns = [
        /(?:###?\s*|\*\*)\s*(?:จุดที่ต้องระวัง|ความเสี่ยงและจุดบกพร่อง|มุมกลับผู้เห็นต่าง|การวิเคราะห์ขัดแย้ง|Contrarian Analysis\s*&\s*Trade-offs?)[^*#]*\n([\s\S]*?)(?=\n##|\n#type|\n\*\*เชื่อมโยง|$)/i
    ];
    
    let contrarianHtml = "";
    let matchedPattern = false;
    
    for (const pattern of contrarianRegexPatterns) {
        const match = pattern.exec(cleanBody);
        if (match) {
            const rawContrarianText = match[1].trim();
            // Parse Markdown of the contrarian text
            contrarianHtml = marked.parse(rawContrarianText);
            
            // Remove the Contrarian section from the main cleanBody to prevent duplication
            cleanBody = cleanBody.replace(match[0], "");
            matchedPattern = true;
            break;
        }
    }
    
    if (matchedPattern && contrarianHtml) {
        contrarianHighlight.classList.remove("hidden");
        contrarianBody.innerHTML = contrarianHtml;
    } else {
        contrarianHighlight.classList.add("hidden");
    }
    
    // 3. Render Markdown of the remaining clean body
    let html = marked.parse(cleanBody);
    
    // 4. Convert Wiki Links [[Note Name]] or [[Note Name|Display Name]] into clickable HTML links!
    // Regex for Obsidian wiki-links: [[NoteName]] or [[NoteName|DisplayName]]
    const wikiLinkRegex = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;
    html = html.replace(wikiLinkRegex, (match, noteTarget, displayName) => {
        const targetClean = noteTarget.trim();
        const displayClean = displayName ? displayName.trim() : targetClean;
        
        // Find if target note exists in our vault files (ignoring extension)
        const matchedFile = Object.values(vaultFiles).find(f => f.name.toLowerCase() === targetClean.toLowerCase());
        
        if (matchedFile) {
            return `<a href="#" class="wiki-link" onclick="event.preventDefault(); selectNote('${matchedFile.fileName}');">${displayClean}</a>`;
        } else {
            // Note doesn't exist yet, show it as a dimmed unresolved wiki-link
            return `<span class="unresolved-wiki-link" title="ยังไม่มีโน้ตหัวข้อนี้" style="opacity: 0.6; border-bottom: 1px dotted var(--color-text-muted); cursor: help;">${displayClean}</span>`;
        }
    });
    
    noteBody.innerHTML = html;
}

// Expose selectNote to global window context so onclick wiki-links work
window.selectNote = selectNote;

/* ==========================================
   4. Tab Navigation Systems
   ========================================== */
tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        // Toggle Buttons
        tabBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        
        // Toggle Contents
        const tabId = btn.getAttribute("data-tab");
        tabContents.forEach(content => {
            if (content.id === tabId) {
                content.classList.add("active-content");
            } else {
                content.classList.remove("active-content");
            }
        });
        
        // Resize Canvas if graph tab is active
        if (tabId === "tab-graph") {
            const canvas = document.getElementById("graph-canvas");
            resizeCanvas(canvas);
        }
    });
});

function resizeCanvas(canvas) {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
}

/* ==========================================
   5. Interactive Mind Map Network Graph
   ========================================== */
function initMindGraph(activeFileName) {
    const canvas = document.getElementById("graph-canvas");
    const ctx = canvas.getContext("2d");
    resizeCanvas(canvas);
    
    // Build Graph Data
    // Nodes: all files in the vault (or just the active file and its connected notes to keep it neat)
    const nodes = [];
    const links = [];
    const addedNodeNames = new Set();
    
    // Root Node (the active note)
    const activeNote = vaultFiles[activeFileName];
    if (!activeNote) return;
    
    nodes.push({
        id: activeNote.fileName,
        name: activeNote.name,
        x: canvas.width / 2,
        y: canvas.height / 2,
        r: 12,
        color: "var(--color-primary)",
        isActive: true
    });
    addedNodeNames.add(activeNote.name.toLowerCase());
    
    // Find all outgoing Wiki links in the active file
    const wikiLinkRegex = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;
    let match;
    while ((match = wikiLinkRegex.exec(activeNote.content)) !== null) {
        const targetName = match[1].trim();
        const targetFile = Object.values(vaultFiles).find(f => f.name.toLowerCase() === targetName.toLowerCase());
        
        if (targetFile) {
            if (!addedNodeNames.has(targetFile.name.toLowerCase())) {
                // Generate a random position around the center
                const angle = Math.random() * Math.PI * 2;
                const distance = 120 + Math.random() * 60;
                
                nodes.push({
                    id: targetFile.fileName,
                    name: targetFile.name,
                    x: canvas.width / 2 + Math.cos(angle) * distance,
                    y: canvas.height / 2 + Math.sin(angle) * distance,
                    r: 8,
                    color: "hsl(215, 20%, 65%)",
                    isActive: false
                });
                addedNodeNames.add(targetFile.name.toLowerCase());
            }
            
            links.push({
                source: activeNote.fileName,
                target: targetFile.fileName
            });
        }
    }
    
    // Find all incoming Wiki links (notes that link TO the active file)
    Object.values(vaultFiles).forEach(file => {
        if (file.fileName === activeNote.fileName) return;
        
        let hasLink = false;
        let innerMatch;
        const innerRegex = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;
        while ((innerMatch = innerRegex.exec(file.content)) !== null) {
            const targetName = innerMatch[1].trim();
            if (targetName.toLowerCase() === activeNote.name.toLowerCase()) {
                hasLink = true;
                break;
            }
        }
        
        if (hasLink) {
            if (!addedNodeNames.has(file.name.toLowerCase())) {
                const angle = Math.random() * Math.PI * 2;
                const distance = 120 + Math.random() * 60;
                
                nodes.push({
                    id: file.fileName,
                    name: file.name,
                    x: canvas.width / 2 + Math.cos(angle) * distance,
                    y: canvas.height / 2 + Math.sin(angle) * distance,
                    r: 8,
                    color: "hsl(250, 40%, 45%)",
                    isActive: false
                });
                addedNodeNames.add(file.name.toLowerCase());
            }
            
            links.push({
                source: file.fileName,
                target: activeNote.fileName
            });
        }
    });
    
    // Physics Simulation parameters
    const k = 0.05; // Spring constant
    const repulse = 1500; // Repulsion constant
    const damping = 0.85; // Damping/friction factor
    
    // Drag-and-drop state
    let draggedNode = null;
    let offsetX = 0;
    let offsetY = 0;
    
    // Canvas event listeners for dragging and clicking
    canvas.onmousedown = (e) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        
        // Check if mouse clicked on any node
        for (const node of nodes) {
            const dist = Math.hypot(node.x - mouseX, node.y - mouseY);
            if (dist <= node.r + 5) {
                draggedNode = node;
                offsetX = mouseX - node.x;
                offsetY = mouseY - node.y;
                return;
            }
        }
    };
    
    canvas.onmousemove = (e) => {
        if (!draggedNode) return;
        const rect = canvas.getBoundingClientRect();
        draggedNode.x = e.clientX - rect.left - offsetX;
        draggedNode.y = e.clientY - rect.top - offsetY;
    };
    
    canvas.onmouseup = (e) => {
        if (draggedNode) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            // If they just clicked on a non-active node without dragging much, select it!
            const dist = Math.hypot(draggedNode.x - (mouseX - offsetX), draggedNode.y - (mouseY - offsetY));
            if (dist < 3 && !draggedNode.isActive) {
                selectNote(draggedNode.id);
            }
            draggedNode = null;
        }
    };
    
    // Stop previous simulation
    if (graphSimulation) {
        cancelAnimationFrame(graphSimulation);
    }
    
    // Simulation Loop
    function simulate() {
        // 1. Repulsion force between all nodes
        for (let i = 0; i < nodes.length; i++) {
            const n1 = nodes[i];
            n1.fx = n1.fx || 0;
            n1.fy = n1.fy || 0;
            
            for (let j = 0; j < nodes.length; j++) {
                if (i === j) continue;
                const n2 = nodes[j];
                const dx = n1.x - n2.x;
                const dy = n1.y - n2.y;
                const dist = Math.hypot(dx, dy) || 1;
                
                if (dist < 250) {
                    const force = repulse / (dist * dist);
                    n1.fx += (dx / dist) * force;
                    n1.fy += (dy / dist) * force;
                }
            }
        }
        
        // 2. Attraction force along the links/springs
        links.forEach(link => {
            const n1 = nodes.find(n => n.id === link.source);
            const n2 = nodes.find(n => n.id === link.target);
            if (!n1 || !n2) return;
            
            const dx = n1.x - n2.x;
            const dy = n1.y - n2.y;
            const dist = Math.hypot(dx, dy) || 1;
            const restLength = 120;
            const force = k * (dist - restLength);
            
            n1.fx -= (dx / dist) * force;
            n1.fy -= (dy / dist) * force;
            n2.fx += (dx / dist) * force;
            n2.fy += (dy / dist) * force;
        });
        
        // 3. Apply forces to velocities and positions
        nodes.forEach(node => {
            if (node === draggedNode) {
                node.vx = 0;
                node.vy = 0;
                node.fx = 0;
                node.fy = 0;
                return;
            }
            
            node.vx = (node.vx || 0) * damping + (node.fx || 0);
            node.vy = (node.vy || 0) * damping + (node.fy || 0);
            
            node.x += node.vx;
            node.y += node.vy;
            
            // Constrain nodes inside canvas
            node.x = Math.max(node.r, Math.min(canvas.width - node.r, node.x));
            node.y = Math.max(node.r, Math.min(canvas.height - node.r, node.y));
            
            // Reset force accumulations
            node.fx = 0;
            node.fy = 0;
        });
        
        // 4. Clear and Draw the network graph
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw Links/Lines
        ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
        ctx.lineWidth = 1.5;
        links.forEach(link => {
            const n1 = nodes.find(n => n.id === link.source);
            const n2 = nodes.find(n => n.id === link.target);
            if (!n1 || !n2) return;
            
            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(n2.x, n2.y);
            ctx.stroke();
        });
        
        // Draw Nodes/Circles & Text labels
        nodes.forEach(node => {
            // Shadow glow for active node
            if (node.isActive) {
                ctx.shadowColor = "var(--color-primary)";
                ctx.shadowBlur = 12;
            } else {
                ctx.shadowBlur = 0;
            }
            
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
            ctx.fillStyle = node.color;
            ctx.fill();
            
            // Reset shadow
            ctx.shadowBlur = 0;
            
            // Text Label
            ctx.fillStyle = node.isActive ? "#ffffff" : "var(--color-text-secondary)";
            ctx.font = node.isActive ? "bold 12.5px 'Outfit', sans-serif" : "11px 'Outfit', sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(node.name, node.x, node.y + node.r + 16);
        });
        
        graphSimulation = requestAnimationFrame(simulate);
    }
    
    // Start physics simulation loop
    simulate();
}
