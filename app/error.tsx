'use client';
export default function Error({reset}:{reset:()=>void}){return <main className="error-state"><h1>The workspace couldn’t load</h1><p>Please try again. Your session has not changed the benchmark data.</p><button onClick={reset}>Try again</button></main>}
