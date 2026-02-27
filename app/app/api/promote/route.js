import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";
import { NextResponse } from "next/server";
import { getDraftDocument, getVaultRoot } from "../../../lib/vault";

export const runtime = "nodejs";

const DEFAULT_FIT_DOCS_ROOT = "D:\\dev\\github\\fit-docs\\docs";
const MAX_SCAN_LEVELS = 8;

function getFitDocsRoot() {
  return process.env.FIT_DOCS_ROOT || DEFAULT_FIT_DOCS_ROOT;
}

function findRepoRoot() {
  if (process.env.FIT_FORGE_ROOT) {
    return path.resolve(process.env.FIT_FORGE_ROOT);
  }

  let current = process.cwd();
  for (let i = 0; i < MAX_SCAN_LEVELS; i += 1) {
    if (fs.existsSync(path.join(current, "agent", "promote.py"))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) {
      break;
    }
    current = parent;
  }

  return path.resolve(process.cwd(), "..");
}

function runPromote({ draft, vaultRoot, fitDocsRoot, repoRoot }) {
  return new Promise((resolve) => {
    const pythonBin = process.env.PYTHON_BIN || "python";
    const scriptPath = path.join(repoRoot, "agent", "promote.py");
    const args = [
      scriptPath,
      "--no-commit",
      "--vault",
      vaultRoot,
      "--fit-docs",
      fitDocsRoot,
      draft,
    ];

    const child = spawn(pythonBin, args, { cwd: repoRoot });
    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += String(chunk);
    });

    child.stderr.on("data", (chunk) => {
      stderr += String(chunk);
    });

    child.on("error", (error) => {
      resolve({ code: 1, stdout, stderr: `${stderr}\n${error.message}`.trim() });
    });

    child.on("close", (code) => {
      resolve({ code: code ?? 1, stdout, stderr });
    });
  });
}

function firstLine(text) {
  if (!text) {
    return "";
  }
  const line = String(text).trim().split(/\r?\n/)[0];
  return line || "";
}

function parsePromotedTarget(stdout) {
  const match = String(stdout || "").match(/^Promoted ->\s*(.+)$/m);
  return match ? match[1].trim() : "";
}

export async function POST(request) {
  let payload;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const draft = typeof payload?.draft === "string" ? payload.draft.trim() : "";
  if (!draft) {
    return NextResponse.json({ error: "Missing draft path." }, { status: 400 });
  }

  const doc = await getDraftDocument(draft);
  if (doc.error) {
    return NextResponse.json({ error: doc.error }, { status: 400 });
  }

  if (doc.metadata?.status !== "promote-ready") {
    return NextResponse.json(
      { error: "Status must be 'promote-ready' before approve." },
      { status: 400 },
    );
  }

  const failedGates = doc.gates.filter((gate) => !gate.value).map((gate) => gate.name);
  if (failedGates.length > 0) {
    return NextResponse.json(
      { error: `Gate check failed: ${failedGates.join(", ")}` },
      { status: 400 },
    );
  }

  const vaultRoot = getVaultRoot();
  const fitDocsRoot = getFitDocsRoot();
  const repoRoot = findRepoRoot();
  const result = await runPromote({ draft, vaultRoot, fitDocsRoot, repoRoot });

  if (result.code !== 0) {
    return NextResponse.json(
      {
        error: firstLine(result.stderr) || "Promote command failed.",
        stdout: result.stdout,
        stderr: result.stderr,
      },
      { status: 500 },
    );
  }

  return NextResponse.json({
    ok: true,
    target: parsePromotedTarget(result.stdout),
    stdout: result.stdout,
  });
}
