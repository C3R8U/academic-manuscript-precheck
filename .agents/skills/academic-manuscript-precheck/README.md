# Academic Manuscript Precheck Skill｜论文初稿 AI 预审

这是一个符合 [Agent Skills](https://agentskills.io/specification) 目录规范的可移植 Skill。它让支持 Skills 的 AI 助手按照一致的学术审稿流程，检查**论文初稿**并生成有原文依据的模拟评审报告。并非期刊官方审稿系统。

## 特色
- 提交前评审：问题定位到章节、PDF页码或 DOCX 段落索引（不虚构 Word 页码）。
- 以证据为中心：每条 A/B/C 问题包含原文短摘录、科学影响和最小修改建议。
- 重视实验：数据来源、数据泄漏、对比实验、消融、复现参数、统计和引用。
- 重视稿件长度：可按期刊格式约束检查冗余，并保留核心实验。
- 区分初稿预审与修订后复审；拒绝编造实验结果、p值、DOI 和外部审稿身份。

## 安装

**Codex 项目内**：将整个目录复制至 `<项目根目录>/.agents/skills/academic-manuscript-precheck/`，随后在 Codex 中输入 `$academic-manuscript-precheck` 或用自然语言指定。

**Claude Code 项目内**：将目录放入 `<项目根目录>/.claude/skills/academic-manuscript-precheck/`，调用具体方式参照客户端版本。

**ChatGPT**：按 [ChatGPT 官方 Build skills](https://learn.chatgpt.com/docs/build-skills) 在具备技能创建/导入能力的 ChatGPT Work 或桌面环境中使用 `@skill-creator`，或把 `SKILL.md` 内容作为当前任务的审稿规范使用。**单纯把 ZIP 放到 GitHub 不会自动安装到聊天。**

**GitHub**：创建普通仓库（公开或私有），上传整个技能文件夹；对于未投稿论文建议使用私有仓库。上传不等于云端自动运行，运行仍需要支持 Skills 的 AI agent，或另建 GitHub Action / 服务端。

## 使用
直接对支持 Skill 的助手说：

> 请使用 academic-manuscript-precheck，对我上传的原始初稿进行一次严格的中文 AI 学术预审。每条问题标注具体位置、原文依据、严重级别、影响和最小修改方向。重点检查方法、数据泄漏、实验结果、引文与12页单栏限制，不要虚构任何实验结果。

## 可选离线工具
```
python -m pip install -r requirements.txt
python scripts/extract_manuscript.py manuscript.docx --output manuscript.source.json
# 将 manuscript.source.json 和技能规范交给 AI 审稿，输出 review.json
python scripts/verify_review.py --source manuscript.source.json --review review.json
python scripts/render_review.py --source manuscript.source.json --review review.json --output AI_pre_review.md
```

支持 `.pdf`、`.docx`、`.md`、`.txt`。脚本只做文本提取、引文锚点核对、报告格式化；**不会自行调用AI模型**。评审由加载 `SKILL.md` 的 AI 助手完成。PDF 图片、扫描文字和复杂公式需要视觉检查。不要将未公开论文、隐私材料未经许可推送到公有 GitHub 或联网服务。

## 目录
```
academic-manuscript-precheck/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── extract_manuscript.py
│   ├── verify_review.py
│   └── render_review.py
├── references/
│   ├── review-checklist.md
│   └── evidence-policy.md
└── assets/
    ├── review-report-template.md
    └── review-report-example.json
```

## 责任与限制
报告仅为AI辅助预审。引文存在性、原始实验、伦理审批、第三方数据权限等需要独立核验。审稿结论不等于真实发表决定；检测不到的PDF公式和图像应如实标记。
