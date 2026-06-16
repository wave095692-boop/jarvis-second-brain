// System State
let notesList = [];
let audioCtx = null;
let collapsedRooms = { Boss: false, Friend1: true, Friend2: true, Friend3: true, Friend4: true };
let currentRoomLabels = {};

// Initialize System
document.addEventListener("DOMContentLoaded", () => {
    // Render Icons
    lucide.createIcons();
    
    // Initialize the Game-like loader overlay flow
    initGameLoader();
    
    // Check boss session state
    checkBossSession();
    
    // Start status polling loop (every 3 seconds)
    setInterval(fetchStatus, 3000);
});


// Web Audio API Synthesizer (Cyber HUD Sound FX)
function initAudio() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    logToTerminal("[AUDIO] Web Audio Context established. Audio Engine loaded.");
    playSynthSound('startup');
}

// Game Loading Screen logic
function initGameLoader() {
    const startBtn = document.getElementById("loader-start-btn");
    const initScreen = document.getElementById("loader-init-screen");
    const progressScreen = document.getElementById("loader-progress-screen");
    const fill = document.getElementById("loader-progress-fill");
    const statusText = document.getElementById("loader-status-text");
    const percentageText = document.getElementById("loader-percentage");
    const logsContainer = document.getElementById("loader-terminal-logs");
    const overlay = document.getElementById("loader-overlay");

    if (!startBtn) return;

    startBtn.addEventListener("click", () => {
        // Initialize audio on click (browser gesture requirement met)
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }

        // Play laser boot click sound
        playSynthSound('click');

        // Transition screens
        initScreen.style.display = "none";
        progressScreen.style.display = "block";

        const logMessages = [
            { pct: 5, msg: ">> INITIALIZING NEURAL BACKLINK LAYER...", type: "info" },
            { pct: 12, msg: ">> CORE MATRIX ONLINE (VER: 2.5.9)", type: "success" },
            { pct: 20, msg: ">> AUTHENTICATING DEEP COGNITIVE SIGNALS...", type: "info" },
            { pct: 28, msg: ">> ACCESS GRANTED: ADMINISTRATOR บอส (BOSS)", type: "success" },
            { pct: 35, msg: ">> RESOLVING DYNAMIC DNS ENVELOPE...", type: "info" },
            { pct: 45, msg: ">> STABILIZING SSH REVERSE TUNNEL PROTOCOLS...", type: "info" },
            { pct: 54, msg: ">> ESTABLISHING SECURE HANDSHAKES ON PORT 8500...", type: "info" },
            { pct: 60, msg: ">> BOOTING YOUTUBE PREMIUM CLONE SERVER...", type: "info" },
            { pct: 68, msg: ">> CONNECTING YOUTUBE APP TO PORT 8000...", type: "success" },
            { pct: 75, msg: ">> FETCHING SECOND BRAIN MEMORY NOTES...", type: "info" },
            { pct: 83, msg: ">> DOWNLOADING RUDEDOG FAIR CAMPAIGN MAPS...", type: "info" },
            { pct: 90, msg: ">> SYNAPSE CALIBRATION COMPLETED.", type: "success" },
            { pct: 95, msg: ">> FLUSHING CYBER HUD INTERFACE...", type: "info" },
            { pct: 100, msg: ">> WELCOME BACK, BOSS. ALL SYSTEMS NOMINAL.", type: "success" }
        ];

        let currentPct = 0;
        let logIndex = 0;

        function addLog(text, type = "info") {
            const el = document.createElement("div");
            el.className = "log-entry" + (type === "success" ? " success" : (type === "warn" ? " warn" : ""));
            el.innerText = text;
            logsContainer.appendChild(el);
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }

        let nextSoundPct = 0;

        const interval = setInterval(() => {
            currentPct += Math.floor(Math.random() * 4) + 1;
            if (currentPct > 100) currentPct = 100;

            fill.style.width = currentPct + "%";
            percentageText.innerText = currentPct + "%";

            if (currentPct >= nextSoundPct && currentPct < 100) {
                playLoadingPulse(currentPct);
                nextSoundPct = currentPct + 8 + Math.floor(Math.random() * 5);
            }

            while (logIndex < logMessages.length && currentPct >= logMessages[logIndex].pct) {
                const item = logMessages[logIndex];
                addLog(item.msg, item.type);
                statusText.innerText = item.msg.replace(">> ", "");
                logIndex++;
                playSynthSound('click');
            }

            if (currentPct === 100) {
                clearInterval(interval);
                playChimeVictory();

                setTimeout(() => {
                    overlay.classList.add("fade-out");
                    fetchStatus();
                    fetchNotes();
                    fetchUploadedFiles();
                    fetchProjectFiles();
                }, 1200);
            }
        }, 120);
    });
}

function playLoadingPulse(pct) {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    osc.type = 'triangle';
    const startFreq = 200 + (pct * 3.5);
    osc.frequency.setValueAtTime(startFreq, now);
    osc.frequency.exponentialRampToValueAtTime(startFreq * 1.3, now + 0.12);
    
    gainNode.gain.setValueAtTime(0.06, now);
    gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
    
    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    osc.start(now);
    osc.stop(now + 0.13);
}

function playChimeVictory() {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    
    const notes = [523.25, 659.25, 783.99, 1046.50]; 
    const durations = [0.08, 0.08, 0.08, 0.35];
    let timeAccumulator = 0;

    notes.forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = (i === notes.length - 1) ? 'sine' : 'triangle';
        osc.frequency.setValueAtTime(freq, now + timeAccumulator);
        
        gainNode.gain.setValueAtTime(0, now + timeAccumulator);
        gainNode.gain.linearRampToValueAtTime(0.12, now + timeAccumulator + 0.02);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + timeAccumulator + durations[i]);
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start(now + timeAccumulator);
        osc.stop(now + timeAccumulator + durations[i] + 0.05);
        
        timeAccumulator += 0.08;
    });
}

function playSynthSound(type) {
    if (!audioCtx) return;
    
    // Resume context if suspended (browser security)
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    
    const now = audioCtx.currentTime;
    
    if (type === 'startup') {
        // Stark Cyber Computer boot-up sweep
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc1.type = 'sine';
        osc2.type = 'triangle';
        
        osc1.frequency.setValueAtTime(120, now);
        osc1.frequency.exponentialRampToValueAtTime(880, now + 0.6);
        
        osc2.frequency.setValueAtTime(60, now);
        osc2.frequency.exponentialRampToValueAtTime(440, now + 0.6);
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.15, now + 0.1);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.6);
        
        osc1.connect(gainNode);
        osc2.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc1.start(now);
        osc2.start(now);
        osc1.stop(now + 0.65);
        osc2.stop(now + 0.65);
        
    } else if (type === 'click') {
        // High-tech laser blip
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1200, now);
        osc.frequency.exponentialRampToValueAtTime(400, now + 0.08);
        
        gainNode.gain.setValueAtTime(0.12, now);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + 0.09);
        
    } else if (type === 'success') {
        // Chime for successful build/compile
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(523.25, now); // C5
        osc1.frequency.setValueAtTime(659.25, now + 0.1); // E5
        osc1.frequency.setValueAtTime(783.99, now + 0.2); // G5
        
        osc2.type = 'triangle';
        osc2.frequency.setValueAtTime(261.63, now); // C4
        osc2.frequency.exponentialRampToValueAtTime(783.99, now + 0.3);
        
        gainNode.gain.setValueAtTime(0, now);
        gainNode.gain.linearRampToValueAtTime(0.12, now + 0.05);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        
        osc1.connect(gainNode);
        osc2.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc1.start(now);
        osc2.start(now);
        osc1.stop(now + 0.5);
        osc2.stop(now + 0.5);
        
    } else if (type === 'delete') {
        // Low pitch synth swoop down
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.linearRampToValueAtTime(50, now + 0.15);
        
        gainNode.gain.setValueAtTime(0.08, now);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + 0.16);
    }
}

