# Private Stream Recovery

## Trigger

- Private user stream silent beyond threshold
- Authentication failure
- Subscription restore failure
- Reconciliation mismatch after recovery

## Automatic Response

- 立即将 venue trade mode 设置为 `REDUCE_ONLY`
- 启动恢复流程（重连私有流、恢复订阅）
- 执行订单、仓位、余额三类对账
- 在恢复完成且对账前，tradeability 必须保持 `REDUCE_ONLY`

## Recovery → Reconciliation → Tradeability

1. **恢复未完成**
   - 无论私有流是否部分恢复，只要未进入完整对账决策阶段，仍保持 `REDUCE_ONLY`
2. **对账失败**
   - 任一订单 / 仓位 / 余额存在不可解释差异，必须升级为 `BLOCKED`
   - `blocker evidence` 需记录具体差异键（如 `missing_order:*`、`mismatch_position:*`）
3. **对账通过**
   - 仍然保持 `REDUCE_ONLY`，状态为 `cooldown_pending`
   - 必须经过 cooldown 与人工复核后，才可执行 force resume
4. **不可解释差异处理**
   - 对无法解释的订单、仓位、余额差异，保持或升级为 `BLOCKED`
   - 未完成解释与审计前，不得恢复开仓

## Manual Actions

1. Verify whether order state is still explainable
2. Review reconciliation diffs
3. Keep venue in `REDUCE_ONLY` until diffs are resolved
4. Move to `BLOCKED` if order or position truth cannot be confirmed
5. 对账通过后，执行 cooldown + operator review，再评估是否 force resume

## Fault Injection Drill

私有流静默演练先生成注入计划：

```sh
py scripts/inject_private_silence.py --venue BYBIT --duration-seconds 30 --output deploy/state/private-silence.json
```

对账差异演练先生成注入计划：

```sh
py scripts/inject_reconcile_diff.py --venue BYBIT --resource position --diff-kind mismatch --instrument-id BTC-USDT-PERP --output deploy/state/reconcile-diff.json
```

操作员必须记录：

- plan 文件路径
- 进入 `REDUCE_ONLY` 的时间
- 对账差异键或差异类型
- 是否升级为 `BLOCKED`

## Escalation

- Unknown order state
- Critical position diff
- Critical balance diff
- Any unexplained order / position / balance diff remains `BLOCKED`
