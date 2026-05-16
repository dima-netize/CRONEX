# CRONEX / Lumix NovaCore

Це **NovaCore Mini v3**: працюючий прототип із робочою пам'яттю, причинним слідом, multi-check verifier і заготовкою нового гібридного блока.

## Що вже є

- Ядро pipeline: `ObjectParser -> Planner -> OperationEngine -> Verifier`.
- Явна `WorkingMemory` + `CausalWorldModel` для відстеження наслідків дій.
- `HybridNovaBlock` (attention + state + memory router) як перший крок до “не стандартного” трансформерного ядра.
- `ErrorMemory` для накопичення verification-fail патернів.
- Розширені тести та демо.

## Швидкий запуск

```bash
python -m novacore.training.demo_run
pytest -q novacore/tests
```

## Нові ідеї для наступних ітерацій

1. Додати `repair loop`: якщо verifier fail, авто-виправлення плану і повторний прогін.
2. Розширити DSL (`UNPAIR`, `IF`, `ROLLBACK`) для складніших reason-задач.
3. Додати benchmark-таблицю: accuracy / verifier catch rate / re-run success.
4. Зробити policy head, який обирає: symbolic engine vs neural генерація.


## Що це таке і що він може

**NovaCore Mini** — це прототип AI-ядра, яке вирішує DSL-задачі не через “вгадування тексту”, а через: парсинг об'єктів, явну пам'ять, причинний слід, план виконання та перевірку перед відповіддю.

Що вміє зараз:
- виконує `STORE_COLOR`, `SHIFT`, `PAIR`, `QUERY`;
- тримає проміжні факти у `WorkingMemory`;
- веде причинний trace у `CausalWorldModel`;
- перевіряє відповідь через multi-check `Verifier`;
- повертає `trace` і `block_signal` для аналізу.

Для чого це потрібно:
- для дослідження архітектури з меншою кількістю “впевнених помилок”;
- для прозорого дебагу reasoning-проходу;
- як фундамент для майбутнього сильнішого гібридного трансформерного ядра.


## Чи наближує це до AGI?

Коротко: **так, частково наближує як дослідницький крок**, але це ще не AGI.

Чому наближує:
- є явна робоча пам'ять;
- є причинний trace;
- є verifier і retry-loop;
- є метрики якості (`accuracy`, `avg_retries`) для об'єктивного прогресу.

Чого поки бракує до AGI:
- широкого узагальнення за межами DSL;
- навчання на великих різнорідних середовищах;
- автономного довгого планування з інструментами.

Тобто це правильний напрямок: **small structured cognition first -> scale later**.


## Останній апгрейд (потужніший контур)

- Додано `RepairPolicy`: якщо програма не має базового кольору і падає на верифікації, ядро автоматично додає fallback `STORE_COLOR C0` і повторює прогін.
- `NovaCoreOutput` тепер повертає `final_program`, щоб бачити, яку саме програму виконано після авто-ремонту.
- `eval_novacore` доповнено кейсом `QUERY` без контексту, щоб вимірювати реальну користь retry + repair.


## Новий етап (learned repair + складніший DSL + інструменти)

Зроблено 3 ключові апгрейди:
- **Learned-like Repair Policy**: `LearnedRepairPolicy` з вагами дій і оновленням ваг по успіху/помилці.
- **Складніший DSL**: додано умовну гілку `IF_SHIFT_GT threshold STORE_COLOR Cx`.
- **Multi-step з інструментами**: додано `TOOL_ADD a b OUT_KEY` + `QUERY OUT_KEY` для tool-assisted планів.

Це робить ядро ближчим до реального агентного мислення: не тільки виконання правил, а адаптивна автокорекція + умовні рішення + інструментальні кроки.


## Що ще потрібно для AGI (наступні обов'язкові кроки)

Поточний NovaCore Mini вже має важливі властивості: пам'ять, verifier, branching, tool-steps, learned-like repair.
Але для реального AGI ще критично потрібно:

1. **Навчання в відкритому середовищі**: не тільки DSL, а web/code/simulation tasks.
2. **Довгий горизонт планування**: десятки/сотні кроків з відкладеними цілями.
3. **Meta-learning**: швидка адаптація до нових правил без повного донавчання.
4. **Надійна безпека**: policy constraints + fail-safe режими при невизначеності.
5. **Єдина neural+symbolic модель**: глибша інтеграція, а не тільки зв'язка модулів.

Додано скрипт `python -m novacore.training.agi_report`, який оцінює поточний рівень готовності прототипу за ключовими напрямками.


## NovaCore Next-Gen (нове ядро)

