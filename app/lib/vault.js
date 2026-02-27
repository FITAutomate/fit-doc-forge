import fs from "node:fs/promises";
import path from "node:path";
import { load as loadYaml } from "js-yaml";

const DEFAULT_VAULT_ROOT = "D:\\Vaults\\FIT-Vault";
const DRAFT_ROOTS = ["02-DRAFTS", "03-REVIEW"];
const BASE_GATES = [
  "gate_has_owner",
  "gate_metadata_complete",
  "gate_heading_structure_valid",
  "gate_reviewed_by_human",
];
const PUBLIC_GATES = ["gate_no_internal_refs", "gate_no_invented_slas"];

function normalizeRelativePath(relativePath) {
  return String(relativePath || "").replaceAll("\\", "/").replace(/^\/+/, "");
}

function isAllowedDraftPath(relativePath) {
  const normalized = normalizeRelativePath(relativePath);
  if (!normalized.endsWith(".md")) {
    return false;
  }
  if (normalized.includes("..")) {
    return false;
  }
  return DRAFT_ROOTS.some(
    (prefix) => normalized === prefix || normalized.startsWith(`${prefix}/`),
  );
}

function parseFrontmatter(text) {
  if (!text.startsWith("---")) {
    return { metadata: {}, body: text };
  }

  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) {
    return { metadata: {}, body: text };
  }

  let metadata = {};
  try {
    const parsed = loadYaml(match[1]);
    if (parsed && typeof parsed === "object") {
      metadata = parsed;
    }
  } catch {
    metadata = {};
  }

  return { metadata, body: text.slice(match[0].length) };
}

async function exists(pathname) {
  try {
    await fs.access(pathname);
    return true;
  } catch {
    return false;
  }
}

async function walkMarkdownFiles(directory, bucket) {
  const entries = await fs.readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await walkMarkdownFiles(fullPath, bucket);
      continue;
    }
    if (entry.isFile() && entry.name.toLowerCase().endsWith(".md")) {
      bucket.push(fullPath);
    }
  }
}

function getGateStates(metadata) {
  const gates = [...BASE_GATES];
  const target = String(metadata.kb_target || "").toUpperCase();
  if (target === "PUBLIC_WEB" || target === "DUAL") {
    gates.push(...PUBLIC_GATES);
  }
  return gates.map((name) => ({
    name,
    value: Boolean(metadata[name]),
  }));
}

function toPathSegments(relativePath) {
  return normalizeRelativePath(relativePath).split("/").filter(Boolean);
}

function toDisplayTitle(relativePath, metadata) {
  if (metadata.title) {
    return String(metadata.title);
  }
  const base = path.basename(relativePath);
  return base.replace(/\.md$/i, "");
}

export function getVaultRoot() {
  return process.env.VAULT_ROOT || DEFAULT_VAULT_ROOT;
}

export async function listDraftDocuments() {
  const vaultRoot = getVaultRoot();
  const availableRoots = [];
  for (const draftRoot of DRAFT_ROOTS) {
    const fullRoot = path.join(vaultRoot, draftRoot);
    if (await exists(fullRoot)) {
      availableRoots.push(fullRoot);
    }
  }

  if (availableRoots.length === 0) {
    return {
      vaultRoot,
      available: false,
      files: [],
    };
  }

  const files = [];
  for (const root of availableRoots) {
    await walkMarkdownFiles(root, files);
  }

  const records = [];
  for (const absolutePath of files) {
    const relativePath = normalizeRelativePath(path.relative(vaultRoot, absolutePath));
    const text = await fs.readFile(absolutePath, "utf-8");
    const { metadata } = parseFrontmatter(text);
    records.push({
      relativePath,
      title: toDisplayTitle(relativePath, metadata),
      status: metadata.status ? String(metadata.status) : "",
      type: metadata.type ? String(metadata.type) : "",
      gates: getGateStates(metadata),
    });
  }

  records.sort((a, b) => a.relativePath.localeCompare(b.relativePath));
  return {
    vaultRoot,
    available: true,
    files: records,
  };
}

export async function getDraftDocument(relativePath) {
  if (!isAllowedDraftPath(relativePath)) {
    return {
      error:
        "Invalid draft path. Only files in 02-DRAFTS/ and 03-REVIEW/ are allowed.",
    };
  }

  const vaultRoot = getVaultRoot();
  const resolvedVaultRoot = path.resolve(vaultRoot);
  const resolvedFile = path.resolve(vaultRoot, ...toPathSegments(relativePath));
  if (!resolvedFile.startsWith(resolvedVaultRoot)) {
    return { error: "Invalid draft path." };
  }

  if (!(await exists(resolvedFile))) {
    return { error: `Draft not found at ${relativePath}` };
  }

  const text = await fs.readFile(resolvedFile, "utf-8");
  const { metadata, body } = parseFrontmatter(text);

  return {
    relativePath: normalizeRelativePath(relativePath),
    metadata,
    body,
    gates: getGateStates(metadata),
  };
}
