// GLSL ES 3.00 shaders for the terrain viewer.

export const terrainVS = /* glsl */ `#version 300 es
precision highp float;

layout(location = 0) in vec2 aGrid;
layout(location = 1) in float aBottom;

uniform sampler2D uHeight;
uniform mat4 uViewProj;
uniform vec2 uWorldSize;
uniform float uExag;
uniform float uBaseY;

out vec2 vUv;
out vec3 vWorld;
out float vBottom;

void main() {
  vUv = aGrid;
  float h = texture(uHeight, aGrid).r;
  float y = mix(h * uExag, uBaseY, aBottom);
  vec2 xz = (aGrid - 0.5) * uWorldSize;
  vWorld = vec3(xz.x, y, xz.y);
  vBottom = aBottom;
  gl_Position = uViewProj * vec4(vWorld, 1.0);
}
`;

export const terrainFS = /* glsl */ `#version 300 es
precision highp float;

in vec2 vUv;
in vec3 vWorld;
in float vBottom;

uniform sampler2D uHeight;
uniform vec2 uWorldSize;
uniform vec2 uTexel;
uniform float uExag;
uniform vec3 uSunDir;
uniform vec3 uCameraPos;
uniform vec3 uFogColor;
uniform int uContours;
uniform float uContourStep;
uniform int uShadows;
uniform int uRampMode;
uniform float uMinH;
uniform float uMaxH;

out vec4 outColor;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

float vnoise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  float a = hash(i);
  float b = hash(i + vec2(1.0, 0.0));
  float c = hash(i + vec2(0.0, 1.0));
  float d = hash(i + vec2(1.0, 1.0));
  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

vec3 elevationRamp(float h) {
  vec3 c0 = vec3(0.010, 0.035, 0.052);
  vec3 c1 = vec3(0.035, 0.120, 0.150);
  vec3 c2 = vec3(0.180, 0.320, 0.230);
  vec3 c3 = vec3(0.310, 0.450, 0.235);
  vec3 c4 = vec3(0.455, 0.505, 0.250);
  vec3 c5 = vec3(0.585, 0.525, 0.300);
  vec3 c6 = vec3(0.635, 0.510, 0.370);
  vec3 c7 = vec3(0.690, 0.615, 0.525);
  vec3 c8 = vec3(0.820, 0.795, 0.750);
  vec3 c9 = vec3(0.960, 0.958, 0.945);

  vec3 c = mix(c0, c1, smoothstep(-100.0, -20.0, h));
  c = mix(c, c2, smoothstep(-20.0, 0.0, h));
  c = mix(c, c3, smoothstep(0.0, 25.0, h));
  c = mix(c, c4, smoothstep(25.0, 90.0, h));
  c = mix(c, c5, smoothstep(90.0, 180.0, h));
  c = mix(c, c6, smoothstep(180.0, 320.0, h));
  c = mix(c, c7, smoothstep(320.0, 500.0, h));
  c = mix(c, c8, smoothstep(500.0, 700.0, h));
  c = mix(c, c9, smoothstep(700.0, 900.0, h));
  return c;
}

vec3 mountainRamp(float h) {
  float t = clamp((h - uMinH) / max(uMaxH - uMinH, 1.0), 0.0, 1.0);
  vec3 c0 = vec3(0.050, 0.095, 0.078);
  vec3 c1 = vec3(0.100, 0.205, 0.115);
  vec3 c2 = vec3(0.205, 0.315, 0.140);
  vec3 c3 = vec3(0.355, 0.400, 0.180);
  vec3 c4 = vec3(0.500, 0.455, 0.265);
  vec3 c5 = vec3(0.575, 0.505, 0.385);
  vec3 c6 = vec3(0.630, 0.595, 0.530);
  vec3 c7 = vec3(0.760, 0.735, 0.690);

  vec3 c = mix(c0, c1, smoothstep(0.0, 0.18, t));
  c = mix(c, c2, smoothstep(0.18, 0.38, t));
  c = mix(c, c3, smoothstep(0.38, 0.55, t));
  c = mix(c, c4, smoothstep(0.55, 0.72, t));
  c = mix(c, c5, smoothstep(0.72, 0.86, t));
  c = mix(c, c6, smoothstep(0.86, 0.95, t));
  c = mix(c, c7, smoothstep(0.95, 1.0, t));
  return c;
}

void main() {
  float dist = length(vWorld - uCameraPos);
  float fog = 1.0 - exp(-pow(dist / 380000.0, 2.1));
  fog = clamp(fog, 0.0, 0.68);

  // -- cut-away side walls ------------------------------------------------
  if (vBottom > 0.001) {
    float depthT = smoothstep(0.0, 1.0, vBottom);
    vec3 wall = mix(vec3(0.185, 0.160, 0.135), vec3(0.028, 0.034, 0.040), depthT);
    float strata = 0.92 + 0.08 * sin(vWorld.y * 0.021 + vWorld.x * 0.0013);
    wall *= strata;
    // Slightly lit rim right below the surface.
    wall = mix(wall, vec3(0.33, 0.30, 0.25), smoothstep(0.055, 0.0, vBottom) * 0.55);
    vec3 col = mix(wall, uFogColor, fog * 0.9);
    outColor = vec4(col, 1.0);
    return;
  }

  // -- surface ------------------------------------------------------------
  float h = texture(uHeight, vUv).r;
  // Sample a few texels out so lighting follows landforms instead of
  // single-cell SRTM noise (which looks like needles when exaggerated).
  vec2 nt = uTexel * 3.0;
  float hL = texture(uHeight, vUv - vec2(nt.x, 0.0)).r;
  float hR = texture(uHeight, vUv + vec2(nt.x, 0.0)).r;
  float hD = texture(uHeight, vUv - vec2(0.0, nt.y)).r;
  float hU = texture(uHeight, vUv + vec2(0.0, nt.y)).r;

  float dx = max(2.0 * nt.x * uWorldSize.x, 1.0);
  float dz = max(2.0 * nt.y * uWorldSize.y, 1.0);
  float gx = (hR - hL) / dx;
  float gz = (hU - hD) / dz;

  float shadeExag = max(1.0, uExag * 0.45);
  vec3 n = normalize(vec3(-gx * shadeExag, 1.0, -gz * shadeExag));
  float grad = length(vec2(gx, gz));

  vec3 base = (uRampMode == 1) ? mountainRamp(h) : elevationRamp(h);
  float grain = vnoise(vWorld.xz * 0.0017) * 0.6 + vnoise(vWorld.xz * 0.0075) * 0.4;
  base *= 0.94 + grain * 0.12;

  // Rock / bare ground on steep upper slopes.
  float rock = smoothstep(0.50, 1.15, grad) * smoothstep(120.0, 340.0, h);
  base = mix(base, vec3(0.40, 0.385, 0.355), rock * 0.65);

  vec3 viewDir = normalize(uCameraPos - vWorld);

  // Cheap heightfield shadow march towards the sun.
  float shadow = 1.0;
  if (uShadows == 1 && uSunDir.y > 0.04) {
    const int STEPS = 28;
    const float RANGE = 30000.0;
    vec2 stepUV = uSunDir.xz / uWorldSize * (RANGE / float(STEPS));
    float stepY = uSunDir.y * (RANGE / float(STEPS));
    vec2 suv = vUv;
    float rayY = h * uExag + 18.0;
    float occl = 0.0;
    for (int i = 0; i < STEPS; i++) {
      suv += stepUV;
      rayY += stepY;
      if (suv.x < 0.0 || suv.x > 1.0 || suv.y < 0.0 || suv.y > 1.0) break;
      float hs = texture(uHeight, suv).r * uExag;
      occl = max(occl, smoothstep(-25.0, 260.0, hs - rayY));
    }
    shadow = 1.0 - occl * 0.86;
  }

  float ndl = max(dot(n, uSunDir), 0.0);
  float sky = 0.5 + 0.5 * n.y;
  vec3 lit = base * (0.34 + 0.80 * ndl * shadow + 0.16 * sky);

  // Cheap curvature shading: open valleys fall into shade, ridges catch light.
  float lap = (hL + hR + hD + hU - 4.0 * h) * 0.25;
  lit *= 1.0 - clamp(lap * 0.014, 0.0, 0.32);
  lit *= 1.0 + clamp(-lap * 0.0045, 0.0, 0.10);
  lit += vec3(0.05, 0.065, 0.07) * pow(1.0 - max(dot(n, viewDir), 0.0), 3.0);

  // Contour lines (elevation).
  if (uContours == 1) {
    float f = h / max(uContourStep, 1.0);
    float w = max(fwidth(f) * 1.15, 0.0008);
    float line = 1.0 - smoothstep(0.0, w, abs(fract(f + 0.5) - 0.5));
    line *= smoothstep(1.6, 0.5, w);
    lit = mix(lit, lit * 0.52, line * 0.6);
  }

  lit = mix(lit, uFogColor, fog);
  outColor = vec4(lit, 1.0);
}
`;

