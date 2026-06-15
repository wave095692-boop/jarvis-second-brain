// Invidious API instances to use as fallback
const INVIDIOUS_INSTANCES = [
    "https://yewtu.be",
    "https://invidious.privacydev.net",
    "https://inv.nadeko.net",
    "https://invidious.projectsegfau.lt",
    "https://inv.tux.im",
    "https://vid.puffyan.us",
    "https://invidious.flokinet.to"
];

let workingInstances = [...INVIDIOUS_INSTANCES];
let currentInstanceIndex = 0;

// Load YouTube Iframe API dynamically
const tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let ytPlayer = null;

window.onYouTubeIframeAPIReady = function() {
    console.log("YouTube Iframe Player API Ready");
};

// Measure responsiveness of Invidious nodes on startup
async function checkInstanceResponsiveness() {
    console.log("Measuring Invidious instances responsiveness...");
    const checkPromises = INVIDIOUS_INSTANCES.map(async (url) => {
        const start = performance.now();
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 2000); // 2 second timeout
            
            // Check searching lofi as a query which uses real Invidious logic
            const response = await fetch(`${url}/api/v1/search?q=lofi&type=video`, { signal: controller.signal });
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const duration = performance.now() - start;
                return { url, duration, ok: true };
            }
        } catch (e) {
            // Fails or times out
        }
        return { url, duration: Infinity, ok: false };
    });
    
    const results = await Promise.all(checkPromises);
    
    // Sort successful ones by time
    const successful = results
        .filter(r => r.ok)
        .sort((a, b) => a.duration - b.duration)
        .map(r => r.url);
        
    const failed = results
        .filter(r => !r.ok)
        .map(r => r.url);
        
    if (successful.length > 0) {
        workingInstances = [...successful, ...failed];
        console.log("Responsive Invidious instances sorted:", workingInstances);
    } else {
        console.warn("All Invidious instance checks failed. Using default order.");
        workingInstances = [...INVIDIOUS_INSTANCES];
    }
    currentInstanceIndex = 0;
}

// Wait up to 3 seconds for the YouTube Iframe API script to fully load
function ensureYoutubeApi() {
    return new Promise((resolve) => {
        if (typeof YT !== 'undefined' && YT.Player) {
            resolve(true);
            return;
        }
        
        let elapsed = 0;
        const interval = setInterval(() => {
            elapsed += 100;
            if (typeof YT !== 'undefined' && YT.Player) {
                clearInterval(interval);
                resolve(true);
            } else if (elapsed >= 3000) {
                clearInterval(interval);
                resolve(false);
            }
        }, 100);
    });
}

// Watchdog timer variables for stuck play state
let playbackWatchdog = null;

function startPlaybackWatchdog() {
    clearPlaybackWatchdog();
    playbackWatchdog = setTimeout(() => {
        if (ytPlayer && typeof ytPlayer.getPlayerState === 'function') {
            const state = ytPlayer.getPlayerState();
            console.log("Watchdog check state:", state);
            // If the state is still -1 (unstarted), 3 (buffering), or 5 (cued), play has failed or is blocked
            if (state === -1 || state === 3 || state === 5) {
                console.warn("Watchdog detected player is stuck. Auto-switching to Backup Player.");
                showToast("พบปัญหาในการเล่นวิดีโอหลัก กำลังสลับไปใช้เครื่องเล่นสำรองอัตโนมัติครับบอส...");
                toggleBackupPlayer();
            }
        }
    }, 6000); // 6 seconds timeout
}

function clearPlaybackWatchdog() {
    if (playbackWatchdog) {
        clearTimeout(playbackWatchdog);
        playbackWatchdog = null;
    }
}

