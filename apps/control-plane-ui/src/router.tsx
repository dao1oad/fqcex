import {
  createBrowserRouter,
  Navigate,
  NavLink,
  Outlet,
  useOutletContext,
} from "react-router-dom";
import { startTransition, useDeferredValue, useMemo, useState } from "react";
import {
  auditEvents,
  type AuditEvent,
  type OperatorActionName,
  instrumentTradeability,
  operatorActionTargets,
  recoveryRuns,
  venueTradeability,
} from "./static-data";

type ShellContextValue = {
  auditTimeline: AuditEvent[];
  appendAuditEvent: (event: AuditEvent) => void;
};

function useShellContext() {
  return useOutletContext<ShellContextValue>();
}

function Shell() {
  const [auditTimeline, setAuditTimeline] = useState<AuditEvent[]>(auditEvents);

  function appendAuditEvent(event: AuditEvent) {
    startTransition(() => {
      setAuditTimeline((current) => [event, ...current]);
    });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <p className="eyebrow">Phase 5</p>
        <h1>Operator Acceptance Console</h1>
        <p className="sidebar-copy">
          Acceptance surface for tradeability, recovery, audit evidence, and guarded
          operator actions.
        </p>
        <nav className="nav">
          <NavLink to="/tradeability">Tradeability</NavLink>
          <NavLink to="/recovery">Recovery</NavLink>
          <NavLink to="/audit">Audit</NavLink>
          <NavLink to="/actions">Actions</NavLink>
        </nav>
        <section className="closeout-card">
          <h2>Closeout Focus</h2>
          <p>
            This console exists to verify venue readiness, recovery posture, audit
            continuity, and the minimal guarded operator actions required before live
            canary closeout.
          </p>
        </section>
      </aside>
      <main className="main-panel">
        <Outlet context={{ auditTimeline, appendAuditEvent }} />
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
  const { auditTimeline } = useShellContext();
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const filteredEvents = useMemo(() => {
    const normalized = deferredQuery.trim().toLowerCase();
    if (!normalized) {
      return auditTimeline;
    }
    return auditTimeline.filter((event) =>
      [event.eventType, event.correlationId, event.scope.venue]
        .join(" ")
        .toLowerCase()
        .includes(normalized),
    );
  }, [auditTimeline, deferredQuery]);

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

function ActionsPage() {
  const { auditTimeline, appendAuditEvent } = useShellContext();
  const [targetId, setTargetId] = useState(operatorActionTargets[0].id);
  const [action, setAction] = useState<OperatorActionName>("force_resume");
  const [reason, setReason] = useState("");
  const [submissionCount, setSubmissionCount] = useState(0);

  const target = useMemo(
    () => operatorActionTargets.find((item) => item.id === targetId) ?? operatorActionTargets[0],
    [targetId],
  );

  const requirements = useMemo(() => {
    const shared = [{ key: "reasonProvided", satisfied: reason.trim().length > 0 }];
    if (action === "force_block") {
      return shared;
    }
    if (action === "force_reduce_only") {
      return [...shared, { key: "allowReduce", satisfied: target.allowReduce }];
    }
    return [
      ...shared,
      { key: "recoveryReady", satisfied: target.recoveryReady },
      { key: "approvalRecorded", satisfied: target.approvalRecorded },
      { key: "killSwitchInactive", satisfied: target.killSwitchInactive },
      { key: "notAlreadyLive", satisfied: target.supervisorState !== "LIVE" },
    ];
  }, [action, reason, target]);

  const canSubmit = requirements.every((item) => item.satisfied);
  const recentOperatorEvents = auditTimeline.filter(
    (event) => event.sourceComponent === "operator-ui",
  );

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) {
      return;
    }

    const nextIndex = submissionCount + 1;
    const correlationId = `corr-action-${String(nextIndex).padStart(3, "0")}`;
    appendAuditEvent({
      eventId: `audit-action-${String(nextIndex).padStart(3, "0")}`,
      eventType: action,
      occurredAt: new Date(Date.UTC(2026, 2, 21, 11, 10 + nextIndex, 0)).toISOString(),
      sourceComponent: "operator-ui",
      correlationId,
      scope: {
        venue: target.venue,
        instrumentId: target.instrumentId,
      },
    });
    setSubmissionCount(nextIndex);
    setReason("");
  }

  return (
    <section className="page">
      <header className="page-header">
        <p className="eyebrow">Guarded Action View</p>
        <h2>Operator Actions</h2>
        <p>
          Static acceptance harness for guarded operator actions before the live canary
          stage switches to real control-plane writes.
        </p>
      </header>

      <div className="card-grid">
        {operatorActionTargets.map((item) => (
          <article className="status-card" key={item.id}>
            <div className="status-row">
              <strong>{item.label}</strong>
              <span className={`badge badge-${item.supervisorState.toLowerCase()}`}>
                {item.supervisorState}
              </span>
            </div>
            <dl className="metric-grid">
              <div>
                <dt>recoveryReady</dt>
                <dd>{item.recoveryReady ? "yes" : "no"}</dd>
              </div>
              <div>
                <dt>approvalRecorded</dt>
                <dd>{item.approvalRecorded ? "yes" : "no"}</dd>
              </div>
              <div>
                <dt>killSwitchInactive</dt>
                <dd>{item.killSwitchInactive ? "yes" : "no"}</dd>
              </div>
              <div>
                <dt>allowReduce</dt>
                <dd>{item.allowReduce ? "yes" : "no"}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>

      <div className="actions-layout">
        <form className="form-card" onSubmit={handleSubmit}>
          <div className="section-heading">
            <h3>Action Form</h3>
            <p>Submission stays disabled until every required precondition is satisfied.</p>
          </div>

          <label className="field">
            <span>Target</span>
            <select
              aria-label="Target"
              value={targetId}
              onChange={(event) => setTargetId(event.target.value)}
            >
              {operatorActionTargets.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.label}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Action</span>
            <select
              aria-label="Action"
              value={action}
              onChange={(event) => setAction(event.target.value as OperatorActionName)}
            >
              <option value="force_reduce_only">force_reduce_only</option>
              <option value="force_block">force_block</option>
              <option value="force_resume">force_resume</option>
            </select>
          </label>

          <label className="field">
            <span>Reason</span>
            <textarea
              aria-label="Reason"
              value={reason}
              onChange={(event) => setReason(event.target.value)}
              placeholder="describe the operator action"
              rows={4}
            />
          </label>

          <div className="requirements-card">
            <div className="section-heading">
              <h3>Preconditions</h3>
              <p>Each item mirrors the current fixture-backed live safety contract.</p>
            </div>
            <ul className="requirements-list">
              {requirements.map((item) => (
                <li key={item.key} className={item.satisfied ? "ok" : "blocked"}>
                  <code>{item.key}</code>
                  <span>{item.satisfied ? "satisfied" : "missing"}</span>
                </li>
              ))}
            </ul>
          </div>

          <button type="submit" disabled={!canSubmit}>
            Submit Action
          </button>
        </form>

        <section className="timeline-card">
          <div className="section-heading">
            <h3>Audit Echo</h3>
            <p>Accepted actions are reflected into the shared audit timeline immediately.</p>
          </div>
          <div className="stack">
            {recentOperatorEvents.length === 0 ? (
              <p className="empty-state">No operator action has been accepted in this session yet.</p>
            ) : (
              recentOperatorEvents.map((event) => (
                <article className="timeline-card nested-card" key={event.eventId}>
                  <div className="status-row">
                    <strong>{event.eventType}</strong>
                    <span className="mono">{event.occurredAt}</span>
                  </div>
                  <p className="mono">{event.correlationId}</p>
                  <p>
                    {event.scope.venue} · {event.scope.instrumentId}
                  </p>
                </article>
              ))
            )}
          </div>
        </section>
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
      { path: "/actions", element: <ActionsPage /> },
    ],
  },
]);