// Log Terminal Outputs
function logToTerminal(message) {
    const term = document.getElementById("terminal-body");
    if (!term) return;
    
    const time = new Date().toLocaleTimeString('th-TH');
    term.innerHTML += `\n[${time}] ${message}`;
    term.scrollTop = term.scrollHeight;
}

// Fetch Statuses from server
function fetchStatus() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            // Meta updates
            document.getElementById('hud-lan-ip').innerText = data.lan_ip;
            document.getElementById('hud-cpu').innerText = data.system.cpu_load || 'N/A';
            document.getElementById('hud-disk').innerText = data.system.disk_free || 'N/A';
            
            // Dynamic Dashboard URL (using browser window location origin)
            const lanLink = document.getElementById('lan-link');
            lanLink.innerText = window.location.origin;
            lanLink.href = window.location.origin;
            
            // Dynamic YouTube Clone URL based on client connection network
            const tunnelLink = document.getElementById('tunnel-link');
            let ytUrl = data.youtube_clone.url; // Dynamic URL from backend
            const currentHost = window.location.hostname;
            
            if (currentHost === "localhost" || currentHost === "127.0.0.1") {
                ytUrl = `http://${currentHost}:8000`;
            } else if (currentHost.match(/^\d+\.\d+\.\d+\.\d+$/)) {
                ytUrl = `${window.location.protocol}//${currentHost}:8000`;
            }
            
            tunnelLink.innerText = ytUrl;
            tunnelLink.href = ytUrl;

            // YouTube Diagnostics
            const ytTxt = document.getElementById('yt-status-text');
            const ytLed = document.getElementById('yt-status-led');
            ytTxt.innerText = data.youtube_clone.status;
            ytLed.className = 'status-led ' + (data.youtube_clone.status === 'ONLINE' ? 'led-green' : 'led-red');
            
            // Tunnel Diagnostics
            const tunTxt = document.getElementById('tunnel-status-text');
            const tunLed = document.getElementById('tunnel-status-led');
            tunTxt.innerText = data.tunnel.status;
            tunLed.className = 'status-led ' + (data.tunnel.status === 'ONLINE' ? 'led-green' : 'led-red');
            
            // PDF Diagnostics
            const pdfTxt = document.getElementById('pdf-status-text');
            const pdfLed = document.getElementById('pdf-status-led');
            const pdfMtime = document.getElementById('pdf-mtime');
            pdfTxt.innerText = data.pdf.status;
            pdfLed.className = 'status-led ' + (data.pdf.status === 'FOUND' ? 'led-cyan' : 'led-red');
            pdfMtime.innerText = data.pdf.last_modified || 'Unavailable';
        })
        .catch(err => {
            console.error("Dashboard diagnostics polling failed:", err);
            // Gray out HUD on connection drop
            document.getElementById('hud-lan-ip').innerText = "DISCONNECTED";
            document.getElementById('yt-status-text').innerText = "UNAVAILABLE";
            document.getElementById('yt-status-led').className = 'status-led led-gray';
            document.getElementById('tunnel-status-text').innerText = "UNAVAILABLE";
            document.getElementById('tunnel-status-led').className = 'status-led led-gray';
            document.getElementById('pdf-status-text').innerText = "UNAVAILABLE";
            document.getElementById('pdf-status-led').className = 'status-led led-gray';
        });
}

// Action Trigger
function runAction(actionName) {
    playSynthSound('click');
    logToTerminal(`[EXECUTE] Triggered control command: ${actionName.toUpperCase()}...`);
    
    fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: actionName })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            playSynthSound('success');
            logToTerminal(`[SUCCESS] ${data.log}`);
            fetchStatus(); // Immediately poll status
        } else {
            playSynthSound('delete');
            logToTerminal(`[FAILED] Command returned error: ${data.error}`);
        }
    })
    .catch(err => {
        playSynthSound('delete');
        logToTerminal(`[CRITICAL] Server connection timed out during execution: ${err.message}`);
    });
}

// Fetch Notes list
function fetchNotes() {
    fetch('/api/notes')
        .then(res => res.json())
        .then(data => {
            notesList = data;
            renderNotes();
        })
        .catch(err => {
            console.error("Failed to load Second Brain notes database:", err);
        });
}

// Render Notes to Screen
function renderNotes() {
    const list = document.getElementById('notes-list');
    if (!list) return;
    
    if (notesList.length === 0) {
        list.innerHTML = `<div style="text-align: center; padding: 30px; font-size: 13px; color: var(--text-dim);">ไม่มีบันทึกความจำขณะนี้</div>`;
        return;
    }
    
    // Sort descending by id (latest on top)
    const sorted = [...notesList].sort((a, b) => b.id - a.id);
    
    list.innerHTML = sorted.map(note => {
        return `
            <div class="note-item fade-in">
                <div class="note-content">
                    <span class="note-text">${escapeHtml(note.text)}</span>
                    <span class="note-time">${note.timestamp}</span>
                </div>
                <button class="btn-delete" onclick="deleteNote(${note.id})">
                    <i data-lucide="trash-2" style="width: 14px; height: 14px;"></i>
                </button>
            </div>
        `;
    }).join('');
    
    lucide.createIcons();
}

// Add a New Note
function addNote() {
    const input = document.getElementById('note-input');
    const text = input.value.trim();
    if (!text) return;
    
    playSynthSound('click');
    
    const now = new Date();
    const timestamp = now.getFullYear() + '-' + 
                      String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                      String(now.getDate()).padStart(2, '0') + ' ' + 
                      String(now.getHours()).padStart(2, '0') + ':' + 
                      String(now.getMinutes()).padStart(2, '0') + ':' + 
                      String(now.getSeconds()).padStart(2, '0');
                      
    const newNote = {
        id: notesList.length > 0 ? Math.max(...notesList.map(n => n.id)) + 1 : 1,
        text: text,
        timestamp: timestamp
    };
    
    notesList.push(newNote);
    input.value = "";
    
    // Save to server database
    saveNotes();
}

function handleNoteKeyPress(event) {
    if (event.key === 'Enter') {
        addNote();
    }
}

// Delete Note
function deleteNote(id) {
    playSynthSound('delete');
    notesList = notesList.filter(n => n.id !== id);
    saveNotes();
}