// Application State
let currentState = {
    history: JSON.parse(localStorage.getItem('yt_premium_history') || '[]'),
    watchLater: JSON.parse(localStorage.getItem('yt_premium_watch_later') || '[]'),
    favorites: JSON.parse(localStorage.getItem('yt_premium_favorites') || '[]'),
    currentVideo: null,
    currentView: 'home',
    isMiniPlayer: false
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    checkInstanceResponsiveness();
    loadDefaultHomeFeed();
    renderGrids();

    // Loader elements
    const introLoader = document.getElementById('intro-loader');
    const introRing = document.getElementById('intro-ring');
    const introLogo = document.getElementById('intro-logo');
    const introBar = document.getElementById('intro-bar');
    const introProgress = document.getElementById('intro-progress');

    let isInitialized = false;
    const initializeSystem = () => {
        if (isInitialized) return;
        isInitialized = true;

        // Play sounds using a single, explicitly-resumed AudioContext
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            playTudum(audioCtx);
            playDownloadSound(audioCtx);
        } catch (e) {
            console.error("Audio play failed:", e);
        }

        // Add CSS animation classes
        if (introRing) introRing.classList.add('animate');
        if (introLogo) introLogo.classList.add('animate');
        if (introBar) introBar.classList.add('animate');

        // Animate loading percentage text
        if (introProgress) {
            let percent = 0;
            introProgress.innerText = "DOWNLOADING PROTOCOLS: 0%";
            const interval = setInterval(() => {
                percent += Math.floor(Math.random() * 8) + 4; // increment randomly between 4% and 11%
                if (percent >= 100) {
                    percent = 100;
                    introProgress.innerText = "COMPLETE - DOWNLOADING PROTOCOLS: 100%";
                    introProgress.style.color = "var(--border-yellow)";
                    introProgress.style.textShadow = "0 0 10px rgba(255, 255, 0, 0.8)";
                    clearInterval(interval);
                } else {
                    introProgress.innerText = `DOWNLOADING PROTOCOLS: ${percent}%`;
                }
            }, 60);
        }

        // Fade out loader screen automatically after 2.2s zoom animation
        setTimeout(() => {
            if (introLoader) {
                introLoader.style.opacity = '0';
                setTimeout(() => {
                    introLoader.style.display = 'none';
                }, 800);
            }
        }, 2200);
    };

    if (introLoader) {
        introLoader.addEventListener('click', initializeSystem);
        // Fallback for keyboard access
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                initializeSystem();
            }
        });
    } else {
        initializeSystem();
    }

    // Fetch network information for sidebar HUD
    fetchNetworkInfo();

    // Initialize browser history state
    try {
        history.replaceState({ view: 'home' }, '', '#home');
    } catch(e) {}
});

// Fetch network status from custom server.py API
function fetchNetworkInfo() {
    fetch('/api/network')
        .then(res => {
            if (!res.ok) throw new Error("API not ok");
            return res.json();
        })
        .then(data => {
            const lanEl = document.getElementById('hud-lan-ip');
            const pubEl = document.getElementById('hud-public-ip');
            
            if (lanEl && data.lan_ip) {
                lanEl.innerText = `http://${data.lan_ip}:8000`;
                lanEl.href = `http://${data.lan_ip}:8000`;
            }
            if (pubEl && data.public_ip) {
                pubEl.innerText = data.public_ip;
            }
        })
        .catch(err => {
            console.warn("Failed to fetch network info:", err);
            const lanEl = document.getElementById('hud-lan-ip');
            const pubEl = document.getElementById('hud-public-ip');
            if (lanEl) {
                lanEl.innerText = "http://localhost:8000";
                lanEl.href = "http://localhost:8000";
            }
            if (pubEl) pubEl.innerText = "Unavailable";
        });
}

// Synthesize Netflix "Tudum" sound programmatically using Web Audio API
function playTudum(ctx) {
    if (!ctx) return;
    
    // Lowpass filter for warm cinematic tone (slightly higher cutoff for laptop speakers)
    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(450, ctx.currentTime);
    filter.connect(ctx.destination);

    // Note 1 (First bass thump - shifted up to 130Hz for laptop speaker audibility)
    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sawtooth';
    osc1.frequency.setValueAtTime(130, ctx.currentTime); 
    gain1.gain.setValueAtTime(0, ctx.currentTime);
    gain1.gain.linearRampToValueAtTime(0.8, ctx.currentTime + 0.08); // Higher gain
    gain1.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.8);
    osc1.connect(gain1);
    gain1.connect(filter);
    
    // Note 2 (Second bass thump - overlapping and higher, 165Hz)
    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'sawtooth';
    osc2.frequency.setValueAtTime(165, ctx.currentTime + 0.12); 
    gain2.gain.setValueAtTime(0, ctx.currentTime + 0.12);
    gain2.gain.linearRampToValueAtTime(0.9, ctx.currentTime + 0.20); // Higher gain
    gain2.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1.2);
    osc2.connect(gain2);
    gain2.connect(filter);

    // Note 3 (High harmony synth pad - 330Hz, very clear)
    const osc3 = ctx.createOscillator();
    const gain3 = ctx.createGain();
    osc3.type = 'triangle';
    osc3.frequency.setValueAtTime(330, ctx.currentTime + 0.22); 
    gain3.gain.setValueAtTime(0, ctx.currentTime + 0.22);
    gain3.gain.linearRampToValueAtTime(0.45, ctx.currentTime + 0.50); // Higher gain (0.45)
    gain3.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.6);
    osc3.connect(gain3);
    gain3.connect(ctx.destination); // bypass filter for brightness

    // Note 4 (High metallic ring chime for premium gamer feel)
    const osc4 = ctx.createOscillator();
    const gain4 = ctx.createGain();
    osc4.type = 'sine';
    osc4.frequency.setValueAtTime(880, ctx.currentTime + 0.25); // A5 (880Hz)
    gain4.gain.setValueAtTime(0, ctx.currentTime + 0.25);
    gain4.gain.linearRampToValueAtTime(0.25, ctx.currentTime + 0.35);
    gain4.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.0);
    osc4.connect(gain4);
    gain4.connect(ctx.destination);

    osc1.start(ctx.currentTime);
    osc1.stop(ctx.currentTime + 1.2);
    
    osc2.start(ctx.currentTime);
    osc2.stop(ctx.currentTime + 1.5);

    osc3.start(ctx.currentTime);
    osc3.stop(ctx.currentTime + 2.0);

    osc4.start(ctx.currentTime);
    osc4.stop(ctx.currentTime + 1.5);
}

