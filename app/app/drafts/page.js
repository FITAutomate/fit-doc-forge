import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { getDraftDocument, listDraftDocuments } from "../../lib/vault";

function renderValue(value) {
  if (value === null || value === undefined || value === "") {
    return "—";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

function GatePanel({ gates }) {
  if (!gates.length) {
    return (
      <section className="panel">
        <h3>Gate Status</h3>
        <p>No gate fields detected.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h3>Gate Status</h3>
      <ul className="gate-list">
        {gates.map((gate) => (
          <li key={gate.name} className="gate-item">
            <span>{gate.name}</span>
            <span className={gate.value ? "gate-pass" : "gate-fail"}>
              {gate.value ? "PASS" : "FAIL"}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}

function FrontmatterPanel({ metadata }) {
  const entries = Object.entries(metadata || {});
  return (
    <section className="panel">
      <h3>Frontmatter</h3>
      {entries.length === 0 ? (
        <p>No YAML frontmatter found.</p>
      ) : (
        <table className="meta-table">
          <thead>
            <tr>
              <th>Field</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {entries.map(([key, value]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{renderValue(value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default async function DraftsPage({ searchParams }) {
  const listing = await listDraftDocuments();

  if (!listing.available) {
    return (
      <main className="page">
        <h1>Draft Browser</h1>
        <p>Vault root not found: <code>{listing.vaultRoot}</code></p>
        <p>Set <code>VAULT_ROOT</code> to a valid path with <code>02-DRAFTS</code> or <code>03-REVIEW</code>.</p>
      </main>
    );
  }

  const selectedRelativePath =
    typeof searchParams?.file === "string"
      ? searchParams.file
      : listing.files[0]?.relativePath;

  let selected = null;
  let selectedError = null;
  if (selectedRelativePath) {
    const loaded = await getDraftDocument(selectedRelativePath);
    if (loaded.error) {
      selectedError = loaded.error;
    } else {
      selected = loaded;
    }
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1>Draft Browser</h1>
        <p>Read-only preview for vault drafts in <code>{listing.vaultRoot}</code>.</p>
      </header>

      <section className="browser-layout">
        <aside className="sidebar panel">
          <h2>Files</h2>
          <ul className="file-list">
            {listing.files.map((file) => {
              const active = selected?.relativePath === file.relativePath;
              return (
                <li key={file.relativePath}>
                  <Link
                    className={active ? "file-link active" : "file-link"}
                    href={{ pathname: "/drafts", query: { file: file.relativePath } }}
                  >
                    <span>{file.title}</span>
                    <small>{file.relativePath}</small>
                  </Link>
                </li>
              );
            })}
          </ul>
        </aside>

        <article className="content panel">
          {selectedError && (
            <div className="error-box">
              <strong>Unable to open file:</strong> {selectedError}
            </div>
          )}

          {!selected && !selectedError && <p>Select a file to preview.</p>}

          {selected && (
            <>
              <h2>{selected.metadata.title || selected.relativePath}</h2>
              <p className="muted">
                <code>{selected.relativePath}</code>
              </p>
              <div className="markdown-body">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{selected.body}</ReactMarkdown>
              </div>
            </>
          )}
        </article>

        <aside className="details">
          <GatePanel gates={selected?.gates || []} />
          <FrontmatterPanel metadata={selected?.metadata || {}} />
        </aside>
      </section>
    </main>
  );
}
