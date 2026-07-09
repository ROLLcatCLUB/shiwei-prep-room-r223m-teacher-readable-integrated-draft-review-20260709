#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "R223M_teacher_readable_integrated_draft.md",
    "R223M_teacher_readable_integrated_draft.html",
    "R223M_reasoning_trace_appendix.md",
    "R223M_component_embedding_notes.md",
    "R223M_material_and_evidence_embedding_notes.md",
    "R223M_before_after_compare_with_R223L_P2.md",
    "R223M_report.md",
    "README_FOR_GPT_REVIEW.md",
    "README.md",
]

MAIN_REQUIRED = [
    "一、课时定位",
    "二、教学依据",
    "三、教学目标",
    "四、教学重难点",
    "五、教学准备",
    "六、教学过程",
    "七、评价与证据",
    "八、板书 / 大屏结构",
    "九、附：生成依据与推理链说明",
    "不是让学生随意装饰文具",
    "真实使用问题",
    "1+1 小设计",
    "1+n 文具大变身",
    "笔友汇",
    "购买文具建议书",
    "文具课堂使用指南",
]

HTML_REQUIRED = [
    "1013R_R223M_TEACHER_READABLE_INTEGRATED_DRAFT_PRODUCT",
    "data-card-wall=\"false\"",
    "《我为文具代言》：智造·新朋友",
    "课时定位",
    "教学依据",
    "教学过程",
    "评价与证据",
    "教师可读整合稿",
    "不是正式 UI",
]

APPENDIX_REQUIRED = [
    "大观念",
    "基本问题",
    "表现性任务",
    "四阶段责任",
    "本课责任",
    "活动链",
    "评价证据",
    "Teacher Confirmation Points",
]

FORBIDDEN = [
    "正式 UI 已放行",
    "formal UI approved",
    "R97B route implemented",
    "provider call enabled",
    "database write enabled",
    "R224 started",
]


def text(name):
    return (ROOT / name).read_text(encoding="utf-8")


def main():
    checks = []
    failures = []

    def check(name, passed, detail=""):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})
        if not passed:
            failures.append({"name": name, "detail": detail})

    for name in REQUIRED_FILES:
        path = ROOT / name
        check(f"required_file:{name}", path.exists(), str(path))
        if path.exists():
            check(f"non_empty:{name}", path.stat().st_size > 0, str(path.stat().st_size))

    main_md = text("R223M_teacher_readable_integrated_draft.md")
    html = text("R223M_teacher_readable_integrated_draft.html")
    appendix = text("R223M_reasoning_trace_appendix.md")
    component = text("R223M_component_embedding_notes.md")
    material = text("R223M_material_and_evidence_embedding_notes.md")
    compare = text("R223M_before_after_compare_with_R223L_P2.md")
    report = text("R223M_report.md")
    readme = text("README_FOR_GPT_REVIEW.md")

    for needle in MAIN_REQUIRED:
        check(f"main_contains:{needle}", needle in main_md)

    for needle in HTML_REQUIRED:
        check(f"html_contains:{needle}", needle in html)

    for needle in APPENDIX_REQUIRED:
        check(f"appendix_contains:{needle}", needle in appendix)

    check("main_not_card_wall_phrase", "卡片墙" not in main_md)
    check("html_declares_not_card_wall", 'data-card-wall="false"' in html)
    check("component_notes_no_tool_shelf", "tool shelf" in component and "Do not list 12 components" in component)
    check("material_notes_evidence_chain", "发现问题" in material and "后续购买建议书 / 课堂使用指南" in material)
    check("compare_records_shift", "Teacher-readable integrated draft" in compare)
    check("report_blocks_formal_ui", "formal UI" in report and "blocked" in report)

    section_count = sum(1 for marker in ["## 一、", "## 二、", "## 三、", "## 四、", "## 五、", "## 六、", "## 七、", "## 八、", "## 九、"] if marker in main_md)
    check("main_has_9_sections", section_count == 9, str(section_count))

    # The main draft should read as prose, not as a table/card artifact.
    check("main_table_count_low", main_md.count("|") <= 2, str(main_md.count("|")))
    check("html_card_class_absent", "component-card" not in html and "chain-node" not in html)

    for label, content in [
        ("main", main_md),
        ("html", html),
        ("appendix", appendix),
        ("component", component),
        ("material", material),
        ("compare", compare),
        ("report", report),
        ("readme", readme),
    ]:
        for phrase in FORBIDDEN:
            check(f"forbidden_absent:{label}:{phrase}", phrase not in content)

    screenshot = ROOT / "R223M_teacher_readable_integrated_draft_screenshot.png"
    check("screenshot_exists", screenshot.exists())
    if screenshot.exists():
        check("screenshot_non_empty", screenshot.stat().st_size > 1000, str(screenshot.stat().st_size))

    smoke_path = ROOT / "R223M_screenshot_smoke_result.json"
    if smoke_path.exists():
        try:
            smoke = json.loads(smoke_path.read_text(encoding="utf-8"))
            check("smoke_json_valid", True)
            check("smoke_no_horizontal_overflow", smoke.get("no_horizontal_overflow") is True)
            check("smoke_not_card_wall", smoke.get("card_like_count", 0) <= 3, str(smoke.get("card_like_count")))
            check("smoke_key_sections_present", smoke.get("key_sections_present") is True)
        except Exception as exc:
            check("smoke_json_valid", False, repr(exc))

    result = {
        "passed": not failures,
        "check_count": len(checks),
        "failed": len(failures),
        "failures": failures,
        "checks": checks,
    }

    out = ROOT / "validate_1013R_R223M_teacher_readable_integrated_draft_product_result.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "check_count": result["check_count"], "failed": result["failed"]}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

