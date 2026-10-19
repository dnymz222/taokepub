import { transformPoint } from './mat4.js';
import {
  terrainVS,
  terrainFS,
  wireVS,
  wireFS,
  skyVS,
  skyFS,
  waterVS,
  waterFS,
} from './shaders.js';

const FOG_COLOR = [0.300, 0.410, 0.465];

function compileShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const log = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader);
    throw new Error(`Shader compile failed: ${log}`);
  }
  return shader;
}

function createProgram(gl, vsSource, fsSource) {
  const vs = compileShader(gl, gl.VERTEX_SHADER, vsSource);
  const fs = compileShader(gl, gl.FRAGMENT_SHADER, fsSource);
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  gl.deleteShader(vs);
  gl.deleteShader(fs);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const log = gl.getProgramInfoLog(program);
    gl.deleteProgram(program);
    throw new Error(`Program link failed: ${log}`);
  }
  return program;
}

function uniformMap(gl, program, names) {
  const map = {};
  for (const name of names) map[name] = gl.getUniformLocation(program, name);
  return map;
}

function sunVector(azimuthDeg, altitudeDeg) {
  const az = (azimuthDeg * Math.PI) / 180;
  const alt = (altitudeDeg * Math.PI) / 180;
  const ca = Math.cos(alt);
  return [Math.sin(az) * ca, Math.sin(alt), -Math.cos(az) * ca];
}

