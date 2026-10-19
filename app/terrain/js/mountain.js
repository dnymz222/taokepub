import { OrbitCamera } from './camera.js';
import { TerrainRenderer } from './renderer.js';
import { fetchBinary, fetchJSON } from './terrain.js';
import { pickTerrain } from './picking.js';
import { transformPoint } from './mat4.js';

const DEG = Math.PI / 180;
const $ = (id) => document.getElementById(id);

const canvas = $('scene');
const els = {
  peakName: $('peak-name'),
  peakSub: $('peak-sub'),
  factElev: $('fact-elev'),
  factDem: $('fact-dem'),
  factRadius: $('fact-radius'),
  factArea: $('fact-area'),
  lodGroup: $('lod-group'),
  lodOut: $('lod-out'),
  exag: $('exag'),
  exagOut: $('exag-out'),
  sunAz: $('sun-az'),
  sunAzOut: $('sun-az-out'),
  sunAlt: $('sun-alt'),
  sunAltOut: $('sun-alt-out'),
  shadows: $('toggle-shadows'),
  contours: $('toggle-contours'),
  contourStep: $('contour-step'),
  wire: $('toggle-wire'),
  rotate: $('toggle-rotate'),
  reset: $('reset'),
  fps: $('fps'),
  triangles: $('triangles'),
  compassDial: $('compass-dial'),
  compass: $('compass'),
  legendMin: $('legend-min'),
  legendMax: $('legend-max'),
  readoutCoord: $('readout-coord'),
  readoutElev: $('readout-elev'),
  marker: $('peak-marker'),
  markerId: $('marker-id'),
  markerName: $('marker-name'),
  markerAlt: $('marker-alt'),
  loader: $('loader'),
  loaderTitle: $('loader-title'),
  loaderProgress: $('loader-progress'),
  loaderStatus: $('loader-status'),
  fatal: $('fatal'),
  fatalMessage: $('fatal-message'),
  panelToggle: $('panel-toggle'),
  panelClose: $('panel-close'),
};

const state = {
  exag: 2.5,
  sunAzimuth: 315,
  sunAltitude: 35,
  shadows: true,
  contours: false,
  contourStep: 100,
  wireframe: false,
  autoRotate: false,
  lod: 512,
  rampMode: 1,
  water: false,
};

const config = window.MOUNTAIN_CONFIG || {};

const peakId = config.id || (() => {
  const match = location.pathname.match(/^\/mountain\/terrain\/([^/]+)\/?$/)
    || location.pathname.match(/^\/terrain\/mountain\/([^/]+)\/?$/);
  return match ? decodeURIComponent(match[1]) : null;
})();

const camera = new OrbitCamera();
let renderer = null;
let meta = null;
let terrain = null;
let peakElevation = 0;
let peakWorldY = 0;
let loadToken = 0;

const pointers = new Map();
let dragMode = null;
let pinch = null;
let pointerNdc = null;
let pointerInside = false;
let lastPick = 0;

let fpsFrames = 0;
let fpsLast = performance.now();
let lastFrame = performance.now();

/* ------------------------------------------------------------------ */
/* Formatting                                                          */
/* ------------------------------------------------------------------ */

const MINUS = '\u2212';

function formatLon(lon) {
  return `${Math.abs(lon).toFixed(4)}°${lon >= 0 ? 'E' : 'W'}`;
}

function formatLat(lat) {
  return `${Math.abs(lat).toFixed(4)}°${lat >= 0 ? 'N' : 'S'}`;
}

function formatDms(value, axis) {
  const dir = axis === 'lat'
    ? (value >= 0 ? 'N' : 'S')
    : (value >= 0 ? 'E' : 'W');
  const abs = Math.abs(value);
  const deg = Math.floor(abs);
  const min = Math.floor((abs - deg) * 60);
  const sec = Math.round(((abs - deg) * 60 - min) * 60);
  return `${deg}°${String(min).padStart(2, '0')}′${String(sec).padStart(2, '0')}″${dir}`;
}

function meters(value) {
  return `${Math.round(value).toLocaleString('en-US')} m`;
}

/* ------------------------------------------------------------------ */
/* Fatal / loading                                                     */
/* ------------------------------------------------------------------ */

