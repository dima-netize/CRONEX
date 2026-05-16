# Lumix NovaCore Architecture (Improved Draft)

## 1. Formal state view

Let:
- `x` be input token sequence,
- `M_t` be working memory at step `t`,
- `G_t` be current goal/plan graph,
- `C_t` be causal state estimator,
- `y` be candidate output.

Pipeline:

1. `h = Encoder(x)`
2. `O = ParseObjects(h)`
3. `M_0 = InitMemory(O)`
4. `G_0 = Plan(M_0, goal)`
5. iterative loop:
   - `C_t = Simulate(M_t, G_t)`
   - `y_t = Generate(M_t, G_t, C_t)`
   - `v_t = Verify(y_t, M_t, G_t, C_t)`
   - if pass: return `y_t`
   - else: `M_t+1, G_t+1 = Repair(M_t, G_t, v_t)`

## 2. Object Working Memory (OWM)

Memory cell:

```text
Cell = {
  key, type, value, provenance, confidence, ttl
}
```

Operations:
- `WRITE(cell)`
- `UPDATE(key, delta)`
- `READ(query)`
- `LINK(key_a, relation, key_b)`
- `EVICT(policy)`

Recommended policies:
- priority by `goal relevance * confidence`.
- decay by `ttl` with verifier-protected cells.

## 3. Causal World Model

Represent causal graph `K = (V, E)` where:
- `V`: states/events,
- `E`: directed effects with strength and uncertainty.

Transition:

```text
P(s_{t+1} | s_t, a_t, M_t)
```

Verifier queries model for:
- contradiction detection,
- impossible transitions,
- high-risk actions.

## 4. Planner

Use two-tier planning:
1. **Symbolic coarse planner** (task decomposition graph).
2. **Neural micro-planner** (step scoring under uncertainty).

Objective:

```text
score(plan) = success_prob - λ1*cost - λ2*risk - λ3*inconsistency
```

## 5. Verifier design

Verifier should run 4 checks:
1. **Constraint check**: satisfies explicit rules?
2. **Recompute check**: same answer via alternative path?
3. **Memory check**: answer grounded in memory cells?
4. **Causal check**: no forbidden consequence?

Decision:
- pass if all hard checks pass and confidence > threshold.
- otherwise return structured error tags for repair.

## 6. NovaCore Mini benchmark set

- `binding`
- `reverse_binding`
- `conditional_shift`
- `multi-hop tool decision`
- `code patch sanity`

Track not only final accuracy, but also:
- invalid memory writes,
- verifier catch rate,
- repeated-error frequency.

## 7. First implementation roadmap (4 weeks)

### Week 1
- Implement parser + working memory table.
- Add synthetic binding datasets.

### Week 2
- Add operation engine + shift tasks.
- Add intermediate supervision loss.

### Week 3
- Add verifier head + regenerate loop.
- Add logging of error categories.

### Week 4
- Add causal transition module + ablations.
- Compare baseline LLM head vs NovaCore loop.

## 8. Key upgrade over baseline LLM

Baseline: `x -> y`

NovaCore: `x -> objects -> memory -> causal simulation -> plan -> y -> verify -> y*`

This enforces explicit internal structure before output and should improve reliability on compositional and error-sensitive tasks.
