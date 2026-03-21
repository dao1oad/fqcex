type VenueTradeability = {
  venue: string;
  supervisorState: "LIVE" | "DEGRADED" | "REDUCE_ONLY";
  allowOpen: boolean;
  allowReduce: boolean;
  reason: string;
};

type InstrumentTradeability = {
  instrumentId: string;
  venue: string;
  supervisorState: string;
  allowOpen: boolean;
  allowReduce: boolean;
};

type RecoveryRun = {
  runId: string;
  phase: string;
  status: "running" | "ready" | "blocked";
  triggerReason: string;
  blockersJson: string;
};

type AuditEvent = {
  eventId: string;
  eventType: string;
  occurredAt: string;
  sourceComponent: string;
  correlationId: string;
  scope: {
    venue: string;
    instrumentId?: string;
  };
};

export const venueTradeability: VenueTradeability[] = [
  {
    venue: "BYBIT",
    supervisorState: "LIVE",
    allowOpen: true,
    allowReduce: true,
    reason: "streams healthy and reconciliation green",
  },
  {
    venue: "BINANCE",
    supervisorState: "DEGRADED",
    allowOpen: true,
    allowReduce: true,
    reason: "public stream recovered, observation window still active",
  },
  {
    venue: "OKX",
    supervisorState: "REDUCE_ONLY",
    allowOpen: false,
    allowReduce: true,
    reason: "kill switch approval required before live canary",
  },
];

export const instrumentTradeability: InstrumentTradeability[] = [
  {
    instrumentId: "BTC-USDT-PERP",
    venue: "BYBIT",
    supervisorState: "LIVE",
    allowOpen: true,
    allowReduce: true,
  },
  {
    instrumentId: "ETH-USDT-PERP",
    venue: "BINANCE",
    supervisorState: "DEGRADED",
    allowOpen: true,
    allowReduce: true,
  },
  {
    instrumentId: "BTC-USDT-PERP",
    venue: "OKX",
    supervisorState: "REDUCE_ONLY",
    allowOpen: false,
    allowReduce: true,
  },
];

export const recoveryRuns: RecoveryRun[] = [
  {
    runId: "run-bybit-20260321-01",
    phase: "reconciling balances",
    status: "ready",
    triggerReason: "manual canary checkpoint",
    blockersJson: "[]",
  },
  {
    runId: "run-okx-20260321-02",
    phase: "rechecking private stream",
    status: "running",
    triggerReason: "kill switch review window",
    blockersJson: "[\"awaiting operator approval\"]",
  },
];

export const auditEvents: AuditEvent[] = [
  {
    eventId: "audit-201",
    eventType: "approve_live_canary",
    occurredAt: "2026-03-21T07:15:00Z",
    sourceComponent: "control-plane",
    correlationId: "corr-live-001",
    scope: {
      venue: "BYBIT",
      instrumentId: "BTC-USDT-PERP",
    },
  },
  {
    eventId: "audit-202",
    eventType: "recovery_completed",
    occurredAt: "2026-03-21T07:28:00Z",
    sourceComponent: "supervisor",
    correlationId: "corr-live-001",
    scope: {
      venue: "BYBIT",
    },
  },
  {
    eventId: "audit-203",
    eventType: "approve_live_canary",
    occurredAt: "2026-03-21T08:05:00Z",
    sourceComponent: "control-plane",
    correlationId: "corr-live-002",
    scope: {
      venue: "OKX",
      instrumentId: "ETH-USDT-PERP",
    },
  },
];
