import {
  createBrowserRouter,
  Navigate,
  NavLink,
  Outlet,
} from "react-router-dom";
import { useDeferredValue, useMemo, useState } from "react";
import {
  auditEvents,
  instrumentTradeability,
  recoveryRuns,
  venueTradeability,
} from "./static-data";

function Shell() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <p className="eyebrow">Phase 5</p>
        <h1>Operator Acceptance Console</h1>
        <p className="sidebar-copy">
          Read-only acceptance surface for tradeability, recovery, and audit evidence.
        </p>
        <nav className="nav">
          <NavLink to="/tradeability">Tradeability</NavLink>
          <NavLink to="/recovery">Recovery</NavLink>
          <NavLink to="/audit">Audit</NavLink>
        </nav>
        <section className="closeout-card">
          <h2>Closeout Focus</h2>
          <p>
            This console is read-only. It exists to verify venue readiness, recovery
            posture, and audit continuity before live canary closeout.
          </p>
        </section>
      </aside>
      <main className="main-panel">
        <Outlet />
      </main>
    </div>
  );
}

function TradeabilityPage() {
  return (
    <section className="page">
      <header className="page-header">
        <p className="eyebrow">Readonly View</p>
        <h2>Venue Tradeability</h2>
        <p>
          Supervisor-driven tradeability projections for Phase 5 acceptance.
        </p>
      </header>

      <div className="card-grid">
        {venueTradeability.map((item) => (
          <article className="status-card" key={item.venue}>
            <div className="status-row">
              <strong>{item.venue}</strong>
              <span className={`badge badge-${item.supervisorState.toLowerCase()}`}>
                {item.supervisorState}
              </span>
            </div>
            <p>{item.reason}</p>
            <dl className="metric-grid">
              <div>
                <dt>Allow Open</dt>
                <dd>{item.allowOpen ? "yes" : "no"}</dd>
              </div>
              <div>
                <dt>Allow Reduce</dt>
                <dd>{item.allowReduce ? "yes" : "no"}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>

      <section className="table-card">
        <div className="section-heading">
          <h3>Instrument Tradeability</h3>
          <p>Frozen Phase 1 canary instruments only.</p>
        </div>
        <table>
          <thead>
            <tr>
              <th>Instrument</th>
              <th>Venue</th>
              <th>State</th>
              <th>Open</th>
              <th>Reduce</th>
            </tr>
          </thead>
          <tbody>
            {instrumentTradeability.map((item) => (
              <tr key={`${item.venue}-${item.instrumentId}`}>
                <td>{item.instrumentId}</td>
                <td>{item.venue}</td>
                <td>{item.supervisorState}</td>
                <td>{item.allowOpen ? "yes" : "no"}</td>
                <td>{item.allowReduce ? "yes" : "no"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </section>
  );
}

function RecoveryPage() {
  return (
    <section className="page">
      <header className="page-header">
        <p className="eyebrow">Readonly View</p>
        <h2>Recovery Runs</h2>
        <p>Recovery and reconciliation progress as closeout evidence.</p>
      </header>
      <div className="stack">
        {recoveryRuns.map((run) => (
          <article className="timeline-card" key={run.runId}>
            <div className="status-row">
              <strong>{run.runId}</strong>
              <span className={`badge badge-${run.status.toLowerCase()}`}>{run.status}</span>
            </div>
            <p className="timeline-phase">{run.phase}</p>
            <p>{run.triggerReason}</p>
            <code>{run.blockersJson}</code>
          </article>
        ))}
      </div>
    </section>
  );
}

function AuditPage() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const filteredEvents = useMemo(() => {
    const normalized = deferredQuery.trim().toLowerCase();
    if (!normalized) {
      return auditEvents;
    }
    return auditEvents.filter((event) =>
      [event.eventType, event.correlationId, event.scope.venue]
        .join(" ")
        .toLowerCase()
        .includes(normalized),
    );
  }, [deferredQuery]);

  return (
    <section className="page">
      <header className="page-header">
        <p className="eyebrow">Readonly View</p>
        <h2>Audit Events</h2>
        <p>Redacted audit trail supporting live canary approval and recovery review.</p>
      </header>
      <label className="search-card">
        <span>Filter by correlation or event type</span>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="corr-live-001"
        />
      </label>
      <div className="stack">
        {filteredEvents.map((event) => (
          <article className="timeline-card" key={event.eventId}>
            <div className="status-row">
              <strong>{event.eventType}</strong>
              <span className="mono">{event.occurredAt}</span>
            </div>
            <p className="mono">{event.correlationId}</p>
            <p>
              {event.sourceComponent} · venue={event.scope.venue}
              {event.scope.instrumentId ? ` · ${event.scope.instrumentId}` : ""}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Shell />,
    children: [
      { index: true, element: <Navigate to="/tradeability" replace /> },
      { path: "/tradeability", element: <TradeabilityPage /> },
      { path: "/recovery", element: <RecoveryPage /> },
      { path: "/audit", element: <AuditPage /> },
    ],
  },
]);