Додано новий рівень, який виходить за межі базового DSL:
- **Єдине neural-symbolic ядро**: `NeuroSymbolicCore` об'єднує нейронний сигнал і символьні факти в `fusion_score`.
- **Довші автономні плани**: `REPEAT N ...` розгортається planner-ом у long-horizon послідовності кроків.
- **Швидка адаптація**: `learn_runtime_rule(alias, canonical)` дозволяє вчити нові правила на льоту (без перевчання всієї моделі).
- **Системна безпека**: `SafetyGuard` блокує небезпечні патерни (`DELETE_ALL`, `FORMAT_DISK`, `DROP_DB`).

Це вже суттєво сильніше за базовий прототип і ближче до практичного агентного ядра.


## Ще одна сильна ідея: Governance Layer

Додано `PolicyGovernor`, який керує режимом виконання:
- `normal` — стабільний запуск;
- `cautious` — низька впевненість/забагато retries;
- `halt` — safety-порушення.

Це важливо для AGI-рівня систем: не тільки “знати відповідь”, а і **знати, коли зупинитись або перейти в безпечний режим**.

Також додано `curriculum_eval.py` для оцінки по рівнях складності (easy/medium/hard), що дає більш реалістичний трек прогресу до узагальнення.


## Next-Gen++ (не базовий, а потужний контур)

Додано ключові апгрейди для реального руху до AGI:
- **Uncertainty calibration**: калібровані довірчі інтервали `confidence_lower/upper`, а не тільки поріг fusion.
- **Hierarchical planner**: ціль -> підцілі (`setup_state`, `transform_state`, `emit_answer`) і контроль підпланів.
- **Tool sandbox policies**: інструменти дозволяються/блокуються залежно від governance-політики.
- **Continual memory pruning**: кероване забування низьковпевнених фактів через `prune(min_confidence)`.
- **Open-world eval suite**: окремий сценарій `open_world_eval.py` з code-like, web-grounded-like і safety-adversarial задачами.

### Що ще треба, щоб наблизитися до AGI ще сильніше
1. World-model з контрфактуальним симулятором дій (не тільки детерміністичні правила).
2. Lifelong learning з зовнішньою пам'яттю і перевіркою дрейфу знань.
3. Multi-agent coordination для розподілу задач і взаємної верифікації.
4. Formal safety proofs для критичних policy-модулів.
5. Реальні benchmark-и за межами synthetic DSL (код, інтернет-задачі, довгі інструментальні workflow).


## Ultra Next-Gen (AGI-oriented core)

Нові небазові компоненти:
- **Контрфактуальний world-model**: модуль `CounterfactualWorldModel` оцінює ризик дій до виконання.
- **Lifelong adaptation + drift control**: `LifelongAdapter` веде статистику успіх/помилка і рахує `drift_score`.
- **Multi-agent self-critique**: два критики голосують за валідність фінальної відповіді.
- **Формальна safety-верифікація**: `FormalSafetyVerifier` перевіряє інваріанти та повертає proof-trace.
- **Реалістичніший open-world benchmark**: `open_world_realistic_eval.py` з code/web/safety сценаріями.

### Що ще потрібно для повноцінного AGI
1. Справжня multimodal grounding (текст+код+візія+дії в середовищі).
2. Довготривала пам'ять зі стислим реплеєм і causal credit assignment.
3. Механізм власного створення інструментів і перевірки їхньої коректності.
4. Автономне планування на горизонті тисяч кроків із гарантіями безпеки.
5. Науково валідовані external benchmarks проти state-of-the-art систем.


## AGI Delta++ (наступний потужний рівень)

Реалізовано нові контури:
- **Multimodal grounding scaffold**: `MultimodalGrounder` (текст/візуальні/tool сигнали в одному контексті).
- **Long-horizon control**: `LongHorizonController` з step-budget guard для сотень/тисяч кроків.
- **Policy-level formal guarantees**: `PolicyFormalGuarantee` для формальної перевірки інструментальних політик.
- **External SOTA benchmark roadmap**: `sota_bench.py` + `sota_benchmark_plan.py` (SWE-bench/MMLU-like/Agent-safety proxy).

### Що ще треба для повноцінного AGI
1. Реальний мультимодальний агент у середовищі (візія+мовлення+дії в realtime).
2. Самонавчання з довгим горизонтом і доказовим safety-shield.
3. Онлайновий causal discovery (оновлення world-model з нових спостережень).
4. Економіка інструментів: вибір, валідація, самостворення і self-debug tools.
5. Порівняння із SOTA на публічних бенчмарках із відтворюваними протоколами.


## Поточний рівень системи

Додано `full_system_report.py`, який збирає єдиний звіт:
- task accuracy
- avg retries
- AGI readiness
- maturity level (`L1..L5`)

На поточному етапі система зазвичай потрапляє в **L4-Pre-AGI**: сильний агентний каркас із safety/governance/neuro-symbolic контуром, але ще без універсального open-world узагальнення.


## AGI Omega Upgrade (реально потужний контур)