// Save Notes to Backend API
function saveNotes() {
    fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(notesList)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            logToTerminal(`[DB UPDATE] Notes database synchronized successfully.`);
            renderNotes();
        } else {
            logToTerminal(`[DB ERROR] Synchronize failed: ${data.error}`);
        }
    })
    .catch(err => {
        logToTerminal(`[DB CRITICAL] Sync connection lost: ${err.message}`);
    });
}

// HTML Escaper helper
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.toString().replace(/[&<>"']/g, function(m) { return map[m]; });
}

// Open and View Code File in Modal
function viewCodeFile(key, filename) {
    playSynthSound('click');
    
    const modal = document.getElementById("code-viewer-modal");
    const codeBlock = document.getElementById("modal-code-block");
    const title = document.getElementById("modal-file-title");
    const pathEl = document.getElementById("modal-file-path");
    
    if (!modal) return;
    
    const preBlock = document.getElementById("modal-pre-block");
    const customPreview = document.getElementById("modal-custom-preview");
    if (preBlock) preBlock.style.display = "block";
    if (customPreview) customPreview.style.display = "none";
    
    // Set loading state
    title.innerHTML = `<i data-lucide="file-code"></i> FILE VIEWER // ${filename.toUpperCase()}`;
    pathEl.innerText = `PATH: LOADING LOCATION FOR ${key}...`;
    codeBlock.innerText = "Connecting to Jarvis Core... Fetching file data stream...";
    modal.style.display = "flex";
    
    lucide.createIcons();
    
    // Fetch file content
    fetch(`/api/file?key=${key}`)
        .then(res => {
            if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
            return res.text();
        })
        .then(content => {
            // Set code block text
            codeBlock.innerText = content;
            
            // Map paths for display
            const pathMap = {
                'strategy_md': '/Users/apple/.gemini/antigravity-ide/brain/.../rudedog_fair_10days_content.md',
                'yt_html': '/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/index.html',
                'yt_js': '/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/app.js',
                'yt_css': '/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/index.css',
                'yt_server': '/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone/server.py',
                'pdf_script': '/Users/apple/.gemini/antigravity-ide/scratch/generate_dark_pdf.py',
                'pdf_script_beautiful': '/Users/apple/.gemini/antigravity-ide/scratch/generate_beautiful_pdf.py'
            };
            pathEl.innerText = `PATH: ${pathMap[key] || filename}`;
            logToTerminal(`[FILE VIEW] Loaded file stream: ${filename}`);
        })
        .catch(err => {
            playSynthSound('delete');
            codeBlock.innerText = `[CRITICAL ERROR] Failed to load file stream: ${err.message}`;
            pathEl.innerText = `PATH: CONNECTION ERROR`;
            logToTerminal(`[ERROR] Failed to load file content for ${filename}: ${err.message}`);
        });
}

// Close File Viewer Modal
function closeFileViewer() {
    playSynthSound('click');
    const modal = document.getElementById("code-viewer-modal");
    if (modal) {
        modal.style.display = "none";
    }
}

// Upload file functions
function triggerFileUpload() {
    playSynthSound('click');
    const fileInput = document.getElementById("pdf-upload-file");
    if (fileInput) {
        fileInput.click();
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const roomSelect = document.getElementById("user-room-select");
    const room = roomSelect ? roomSelect.value : "Boss";
    
    logToTerminal(`[UPLOAD] Sending ${file.name} (${(file.size/1024).toFixed(1)} KB) to Room: ${room}...`);
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const arrayBuffer = e.target.result;
        
        fetch(`/api/upload-file?room=${room}&filename=${encodeURIComponent(file.name)}`, {
            method: 'POST',
            body: arrayBuffer
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                playSynthSound('success');
                logToTerminal(`[UPLOAD SUCCESS] Saved as ${data.filename} in uploads/${room} folder.`);
                document.getElementById("pdf-upload-file").value = "";
                fetchUploadedFiles();
                fetchNotes();
            } else {
                playSynthSound('delete');
                logToTerminal(`[UPLOAD FAILED] Server error: ${data.error}`);
            }
        })
        .catch(err => {
            playSynthSound('delete');
            logToTerminal(`[UPLOAD ERROR] Connection failed: ${err.message}`);
        });
    };
    reader.readAsArrayBuffer(file);
}

function fetchUploadedFiles() {
    fetch('/api/uploads')
        .then(res => res.json())
        .then(data => {
            renderUploadedFiles(data.files, data.labels);
        })
        .catch(err => {
            console.error("Failed to load uploaded files list:", err);
        });
}

function renderUploadedFiles(roomsData, roomLabels) {
    const container = document.getElementById("uploaded-files-list");
    if (!container) return;
    
    if (!roomLabels) {
        roomLabels = {
            Boss: "บอส (Boss)",
            Friend1: "เพื่อน 1 (Friend 1)",
            Friend2: "เพื่อน 2 (Friend 2)",
            Friend3: "เพื่อน 3 (Friend 3)",
            Friend4: "เพื่อน 4 (Friend 4)"
        };
    }
    currentRoomLabels = roomLabels;
    
    const rooms = [
        { key: "Boss", label: roomLabels.Boss || "บอส (Boss)" },
        { key: "Friend1", label: roomLabels.Friend1 || "เพื่อน 1 (Friend 1)" },
        { key: "Friend2", label: roomLabels.Friend2 || "เพื่อน 2 (Friend 2)" },
        { key: "Friend3", label: roomLabels.Friend3 || "เพื่อน 3 (Friend 3)" },
        { key: "Friend4", label: roomLabels.Friend4 || "เพื่อน 4 (Friend 4)" }
    ];
    
    // Update dropdown select option elements in index.html dynamically
    updateRoomDropdownLabels(roomLabels);
    
    container.innerHTML = rooms.map(room => {
        const files = roomsData[room.key] || [];
        const isCollapsed = collapsedRooms ? collapsedRooms[room.key] : false;
        const arrowIcon = isCollapsed ? 'chevron-right' : 'chevron-down';
        const folderIcon = isCollapsed ? 'folder' : 'folder-open';
        
        const filesHtml = isCollapsed 
            ? '' 
            : (files.length === 0 
                ? `<div style="padding: 10px 14px; font-size: 11px; color: var(--text-dim); font-style: italic;">ไม่มีไฟล์ในห้องนี้</div>`
                : files.map(file => {
                    return `
                        <div class="exp-file fade-in" style="padding: 6px 12px; display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                            <span title="${file}" style="font-family: var(--font-tech); font-size: 11px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; color: var(--text-secondary);">📄 ${file}</span>
                            <div style="display: flex; gap: 4px; flex-shrink: 0;">
                                <button class="btn-icon-action" onclick="viewUploadedFile('${room.key}', '${file}')" title="ดูพรีวิว">
                                    <i data-lucide="eye" style="width: 11px; height: 11px;"></i>
                                </button>
                                <a class="btn-icon-action" href="/view/upload?room=${room.key}&file=${encodeURIComponent(file)}" target="_blank" title="ดาวน์โหลด">
                                    <i data-lucide="download" style="width: 11px; height: 11px;"></i>
                                </a>
                                <button class="btn-icon-action" onclick="renameUploadedFile('${room.key}', '${file}')" title="เปลี่ยนชื่อ">
                                    <i data-lucide="edit-2" style="width: 11px; height: 11px;"></i>
                                </button>
                                <button class="btn-icon-action text-pink" onclick="deleteUploadedFile('${room.key}', '${file}')" title="ลบไฟล์">
                                    <i data-lucide="trash-2" style="width: 11px; height: 11px;"></i>
                                </button>
                            </div>
                        </div>
                    `;
                }).join(''));
                
        // Only allow folder renaming if unlocked (or if it's not Boss)
        const canRenameFolder = (room.key !== 'Boss' || sessionStorage.getItem('boss_unlocked') === 'true');
        const roomLabelHtml = canRenameFolder 
            ? `<span onclick="event.stopPropagation(); renameRoomFolder('${room.key}')" title="คลิกเพื่อเปลี่ยนชื่อห้อง" style="cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: color 0.2s;" onmouseover="this.style.color='var(--neon-pink)'" onmouseout="this.style.color='var(--neon-cyan)'">
                   <span>${room.label}</span>
                   <i data-lucide="edit-2" style="width: 10px; height: 10px; opacity: 0.6;"></i>
               </span>`
            : `<span>${room.label}</span>`;
                
        return `
            <div class="room-folder" style="margin-bottom: 8px; border: 1px solid rgba(255, 255, 255, 0.02); border-radius: 6px; overflow: hidden;">
                <div class="room-title" onclick="toggleRoomCollapse('${room.key}')" style="font-weight: 600; font-size: 11.5px; color: var(--neon-cyan); padding: 8px 12px; display: flex; align-items: center; gap: 8px; background: rgba(0,0,0,0.2); cursor: pointer; user-select: none; transition: background 0.2s;">
                    <i data-lucide="${arrowIcon}" style="width: 12px; height: 12px; color: var(--text-secondary);"></i>
                    <i data-lucide="${folderIcon}" style="width: 12px; height: 12px; color: var(--neon-yellow);"></i> 
                    <span style="flex: 1; display: flex; align-items: center;">
                        ${roomLabelHtml}
                    </span>
                    <span style="font-size: 10px; color: var(--text-dim); background: rgba(255,255,255,0.05); padding: 1px 6px; border-radius: 10px;">${files.length}</span>
                </div>
                ${!isCollapsed ? `<div class="room-files" style="padding: 4px 0; background: rgba(255,255,255,0.01); border-top: 1px solid rgba(255,255,255,0.03);">
                     ${filesHtml}
                </div>` : ''}
            </div>
        `;
    }).join('');

    
    lucide.createIcons();
}

