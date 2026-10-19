import {
  mat4Create,
  mat4LookAt,
  mat4Multiply,
  mat4Perspective,
} from './mat4.js';

const DEG = Math.PI / 180;
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

/**
 * Damped orbit camera, azimuth measured clockwise from south
 * (azimuth 0 puts the camera south of the target, looking north).
 */
export class OrbitCamera {
  constructor() {
    this.target = [0, 0, 0];
    this.goalTarget = [0, 0, 0];
    this.azimuth = 0.55;
    this.goalAzimuth = 0.55;
    this.elevation = 0.62;
    this.goalElevation = 0.62;
    this.distance = 120000;
    this.goalDistance = 120000;

    this.fov = 50 * DEG;
    this.near = 150;
    this.far = 900000;
    this.minDistance = 600;
    this.maxDistance = 650000;
    this.damping = 11;
    this.meta = null;
    this.targetY = 0;

    this._view = mat4Create();
    this._proj = mat4Create();
    this._viewProj = mat4Create();
  }

  frame(meta, snap = true) {
    this.meta = meta;
    this.targetY = 0;
    const [width, depth] = meta.sizeMeters;
    this.goalTarget = [0, 0, depth * 0.045];
    this.goalAzimuth = 24 * DEG;
    this.goalElevation = 40 * DEG;
    this.goalDistance = Math.max(width, depth) * 1.16;
    this.minDistance = Math.max(width, depth) * 0.03;
    this.maxDistance = Math.max(width, depth) * 6;
    if (snap) {
      this.target = [...this.goalTarget];
      this.azimuth = this.goalAzimuth;
      this.elevation = this.goalElevation;
      this.distance = this.goalDistance;
    }
  }

  reset(meta = this.meta) {
    if (meta) this.frame(meta, false);
  }

  rotate(dx, dy) {
    this.goalAzimuth -= dx * 0.0045;
    this.goalElevation = clamp(this.goalElevation + dy * 0.0035, 0.045, 1.45);
  }

  pan(dx, dy, viewportHeight) {
    const eye = this.getEye();
    let fx = this.target[0] - eye[0];
    let fy = this.target[1] - eye[1];
    let fz = this.target[2] - eye[2];
    let len = Math.hypot(fx, fy, fz) || 1;
    fx /= len; fy /= len; fz /= len;

    let rx = -fz;
    let rz = fx;
    len = Math.hypot(rx, rz) || 1;
    rx /= len; rz /= len;

    let gx = fx, gz = fz;
    len = Math.hypot(gx, gz) || 1;
    gx /= len; gz /= len;

    const worldPerPixel =
      (2 * this.distance * Math.tan(this.fov / 2)) / Math.max(1, viewportHeight);
    const sx = dx * worldPerPixel;
    const sy = dy * worldPerPixel;

    this.goalTarget[0] += -rx * sx + gx * sy;
    this.goalTarget[2] += -rz * sx + gz * sy;

    if (this.meta) {
      const limitX = this.meta.sizeMeters[0] * 0.75;
      const limitZ = this.meta.sizeMeters[1] * 0.75;
      this.goalTarget[0] = clamp(this.goalTarget[0], -limitX, limitX);
      this.goalTarget[2] = clamp(this.goalTarget[2], -limitZ, limitZ);
    }
    this.goalTarget[1] = this.targetY;
  }

  /** Rotate to the nearest north-up heading (screen up = north, right = east). */
  faceNorth() {
    const turn = Math.PI * 2;
    this.goalAzimuth = Math.round(this.azimuth / turn) * turn;
  }

  /** Raise/lower the point the camera orbits around (used for peak framing). */
  setTargetHeight(y, snap = false) {
    this.targetY = y;
    this.goalTarget[1] = y;
    if (snap) this.target[1] = y;
  }

  zoom(factor) {
    this.goalDistance = clamp(
      this.goalDistance * factor,
      this.minDistance,
      this.maxDistance,
    );
  }

  update(dt, autoRotate = false) {
    if (autoRotate) this.goalAzimuth += dt * 0.055;
    const k = 1 - Math.exp(-this.damping * Math.min(dt, 0.1));
    this.azimuth += (this.goalAzimuth - this.azimuth) * k;
    this.elevation += (this.goalElevation - this.elevation) * k;
    this.distance += (this.goalDistance - this.distance) * k;
    for (let i = 0; i < 3; i++) {
      this.target[i] += (this.goalTarget[i] - this.target[i]) * k;
    }
  }

  getEye() {
    const ce = Math.cos(this.elevation);
    return [
      this.target[0] + this.distance * ce * Math.sin(this.azimuth),
      this.target[1] + this.distance * Math.sin(this.elevation),
      this.target[2] + this.distance * ce * Math.cos(this.azimuth),
    ];
  }

  getForward() {
    const eye = this.getEye();
    let x = this.target[0] - eye[0];
    let y = this.target[1] - eye[1];
    let z = this.target[2] - eye[2];
    const len = Math.hypot(x, y, z) || 1;
    return [x / len, y / len, z / len];
  }

  getViewProj(aspect) {
    const eye = this.getEye();
    mat4LookAt(this._view, eye, this.target, [0, 1, 0]);
    mat4Perspective(this._proj, this.fov, aspect, this.near, this.far);
    mat4Multiply(this._viewProj, this._proj, this._view);
    return this._viewProj;
  }
}