Додано небазові компоненти наступного рівня:
- **Multimodal online-agent**: `MultimodalOnlineAgent` для онлайн-циклу observe->act.
- **Long-horizon ready execution**: горизонти контролюються budget-механізмом у runtime.
- **Self-learning + controlled forgetting**: `SelfLearningController` з bounded decay.
- **Formal toolchain safety**: `ToolchainSafetyVerifier` перевіряє обов'язкові правила безпеки (`sandbox_enabled`, `policy_checked`, `audit_log`).
- **Reproducible SOTA-style benchmark protocol**: `repro_benchmark.py` з фіксованим seed і JSON-звітом.

### Що ще треба до повноцінного AGI
1. Реальні інтеграції з live web/tools/vision stack.
2. Незалежна external валідація результатів на публічних SOTA benchmark-ах.
3. Self-improving objective з формальними safety-обмеженнями.
4. Multi-agent collaboration + adversarial red-team loops.
5. Відтворювані наукові протоколи (seeded runs, ablations, confidence stats, peer review).


## L5 Upgrade Program (experimental)

Щоб перейти з L4 до L5-кандидата, додано реальні внутрішні гейти:
- Відтворюваний зовнішній benchmark-протокол (`ExternalBenchmarkProtocol`): seed, coverage, safety-coverage.
- Long-horizon автономний сценарій (`autonomous_mission.py`) на сотні кроків.
- L5 upgrade report (`l5_upgrade_report.py`) із формальними критеріями переходу в `L5-Candidate-Experimental`.

> Важливо: це **внутрішній експериментальний L5-candidate**, не фінальна наукова гарантія AGI.


## Hardening Upgrade (accuracy/robustness/stability)

Зроблено посилення під реальні вимоги:
- `open_world_hard_eval.py`: складніші open-world сценарії + метрики accuracy/safety_coverage.
- `repro_stability.py`: багатократний відтворюваний прогін (5 повторів з одним seed) для перевірки стабільності.
- `public_sota_protocol_status.py`: чесний статус інтеграції публічних SOTA протоколів (без фейкових claim-ів).
- Піднято безпечний ліміт довжини програми у `SafetyGuard` для long-horizon місій.


## Public SOTA Integration (non-proxy path)

Додано реальний шлях інтеграції зовнішніх протоколів:
- `public_sota.py`: runner, який читає JSONL кейси з зовнішніх наборів.
- `public_sota_run.py`: запуск SWE-bench / MMLU / AgentSafety через зовнішні файли (`external/*.jsonl` або ENV).
- Якщо датасетів немає — статус `UNAVAILABLE` (чесно), без фейкових метрик.

У hard open-world оцінці додано `task_success_rate`, де safety-halt у adversarial кейсах рахується як правильний успіх політики.


## External JSONL hooked (real run path)

Підключено фактичні JSONL-файли в `external/`:
- `external/swe_bench.jsonl`
- `external/mmlu.jsonl`
- `external/agent_safety.jsonl`

`public_sota_run.py` тепер дає не тільки per-suite вивід, а і агрегований JSON summary (`aggregate_rate`, total passed/total).
За потреби шляхи можна перевизначати через ENV:
- `SWE_BENCH_JSONL`
- `MMLU_JSONL`
- `AGENT_SAFETY_JSONL`


## AGI Sprint Execution Update

Додано production-like артефакти:
- `external/*.jsonl` розширено до 30 кейсів на suite.
- `training/long_horizon_1000.py` для 500/1000/1500-крокових місій з метриками completion/safety/cost.
- `training/leaderboard_report.py` + `leaderboard.json` для історії по комітах.
- `ExperienceReplayStore` для lifelong replay та контролю forgetting.
- `tests/test_regression_guard.py` як quality-гард від регресій.


## Advanced AGI Track Upgrades

Додано:
- `hard_error_mining.py` для збору top-типів помилок на hard open-world.
- Weighted scoring у `Verifier` (каузальність/узгодженість/trace мають різну вагу).
- `long_horizon_stress.py` (100 запусків × 500/1000/1500) з auto-fail gate `completion_rate >= 0.9`.
- Priority replay в `ExperienceReplayStore` + `weighted_success_rate`.
- `forgetting_audit.py` з gate деградації не більше 2%.
- `protocol_export.py` для artifact bundle (seed, commit, config, outputs).
- Розширені machine-checkable safety invariants (tool preconditions, postconditions, forbidden transitions).
- Safety red-team suite на 100 adversarial кейсів.


## L5 Gate Dashboard (production-style)

Додано `training/l5_gate_dashboard.py`, який рахує єдиний L5 gate status:
- raw_accuracy_hard
- task_success_rate_hard
- long_horizon_completion
- safety_coverage
- forgetting_degradation
- reproducibility_20x
- public_sota_aggregate

Результат пишеться в `artifacts/l5_gate_status.json` і показує, чи виконується умова `l5_candidate`.