function toggleRoomCollapse(roomKey) {
    if (roomKey === 'Boss' && sessionStorage.getItem('boss_unlocked') !== 'true') {
        playSynthSound('delete');
        logToTerminal('[ACCESS ERROR] Folder "Boss" is restricted. Redirecting to authorization vault...');
        switchTab('boss');
        return;
    }
    collapsedRooms[roomKey] = !collapsedRooms[roomKey];
    fetchUploadedFiles();
}


function viewUploadedFile(room, file) {
    playSynthSound('click');
    
    const modal = document.getElementById("code-viewer-modal");
    const codeBlock = document.getElementById("modal-code-block");
    const title = document.getElementById("modal-file-title");
    const pathEl = document.getElementById("modal-file-path");
    
    const preBlock = document.getElementById("modal-pre-block");
    const customPreview = document.getElementById("modal-custom-preview");
    
    if (!modal) return;
    
    title.innerHTML = `<i data-lucide="file"></i> PREVIEW // ${room.toUpperCase()} // ${file.toUpperCase()}`;
    pathEl.innerText = `PATH: uploads/${room}/${file}`;
    modal.style.display = "flex";
    
    // Clear and show loading
    codeBlock.innerText = "Loading file content...";
    if (preBlock) preBlock.style.display = "block";
    if (customPreview) customPreview.style.display = "none";
    
    const ext = file.split('.').pop().toLowerCase();
    const fileUrl = `/view/upload?room=${room}&file=${encodeURIComponent(file)}`;
    
    const imageExtensions = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'];
    const textExtensions = ['txt', 'py', 'js', 'json', 'html', 'css', 'md', 'sh', 'log'];
    const officeExtensions = ['doc', 'xls', 'xlsx', 'ppt', 'pptx'];
    
    if (imageExtensions.includes(ext)) {
        if (preBlock) preBlock.style.display = "none";
        if (customPreview) {
            customPreview.style.display = "block";
            customPreview.innerHTML = `<img src="${fileUrl}" style="max-width: 100%; max-height: 500px; display: block; margin: 0 auto; border: 1px solid var(--border); box-shadow: 0 4px 10px rgba(0,0,0,0.5);">`;
        }
    } else if (ext === 'pdf') {
        if (preBlock) preBlock.style.display = "none";
        if (customPreview) {
            customPreview.style.display = "block";
            customPreview.innerHTML = `<iframe src="${fileUrl}" style="width: 100%; height: 500px; border: none; background: #fff;"></iframe>`;
        }
    } else if (ext === 'docx') {
        if (preBlock) preBlock.style.display = "none";
        if (customPreview) {
            customPreview.style.display = "block";
            customPreview.innerHTML = `
                <div style="text-align: center; padding: 50px 20px; font-family: 'Kanit'; color: var(--text-dim);">
                    <div class="cyber-blink red-blink" style="margin: 0 auto 15px auto; width: 10px; height: 10px;"></div>
                    <div style="font-size: 14px; margin-bottom: 10px; color:#fff;">กำลังแปลและจัดรูปแบบกระดาษแคมเปญ (.docx)...</div>
                </div>
            `;
            
            fetch(fileUrl)
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
                    return res.arrayBuffer();
                })
                .then(arrayBuffer => {
                    return mammoth.convertToHtml({ arrayBuffer: arrayBuffer });
                })
                .then(result => {
                    const html = result.value || "<p><i>(ไฟล์ว่างเปล่าหรือไม่สามารถแปลงข้อมูลได้)</i></p>";
                    try {
                        const beautifulHtml = renderBeautifulDocx(html);
                        customPreview.innerHTML = beautifulHtml;
                    } catch (e) {
                        console.error("Beautiful docx rendering failed:", e);
                        customPreview.innerHTML = `<div class="docx-viewer">${html}</div>`;
                    }
                    lucide.createIcons();
                })
                .catch(err => {
                    customPreview.innerHTML = `
                        <div style="text-align: center; padding: 50px 20px; font-family: 'Kanit'; color: var(--text-dim);">
                            <i data-lucide="alert-octagon" style="width: 48px; height: 48px; color: var(--neon-pink); margin-bottom: 15px;"></i>
                            <div style="font-size: 14px; margin-bottom: 10px; color:#fff;">ไม่สามารถแปลงพรีวิวไฟล์ .docx ได้อัตโนมัติ</div>
                            <div style="font-size: 12px; margin-bottom: 20px; color: var(--text-secondary);">${err.message}</div>
                            <a class="btn-hud btn-pink" href="${fileUrl}" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-size: 12px; margin: 0 auto; border: 1px solid var(--neon-pink); cursor: pointer;">
                                <i data-lucide="download"></i> ดาวน์โหลดไฟล์โดยตรง
                            </a>
                        </div>
                    `;
                    lucide.createIcons();
                });
        }
    } else if (officeExtensions.includes(ext)) {
        if (preBlock) preBlock.style.display = "none";
        if (customPreview) {
            customPreview.style.display = "block";
            
            const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
            if (isLocal) {
                customPreview.innerHTML = `
                    <div style="text-align: center; padding: 50px 20px; font-family: 'Kanit'; color: var(--text-dim);">
                        <i data-lucide="info" style="width: 48px; height: 48px; color: var(--neon-cyan); margin-bottom: 15px;"></i>
                        <div style="font-size: 14px; margin-bottom: 15px; color:#fff;">ไฟล์เอกสาร Microsoft Office (${ext.toUpperCase()})</div>
                        <div style="font-size: 12px; margin-bottom: 20px; color: #85837C;">
                            เนื่องจากบอสใช้งานผ่าน Localhost ระบบจึงไม่สามารถใช้ Google Viewer พรีวิวได้แบบสด<br>
                            หากต้องการดูพรีวิวแบบสด กรุณาเข้าใช้งานผ่านลิงก์ออนไลน์ (Localtunnel) ของเรา หรือกดดาวน์โหลดด้านล่างนี้ครับ
                        </div>
                        <a class="btn-hud btn-cyan" href="${fileUrl}" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-size: 12px; margin: 0 auto; border: 1px solid var(--neon-cyan); cursor: pointer;">
                            <i data-lucide="download"></i> ดาวน์โหลดไฟล์โดยตรง
                        </a>
                    </div>
                `;
            } else {
                const publicFileUrl = window.location.origin + fileUrl;
                const viewerUrl = `https://docs.google.com/gview?url=${encodeURIComponent(publicFileUrl)}&embedded=true`;
                customPreview.innerHTML = `<iframe src="${viewerUrl}" style="width: 100%; height: 500px; border: none; background: #fff;"></iframe>`;
            }
            lucide.createIcons();
        }
    } else if (textExtensions.includes(ext)) {
        if (preBlock) preBlock.style.display = "block";
        if (customPreview) customPreview.style.display = "none";
        
        fetch(fileUrl)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
                return res.text();
            })
            .then(text => {
                codeBlock.innerText = text;
            })
            .catch(err => {
                codeBlock.innerText = `Error loading file text: ${err.message}`;
            });
    } else {
        if (preBlock) preBlock.style.display = "none";
        if (customPreview) {
            customPreview.style.display = "block";
            customPreview.innerHTML = `
                <div style="text-align: center; padding: 60px 20px; font-family: 'Kanit'; color: var(--text-dim);">
                    <i data-lucide="alert-octagon" style="width: 48px; height: 48px; color: var(--neon-pink); margin-bottom: 15px;"></i>
                    <div style="font-size: 14px; margin-bottom: 20px;">ไฟล์ประเภทนี้ไม่รองรับการแสดงพรีวิวแบบสดบนหน้าเว็บ</div>
                    <a class="btn-hud btn-pink" href="${fileUrl}" target="_blank" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-size: 12px; margin: 0 auto; border: 1px solid var(--neon-pink);">
                        <i data-lucide="download"></i> ดาวน์โหลดไฟล์
                    </a>
                </div>
            `;
            lucide.createIcons();
        }
    }
    
    lucide.createIcons();
}