export const wireVS = /* glsl */ `#version 300 es
precision highp float;

layout(location = 0) in vec2 aGrid;

uniform sampler2D uHeight;
uniform mat4 uViewProj;
uniform vec2 uWorldSize;
uniform float uExag;

void main() {
  float h = texture(uHeight, aGrid).r;
  vec2 xz = (aGrid - 0.5) * uWorldSize;
  vec4 p = uViewProj * vec4(xz.x, h * uExag, xz.y, 1.0);
  p.z -= 0.0009 * p.w;
  gl_Position = p;
}
`;

export const wireFS = /* glsl */ `#version 300 es
precision highp float;
out vec4 outColor;
void main() {
  outColor = vec4(0.60, 0.88, 0.84, 0.30);
}
`;

export const skyVS = /* glsl */ `#version 300 es
precision highp float;
out vec2 vUv;
void main() {
  vec2 p = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));
  vUv = p;
  gl_Position = vec4(p * 2.0 - 1.0, 1.0, 1.0);
}
`;

export const skyFS = /* glsl */ `#version 300 es
precision highp float;

uniform vec2 uResolution;
uniform vec2 uSunScreen;
uniform float uSunVisible;

out vec4 outColor;

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  vec3 horizon = vec3(0.300, 0.410, 0.465);
  vec3 zenith = vec3(0.013, 0.032, 0.050);
  float t = clamp(uv.y, 0.0, 1.0);
  vec3 col = mix(horizon, zenith, pow(t, 0.55));

  // Soft warm glow where the sun sits.
  float d = distance(uv, uSunScreen);
  float glow = exp(-d * d * 34.0) * uSunVisible;
  col += vec3(1.00, 0.78, 0.52) * glow * 0.42;
  col += vec3(1.00, 0.84, 0.62) * exp(-d * 4.2) * uSunVisible * 0.05;

  // Haze band just above the horizon.
  col = mix(col, vec3(0.38, 0.49, 0.54), (1.0 - smoothstep(0.0, 0.18, t)) * 0.25);

  outColor = vec4(col, 1.0);
}
`;