function showFatal(error) {
  const message = error instanceof Error ? error.message : String(error);
  els.fatalMessage.textContent = message;
  els.fatal.hidden = false;
  els.loader.classList.add('hidden');
  document.body.dataset.ready = 'error';
  console.error(error);
}

function openLoader(title) {
  els.loaderTitle.textContent = title;
  els.loader.classList.remove('hidden');
  setLoaderProgress(0, '正在读取山峰数据…');
}

function setLoaderProgress(fraction, text) {
  const pct = Math.max(0, Math.min(100, fraction * 100));
  els.loaderProgress.style.width = `${pct}%`;
  if (text) els.loaderStatus.textContent = text;
}

function closeLoader() {
  setLoaderProgress(1, '准备就绪');
  setTimeout(() => els.loader.classList.add('hidden'), 260);
}

/* ------------------------------------------------------------------ */
/* Camera                                                              */
/* ------------------------------------------------------------------ */

function defaultView(snap = false) {
  if (!meta) return;
  const targetY = peakElevation * state.exag * 0.42;
  peakWorldY = peakElevation * state.exag;
  camera.fov = 45 * DEG;
  camera.setTargetHeight(targetY, snap);
  camera.goalTarget[0] = 0;
  camera.goalTarget[2] = 0;
  camera.goalAzimuth = 26 * DEG;
  camera.goalElevation = 31.5 * DEG;
  camera.goalDistance = Math.max(meta.sizeMeters[0], meta.sizeMeters[1]) * 1.35;
  if (snap) {
    camera.target = [0, targetY, 0];
    camera.azimuth = camera.goalAzimuth;
    camera.elevation = camera.goalElevation;
    camera.distance = camera.goalDistance;
  }
}

function updateExaggeration(value) {
  state.exag = value;
  els.exagOut.textContent = `× ${value.toFixed(1)}`;
  if (meta) {
    peakWorldY = peakElevation * value;
    camera.setTargetHeight(peakElevation * value * 0.42);
  }
  clearReadout();
}

/* ------------------------------------------------------------------ */
/* Load                                                                */
/* ------------------------------------------------------------------ */

async function loadMountain() {
  if (!peakId) {
    location.replace('/mountain/terrain');
    return;
  }
  const token = ++loadToken;
  document.body.dataset.ready = '0';
  const base = config.dataBase
    || `/data/mountains/${encodeURIComponent(peakId)}`;

  openLoader(peakId);
  try {
    setLoaderProgress(0.04, '读取山峰元数据…');
    const loadedMeta = await fetchJSON(`${base}/meta.json`);
    if (token !== loadToken) return;
    meta = loadedMeta;
    peakElevation = Number(meta.peakElevation ?? meta.peak?.elevation) || 0;
    updateMetaUI(meta);

    setLoaderProgress(0.1, '下载高程数据…');
    const buffer = await fetchBinary(`${base}/heightmap.f16`, (fraction, received) => {
      if (token !== loadToken) return;
      const meg = (received / 1048576).toFixed(1);
      setLoaderProgress(0.1 + fraction * 0.78, `下载高程数据 ${Math.round(fraction * 100)}% · ${meg} MB`);
    });
    if (token !== loadToken) return;
    if (buffer.byteLength % 2 !== 0) throw new Error('高程数据长度异常');
    const data = new Uint16Array(buffer);
    const expected = meta.width * meta.height;
    if (data.length !== expected) {
      throw new Error(`高程样本数量不匹配：${data.length} / ${expected}`);
    }

    setLoaderProgress(0.92, '上传高程纹理…');
    await new Promise((resolve) => requestAnimationFrame(resolve));
    if (token !== loadToken) return;

    renderer.setTerrain({ meta, data });
    renderer.setMeshResolution(state.lod);
    terrain = { meta, data };
    camera.frame(meta, true);
    defaultView(true);
    updateStats();
    updateLodUI();
    clearReadout();
    closeLoader();
    document.body.dataset.ready = '1';
  } catch (error) {
    if (token === loadToken) {
      showFatal(
        new Error(
          `未找到山峰 ${peakId} 的地形数据（${error.message}）。`
          + ' 请先运行 scripts/make_mountain.py 生成。',
        ),
      );
    }
  }
}