// Beautiful Brutalist parser that formats Mammoth.js output to match the original campaign PDF template
function renderBeautifulDocx(html) {
    const div = document.createElement('div');
    div.innerHTML = html;
    
    const container = document.createElement('div');
    container.className = 'docx-beautiful-container';
    
    const children = Array.from(div.children);
    
    let currentCard = null;
    let currentCardBody = null;
    let currentIdeaBox = null;
    let currentIdeaList = null;
    
    let inIntro = true;
    let introHeader = document.createElement('div');
    introHeader.className = 'docx-intro-header';
    
    let introRules = null;
    
    for (let i = 0; i < children.length; i++) {
        const el = children[i];
        const text = el.innerText.trim();
        
        if (!text) continue;
        
        // 1. Title detection
        if (text.includes("RUDEDOG FAIR") && inIntro && (el.tagName.startsWith('H') || text.length < 30)) {
            const titleEl = document.createElement('h1');
            titleEl.innerText = text;
            introHeader.appendChild(titleEl);
            continue;
        }
        
        // 2. Subtitle / Content Pack line
        if (text.includes("CONTENT PACK") && inIntro) {
            const subEl = document.createElement('div');
            subEl.className = 'docx-intro-subtitle';
            subEl.innerText = text;
            introHeader.appendChild(subEl);
            continue;
        }
        
        // 3. Mission / Meta line: e.g. ภารกิจ: โกดังแตก | เป้า 8,000 คน
        if (text.startsWith("ภารกิจ:") && inIntro) {
            const metaGrid = document.createElement('div');
            metaGrid.className = 'docx-meta-grid';
            
            const parts = text.split('|');
            parts.forEach(part => {
                const subParts = part.split(':');
                const label = subParts[0] ? subParts[0].trim() : "ข้อมูล";
                const value = subParts[1] ? subParts[1].trim() : part.trim();
                
                const metaItem = document.createElement('div');
                metaItem.className = 'docx-meta-item';
                metaItem.innerHTML = `
                    <b>${value}</b>
                    <span>${label}</span>
                `;
                metaGrid.appendChild(metaItem);
            });
            introHeader.appendChild(metaGrid);
            continue;
        }
        
        // 4. Phases block
        if (text.includes("3 เฟส:") && inIntro) {
            const phaseBox = document.createElement('div');
            phaseBox.className = 'docx-phase-box';
            phaseBox.innerHTML = `<h4>3 เฟสหลักของแคมเปญ</h4>`;
            
            const list = document.createElement('ul');
            while (i + 1 < children.length) {
                const nextText = children[i+1].innerText.trim();
                if (nextText.includes("กฎทอง") || nextText.match(/^(D-\d+|LIVE)/i)) {
                    break;
                }
                i++;
                const li = document.createElement('li');
                li.innerText = children[i].innerText.trim();
                list.appendChild(li);
            }
            phaseBox.appendChild(list);
            introHeader.appendChild(phaseBox);
            continue;
        }
        
        // 5. Golden Rules block
        if (text.includes("กฎทองของทุกตอน") && inIntro) {
            introRules = document.createElement('div');
            introRules.className = 'docx-rules-box';
            introRules.innerHTML = `<h4>⚠️ กฎทองของทุกตอน (Golden Rules)</h4>`;
            
            const list = document.createElement('ul');
            if (children[i+1] && children[i+1].tagName === 'UL') {
                i++;
                const ulChildren = Array.from(children[i].children);
                ulChildren.forEach(liEl => {
                    const li = document.createElement('li');
                    li.innerText = liEl.innerText.trim();
                    list.appendChild(li);
                });
            } else {
                while (i + 1 < children.length) {
                    const nextText = children[i+1].innerText.trim();
                    if (nextText.match(/^(D-\d+|LIVE)/i)) break;
                    i++;
                    const li = document.createElement('li');
                    li.innerText = children[i].innerText.trim();
                    list.appendChild(li);
                }
            }
            introRules.appendChild(list);
            introHeader.appendChild(introRules);
            continue;
        }
        
        // 6. Episode/Day Card trigger: starts with D-X or LIVE
        const dayMatch = text.match(/^(D-\d+|LIVE)/i);
        if (dayMatch) {
            inIntro = false;
            
            if (currentCard) {
                container.appendChild(currentCard);
            }
            
            currentIdeaBox = null;
            currentIdeaList = null;
            
            let phaseClass = 'reach';
            if (text.toUpperCase().includes('BELIEVE')) {
                phaseClass = 'believe';
            } else if (text.toUpperCase().includes('MOVE') || text.toUpperCase().includes('LIVE')) {
                phaseClass = 'move';
            }
            
            currentCard = document.createElement('div');
            currentCard.className = `docx-card ${phaseClass}`;
            
            const cardHeader = document.createElement('div');
            cardHeader.className = 'docx-card-header';
            
            const parts = text.split('|');
            const epDay = parts[0] ? parts[0].trim() : text;
            const duration = parts[1] ? parts[1].trim() : '';
            
            let epTitle = '';
            if (i + 1 < children.length && (children[i+1].innerText.trim().startsWith('EP.') || children[i+1].innerText.trim().startsWith('LIVE.'))) {
                i++;
                epTitle = children[i].innerText.trim();
            }
            
            cardHeader.innerHTML = `
                <div class="ep-info">
                    <span class="ep-num">${epDay} ${duration ? ' | ' + duration : ''}</span>
                    <h3 class="ep-title">${epTitle || 'แผนงานประจำวัน'}</h3>
                </div>
                <span class="badge ${phaseClass}">${phaseClass.toUpperCase()}</span>
            `;
            currentCard.appendChild(cardHeader);
            
            currentCardBody = document.createElement('div');
            currentCardBody.className = 'docx-card-body';
            currentCard.appendChild(currentCardBody);
            continue;
        }
        
        if (inIntro) {
            const p = document.createElement('p');
            p.innerText = text;
            introHeader.appendChild(p);
            continue;
        }
        
        // 7. Inside Episode Card processing
        if (currentCardBody) {
            if (text.startsWith("จิตวิทยา:") || text.startsWith("เป้าหมาย:")) {
                const metaLine = document.createElement('div');
                metaLine.className = 'docx-card-meta-line';
                const parts = text.split(':');
                const label = parts[0].trim();
                const value = parts.slice(1).join(':').trim();
                metaLine.innerHTML = `<strong>${label}:</strong> ${value}`;
                currentCardBody.appendChild(metaLine);
                continue;
            }
            
            if (text.startsWith('[') && text.endsWith(']')) {
                const tag = document.createElement('div');
                tag.className = 'docx-card-tag';
                tag.innerText = text;
                currentCardBody.appendChild(tag);
                continue;
            }
            
            // Time script blocks: e.g. "0-3 วิ – HOOK"
            const timeBlockMatch = text.match(/^(\d+-\d+\s*วิ\s*–?\s*\w+)/i) || text.match(/^\d+-\d+\s*วิ/);
            if (timeBlockMatch) {
                currentIdeaBox = document.createElement('div');
                currentIdeaBox.className = 'docx-idea-box';
                
                const ideaTitle = document.createElement('div');
                ideaTitle.className = 'docx-idea-title';
                ideaTitle.innerText = text;
                currentIdeaBox.appendChild(ideaTitle);
                
                currentIdeaList = document.createElement('ul');
                currentIdeaList.className = 'docx-idea-details';
                currentIdeaBox.appendChild(currentIdeaList);
                
                currentCardBody.appendChild(currentIdeaBox);
                continue;
            }
            
            if (currentIdeaList) {
                if (el.tagName === 'UL' || el.tagName === 'OL') {
                    const ulChildren = Array.from(el.children);
                    ulChildren.forEach(liEl => {
                        const li = document.createElement('li');
                        li.innerHTML = liEl.innerHTML;
                        currentIdeaList.appendChild(li);
                    });
                } else {
                    const li = document.createElement('li');
                    li.innerHTML = el.innerHTML;
                    currentIdeaList.appendChild(li);
                }
            } else {
                const p = document.createElement('p');
                p.innerHTML = el.innerHTML;
                currentCardBody.appendChild(p);
            }
        }
    }
    
    if (currentCard) {
        container.appendChild(currentCard);
    }
    
    if (introHeader.children.length > 0) {
        container.insertBefore(introHeader, container.firstChild);
    }
    
    return container.outerHTML;
}

