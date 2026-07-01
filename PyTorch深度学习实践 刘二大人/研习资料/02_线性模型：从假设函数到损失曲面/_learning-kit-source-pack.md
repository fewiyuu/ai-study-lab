# 02 线性模型：从假设函数到损失曲面｜source pack

## Source boundary

- Course index: `index.html`
- Current unit page: `02_线性模型：从假设函数到损失曲面/学习页.html`
- Snapshot date: `2026-06-21`
- Access date for the local course tree: `2026-06-21`
- No external web sources. Only the local course tree is in scope.

## Index alignment

- Unit role in the course map: foundation.
- The index places this unit after the course overview and before gradient descent.
- The page should make the learner able to trace: 假设函数 -> 预测 -> 残差 -> 损失 -> 损失曲面 -> 下一讲的更新方向。
- Keep the boundary clear: this unit explains why the loss surface matters and why brute-force scanning is only a teaching aid; the actual update rule belongs to the next unit.

## What the old page already covers

- Opening idea: `y_hat = wx + b` and MSE are the first concrete handles.
- Main teaching chunks:
  - linear hypothesis function
  - loss function as a single scalar
  - exhaustive search as an illustration, not the real training method
  - bias term and why it matters
  - sample count, model capacity, underfitting / overfitting
  - bridge from linear model to `nn.Linear`
- Inspectable examples already present:
  - hand-traced batch: `x=[1,2,3]`, `y=[2,4,6]`
  - parameter comparison: `w=1` vs `w=2`
  - loss formula and residual tracing
  - tiny code bridge using `for x, y in loader`, `criterion`, and `nn.Linear`
- Common mistakes already visible in the old page:
  - treating MSE like a classification metric
  - omitting the bias term
  - confusing parameter search with actual optimization
  - looking only at training loss
  - mixing up `loss.backward()` and `optimizer.step()`

## Teaching intent for the rebuild

- Make the anchor example persist across sections instead of switching examples every time.
- Let the learner inspect the same tiny data row through prediction, residual, loss, and bias.
- Add one explicit state/read-write table for the central mechanism.
- Add one formula block with symbol definitions near the formula.
- Add one short code bridge to `nn.Linear` so the page stays tied to the learner's working surface.
- Add a boundary note that points to gradient descent as the next unit, without pulling that mechanism into this unit.
- If the page is too thin after the first render, add one complete extra chain: code-reading order -> failure symptom -> repair checklist -> practice hook.
- If thickness is still short, add one more complete chain around squared error: sign cancellation -> penalty size -> alternative loss choice -> practice check.

## Anchor example

- Input row: `x=[1,2,3]`
- Target row: `y=[2,4,6]`
- Baseline parameters: `w=1`, `b=0`
- Better parameters for comparison: `w=2`, `b=0`
- Teaching use:
  - with `w=1`, the residual is visible
  - with `w=2`, the fit becomes obvious
  - with and without `b`, the learner can see the bias term's effect

## Planned output shape

- Teaching sections: 8-10
- Practice groups: 3-4
- Questions: 12-14 mixed items
- Export contexts: at least 5
- Inspectable mechanisms: at least one trace table, one code bridge, one formula block, one failure map, one boundary note