// Synthesize dynamic cyberpunk loading sound using Web Audio API
function playDownloadSound(ctx) {
    if (!ctx) return;
    const now = ctx.currentTime;
    
    // Step 1: 4 digital loading progress blips (pitching upward, louder & higher pitch)
    const freqs = [400, 500, 600, 700];
    freqs.forEach((freq, idx) => {
        const tickTime = now + (idx * 0.25); // play every 250ms
        
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, tickTime);
        
        // Pitch sweep up slightly for each tick
        osc.frequency.exponentialRampToValueAtTime(freq * 1.15, tickTime + 0.12);
        
        gain.gain.setValueAtTime(0, tickTime);
        gain.gain.linearRampToValueAtTime(0.35, tickTime + 0.02); // Higher gain (0.35)
        gain.gain.exponentialRampToValueAtTime(0.001, tickTime + 0.12);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        osc.start(tickTime);
        osc.stop(tickTime + 0.18);
    });
    
    // Step 2: Satisfying Level-up Chime / Laser Sweep when loader finishes (at 1.25s)
    const chimeTime = now + 1.25;
    
    // Base frequency osc (high triangle sweep)
    const oscChime = ctx.createOscillator();
    const gainChime = ctx.createGain();
    oscChime.type = 'triangle';
    oscChime.frequency.setValueAtTime(880, chimeTime); // A5
    oscChime.frequency.exponentialRampToValueAtTime(1760, chimeTime + 0.18); // sweep up to A6
    
    gainChime.gain.setValueAtTime(0, chimeTime);
    gainChime.gain.linearRampToValueAtTime(0.35, chimeTime + 0.06); // Higher gain (0.35)
    gainChime.gain.exponentialRampToValueAtTime(0.001, chimeTime + 0.9);
    
    oscChime.connect(gainChime);
    gainChime.connect(ctx.destination);
    
    // Overlapping sine harmony osc (E6 fifth)
    const oscHarm = ctx.createOscillator();
    const gainHarm = ctx.createGain();
    oscHarm.type = 'sine';
    oscHarm.frequency.setValueAtTime(1320, chimeTime + 0.06); 
    
    gainHarm.gain.setValueAtTime(0, chimeTime + 0.06);
    gainHarm.gain.linearRampToValueAtTime(0.18, chimeTime + 0.12); // Higher gain
    gainHarm.gain.exponentialRampToValueAtTime(0.001, chimeTime + 0.7);
    
    oscHarm.connect(gainHarm);
    gainHarm.connect(ctx.destination);
    
    oscChime.start(chimeTime);
    oscChime.stop(chimeTime + 1.1);
    oscHarm.start(chimeTime + 0.06);
    oscHarm.stop(chimeTime + 0.9);
}

// Helper: Show toast notification
function showToast(message) {
    const toast = document.getElementById('app-toast');
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Switch view
let viewHistory = ['home'];

function switchView(viewName, isBack = false) {
    // Hide all views
    const views = ['home', 'search', 'player', 'history', 'watch-later', 'favorites'];
    views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        if (el) el.style.display = 'none';
    });

    // Remove active class from sidebar menu items
    const menuItems = ['home', 'search', 'history', 'watch-later', 'favorites'];
    menuItems.forEach(item => {
        const el = document.getElementById(`menu-${item}`);
        if (el) el.classList.remove('active');
    });

    // Show target view
    const targetEl = document.getElementById(`view-${viewName}`);
    if (targetEl) targetEl.style.display = 'block';

    // Highlight target menu
    const targetMenu = document.getElementById(`menu-${viewName}`);
    if (targetMenu) targetMenu.classList.add('active');

    // Handle history stack
    if (!isBack) {
        if (viewHistory[viewHistory.length - 1] !== viewName) {
            viewHistory.push(viewName);
            try {
                history.pushState({ view: viewName }, '', '#' + viewName);
            } catch (e) {}
        }
    }

    currentState.currentView = viewName;

    // Reset mini-player class if opening the main player view
    if (viewName === 'player') {
        document.body.classList.remove('mini-player-active');
        currentState.isMiniPlayer = false;
    } else {
        // Stop the video if moving away from player and mini-player is not active
        if (!currentState.isMiniPlayer && ytPlayer) {
            try {
                if (typeof ytPlayer.stopVideo === 'function') {
                    ytPlayer.stopVideo();
                }
            } catch (e) {
                console.warn("Failed to stop video:", e);
            }
            // Clear iframe container
            const playerWrapper = document.getElementById('video-wrapper');
            if (playerWrapper) {
                playerWrapper.innerHTML = '';
            }
        }
    }

    renderGrids();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goBack() {
    if (viewHistory.length > 1) {
        viewHistory.pop(); // Remove current view
        const prevView = viewHistory[viewHistory.length - 1];
        switchView(prevView, true);
        try {
            history.replaceState({ view: prevView }, '', '#' + prevView);
        } catch (e) {}
    } else {
        switchView('home');
    }
}