// Delete uploaded file handler
function deleteUploadedFile(room, file) {
    if (!confirm(`คุณแน่ใจหรือไม่ว่าต้องการลบไฟล์ "${file}" จากห้อง "${room}"?`)) {
        return;
    }
    
    playSynthSound('delete');
    logToTerminal(`[DELETE] Requesting deletion of ${file} from Room: ${room}...`);
    
    fetch(`/api/delete-file?room=${room}&filename=${encodeURIComponent(file)}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            playSynthSound('success');
            logToTerminal(`[DELETE SUCCESS] File ${file} deleted successfully.`);
            fetchUploadedFiles();
            fetchNotes();
        } else {
            playSynthSound('delete');
            logToTerminal(`[DELETE FAILED] Error: ${data.error}`);
            alert(`ไม่สามารถลบไฟล์ได้: ${data.error}`);
        }
    })
    .catch(err => {
        playSynthSound('delete');
        logToTerminal(`[DELETE ERROR] Connection failed: ${err.message}`);
        alert(`การเชื่อมต่อขัดข้อง: ${err.message}`);
    });
}

// Rename uploaded file handler
function renameUploadedFile(room, file) {
    const lastDotIndex = file.lastIndexOf('.');
    const ext = lastDotIndex !== -1 ? file.split('.').pop() : '';
    const baseName = lastDotIndex !== -1 ? file.substring(0, lastDotIndex) : file;
    
    let newBaseName = prompt(`เปลี่ยนชื่อไฟล์ "${file}" เป็น:`, baseName);
    if (newBaseName === null) return; // User cancelled
    
    newBaseName = newBaseName.trim();
    if (!newBaseName) {
        alert("กรุณาป้อนชื่อไฟล์ที่ต้องการ!");
        return;
    }
    
    const newFile = ext ? newBaseName + '.' + ext : newBaseName;
    if (newFile === file) return; // No change
    
    playSynthSound('click');
    logToTerminal(`[RENAME] Requesting rename from ${file} to ${newFile} in Room: ${room}...`);
    
    fetch(`/api/rename-file?room=${room}&old_filename=${encodeURIComponent(file)}&new_filename=${encodeURIComponent(newFile)}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            playSynthSound('success');
            logToTerminal(`[RENAME SUCCESS] Renamed ${file} to ${data.filename} successfully.`);
            fetchUploadedFiles();
            fetchNotes();
        } else {
            playSynthSound('delete');
            logToTerminal(`[RENAME FAILED] Error: ${data.error}`);
            alert(`ไม่สามารถเปลี่ยนชื่อไฟล์ได้: ${data.error}`);
        }
    })
    .catch(err => {
        playSynthSound('delete');
        logToTerminal(`[RENAME ERROR] Connection failed: ${err.message}`);
        alert(`การเชื่อมต่อขัดข้อง: ${err.message}`);
    });
}

