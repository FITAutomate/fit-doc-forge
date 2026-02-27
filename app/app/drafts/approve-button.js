"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

function summarizeFailure(message) {
  if (!message) {
    return "Approve failed.";
  }
  const trimmed = String(message).trim();
  if (!trimmed) {
    return "Approve failed.";
  }
  const lines = trimmed.split(/\r?\n/).filter(Boolean);
  return lines[0];
}

export default function ApproveButton({ relativePath, gates, status }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);

  const gatesPassed = useMemo(() => {
    if (!Array.isArray(gates) || gates.length === 0) {
      return false;
    }
    return gates.every((gate) => gate?.value === true);
  }, [gates]);

  const statusReady = status === "promote-ready";
  const canApprove = Boolean(relativePath) && gatesPassed && statusReady && !busy;

  async function onApprove() {
    setBusy(true);
    setResult(null);
    try {
      const response = await fetch("/api/promote", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ draft: relativePath }),
      });
      const payload = await response.json();

      if (!response.ok) {
        setResult({
          ok: false,
          message: summarizeFailure(payload.error || payload.stderr || payload.stdout),
        });
        return;
      }

      setResult({
        ok: true,
        message: payload.target
          ? `Promoted: ${payload.target}`
          : "Promote completed.",
      });
      router.refresh();
    } catch (error) {
      setResult({
        ok: false,
        message: summarizeFailure(error?.message),
      });
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel">
      <h3>Approve</h3>
      <p className="muted">
        Runs <code>agent/promote.py</code> with <code>--no-commit</code>.
      </p>
      <button
        className="approve-button"
        onClick={onApprove}
        disabled={!canApprove}
        type="button"
      >
        {busy ? "Approving..." : "Approve + Promote"}
      </button>
      {!statusReady && (
        <p className="muted">Status must be <code>promote-ready</code>.</p>
      )}
      {!gatesPassed && <p className="muted">All gate fields must pass.</p>}
      {result && (
        <p className={result.ok ? "notice-success" : "notice-error"}>{result.message}</p>
      )}
    </section>
  );
}
