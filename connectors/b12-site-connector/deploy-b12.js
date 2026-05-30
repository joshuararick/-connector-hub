#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const ROOT = path.resolve(__dirname, '../..');
const DIST = path.join(ROOT, 'dist-b12');
const REQUIRED = ['index.html', 'styles.css', 'app.js', 'agents.json'];
const SECRET_PATTERNS = [
  /sk-[A-Za-z0-9_-]{16,}/,
  /ghp_[A-Za-z0-9_]{20,}/,
  /xox[baprs]-[A-Za-z0-9-]{20,}/,
  /AKIA[0-9A-Z]{16}/,
  /AIza[0-9A-Za-z_-]{20,}/,
  /[A-Za-z0-9_-]{32,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}/
];

function fail(message) {
  console.error(`B12 connector error: ${message}`);
  process.exit(1);
}

function read(file) {
  return fs.readFileSync(path.join(ROOT, file), 'utf8');
}

function validateFiles() {
  for (const file of REQUIRED) {
    const full = path.join(ROOT, file);
    if (!fs.existsSync(full)) fail(`Missing required source file: ${file}`);
    const content = read(file);
    for (const pattern of SECRET_PATTERNS) {
      if (pattern.test(content)) fail(`Possible secret detected in ${file}. Remove it before publishing.`);
    }
  }
}

function writeDist() {
  fs.rmSync(DIST, { recursive: true, force: true });
  fs.mkdirSync(DIST, { recursive: true });
  for (const file of REQUIRED) fs.copyFileSync(path.join(ROOT, file), path.join(DIST, file));
  const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json'), 'utf8'));
  manifest.builtAt = new Date().toISOString();
  manifest.contentHash = crypto
    .createHash('sha256')
    .update(REQUIRED.map(file => read(file)).join('\n---FILE---\n'))
    .digest('hex');
  fs.writeFileSync(path.join(DIST, 'b12-build-manifest.json'), JSON.stringify(manifest, null, 2));
  return manifest;
}

async function deploy(manifest) {
  const url = process.env.B12_DEPLOY_WEBHOOK_URL;
  const token = process.env.B12_DEPLOY_TOKEN;
  if (!url) {
    console.log('No B12_DEPLOY_WEBHOOK_URL configured. Build is ready in dist-b12/.');
    console.log('Production site target: https://agent-command-center.b12sites.com/#overview');
    console.log('Add a B12 deploy webhook/API endpoint as B12_DEPLOY_WEBHOOK_URL to enable automatic publishing.');
    return;
  }

  const payload = {
    site: 'https://agent-command-center.b12sites.com/#overview',
    sourceRepo: manifest.sourceRepo,
    contentHash: manifest.contentHash,
    files: Object.fromEntries(REQUIRED.map(file => [file, read(file)]))
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    fail(`Deploy webhook failed with ${response.status}: ${text.slice(0, 500)}`);
  }

  console.log('B12 deploy webhook accepted the package.');
}

async function main() {
  validateFiles();
  const manifest = writeDist();
  await deploy(manifest);
}

main().catch(error => fail(error.stack || error.message));