export const waterVS = /* glsl */ `#version 300 es
precision highp float;

layout(location = 0) in vec2 aPos;

uniform mat4 uViewProj;
uniform vec2 uWorldSize;
uniform float uSeaLevel;

out vec2 vUv;
out vec3 vWorld;

void main() {
  vUv = aPos + 0.5;
  vec3 world = vec3(aPos.x * uWorldSize.x, uSeaLevel, aPos.y * uWorldSize.y);
  vWorld = world;
  gl_Position = uViewProj * vec4(world, 1.0);
}
`;

export const waterFS = /* glsl */ `#version 300 es
precision highp float;

in vec2 vUv;
in vec3 vWorld;

uniform sampler2D uHeight;
uniform vec3 uSunDir;
uniform vec3 uCameraPos;
uniform float uTime;
uniform vec3 uFogColor;

out vec4 outColor;

void main() {
  float bed = texture(uHeight, vUv).r;
  float depth = clamp(-bed, 0.0, 90.0);
  vec3 shallow = vec3(0.155, 0.340, 0.345);
  vec3 deep = vec3(0.020, 0.095, 0.150);
  vec3 col = mix(shallow, deep, smoothstep(2.0, 55.0, depth));

  vec2 p = vWorld.xz;
  vec3 wn = normalize(vec3(
    sin(p.x * 0.0043 + uTime * 0.70) * 0.045 + sin(p.y * 0.0071 - uTime * 0.52) * 0.028,
    1.0,
    cos(p.y * 0.0048 + uTime * 0.61) * 0.045 + sin(p.x * 0.0057 + uTime * 0.44) * 0.026
  ));

  vec3 viewDir = normalize(uCameraPos - vWorld);
  float fres = pow(1.0 - max(dot(wn, viewDir), 0.0), 3.0);
  col = mix(col, vec3(0.34, 0.47, 0.54), fres * 0.55);

  vec3 hv = normalize(uSunDir + viewDir);
  float spec = pow(max(dot(wn, hv), 0.0), 300.0);
  col += vec3(1.0, 0.90, 0.74) * spec * 0.55;

  float dist = length(vWorld - uCameraPos);
  float fog = clamp(1.0 - exp(-pow(dist / 380000.0, 2.1)), 0.0, 0.68);
  col = mix(col, uFogColor, fog * 0.85);

  float alpha = mix(0.35, 0.88, smoothstep(1.0, 45.0, depth));
  alpha = clamp(alpha + fres * 0.12, 0.0, 0.94);
  outColor = vec4(col, alpha);
}
`;