/* ------------------------------------------------------------------ */
/* UI                                                                  */
/* ------------------------------------------------------------------ */

function updateMetaUI(data) {
  const demPeak = Number(data.peakElevation ?? data.peak?.elevation) || 0;
  const listed = Number(data.listedHeight);
  const hasListed = Number.isFinite(listed) && listed > 0;
  const [width, depth] = data.sizeMeters;
  document.title = `${data.name} · ${data.id} · WebGL 三维地形`;
  els.peakName.textContent = data.name;
  els.peakSub.textContent =
    `${formatDms(data.center[1], 'lat')} · ${formatDms(data.center[0], 'lon')}`
    + ` · ${data.id} · 最高 ${meters(data.maxElevation)}`;
  els.factElev.textContent = meters(hasListed ? listed : demPeak);
  els.factDem.textContent = meters(demPeak);
  els.factRadius.textContent = `${data.radiusKm} km`;
  els.factArea.textContent = `${(width / 1000).toFixed(1)} × ${(depth / 1000).toFixed(1)} km`;
  els.legendMin.textContent = meters(data.minElevation);
  els.legendMax.textContent = meters(data.maxElevation);
  els.markerId.textContent = data.id;
  els.markerName.textContent = data.name;
  els.markerAlt.textContent = `DEM ${meters(demPeak)}`;
  els.loaderTitle.textContent = `${data.name} ${data.id}`;
}

function updateStats() {
  const stats = renderer.getStats();
  els.triangles.textContent = stats.triangles.toLocaleString('en-US');
}

function updateLodUI() {
  els.lodOut.textContent = `${state.lod + 1} × ${state.lod + 1}`;
  for (const button of els.lodGroup.querySelectorAll('button')) {
    button.classList.toggle('active', Number(button.dataset.lod) === state.lod);
  }
}

function setLod(lod) {
  state.lod = lod;
  if (terrain) {
    renderer.setMeshResolution(lod);
    updateStats();
  }
  updateLodUI();
}


function setToggle(input, value) {
  input.checked = value;
}

function setupUI() {
  els.exag.value = String(state.exag);
  els.exagOut.textContent = `× ${state.exag.toFixed(1)}`;
  els.sunAz.value = String(state.sunAzimuth);
  els.sunAzOut.textContent = `${state.sunAzimuth}°`;
  els.sunAlt.value = String(state.sunAltitude);
  els.sunAltOut.textContent = `${state.sunAltitude}°`;
  setToggle(els.shadows, state.shadows);
  setToggle(els.contours, state.contours);
  setToggle(els.wire, state.wireframe);
  setToggle(els.rotate, state.autoRotate);
  els.contourStep.value = String(state.contourStep);
  els.contourStep.disabled = !state.contours;

  els.exag.addEventListener('input', () => {
    updateExaggeration(Number(els.exag.value));
  });

  els.sunAz.addEventListener('input', () => {
    state.sunAzimuth = Number(els.sunAz.value);
    els.sunAzOut.textContent = `${state.sunAzimuth}°`;
  });

  els.sunAlt.addEventListener('input', () => {
    state.sunAltitude = Number(els.sunAlt.value);
    els.sunAltOut.textContent = `${state.sunAltitude}°`;
  });

  els.shadows.addEventListener('change', () => {
    state.shadows = els.shadows.checked;
  });

  els.contours.addEventListener('change', () => {
    state.contours = els.contours.checked;
    els.contourStep.disabled = !state.contours;
  });

  els.contourStep.addEventListener('change', () => {
    state.contourStep = Number(els.contourStep.value);
  });

  els.wire.addEventListener('change', () => {
    state.wireframe = els.wire.checked;
  });

  els.rotate.addEventListener('change', () => {
    state.autoRotate = els.rotate.checked;
  });

  els.lodGroup.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-lod]');
    if (button) setLod(Number(button.dataset.lod));
  });

  els.reset.addEventListener('click', () => defaultView(false));

  const faceNorth = () => {
    state.autoRotate = false;
    setToggle(els.rotate, false);
    camera.faceNorth();
  };
  els.compass.addEventListener('click', faceNorth);
  els.compass.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      event.stopPropagation();
      faceNorth();
    }
  });

  els.panelToggle.addEventListener('click', () => {
    const open = document.body.classList.toggle('panel-open');
    els.panelToggle.setAttribute('aria-expanded', String(open));
  });

  els.panelClose.addEventListener('click', () => {
    document.body.classList.remove('panel-open');
    els.panelToggle.setAttribute('aria-expanded', 'false');
  });

  window.addEventListener('keydown', (event) => {
    if (event.target.closest('input, select, button, textarea')) return;
    const key = event.key.toLowerCase();
    if (key === 'r') {
      defaultView(false);
    } else if (key === 's') {
      state.shadows = !state.shadows;
      setToggle(els.shadows, state.shadows);
    } else if (key === 'c') {
      state.contours = !state.contours;
      setToggle(els.contours, state.contours);
      els.contourStep.disabled = !state.contours;
    } else if (key === 'w') {
      state.wireframe = !state.wireframe;
      setToggle(els.wire, state.wireframe);
    } else if (key === ' ') {
      event.preventDefault();
      state.autoRotate = !state.autoRotate;
      setToggle(els.rotate, state.autoRotate);
    } else if (key === '1' || key === '2' || key === '3') {
      setLod([256, 512, 1024][Number(key) - 1]);
    }
  });
}