// Global popstate event listener for browser Back/Forward navigation
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.view) {
        const idx = viewHistory.indexOf(event.state.view);
        if (idx > -1) {
            viewHistory = viewHistory.slice(0, idx + 1);
        } else {
            viewHistory.push(event.state.view);
        }
        switchView(event.state.view, true);
    } else {
        viewHistory = ['home'];
        switchView('home', true);
    }
});

// Fetch helper from Invidious with automatic fallback
async function fetchFromInvidious(endpoint) {
    let attempts = 0;
    const maxAttempts = INVIDIOUS_INSTANCES.length;

    while (attempts < maxAttempts) {
        const base = INVIDIOUS_INSTANCES[currentInstanceIndex];
        const url = `${base}${endpoint}`;
        console.log(`Trying Invidious instance: ${url}`);
        
        try {
            const controller = new AbortController();
            const id = setTimeout(() => controller.abort(), 7000); // 7-second timeout
            
            const response = await fetch(url, { signal: controller.signal });
            clearTimeout(id);
            
            if (response.ok) {
                const data = await response.json();
                return data;
            }
            throw new Error(`Response not OK: ${response.status}`);
        } catch (err) {
            console.warn(`Instance failed: ${base}. Error: ${err.message}`);
            // Move to next instance
            currentInstanceIndex = (currentInstanceIndex + 1) % INVIDIOUS_INSTANCES.length;
            attempts++;
        }
    }
    throw new Error("All Invidious instances are currently unavailable. Please try using a direct URL instead.");
}

