import { OrbitCamera } from './camera.js';
import { TerrainRenderer } from './renderer.js';
import { loadManifest, loadTerrain } from './terrain.js';
import { pickTerrain } from './picking.js';

const $ = (id) => document.getElementById(id);

const canvas = $('scene');
const els = {
  tileTitle: $('tile-title'),
  tileSub: $('tile-sub'),
  factElev: $('fact-elev'),
  factSize: $('fact-size'),
  factExtent: $('fact-extent'),
  tileSelect: $('tile-select'),
  lodGroup: $('lod-group'),
  lodOut: $('lod-out'),
  exag: $('exag'),
  exagOut: $('exag-out'),
  sunAz: $('sun-az'),
  sunAzOut: $('sun-az-out'),
  sunAlt: $('sun-alt'),
  sunAltOut: $('sun-alt-out'),
  water: $('toggle-water'),
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
  exag: 12,
  sunAzimuth: 240,
  sunAltitude: 32,
  water: true,
  contours: false,
  contourStep: 100,
  shadows: true,
  wireframe: false,
  autoRotate: false,
  lod: 512,
};

const camera = new OrbitCamera();

let renderer = null;
let manifest = null;
let terrain = null;
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

const nextFrame = () => new Promise((resolve) => requestAnimationFrame(resolve));

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

function metersLabel(value) {
  const rounded = Math.round(value);
  return `${rounded < 0 ? MINUS : ''}${Math.abs(rounded)} m`;
}

/* ------------------------------------------------------------------ */
/* Fatal / loader                                                      */
/* ------------------------------------------------------------------ */

function showFatal(error) {
  const message = error instanceof Error ? error.message : String(error);
  els.fatalMessage.textContent = message;
  els.fatal.hidden = false;
  els.loader.classList.add('hidden');
  console.error(error);
}

function setLoaderProgress(fraction, text) {
  const pct = Math.max(0, Math.min(100, fraction * 100));
  els.loaderProgress.style.width = `${pct}%`;
  if (text) els.loaderStatus.textContent = text;
}

function openLoader(title) {
  els.loaderTitle.textContent = title;
  els.loader.classList.remove('hidden');
  setLoaderProgress(0, '正在读取高程数据…');
}

function closeLoader() {
  setLoaderProgress(1, '准备就绪');
  setTimeout(() => els.loader.classList.add('hidden'), 260);
}

/* ------------------------------------------------------------------ */
/* Metadata + tile loading                                             */
/* ------------------------------------------------------------------ */

function populateTiles(tiles) {
  els.tileSelect.innerHTML = '';
  for (const tile of tiles) {
    const option = document.createElement('option');
    option.value = tile.id;
    option.textContent = `${tile.id}  ·  ${metersLabel(tile.minElevation)} ~ ${metersLabel(tile.maxElevation)}`;
    els.tileSelect.appendChild(option);
  }
  els.tileSelect.disabled = tiles.length <= 1;
}

function updateMeta(meta) {
  const [west, south, east, north] = [
    meta.bounds.west, meta.bounds.south, meta.bounds.east, meta.bounds.north,
  ];
  const arcsec = meta.pixelSize[0] * 3600;
  const groundRes = meta.sizeMeters[0] / meta.width;

  document.title = `${meta.id} · WebGL 三维地形`;
  els.tileTitle.textContent = meta.id;
  els.tileSub.textContent =
    `${formatDms(meta.center[1], 'lat')} · ${formatDms(meta.center[0], 'lon')} · `
    + `${arcsec.toFixed(0)}″ (≈${groundRes.toFixed(0)} m)`;
  els.factElev.textContent = `${metersLabel(meta.minElevation)} ~ ${metersLabel(meta.maxElevation)}`;
  els.factSize.textContent = `${meta.width.toLocaleString('en-US')} × ${meta.height.toLocaleString('en-US')}`;
  els.factExtent.textContent =
    `${(meta.sizeMeters[0] / 1000).toFixed(1)} × ${(meta.sizeMeters[1] / 1000).toFixed(1)} km`;
  els.legendMin.textContent = metersLabel(meta.minElevation);
  els.legendMax.textContent = metersLabel(meta.maxElevation);

  console.info(
    `[terrain] ${meta.id} ${west.toFixed(4)},${south.toFixed(4)} → ${east.toFixed(4)},${north.toFixed(4)}`,
  );
}

