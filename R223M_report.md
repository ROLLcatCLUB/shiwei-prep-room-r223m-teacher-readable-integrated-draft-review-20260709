# R223M Report

```text
stage_id=1013R_R223M_TEACHER_READABLE_INTEGRATED_DRAFT_PRODUCT
status=READY_FOR_TEACHER_READABLE_DRAFT_REVIEW
R223L-P2 = PASS_REASONING_CHAIN_PRODUCT_VIEW_WITH_NOTES
R223M = teacher_readable_integrated_draft_product
formal_ui = blocked
R97B / UI / runtime / prompt / model / db = untouched
```

## Result

R223M converts the R223L-P2 reasoning-chain product into a teacher-readable
integrated draft. The main artifact is not a card wall. It is written as a
continuous prep draft with familiar teacher sections:

```text
课时定位
教学依据
教学目标
教学重难点
教学准备
教学过程
评价与证据
板书 / 大屏结构
附：生成依据与推理链说明
```

## Key Design Decision

The reasoning chain is no longer the visible page structure. It is internalized:

```text
大观念 -> 教学依据
基本问题 -> 本课核心问题
学生问题 -> 活动设计顺序
组件 -> 教学过程动作
素材 / 大屏 / 学习单 -> 对应环节落点
评价证据 -> 单元表现性任务连接
```

## Review Order

1. `R223M_teacher_readable_integrated_draft.html`
2. `R223M_teacher_readable_integrated_draft_screenshot.png`
3. `R223M_teacher_readable_integrated_draft.md`
4. `R223M_reasoning_trace_appendix.md`
5. Notes and validator result

## Boundary

This package does not authorize:

```text
formal UI
R97B route/component/CSS modification
frontend/backend implementation
runtime/provider/model/prompt/database
lesson body writeback
real classroom component execution
R224
formal apply
```

## Decision Options

```text
R223M = PASS_TEACHER_READABLE_INTEGRATED_DRAFT_REVIEW
R223M = HOLD_FOR_TEACHER_DRAFT_REWRITE
R223M = STOP_FORMAL_UI_NOT_READY
```