// Helper: Format duration (seconds to MM:SS)
function formatDuration(seconds) {
    if (!seconds) return "";
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Extract YouTube ID from URL
function extractVideoId(url) {
    if (!url) return null;
    
    // Support Shorts
    if (url.includes('shorts/')) {
        const parts = url.split('shorts/');
        if (parts.length > 1) {
            return parts[1].split('?')[0].split('&')[0].substring(0, 11);
        }
    }
    
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}

// Play a video by ID and details
// Play a video by ID and details
let isUsingBackupPlayer = false;

async function playVideo(videoId, title, channel) {
    const video = { videoId, title, author: channel };
    currentState.currentVideo = video;
    
    // Reset backup player state
    isUsingBackupPlayer = false;
    const btnBackup = document.getElementById('btn-backup-player');
    const txtBackup = document.getElementById('txt-backup');
    if (btnBackup) {
        btnBackup.style.borderColor = 'var(--border-yellow)';
        btnBackup.style.color = 'var(--border-yellow)';
        txtBackup.innerText = "เครื่องเล่นสำรอง (หากเล่นไม่ได้)";
    }
    const btnRotate = document.getElementById('btn-backup-rotate');
    if (btnRotate) {
        btnRotate.style.display = 'none';
    }

    // Add to history
    addToHistory(video);
    
    // Switch view to player
    switchView('player');
    
    // Render iframe placeholder
    const playerWrapper = document.getElementById('video-wrapper');
    playerWrapper.innerHTML = `<div id="youtube-player-placeholder" style="width:100%; height:100%;"></div>`;

    // Clear any existing watchdog
    clearPlaybackWatchdog();

    // Ensure YouTube API is fully loaded
    const apiLoaded = await ensureYoutubeApi();

    if (apiLoaded) {
        try {
            ytPlayer = new YT.Player('youtube-player-placeholder', {
                width: '100%',
                height: '100%',
                videoId: videoId,
                playerVars: {
                    'autoplay': 1,
                    'rel': 0,
                    'enablejsapi': 1,
                    'origin': window.location.origin
                },
                events: {
                    'onStateChange': onPlayerStateChange,
                    'onError': onPlayerError
                }
            });
            // Start the watchdog timer to detect silent embedding block
            startPlaybackWatchdog();
        } catch (e) {
            console.warn("YT Player init error, using standard iframe fallback:", e);
            useStandardIframeFallback(playerWrapper, videoId, title);
        }
    } else {
        console.warn("YT API failed to load in time, using standard iframe fallback");
        useStandardIframeFallback(playerWrapper, videoId, title);
    }

    // Set titles
    document.getElementById('player-title').innerText = title;
    
    // Update button states
    updatePlayerButtonsState();

    // Fetch related/suggested videos
    loadSuggestedVideos(videoId);
}

function useStandardIframeFallback(playerWrapper, videoId, title) {
    playerWrapper.innerHTML = `
        <iframe 
            src="https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&enablejsapi=1&origin=${encodeURIComponent(window.location.origin)}" 
            title="${title}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen>
        </iframe>
    `;
}

// Watch state changes to clear watchdog if playing
function onPlayerStateChange(event) {
    console.log("Player state changed:", event.data);
    // 1 is PLAYING
    if (event.data === 1) {
        console.log("Video playing successfully. Clearing watchdog.");
        clearPlaybackWatchdog();
    }
}

// Automatically detect when a video fails to play and trigger backup player
function onPlayerError(event) {
    console.warn("YouTube player error detected. Error code:", event.data);
    // 2 (invalid parameter), 5 (HTML5 player issue), 101/150 (embedding blocked by owner)
    if (event.data === 101 || event.data === 150 || event.data === 5 || event.data === 2) {
        showToast("วิดีโอนี้บล็อกการเล่นภายนอก กำลังสลับไปใช้เครื่องเล่นสำรองอัตโนมัติครับ...");
        clearPlaybackWatchdog();
        setTimeout(() => {
            if (!isUsingBackupPlayer) {
                toggleBackupPlayer();
            }
        }, 1000);
    }
}

// Toggle between main YouTube embed and backup Invidious player
function toggleBackupPlayer() {
    if (!currentState.currentVideo) return;
    const videoId = currentState.currentVideo.videoId;
    const playerWrapper = document.getElementById('video-wrapper');
    const btnBackup = document.getElementById('btn-backup-player');
    const txtBackup = document.getElementById('txt-backup');
    const btnRotate = document.getElementById('btn-backup-rotate');
    
    clearPlaybackWatchdog();
    
    if (isUsingBackupPlayer) {
        // Switch back to normal
        isUsingBackupPlayer = false;
        if (btnRotate) btnRotate.style.display = 'none';
        playVideo(currentState.currentVideo.videoId, currentState.currentVideo.title, currentState.currentVideo.author);
        showToast("สลับกลับมาใช้เครื่องเล่น YouTube หลักแล้วครับ");
    } else {
        // Switch to backup Invidious player
        const activeInstance = workingInstances[currentInstanceIndex];
        playerWrapper.innerHTML = `
            <iframe 
                src="${activeInstance}/embed/${videoId}" 
                title="${escapeHtml(currentState.currentVideo.title)}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen>
            </iframe>
        `;
        btnBackup.style.borderColor = 'var(--border-cyan)';
        btnBackup.style.color = 'var(--border-cyan)';
        txtBackup.innerText = "เครื่องเล่นหลัก YouTube";
        isUsingBackupPlayer = true;
        if (btnRotate) btnRotate.style.display = 'flex';
        showToast(`สลับไปใช้เครื่องเล่นสำรอง (${activeInstance.replace('https://', '')}) สำเร็จครับบอส`);
    }
}

// Rotate through working backup instances
function rotateBackupInstance() {
    if (!currentState.currentVideo || !isUsingBackupPlayer) return;
    
    currentInstanceIndex = (currentInstanceIndex + 1) % workingInstances.length;
    const activeInstance = workingInstances[currentInstanceIndex];
    const videoId = currentState.currentVideo.videoId;
    const playerWrapper = document.getElementById('video-wrapper');
    
    playerWrapper.innerHTML = `
        <iframe 
            src="${activeInstance}/embed/${videoId}" 
            title="${escapeHtml(currentState.currentVideo.title)}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen>
        </iframe>
    `;
    
    showToast(`เปลี่ยนเซิร์ฟเวอร์สำรองเป็น: ${activeInstance.replace('https://', '')}`);
}

// Play via pasting URL
function playFromUrl() {
    const input = document.getElementById('input-url');
    const url = input.value.trim();
    if (!url) {
        showToast("กรุณาใส่ลิงก์ YouTube ครับบอส");
        return;
    }
    
    const videoId = extractVideoId(url);
    if (!videoId) {
        showToast("รูปแบบลิงก์ไม่ถูกต้องครับบอส ลองตรวจสอบอีกครั้งนะครับ");
        return;
    }
    
    input.value = "";
    playVideo(videoId, "วิดีโอจากลิงก์ด่วน", "YouTube Video");
}

// Fetch similar videos helper
function fetchSimilarVideos(firstVideo) {
    return fetchFromInvidious(`/api/v1/videos/${firstVideo.videoId}`)
        .then(details => {
            if (details && details.recommendedVideos && details.recommendedVideos.length > 0) {
                return details.recommendedVideos;
            }
            throw new Error("No recommended videos in details");
        })
        .catch(err => {
            console.warn("Falling back to title search for related videos:", err);
            // Fallback: search for keywords in the video title
            const cleanTitle = firstVideo.title
                .replace(/[\[\]\(\)\-\|\:\,\.\?\!\@]/g, ' ')
                .split(' ')
                .filter(w => w.length > 2)
                .slice(0, 3)
                .join(' ');
            return fetchFromInvidious(`/api/v1/search?q=${encodeURIComponent(cleanTitle || 'music')}&type=video`)
                .then(videos => (videos || []).filter(v => v.videoId !== firstVideo.videoId));
        });
}

// Trigger Search
function triggerSearch() {
    const input = document.getElementById('input-search');
    const query = input.value.trim();
    if (!query) return;

    // Switch view
    switchView('search');
    document.getElementById('search-title').innerText = `ผลการค้นหาสำหรับ: "${query}"`;
    
    // Load skeletons
    const grid = document.getElementById('grid-search');
    grid.innerHTML = Array(8).fill(0).map(() => `
        <div class="video-card">
            <div class="skeleton-thumbnail skeleton"></div>
            <div class="video-info">
                <div class="skeleton-title skeleton"></div>
                <div class="skeleton-meta skeleton"></div>
            </div>
        </div>
    `).join('');

    // Fetch from Invidious
    fetchFromInvidious(`/api/v1/search?q=${encodeURIComponent(query)}&type=video`)
        .then(videos => {
            if (!videos || videos.length === 0) {
                grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-secondary);">ไม่พบข้อมูลวิดีโอที่ค้นหาครับบอส</div>`;
                return;
            }
            
            const mainHtml = videos.map(video => {
                const thumb = `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg`;
                const duration = formatDuration(video.lengthSeconds);
                return `
                    <div class="video-card fade-in" onclick="playVideo('${video.videoId}', '${escapeHtml(video.title)}', '${escapeHtml(video.author)}')">
                        <div class="thumbnail-wrapper">
                            <img class="thumbnail-img" src="${thumb}" alt="${escapeHtml(video.title)}" loading="lazy">
                            ${duration ? `<div class="video-duration">${duration}</div>` : ''}
                        </div>
                        <div class="video-info">
                            <div class="video-title">${escapeHtml(video.title)}</div>
                            <div class="video-meta">
                                <div class="video-channel">${escapeHtml(video.author)}</div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            grid.innerHTML = mainHtml;
            lucide.createIcons();

            // Fetch and append similar/recommended videos based on the top search result
            const topVideo = videos[0];
            fetchSimilarVideos(topVideo)
                .then(similarVideos => {
                    const filtered = (similarVideos || [])
                        .filter(v => v.videoId !== topVideo.videoId)
                        .slice(0, 8);
                    
                    if (filtered.length > 0) {
                        const similarTitleHtml = `
                            <div style="grid-column: 1 / -1; margin-top: 35px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; border-top: 1px dashed var(--border-color); padding-top: 25px;">
                                <span style="font-family: var(--font-gamer); font-size: 14px; font-weight: 800; color: var(--border-pink); letter-spacing: 1px;">💡 วิดีโอแนะนำที่คล้ายกัน (JARVIS PROBABILITY SUGGESTION)</span>
                            </div>
                        `;
                        const similarCardsHtml = filtered.map(video => {
                            const thumb = `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg`;
                            const duration = formatDuration(video.lengthSeconds);
                            return `
                                <div class="video-card fade-in" onclick="playVideo('${video.videoId}', '${escapeHtml(video.title)}', '${escapeHtml(video.author)}')">
                                    <div class="thumbnail-wrapper">
                                        <img class="thumbnail-img" src="${thumb}" alt="${escapeHtml(video.title)}" loading="lazy">
                                        ${duration ? `<div class="video-duration">${duration}</div>` : ''}
                                    </div>
                                    <div class="video-info">
                                        <div class="video-title">${escapeHtml(video.title)}</div>
                                        <div class="video-meta">
                                            <div class="video-channel">${escapeHtml(video.author)}</div>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }).join('');

                        // Append to the search grid
                        grid.innerHTML = mainHtml + similarTitleHtml + similarCardsHtml;
                        lucide.createIcons();
                    }
                })
                .catch(err => {
                    console.warn("Failed to append similar videos to search:", err);
                });
        })
        .catch(err => {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 40px;">
                    <p style="color: var(--primary-red); margin-bottom: 12px;">เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์ค้นหา</p>
                    <p style="font-size: 13px; color: var(--text-secondary);">${err.message}</p>
                </div>
            `;
        });
}

function handleSearchKeyPress(event) {
    if (event.key === 'Enter') {
        triggerSearch();
    }
}

// Load Suggested Videos in Sidebar
function loadSuggestedVideos(videoId) {
    const sidebar = document.getElementById('sidebar-suggestions');
    sidebar.innerHTML = `<div style="text-align: center; color: var(--text-muted); font-size: 13px; padding: 20px;">กำลังโหลดวิดีโอแนะนำ...</div>`;

    // Fetch related videos (using search query from active title or similar)
    const activeTitle = currentState.currentVideo ? currentState.currentVideo.title : '';
    const cleanQuery = activeTitle.split(' ').slice(0, 3).join(' '); // use first few words
    
    fetchFromInvidious(`/api/v1/search?q=${encodeURIComponent(cleanQuery || 'music')}&type=video`)
        .then(videos => {
            // Filter out current video
            const filtered = (videos || []).filter(v => v.videoId !== videoId).slice(0, 5);
            if (filtered.length === 0) {
                sidebar.innerHTML = `<div style="color: var(--text-muted); font-size: 13px;">ไม่มีคำแนะนำเพิ่มเติม</div>`;
                return;
            }
            
            sidebar.innerHTML = filtered.map(video => {
                const thumb = `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg`;
                return `
                    <div class="video-card fade-in" style="flex-direction: row; border-radius: 8px; overflow: hidden;" onclick="playVideo('${video.videoId}', '${escapeHtml(video.title)}', '${escapeHtml(video.author)}')">
                        <div class="thumbnail-wrapper" style="width: 120px; min-width: 120px; padding-top: 67.5px;">
                            <img class="thumbnail-img" src="${thumb}" alt="${escapeHtml(video.title)}">
                        </div>
                        <div class="video-info" style="padding: 8px 12px; gap: 4px; overflow: hidden;">
                            <div class="video-title" style="font-size: 12px; -webkit-line-clamp: 2;">${escapeHtml(video.title)}</div>
                            <div class="video-meta" style="font-size: 10px;">
                                <div class="video-channel">${escapeHtml(video.author)}</div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        })
        .catch(() => {
            sidebar.innerHTML = `<div style="color: var(--text-muted); font-size: 13px;">ไม่สามารถโหลดวิดีโอแนะนำได้</div>`;
        });
}