async function selectTile(id) {
  const summary = manifest?.tiles.find((t) => t.id === id);
  if (!summary) {
    showFatal(new Error(`找不到地形瓦片 ${id}`));
    return;
  }
  const token = ++loadToken;
  document.body.dataset.ready = '0';
  openLoader(summary.id);

  try {
    const loaded = await loadTerrain(summary, (fraction, received) => {
      if (token !== loadToken) return;
      const meg = (received / 1048576).toFixed(1);
      setLoaderProgress(0.06 + fraction * 0.82, `下载高程数据 ${Math.round(fraction * 100)}% · ${meg} MB`);
    });
    if (token !== loadToken) return;

    setLoaderProgress(0.9, '上传高程纹理…');
    await nextFrame();
    if (token !== loadToken) return;

    renderer.setTerrain(loaded);
    renderer.setMeshResolution(state.lod);
    camera.frame(loaded.meta);
    terrain = loaded;
    updateMeta(loaded.meta);
    updateStats();
    updateLodUI();
    clearReadout();
    closeLoader();
    document.body.dataset.ready = '1';
  } catch (error) {
    if (token === loadToken) showFatal(error);
  }
}

/* ------------------------------------------------------------------ */
/* UI wiring                                                           */
/* ------------------------------------------------------------------ */

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
  setToggle(els.water, state.water);
  setToggle(els.shadows, state.shadows);
  setToggle(els.contours, state.contours);
  setToggle(els.wire, state.wireframe);
  setToggle(els.rotate, state.autoRotate);
  els.contourStep.value = String(state.contourStep);
  els.contourStep.disabled = !state.contours;

  els.exag.addEventListener('input', () => {
    state.exag = Number(els.exag.value);
    els.exagOut.textContent = `× ${state.exag.toFixed(1)}`;
    clearReadout();
  });

  els.sunAz.addEventListener('input', () => {
    state.sunAzimuth = Number(els.sunAz.value);
    els.sunAzOut.textContent = `${state.sunAzimuth}°`;
  });

  els.sunAlt.addEventListener('input', () => {
    state.sunAltitude = Number(els.sunAlt.value);
    els.sunAltOut.textContent = `${state.sunAltitude}°`;
  });

  els.water.addEventListener('change', () => {
    state.water = els.water.checked;
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

  els.reset.addEventListener('click', () => {
    if (terrain) camera.reset(terrain.meta);
  });

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

  els.tileSelect.addEventListener('change', () => {
    selectTile(els.tileSelect.value);
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
      if (terrain) camera.reset(terrain.meta);
    } else if (key === 'w') {
      state.wireframe = !state.wireframe;
      setToggle(els.wire, state.wireframe);
    } else if (key === 's') {
      state.shadows = !state.shadows;
      setToggle(els.shadows, state.shadows);
    } else if (key === 'c') {
      state.contours = !state.contours;
      setToggle(els.contours, state.contours);
      els.contourStep.disabled = !state.contours;
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

  canvas.addEventListener('dblclick', () => {
    if (terrain) camera.reset(terrain.meta);
  });

  canvas.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    showFatal(new Error('WebGL 上下文已丢失，请刷新页面重试。'));
  });
}

/* ------------------------------------------------------------------ */
/* Readout + compass + frame loop                                      */
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
  const sign = elevation > 0 ? '+' : '';
  els.readoutElev.textContent =
    `海拔 ${sign}${elevation} m · 距视点 ${(hit.distance / 1000).toFixed(1)} km`;
}

function pickCursor(now) {
  if (!pointerInside || !pointerNdc || !terrain || dragMode) return;
  if (now - lastPick < 55) return;
  lastPick = now;
  const aspect = canvas.width / Math.max(1, canvas.height);
  const vp = camera.getViewProj(aspect);
  updateReadout(pickTerrain(vp, pointerNdc[0], pointerNdc[1], terrain, state.exag));
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

async function boot() {
  if (location.protocol === 'file:') {
    showFatal(new Error('浏览器禁止 file:// 页面读取本地数据文件。请启动本地 HTTP 服务后访问。'));
    return;
  }
  try {
    manifest = await loadManifest();
    if (!manifest.tiles?.length) throw new Error('data/manifest.json 中没有地形瓦片');
    populateTiles(manifest.tiles);
    const initial = manifest.default || manifest.tiles[0].id;
    els.tileSelect.value = initial;
    await selectTile(initial);
  } catch (error) {
    showFatal(error);
  }
}

function main() {
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
  boot();
}

main();

// Small debug surface for the console / automated screenshots.
window.__terrain = {
  camera,
  state,
  get terrain() { return terrain; },
  get renderer() { return renderer; },
  reset() { if (terrain) camera.reset(terrain.meta); },
};
