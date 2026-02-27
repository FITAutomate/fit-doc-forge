import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <h1>fit-docs-forge Preview UI</h1>
      <p>Phase 4 is live. Review drafts, inspect gates, and approve promote-ready docs.</p>
      <p>
        <Link href="/drafts">Open Draft Browser</Link>
      </p>
    </main>
  );
}