// Load Default Home Feed (Lofi Music / Trending Mix)
function loadDefaultHomeFeed() {
    const grid = document.getElementById('grid-home');
    grid.innerHTML = Array(8).fill(0).map(() => `
        <div class="video-card">
            <div class="skeleton-thumbnail skeleton"></div>
            <div class="video-info">
                <div class="skeleton-title skeleton"></div>
                <div class="skeleton-meta skeleton"></div>
            </div>
        </div>
    `).join('');

    fetchFromInvidious(`/api/v1/search?q=lofi+hip+hop+radio+live&type=video`)
        .then(videos => {
            if (!videos || videos.length === 0) throw new Error("No videos found");
            renderHomeFeed(videos.slice(0, 12));
        })
        .catch(() => {
            // Backup static placeholder data if API fails completely to ensure premium UI look
            const fallbackVideos = [
                { videoId: "jfKfPfyJRdk", title: "Lofi Hip Hop Radio 📚 Beats to Relax/Study to", author: "Lofi Girl" },
                { videoId: "5qap5aO4i9A", title: "Lofi Hip Hop Radio 💤 Beats to Sleep/Chill to", author: "Lofi Girl" },
                { videoId: "tNKD01IIkHc", title: "Chill Lofi Mix 🍁 Music to Work/Study", author: "Lofi Garden" },
                { videoId: "dQw4w9WgXcQ", title: "Rick Astley - Never Gonna Give You Up (Official Music Video)", author: "Rick Astley" }
            ];
            renderHomeFeed(fallbackVideos);
        });
}

