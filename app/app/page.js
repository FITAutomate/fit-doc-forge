import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <h1>fit-docs-forge Preview UI</h1>
      <p>Phase 4 scaffold is live. The read-only draft browser is available now.</p>
      <p>
        <Link href="/drafts">Open Draft Browser</Link>
      </p>
    </main>
  );
}
