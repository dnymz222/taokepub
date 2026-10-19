import { mat4Create, mat4Invert, transformPoint } from './mat4.js';

/** Decode a little-endian IEEE-754 half float (stored as uint16). */
export function halfToFloat(h) {
  const sign = h & 0x8000 ? -1 : 1;
  const exponent = (h >> 10) & 0x1f;
  const fraction = h & 0x3ff;
  if (exponent === 0) return sign * 2 ** -14 * (fraction / 1024);
  if (exponent === 31) return fraction ? NaN : sign * Infinity;
  return sign * 2 ** (exponent - 15) * (1 + fraction / 1024);
}

/**
 * Bilinear height sample in normalised texture coordinates.
 * (0,0) is the north-west corner, matching the GPU texture orientation.
 */
export function sampleHeight(terrain, u, v) {
  const { meta, data } = terrain;
  if (!(u >= 0 && u <= 1 && v >= 0 && v <= 1)) return null;
  const w = meta.width;
  const h = meta.height;
  const x = Math.min(w - 1, Math.max(0, u * w - 0.5));
  const y = Math.min(h - 1, Math.max(0, v * h - 0.5));
  const x0 = Math.floor(x);
  const y0 = Math.floor(y);
  const x1 = Math.min(w - 1, x0 + 1);
  const y1 = Math.min(h - 1, y0 + 1);
  const fx = x - x0;
  const fy = y - y0;

  const h00 = halfToFloat(data[y0 * w + x0]);
  const h10 = halfToFloat(data[y0 * w + x1]);
  const h01 = halfToFloat(data[y1 * w + x0]);
  const h11 = halfToFloat(data[y1 * w + x1]);
  return (h00 * (1 - fx) + h10 * fx) * (1 - fy)
    + (h01 * (1 - fx) + h11 * fx) * fy;
}

function unproject(inv, x, y, z) {
  const p = transformPoint(inv, x, y, z);
  if (!p[3]) return null;
  return [p[0] / p[3], p[1] / p[3], p[2] / p[3]];
}

/**
 * March a view ray against the DEM and return the first surface hit.
 * `ndc` values are in [-1, 1] with +y up.
 * `eye` is the camera position in scene space (Y already exaggerated); when
 * provided, `distance` is the real-world distance from the eye to the hit.
 */
export function pickTerrain(vp, ndcX, ndcY, terrain, exag, eye = null) {
  if (!terrain) return null;
  const inv = mat4Invert(mat4Create(), vp);
  if (!inv) return null;
  const near = unproject(inv, ndcX, ndcY, -1);
  const far = unproject(inv, ndcX, ndcY, 1);
  if (!near || !far) return null;

  const ox = near[0];
  const oy = near[1];
  const oz = near[2];
  let dx = far[0] - ox;
  let dy = far[1] - oy;
  let dz = far[2] - oz;
  const len = Math.hypot(dx, dy, dz) || 1;
  dx /= len;
  dy /= len;
  dz /= len;
  const maxT = 900000;
  const steps = 1400;

  const meta = terrain.meta;
  const [worldW, worldD] = meta.sizeMeters;

  const heightAt = (t) => {
    const x = ox + dx * t;
    const z = oz + dz * t;
    const u = x / worldW + 0.5;
    const v = z / worldD + 0.5;
    const h = sampleHeight(terrain, u, v);
    if (h === null) return null;
    return { y: oy + dy * t, h, x, z, u, v };
  };

  let prevT = 0;
  let prev = heightAt(0);
  let hitT = null;
  for (let i = 1; i <= steps; i++) {
    const t = (i / steps) * maxT;
    const cur = heightAt(t);
    if (cur) {
      if (cur.y <= cur.h * exag) {
        let lo = prevT;
        let hi = t;
        for (let k = 0; k < 26; k++) {
          const mid = (lo + hi) * 0.5;
          const s = heightAt(mid);
          if (!s || s.y <= s.h * exag) hi = mid;
          else lo = mid;
        }
        hitT = hi;
        break;
      }
    }
    prevT = t;
    prev = cur;
  }
  if (hitT === null) return null;

  const s = heightAt(hitT);
  if (!s) return null;
  const lon = meta.bounds.west + s.u * (meta.bounds.east - meta.bounds.west);
  const lat = meta.bounds.north - s.v * (meta.bounds.north - meta.bounds.south);
  // The summit sits at the centre of the crop; x/z are already in metres.
  const peakElevation = Number(meta.peakElevation ?? meta.peak?.elevation) || 0;
  const peakDistance = Math.hypot(s.x, s.z, s.h - peakElevation);
  // Generic readout distance: from the eye (not the near plane), with the
  // vertical exaggeration undone.
  const distance = eye
    ? Math.hypot(eye[0] - s.x, eye[1] / exag - s.h, eye[2] - s.z)
    : hitT;
  return {
    lon,
    lat,
    elevation: s.h,
    world: [s.x, s.h * exag, s.z],
    distance,
    peakDistance,
    u: s.u,
    v: s.v,
  };
}