function renderHomeFeed(videos) {
    const grid = document.getElementById('grid-home');
    grid.innerHTML = videos.map(video => {
        const thumb = `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg`;
        const duration = video.lengthSeconds ? formatDuration(video.lengthSeconds) : "";
        return `
            <div class="video-card fade-in" onclick="playVideo('${video.videoId}', '${escapeHtml(video.title)}', '${escapeHtml(video.author)}')">
                <div class="thumbnail-wrapper">
                    <img class="thumbnail-img" src="${thumb}" alt="${escapeHtml(video.title)}" loading="lazy">
                    ${duration ? `<div class="video-duration">${duration}</div>` : ''}
                </div>
                <div class="video-info">
                    <div class="video-title">${escapeHtml(video.title)}</div>
                    <div class="video-meta">
                        <div class="video-channel">${escapeHtml(video.author)}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    lucide.createIcons();
}

// Mini Player toggles
function toggleMiniPlayer() {
    if (currentState.currentView !== 'player') return;

    if (currentState.isMiniPlayer) {
        document.body.classList.remove('mini-player-active');
        currentState.isMiniPlayer = false;
        showToast("ขยายหน้าจอเครื่องเล่นปกติแล้วครับ");
    } else {
        document.body.classList.add('mini-player-active');
        currentState.isMiniPlayer = true;
        showToast("ย่อหน้าจอโหมดลอยสำเร็จ บอสสามารถกดค้นหาหรือดูส่วนอื่นต่อได้ครับ");
        switchView('home'); // Go to home while player floats
    }
}

// LocalStorage helpers
function addToHistory(video) {
    // Remove if already exists to push to front
    currentState.history = currentState.history.filter(v => v.videoId !== video.videoId);
    currentState.history.unshift(video);
    if (currentState.history.length > 50) currentState.history.pop(); // limit to 50
    localStorage.setItem('yt_premium_history', JSON.stringify(currentState.history));
}

function clearHistory() {
    currentState.history = [];
    localStorage.setItem('yt_premium_history', JSON.stringify([]));
    renderGrids();
    showToast("ล้างประวัติการรับชมทั้งหมดเรียบร้อยครับ");
}

function toggleWatchLater(video) {
    const index = currentState.watchLater.findIndex(v => v.videoId === video.videoId);
    if (index > -1) {
        currentState.watchLater.splice(index, 1);
        showToast("ลบจากรายการดูภายหลังแล้วครับบอส");
    } else {
        currentState.watchLater.push(video);
        showToast("เพิ่มลงในรายการดูภายหลังแล้วครับบอส");
    }
    localStorage.setItem('yt_premium_watch_later', JSON.stringify(currentState.watchLater));
    updatePlayerButtonsState();
    renderGrids();
}

function toggleFavorite(video) {
    const index = currentState.favorites.findIndex(v => v.videoId === video.videoId);
    if (index > -1) {
        currentState.favorites.splice(index, 1);
        showToast("ลบจากรายการโปรดแล้วครับบอส");
    } else {
        currentState.favorites.push(video);
        showToast("เพิ่มในรายการโปรดเรียบร้อยครับบอส");
    }
    localStorage.setItem('yt_premium_favorites', JSON.stringify(currentState.favorites));
    updatePlayerButtonsState();
    renderGrids();
}

function toggleFavoriteCurrent() {
    if (currentState.currentVideo) {
        toggleFavorite(currentState.currentVideo);
    }
}

function toggleWatchLaterCurrent() {
    if (currentState.currentVideo) {
        toggleWatchLater(currentState.currentVideo);
    }
}

function updatePlayerButtonsState() {
    if (!currentState.currentVideo) return;
    const video = currentState.currentVideo;

    const isFav = currentState.favorites.some(v => v.videoId === video.videoId);
    const isLater = currentState.watchLater.some(v => v.videoId === video.videoId);

    const btnFav = document.getElementById('btn-fav');
    const txtFav = document.getElementById('txt-fav');
    if (isFav) {
        btnFav.classList.add('active');
        txtFav.innerText = "ลบจากรายการโปรด";
    } else {
        btnFav.classList.remove('active');
        txtFav.innerText = "เพิ่มในรายการโปรด";
    }

    const btnLater = document.getElementById('btn-later');
    const txtLater = document.getElementById('txt-later');
    if (isLater) {
        btnLater.classList.add('active');
        txtLater.innerText = "ลบจากดูภายหลัง";
    } else {
        btnLater.classList.remove('active');
        txtLater.innerText = "ดูภายหลัง";
    }
}

// Render library grids
function renderGrids() {
    renderGrid('grid-history', currentState.history, "ยังไม่มีประวัติการรับชมครับบอส");
    renderGrid('grid-watch-later', currentState.watchLater, "ไม่มีวิดีโอที่เพิ่มลงในรายการดูภายหลังครับบอส");
    renderGrid('grid-favorites', currentState.favorites, "ไม่มีวิดีโอในรายการโปรดครับบอส");
}

function renderGrid(elementId, list, emptyMessage) {
    const grid = document.getElementById(elementId);
    if (!grid) return;

    if (!list || list.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted); font-size: 14px;">${emptyMessage}</div>`;
        return;
    }

    grid.innerHTML = list.map(video => {
        const thumb = `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg`;
        return `
            <div class="video-card fade-in" onclick="playVideo('${video.videoId}', '${escapeHtml(video.title)}', '${escapeHtml(video.author)}')">
                <div class="thumbnail-wrapper">
                    <img class="thumbnail-img" src="${thumb}" alt="${escapeHtml(video.title)}" loading="lazy">
                </div>
                <div class="video-info">
                    <div class="video-title">${escapeHtml(video.title)}</div>
                    <div class="video-meta">
                        <div class="video-channel">${escapeHtml(video.author)}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Copy sharing link
function copyShareLink() {
    if (!currentState.currentVideo) return;
    const url = `https://www.youtube.com/watch?v=${currentState.currentVideo.videoId}`;
    navigator.clipboard.writeText(url).then(() => {
        showToast("คัดลอกลิงก์แชร์ใส่คลิปบอร์ดแล้วครับบอส");
    }).catch(() => {
        showToast("ไม่สามารถคัดลอกลิงก์ได้ครับ");
    });
}

// Escape HTML utility to prevent XSS
function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