/* ------------------------------------------------------------------ */
/* Input                                                               */
/* ------------------------------------------------------------------ */

function updatePointerNdc(event) {
  const rect = canvas.getBoundingClientRect();
  const x = (event.clientX - rect.left) / Math.max(1, rect.width);
  const y = (event.clientY - rect.top) / Math.max(1, rect.height);
  pointerNdc = [x * 2 - 1, 1 - y * 2];
  pointerInside = x >= 0 && x <= 1 && y >= 0 && y <= 1;
}

function setupInput() {
  canvas.addEventListener('contextmenu', (event) => event.preventDefault());

  canvas.addEventListener('pointerdown', (event) => {
    canvas.setPointerCapture(event.pointerId);
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    canvas.classList.add('dragging');
    updatePointerNdc(event);

    if (document.body.classList.contains('panel-open')) {
      document.body.classList.remove('panel-open');
      els.panelToggle.setAttribute('aria-expanded', 'false');
    }

    if (pointers.size === 1) {
      dragMode = (event.button === 2 || event.button === 1 || event.shiftKey)
        ? 'pan' : 'rotate';
      pinch = null;
    } else if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      dragMode = 'pinch';
      pinch = {
        dist: Math.hypot(a.x - b.x, a.y - b.y),
        mid: [(a.x + b.x) / 2, (a.y + b.y) / 2],
      };
    }
  });

  canvas.addEventListener('pointermove', (event) => {
    updatePointerNdc(event);
    const previous = pointers.get(event.pointerId);
    if (!previous) return;
    const dx = event.clientX - previous.x;
    const dy = event.clientY - previous.y;
    previous.x = event.clientX;
    previous.y = event.clientY;

    if (dragMode === 'pan' && pointers.size === 1) {
      camera.pan(dx, dy, canvas.clientHeight);
    } else if (dragMode === 'rotate' && pointers.size === 1) {
      camera.rotate(dx, dy);
    } else if (dragMode === 'pinch' && pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      const dist = Math.hypot(a.x - b.x, a.y - b.y);
      const mid = [(a.x + b.x) / 2, (a.y + b.y) / 2];
      if (pinch && pinch.dist > 0 && dist > 0) {
        camera.zoom(pinch.dist / dist);
        camera.pan(mid[0] - pinch.mid[0], mid[1] - pinch.mid[1], canvas.clientHeight);
      }
      pinch = { dist, mid };
    }
  });

  const release = (event) => {
    pointers.delete(event.pointerId);
    if (pointers.size < 2) pinch = null;
    if (pointers.size === 0) {
      dragMode = null;
      canvas.classList.remove('dragging');
    } else if (pointers.size === 1) {
      dragMode = 'rotate';
    }
  };

  canvas.addEventListener('pointerup', release);
  canvas.addEventListener('pointercancel', release);
  canvas.addEventListener('pointerleave', () => {
    if (!pointers.size) pointerInside = false;
  });

  canvas.addEventListener('wheel', (event) => {
    event.preventDefault();
    const delta = event.deltaMode === 1 ? event.deltaY * 16 : event.deltaY;
    camera.zoom(Math.exp(delta * 0.0012));
  }, { passive: false });

  canvas.addEventListener('dblclick', () => defaultView(false));

  canvas.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    showFatal(new Error('WebGL 上下文已丢失，请刷新页面重试。'));
  });
}

