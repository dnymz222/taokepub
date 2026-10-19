const DATA_ROOT = 'data';

export async function fetchJSON(url) {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`无法加载 ${url}（HTTP ${res.status}）`);
  return res.json();
}

export async function loadManifest() {
  return fetchJSON(`${DATA_ROOT}/manifest.json`);
}

export async function fetchBinary(url, onProgress) {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`无法加载 ${url}（HTTP ${res.status}）`);
  const total = Number(res.headers.get('content-length')) || 0;

  if (!res.body || !total) {
    const buf = await res.arrayBuffer();
    if (onProgress) onProgress(1, buf.byteLength);
    return buf;
  }

  const reader = res.body.getReader();
  const chunks = [];
  let received = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    received += value.byteLength;
    if (onProgress) onProgress(Math.min(1, received / total), received);
  }
  const out = new Uint8Array(received);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return out.buffer;
}

export async function loadTerrain(summary, onProgress) {
  const meta = await fetchJSON(`${DATA_ROOT}/${summary.meta || `${summary.id}.json`}`);
  const buffer = await fetchBinary(
    `${DATA_ROOT}/${summary.file || `${summary.id}.f16`}`,
    onProgress,
  );
  if (buffer.byteLength % 2 !== 0) {
    throw new Error('地形二进制长度异常');
  }
  const data = new Uint16Array(buffer);
  const expected = meta.width * meta.height;
  if (data.length !== expected) {
    throw new Error(`高程样本数量不匹配：${data.length} / ${expected}`);
  }
  return { meta, data, summary };
}