// Collapsible hardcoded explorer groups toggle
function toggleExpGroup(el) {
    const group = el.parentElement;
    const files = group.querySelector('.exp-files');
    const arrow = group.querySelector('.group-arrow');
    const isCollapsed = files.style.display === 'none';
    
    if (isCollapsed) {
        files.style.display = 'flex';
        arrow.setAttribute('data-lucide', 'chevron-down');
    } else {
        files.style.display = 'none';
        arrow.setAttribute('data-lucide', 'chevron-right');
    }
    lucide.createIcons();
}

// Dynamic project file list rendering and actions
function fetchProjectFiles() {
    fetch('/api/project-files')
        .then(res => res.json())
        .then(data => {
            renderProjectFiles('campaign', data.campaign || []);
            renderProjectFiles('youtube', data.youtube || []);
            renderProjectFiles('compiler', data.compiler || []);
        })
        .catch(err => {
            console.error("Failed to load project files list:", err);
        });
}

function renderProjectFiles(category, files) {
    const container = document.getElementById(`project-${category}-files`);
    if (!container) return;
    
    if (files.length === 0) {
        container.innerHTML = `<div style="padding: 10px 14px; font-size: 11px; color: var(--text-dim); font-style: italic;">ไม่มีไฟล์ในกลุ่มนี้</div>`;
        return;
    }
    
    container.innerHTML = files.map(file => {
        let actionBtnHtml = '';
        
        let fileIcon = '📄';
        if (file.type === 'html') fileIcon = '🌐';
        else if (file.type === 'pdf') fileIcon = '📕';
        else if (file.type === 'code') fileIcon = '⚙️';
        
        let statusStyle = '';
        let missingNotice = '';
        if (file.exists === false) {
            statusStyle = 'color: var(--neon-pink); text-decoration: line-through; opacity: 0.6;';
            missingNotice = ' (ไม่พบไฟล์)';
        }

        if (file.canOpen) {
            const isPdf = file.type === 'pdf';
            const actionClass = isPdf ? 'text-pink' : '';
            const actionIcon = isPdf ? 'file-text' : 'external-link';
            actionBtnHtml = `
                <a class="btn-icon-action ${actionClass}" href="${file.openUrl}" target="_blank" title="เปิดไฟล์">
                    <i data-lucide="${actionIcon}" style="width: 11px; height: 11px;"></i>
                </a>
            `;
        } else {
            actionBtnHtml = `
                <button class="btn-icon-action" onclick="viewCodeFile('${file.key}', '${file.name}')" title="ดูพรีวิว">
                    <i data-lucide="eye" style="width: 11px; height: 11px;"></i>
                </button>
            `;
        }
        
        return `
            <div class="exp-file fade-in" style="padding: 6px 12px; display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                <span title="${file.path}" style="font-family: var(--font-tech); font-size: 11px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; ${statusStyle}">${fileIcon} ${file.label}${missingNotice}</span>
                <div style="display: flex; gap: 4px; flex-shrink: 0;">
                    ${actionBtnHtml}
                    <button class="btn-icon-action" onclick="renameProjectFile('${file.key}', '${file.name}')" title="เปลี่ยนชื่อ">
                        <i data-lucide="edit-2" style="width: 11px; height: 11px;"></i>
                    </button>
                    <button class="btn-icon-action text-pink" onclick="deleteProjectFile('${file.key}', '${file.name}')" title="ลบไฟล์">
                        <i data-lucide="trash-2" style="width: 11px; height: 11px;"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
    
    lucide.createIcons();
}

function renameProjectFile(key, currentName) {
    const lastDotIndex = currentName.lastIndexOf('.');
    const ext = lastDotIndex !== -1 ? currentName.split('.').pop() : '';
    const baseName = lastDotIndex !== -1 ? currentName.substring(0, lastDotIndex) : currentName;
    
    let newBaseName = prompt(`เปลี่ยนชื่อไฟล์โปรเจกต์ "${currentName}" เป็น:`, baseName);
    if (newBaseName === null) return;
    
    newBaseName = newBaseName.trim();
    if (!newBaseName) {
        alert("กรุณาป้อนชื่อไฟล์ที่ต้องการ!");
        return;
    }
    
    const newFile = ext ? newBaseName + '.' + ext : newBaseName;
    if (newFile === currentName) return;
    
    playSynthSound('click');
    logToTerminal(`[RENAME] Requesting rename for project file key '${key}' to '${newFile}'...`);
    
    fetch(`/api/rename-project-file?key=${key}&new_filename=${encodeURIComponent(newFile)}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            playSynthSound('success');
            logToTerminal(`[RENAME SUCCESS] Project file renamed to ${data.filename} successfully.`);
            fetchProjectFiles();
            fetchNotes();
        } else {
            playSynthSound('delete');
            logToTerminal(`[RENAME FAILED] Error: ${data.error}`);
            alert(`ไม่สามารถเปลี่ยนชื่อไฟล์โปรเจกต์ได้: ${data.error}`);
        }
    })
    .catch(err => {
        playSynthSound('delete');
        logToTerminal(`[RENAME ERROR] Connection failed: ${err.message}`);
        alert(`การเชื่อมต่อขัดข้อง: ${err.message}`);
    });
}