/* ------------------------------------------------------------------ */
/* Marker / readout / compass / loop                                   */
/* ------------------------------------------------------------------ */

function clearReadout() {
  els.readoutCoord.textContent = '移动光标读取地形';
  els.readoutElev.textContent = '经度 · 纬度 · 海拔';
}

function updateReadout(hit) {
  if (!hit) {
    els.readoutCoord.textContent = '未命中地形';
    els.readoutElev.textContent = '经度 · 纬度 · 海拔';
    return;
  }
  els.readoutCoord.textContent = `${formatLon(hit.lon)} · ${formatLat(hit.lat)}`;
  const elevation = Math.round(hit.elevation);
  els.readoutElev.textContent =
    `海拔 ${elevation > 0 ? '+' : ''}${elevation} m · 距视点 ${(hit.distance / 1000).toFixed(1)} km`;
}

function pickCursor(now) {
  if (!pointerInside || !pointerNdc || !terrain || dragMode) return;
  if (now - lastPick < 55) return;
  lastPick = now;
  const aspect = canvas.width / Math.max(1, canvas.height);
  const vp = camera.getViewProj(aspect);
  updateReadout(pickTerrain(vp, pointerNdc[0], pointerNdc[1], terrain, state.exag, camera.getEye()));
}

function updateMarker() {
  if (!terrain) return;
  const aspect = canvas.width / Math.max(1, canvas.height);
  const vp = camera.getViewProj(aspect);
  const clip = transformPoint(vp, 0, peakWorldY, 0);
  const visible = clip[3] > 0
    && Math.abs(clip[0] / clip[3]) < 1.1
    && Math.abs(clip[1] / clip[3]) < 1.1;
  if (!visible) {
    els.marker.classList.remove('visible');
    return;
  }
  const rect = canvas.getBoundingClientRect();
  const x = (clip[0] / clip[3] * 0.5 + 0.5) * rect.width;
  // The ring sits at the bottom of the marker; compensate for the card's
  // internal padding/margin so the ring centre lands exactly on the summit.
  const y = (1 - (clip[1] / clip[3] * 0.5 + 0.5)) * rect.height + 14;
  els.marker.style.transform =
    `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -100%)`;
  els.marker.classList.add('visible');
}

function updateCompass() {
  const deg = (camera.azimuth * 180) / Math.PI;
  els.compassDial.style.transform = `rotate(${deg.toFixed(2)}deg)`;
}

function frame(now) {
  const dt = Math.min(0.05, (now - lastFrame) / 1000);
  lastFrame = now;
  camera.update(dt, state.autoRotate);

  if (terrain) {
    renderer.render(camera, state, now / 1000);
    updateMarker();
  }
  updateCompass();
  pickCursor(now);

  fpsFrames += 1;
  if (now - fpsLast >= 500) {
    els.fps.textContent = String(Math.round((fpsFrames * 1000) / (now - fpsLast)));
    fpsFrames = 0;
    fpsLast = now;
  }
  requestAnimationFrame(frame);
}

/* ------------------------------------------------------------------ */
/* Boot                                                                */
/* ------------------------------------------------------------------ */

function main() {
  if (!peakId) {
    location.replace('/mountain/terrain');
    return;
  }
  try {
    renderer = new TerrainRenderer(canvas);
  } catch (error) {
    showFatal(error);
    return;
  }
  setupUI();
  setupInput();
  updateLodUI();
  const resizeObserver = new ResizeObserver(() => renderer.resize());
  resizeObserver.observe(canvas);
  requestAnimationFrame(frame);
  loadMountain();
}

main();

window.__mountain = {
  camera,
  state,
  get terrain() { return terrain; },
  get renderer() { return renderer; },
  get meta() { return meta; },
  reset() { defaultView(false); },
};
