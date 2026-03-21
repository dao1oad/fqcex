export type VenueTradeability = {
  venue: string;
  supervisorState: "LIVE" | "DEGRADED" | "REDUCE_ONLY";
  allowOpen: boolean;
  allowReduce: boolean;
  reason: string;
};

export type InstrumentTradeability = {
  instrumentId: string;
  venue: string;
  supervisorState: string;
  allowOpen: boolean;
  allowReduce: boolean;
};

export type RecoveryRun = {
  runId: string;
  phase: string;
  status: "running" | "ready" | "blocked";
  triggerReason: string;
  blockersJson: string;
};

export type AuditEvent = {
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

export type OperatorActionName =
  | "force_reduce_only"
  | "force_block"
  | "force_resume";

export type OperatorActionTarget = {
  id: string;
  label: string;
  venue: string;
  instrumentId: string;
  supervisorState: "LIVE" | "DEGRADED" | "REDUCE_ONLY";
  allowReduce: boolean;
  recoveryReady: boolean;
  approvalRecorded: boolean;
  killSwitchInactive: boolean;
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

export const operatorActionTargets: OperatorActionTarget[] = [
  {
    id: "BYBIT:BTC-USDT-PERP",
    label: "BYBIT:BTC-USDT-PERP",
    venue: "BYBIT",
    instrumentId: "BTC-USDT-PERP",
    supervisorState: "LIVE",
    allowReduce: true,
    recoveryReady: true,
    approvalRecorded: true,
    killSwitchInactive: true,
  },
  {
    id: "BINANCE:ETH-USDT-PERP",
    label: "BINANCE:ETH-USDT-PERP",
    venue: "BINANCE",
    instrumentId: "ETH-USDT-PERP",
    supervisorState: "DEGRADED",
    allowReduce: true,
    recoveryReady: true,
    approvalRecorded: true,
    killSwitchInactive: true,
  },
  {
    id: "OKX:BTC-USDT-PERP",
    label: "OKX:BTC-USDT-PERP",
    venue: "OKX",
    instrumentId: "BTC-USDT-PERP",
    supervisorState: "REDUCE_ONLY",
    allowReduce: true,
    recoveryReady: true,
    approvalRecorded: false,
    killSwitchInactive: true,
  },
];