function deleteProjectFile(key, currentName) {
    if (!confirm(`คุณแน่ใจหรือไม่ว่าต้องการลบไฟล์โปรเจกต์ "${currentName}"? การดำเนินการนี้จะลบไฟล์จริงออกจากระบบ.`)) {
        return;
    }
    
    playSynthSound('delete');
    logToTerminal(`[DELETE] Requesting deletion of project file key '${key}'...`);
    
    fetch(`/api/delete-project-file?key=${key}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            playSynthSound('success');
            logToTerminal(`[DELETE SUCCESS] Project file '${currentName}' deleted successfully.`);
            fetchProjectFiles();
            fetchNotes();
        } else {
            playSynthSound('delete');
            logToTerminal(`[DELETE FAILED] Error: ${data.error}`);
            alert(`ไม่สามารถลบไฟล์โปรเจกต์ได้: ${data.error}`);
        }
    })
    .catch(err => {
        playSynthSound('delete');
        logToTerminal(`[DELETE ERROR] Connection failed: ${err.message}`);
        alert(`การเชื่อมต่อขัดข้อง: ${err.message}`);
    });
}

// Tab Navigation Switcher
function switchTab(tabId) {
    playSynthSound('click');
    
    // Deactivate all tabs and buttons
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
    
    // Activate target tab and button
    const targetTab = document.getElementById(`tab-${tabId}`);
    const targetBtn = document.getElementById(`tab-btn-${tabId}`);
    if (targetTab) targetTab.classList.add('active');
    if (targetBtn) targetBtn.classList.add('active');
    
    logToTerminal(`[NAV] Switched view to tab: ${tabId.toUpperCase()}`);
    lucide.createIcons();
}

// PIN Vault Code Management
let enteredPin = "";

function pressPin(digit) {
    if (enteredPin.length >= 4) return;
    playSynthSound('click');
    enteredPin += digit;
    updatePinDisplay();
}

function clearPin() {
    playSynthSound('click');
    enteredPin = "";
    updatePinDisplay();
    const errorEl = document.getElementById('pin-error-msg');
    if (errorEl) errorEl.style.display = 'none';
}

function updatePinDisplay() {
    const dots = document.querySelectorAll('.pin-display .pin-dot');
    dots.forEach((dot, index) => {
        if (index < enteredPin.length) {
            dot.classList.add('filled');
        } else {
            dot.classList.remove('filled');
        }
    });
}

function submitPin() {
    if (enteredPin.length < 4) {
        playSynthSound('delete');
        return;
    }
    
    logToTerminal(`[SECURITY] Verifying access keycode with auth server...`);
    
    fetch('/api/verify-pin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin: enteredPin })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            playSynthSound('success');
            logToTerminal(`[SECURITY SUCCESS] Access granted. Decrypting workspace...`);
            sessionStorage.setItem('boss_unlocked', 'true');
            checkBossSession();
            
            // Success animation
            const lockCard = document.querySelector('.lock-card');
            if (lockCard) {
                lockCard.style.boxShadow = '0 0 40px rgba(0, 255, 204, 0.25)';
                lockCard.style.borderColor = 'var(--neon-cyan)';
            }
            
            // Switch view
            setTimeout(() => {
                const lockScreen = document.getElementById('boss-lock-screen');
                const workspaceContent = document.getElementById('boss-workspace-content');
                if (lockScreen) lockScreen.style.display = 'none';
                if (workspaceContent) {
                    workspaceContent.style.display = 'flex';
                    workspaceContent.classList.add('fade-in');
                }
            }, 600);
        } else {
            playSynthSound('delete');
            logToTerminal(`[SECURITY FAILURE] Invalid PIN entered. Access Denied.`);
            showPinError();
        }
    })
    .catch(err => {
        playSynthSound('delete');
        logToTerminal(`[SECURITY ERROR] Connection failed: ${err.message}`);
        showPinError();
    });
}

function showPinError() {
    const errorEl = document.getElementById('pin-error-msg');
    if (errorEl) {
        errorEl.style.display = 'block';
        errorEl.innerText = "ACCESS DENIED: INVALID KEYCODE";
    }
    enteredPin = "";
    updatePinDisplay();
}

function checkBossSession() {
    const isUnlocked = sessionStorage.getItem('boss_unlocked') === 'true';
    const lockScreen = document.getElementById('boss-lock-screen');
    const workspaceContent = document.getElementById('boss-workspace-content');
    const bossOption = document.getElementById('room-opt-boss');
    const bossNavIcon = document.getElementById('boss-nav-icon');
    const bossNavText = document.getElementById('boss-nav-text');
    
    if (isUnlocked) {
        if (lockScreen) lockScreen.style.display = 'none';
        if (workspaceContent) workspaceContent.style.display = 'flex';
        if (bossOption) {
            bossOption.disabled = false;
            bossOption.style.display = 'block';
            bossOption.innerText = "บอส (Boss)";
        }
        if (bossNavIcon) {
            bossNavIcon.setAttribute('data-lucide', 'unlock');
            bossNavIcon.style.color = 'var(--neon-cyan)';
        }
        if (bossNavText) {
            bossNavText.innerText = "Boss Center";
        }
    } else {
        if (lockScreen) lockScreen.style.display = 'flex';
        if (workspaceContent) workspaceContent.style.display = 'none';
        if (bossOption) {
            bossOption.disabled = true;
            bossOption.style.display = 'none';
        }
        if (bossNavIcon) {
            bossNavIcon.setAttribute('data-lucide', 'lock');
            bossNavIcon.style.color = 'var(--neon-pink)';
        }
        if (bossNavText) {
            bossNavText.innerText = "Boss Workspace";
        }
    }
    lucide.createIcons();
}

function handleRoomSelectChange() {
    playSynthSound('click');
    const select = document.getElementById('user-room-select');
    if (select) {
        logToTerminal(`[ROOM] Selected upload room: ${select.value}`);
    }
}

function renameRoomFolder(roomKey) {
    playSynthSound('click');
    const currentLabel = currentRoomLabels[roomKey] || roomKey;
    let newLabel = prompt(`เปลี่ยนชื่อกลุ่มโฟลเดอร์ "${currentLabel}" เป็น:`, currentLabel);
    if (newLabel === null) return;
    newLabel = newLabel.trim();
    if (!newLabel) {
        alert("กรุณากรอกชื่อกลุ่มโฟลเดอร์!");
        return;
    }
    
    logToTerminal(`[ROOM] Requesting folder rename for key ${roomKey} to: ${newLabel}...`);
    
    fetch(`/api/rename-room?room=${roomKey}&label=${encodeURIComponent(newLabel)}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            playSynthSound('success');
            logToTerminal(`[ROOM SUCCESS] Room key ${roomKey} display name updated to: ${newLabel}`);
            fetchUploadedFiles();
            fetchNotes();
        } else {
            playSynthSound('delete');
            alert(`ไม่สามารถเปลี่ยนชื่อโฟลเดอร์ได้: ${data.error}`);
        }
    })
    .catch(err => {
        playSynthSound('delete');
        alert(`การเชื่อมต่อขัดข้อง: ${err.message}`);
    });
}

function updateRoomDropdownLabels(roomLabels) {
    const isUnlocked = sessionStorage.getItem('boss_unlocked') === 'true';
    
    const optBoss = document.getElementById('room-opt-boss');
    const optF1 = document.getElementById('room-opt-friend1');
    const optF2 = document.getElementById('room-opt-friend2');
    const optF3 = document.getElementById('room-opt-friend3');
    const optF4 = document.getElementById('room-opt-friend4');
    
    if (optBoss) {
        optBoss.disabled = !isUnlocked;
        optBoss.style.display = isUnlocked ? 'block' : 'none';
        optBoss.innerText = isUnlocked 
            ? (roomLabels.Boss || "บอส (Boss)") 
            : `${roomLabels.Boss || "บอส (Boss)"} - Locked`;
    }
    if (optF1) optF1.innerText = roomLabels.Friend1 || "เพื่อน 1 (Friend 1)";
    if (optF2) optF2.innerText = roomLabels.Friend2 || "เพื่อน 2 (Friend 2)";
    if (optF3) optF3.innerText = roomLabels.Friend3 || "เพื่อน 3 (Friend 3)";
    if (optF4) optF4.innerText = roomLabels.Friend4 || "เพื่อน 4 (Friend 4)";
}

// Bind keyboard support for PIN
document.addEventListener('keyup', (e) => {
    const activeTab = document.querySelector('.tab-content.active');
    if (activeTab && activeTab.id === 'tab-boss' && sessionStorage.getItem('boss_unlocked') !== 'true') {
        if (e.key >= '0' && e.key <= '9') {
            pressPin(e.key);
        } else if (e.key === 'Backspace') {
            clearPin();
        } else if (e.key === 'Enter') {
            submitPin();
        }
    }
});




