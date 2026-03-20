# Public Stream Recovery

## Trigger

- Public order book stream silent beyond threshold
- Sequence gap detected
- Checksum mismatch detected

## Automatic Response

- Set symbol tradeability to `DEGRADED` or `RESYNCING`
- Block new opens for the affected symbol
- Trigger recovery run

## Manual Actions

1. Confirm affected venue, symbol, and timestamps
2. Inspect latest recovery run and step failures
3. If repeated failures continue, set symbol or venue to `REDUCE_ONLY`
4. Escalate to `BLOCKED` if state remains unexplained

## Fault Injection Drill

在演练中，可先生成 WebSocket 断连注入计划：

```sh
py scripts/inject_ws_disconnect.py --venue BYBIT --stream public --duration-seconds 15 --instrument-id BTC-USDT-PERP --output deploy/state/ws-disconnect-public.json
```

操作员必须记录：

- 生成的 plan 文件路径
- 断连开始与结束时间
- checker signal 和 supervisor state 的变化
- 是否出现 `DEGRADED` / `RESYNCING`

## Escalation

- Three consecutive failed recoveries
- Divergence persists after successful reconnect