export class TerrainRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    const gl = canvas.getContext('webgl2', {
      antialias: true,
      alpha: false,
      depth: true,
      stencil: false,
      powerPreference: 'high-performance',
    });
    if (!gl) throw new Error('当前浏览器或设备不支持 WebGL 2');
    this.gl = gl;

    this.terrain = null;
    this.meta = null;
    this.resolution = 0;
    this.dprCap = 2;

    this.terrainProgram = createProgram(gl, terrainVS, terrainFS);
    this.terrainUniforms = uniformMap(gl, this.terrainProgram, [
      'uHeight', 'uViewProj', 'uWorldSize', 'uTexel', 'uExag', 'uSunDir',
      'uCameraPos', 'uFogColor', 'uContours', 'uContourStep', 'uShadows',
      'uRampMode', 'uMinH', 'uMaxH', 'uBaseY',
    ]);

    this.wireProgram = createProgram(gl, wireVS, wireFS);
    this.wireUniforms = uniformMap(gl, this.wireProgram, [
      'uHeight', 'uViewProj', 'uWorldSize', 'uExag',
    ]);

    this.skyProgram = createProgram(gl, skyVS, skyFS);
    this.skyUniforms = uniformMap(gl, this.skyProgram, [
      'uResolution', 'uSunScreen', 'uSunVisible',
    ]);

    this.waterProgram = createProgram(gl, waterVS, waterFS);
    this.waterUniforms = uniformMap(gl, this.waterProgram, [
      'uHeight', 'uViewProj', 'uWorldSize', 'uSunDir', 'uCameraPos',
      'uTime', 'uSeaLevel', 'uFogColor',
    ]);

    this.heightTexture = null;
    this.gridVbo = null;
    this.fillVao = null;
    this.fillIndexBuffer = null;
    this.fillIndexCount = 0;
    this.wireVao = null;
    this.wireIndexBuffer = null;
    this.wireIndexCount = 0;
    this.skirtVao = null;
    this.skirtVbo = null;
    this.skirtIndexBuffer = null;
    this.skirtIndexCount = 0;

    this.skyVao = gl.createVertexArray();
    this.waterVao = gl.createVertexArray();
    this.waterIndexCount = 6;
    this._createWaterGeometry();


    gl.clearColor(0.02, 0.04, 0.06, 1);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.disable(gl.CULL_FACE);
  }

  _createWaterGeometry() {
    const gl = this.gl;
    gl.bindVertexArray(this.waterVao);
    const vbo = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    // Unit quad in XZ, expanded to world size in the vertex shader.
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5]),
      gl.STATIC_DRAW,
    );
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    const ibo = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
    gl.bufferData(
      gl.ELEMENT_ARRAY_BUFFER,
      new Uint16Array([0, 1, 2, 0, 2, 3]),
      gl.STATIC_DRAW,
    );
    gl.bindVertexArray(null);
  }

  setTerrain(terrain) {
    const gl = this.gl;
    const { meta, data } = terrain;
    this.terrain = terrain;
    this.meta = meta;

    if (this.heightTexture) gl.deleteTexture(this.heightTexture);
    const tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);
    gl.texImage2D(
      gl.TEXTURE_2D,
      0,
      gl.R16F,
      meta.width,
      meta.height,
      0,
      gl.RED,
      gl.HALF_FLOAT,
      data,
    );
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    const err = gl.getError();
    if (err !== gl.NO_ERROR) {
      throw new Error(`高程纹理上传失败（WebGL error ${err}）`);
    }
    this.heightTexture = tex;
  }

  setMeshResolution(n) {
    if (n === this.resolution && this.fillVao) return;
    const gl = this.gl;
    this._disposeMesh();
    this.resolution = n;

    const size = n + 1;
    const verts = new Float32Array(size * size * 2);
    for (let j = 0; j < size; j++) {
      for (let i = 0; i < size; i++) {
        const o = (j * size + i) * 2;
        verts[o] = i / n;
        verts[o + 1] = j / n;
      }
    }

    const vbo = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);
    this.gridVbo = vbo;

    // ---- filled surface -------------------------------------------------
    const indices = new Uint32Array(n * n * 6);
    let p = 0;
    for (let j = 0; j < n; j++) {
      for (let i = 0; i < n; i++) {
        const a = j * size + i;
        const b = (j + 1) * size + i;
        const c = j * size + i + 1;
        const d = (j + 1) * size + i + 1;
        indices[p++] = a; indices[p++] = b; indices[p++] = c;
        indices[p++] = b; indices[p++] = d; indices[p++] = c;
      }
    }
    this.fillVao = gl.createVertexArray();
    gl.bindVertexArray(this.fillVao);
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 8, 0);
    this.fillIndexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.fillIndexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);
    this.fillIndexCount = indices.length;

    // ---- wire overlay ---------------------------------------------------
    const step = Math.max(1, Math.round(n / 64));
    const wire = [];
    for (let j = 0; j <= n; j += step) {
      for (let i = 0; i < n; i++) {
        wire.push(j * size + i, j * size + i + 1);
      }
    }
    for (let i = 0; i <= n; i += step) {
      for (let j = 0; j < n; j++) {
        wire.push(j * size + i, (j + 1) * size + i);
      }
    }
    const wireIndices = new Uint32Array(wire);
    this.wireVao = gl.createVertexArray();
    gl.bindVertexArray(this.wireVao);
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 8, 0);
    this.wireIndexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.wireIndexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, wireIndices, gl.STATIC_DRAW);
    this.wireIndexCount = wireIndices.length;

    // ---- side walls -----------------------------------------------------
    const skirt = [];
    const skirtIndices = [];
    let vi = 0;
    const addWall = (aGrid, bGrid) => {
      // top A, bottom A, top B, bottom B
      skirt.push(aGrid[0], aGrid[1], 0, aGrid[0], aGrid[1], 1,
        bGrid[0], bGrid[1], 0, bGrid[0], bGrid[1], 1);
      skirtIndices.push(vi, vi + 1, vi + 2, vi + 1, vi + 3, vi + 2);
      vi += 4;
    };
    for (let i = 0; i < n; i++) {
      addWall([i / n, 0], [(i + 1) / n, 0]);
      addWall([i / n, 1], [(i + 1) / n, 1]);
    }
    for (let j = 0; j < n; j++) {
      addWall([0, j / n], [0, (j + 1) / n]);
      addWall([1, j / n], [1, (j + 1) / n]);
    }
    const skirtData = new Float32Array(skirt);
    const skirtIndexData = new Uint32Array(skirtIndices);

    this.skirtVbo = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.skirtVbo);
    gl.bufferData(gl.ARRAY_BUFFER, skirtData, gl.STATIC_DRAW);
    this.skirtVao = gl.createVertexArray();
    gl.bindVertexArray(this.skirtVao);
    gl.bindBuffer(gl.ARRAY_BUFFER, this.skirtVbo);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 12, 0);
    gl.enableVertexAttribArray(1);
    gl.vertexAttribPointer(1, 1, gl.FLOAT, false, 12, 8);
    this.skirtIndexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.skirtIndexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, skirtIndexData, gl.STATIC_DRAW);
    this.skirtIndexCount = skirtIndexData.length;

    gl.bindVertexArray(null);
    gl.bindBuffer(gl.ARRAY_BUFFER, null);
    this._triangles = n * n * 2;
  }

  _disposeMesh() {
    const gl = this.gl;
    for (const vao of [this.fillVao, this.wireVao, this.skirtVao]) {
      if (vao) gl.deleteVertexArray(vao);
    }
    for (const buf of [
      this.gridVbo, this.fillIndexBuffer, this.wireIndexBuffer,
      this.skirtVbo, this.skirtIndexBuffer,
    ]) {
      if (buf) gl.deleteBuffer(buf);
    }
    this.fillVao = this.wireVao = this.skirtVao = null;
    this.gridVbo = this.fillIndexBuffer = this.wireIndexBuffer = null;
    this.skirtVbo = this.skirtIndexBuffer = null;
    this.fillIndexCount = this.wireIndexCount = this.skirtIndexCount = 0;
  }

  resize() {
    const gl = this.gl;
    const dpr = Math.min(window.devicePixelRatio || 1, this.dprCap);
    const width = Math.max(1, Math.round(this.canvas.clientWidth * dpr));
    const height = Math.max(1, Math.round(this.canvas.clientHeight * dpr));
    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
    }
    gl.viewport(0, 0, width, height);
    return width / height;
  }

  getStats() {
    return {
      resolution: this.resolution,
      triangles: this._triangles || 0,
      vertices: this.resolution ? (this.resolution + 1) ** 2 : 0,
    };
  }

  render(camera, options, timeSeconds) {
    if (!this.terrain) return;
    const gl = this.gl;
    const meta = this.meta;
    const aspect = this.resize();
    const vp = camera.getViewProj(aspect);
    const eye = camera.getEye();
    const [worldW, worldD] = meta.sizeMeters;
    const sun = sunVector(options.sunAzimuth, options.sunAltitude);

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // ---- sky ------------------------------------------------------------
    gl.disable(gl.DEPTH_TEST);
    gl.depthMask(false);
    gl.disable(gl.BLEND);

    const clip = transformPoint(vp, eye[0] + sun[0] * 100000, eye[1] + sun[1] * 100000, eye[2] + sun[2] * 100000);
    let sunScreen = [0.5, 0.5];
    let sunVisible = 0;
    if (clip[3] > 0) {
      const nx = clip[0] / clip[3];
      const ny = clip[1] / clip[3];
      sunScreen = [nx * 0.5 + 0.5, ny * 0.5 + 0.5];
      if (Math.abs(nx) < 2.2 && Math.abs(ny) < 2.2) sunVisible = 1;
    }

    gl.useProgram(this.skyProgram);
    gl.bindVertexArray(this.skyVao);
    gl.uniform2f(this.skyUniforms.uResolution, this.canvas.width, this.canvas.height);
    gl.uniform2f(this.skyUniforms.uSunScreen, sunScreen[0], sunScreen[1]);
    gl.uniform1f(this.skyUniforms.uSunVisible, sunVisible);
    gl.drawArrays(gl.TRIANGLES, 0, 3);

    gl.enable(gl.DEPTH_TEST);
    gl.depthMask(true);

    if (!this.heightTexture || !this.fillVao) return;

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.heightTexture);

    const exag = options.exag;
    const baseY = meta.minElevation * exag
      - Math.max(400, (meta.maxElevation - meta.minElevation) * exag * 0.2);

    // ---- terrain surface + cut walls -----------------------------------
    gl.useProgram(this.terrainProgram);
    const tu = this.terrainUniforms;
    gl.uniformMatrix4fv(tu.uViewProj, false, vp);
    gl.uniform1i(tu.uHeight, 0);
    gl.uniform2f(tu.uWorldSize, worldW, worldD);
    gl.uniform2f(tu.uTexel, 1 / meta.width, 1 / meta.height);
    gl.uniform1f(tu.uExag, exag);
    gl.uniform3f(tu.uSunDir, sun[0], sun[1], sun[2]);
    gl.uniform3f(tu.uCameraPos, eye[0], eye[1], eye[2]);
    gl.uniform3f(tu.uFogColor, FOG_COLOR[0], FOG_COLOR[1], FOG_COLOR[2]);
    gl.uniform1i(tu.uContours, options.contours ? 1 : 0);
    gl.uniform1f(tu.uContourStep, options.contourStep);
    gl.uniform1i(tu.uShadows, options.shadows ? 1 : 0);
    gl.uniform1i(tu.uRampMode, options.rampMode ? 1 : 0);
    gl.uniform1f(tu.uMinH, meta.minElevation);
    gl.uniform1f(tu.uMaxH, meta.maxElevation);
    gl.uniform1f(tu.uBaseY, baseY);

    gl.bindVertexArray(this.fillVao);
    gl.drawElements(gl.TRIANGLES, this.fillIndexCount, gl.UNSIGNED_INT, 0);

    if (this.skirtVao) {
      gl.bindVertexArray(this.skirtVao);
      gl.drawElements(gl.TRIANGLES, this.skirtIndexCount, gl.UNSIGNED_INT, 0);
    }

    // ---- wireframe overlay ---------------------------------------------
    if (options.wireframe && this.wireVao) {
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      gl.depthMask(false);
      gl.useProgram(this.wireProgram);
      gl.uniformMatrix4fv(this.wireUniforms.uViewProj, false, vp);
      gl.uniform1i(this.wireUniforms.uHeight, 0);
      gl.uniform2f(this.wireUniforms.uWorldSize, worldW, worldD);
      gl.uniform1f(this.wireUniforms.uExag, exag);
      gl.bindVertexArray(this.wireVao);
      gl.drawElements(gl.LINES, this.wireIndexCount, gl.UNSIGNED_INT, 0);
      gl.depthMask(true);
      gl.disable(gl.BLEND);
    }

    // ---- water ----------------------------------------------------------
    if (options.water) {
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      gl.depthMask(false);
      gl.useProgram(this.waterProgram);
      const wu = this.waterUniforms;
      gl.uniformMatrix4fv(wu.uViewProj, false, vp);
      gl.uniform1i(wu.uHeight, 0);
      gl.uniform2f(wu.uWorldSize, worldW, worldD);
      gl.uniform3f(wu.uSunDir, sun[0], sun[1], sun[2]);
      gl.uniform3f(wu.uCameraPos, eye[0], eye[1], eye[2]);
      gl.uniform1f(wu.uTime, timeSeconds);
      gl.uniform1f(wu.uSeaLevel, 0.6);
      gl.uniform3f(wu.uFogColor, FOG_COLOR[0], FOG_COLOR[1], FOG_COLOR[2]);
      gl.bindVertexArray(this.waterVao);
      gl.drawElements(gl.TRIANGLES, this.waterIndexCount, gl.UNSIGNED_SHORT, 0);
      gl.depthMask(true);
      gl.disable(gl.BLEND);
    }

    gl.bindVertexArray(null);
  }

}
