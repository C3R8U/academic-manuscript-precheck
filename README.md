# academic-manuscript-precheck
# Academic Manuscript Precheck — 论文初稿 AI 预审 Skill

可在 **OpenAI Codex** 中运行的项目级 Agent Skill。该技能以原始论文为依据开展模拟同行评审：定位原文、提出 A/B/C 级问题、评估方法及实验的可复现性、检查结果和结论的一致性，并给出最小必要修改方向。

**仅用于 AI 辅助预审；不是期刊正式同行评审。** 不会自动查证尚未提供的原始实验数据；不得编造审稿身份、论文引用、实验数值或验证结论。

## 安装与调用

该仓库内的 Skill 文件位于：

```text
.agents/skills/academic-manuscript-precheck/SKILL.md
```

在本地克隆或从 Codex 打开此仓库后，告诉 Codex：

```text
$academic-manuscript-precheck
请对我提供的论文初稿做中文 AI 学术预审。每条问题给出章节/段落原文定位、A/B/C 级别、依据和最小修改建议；检查数据泄漏、指标一致性、实验支撑和页数限制。禁止编造实验或参考文献。
```

上传论文（PDF / DOCX / Markdown / TXT），或将论文放在本地工作目录中并明确其文件位置。仅把文件推送至 GitHub 不会自动生成评审报告，仍需要在 Codex 中启动评审。

## 运行离线工具（可选）

在仓库根目录：

```bash
python -m pip install -r .agents/skills/academic-manuscript-precheck/requirements.txt
python .agents/skills/academic-manuscript-precheck/scripts/extract_manuscript.py manuscript.docx --output manuscript.source.json
```

脚本负责文本提取、证据核对和报告格式化；学术判断由 AI 助手根据 `SKILL.md` 及参考规范完成。运行帮助请参阅技能内 [README](.agents/skills/academic-manuscript-precheck/README.md)。

## 测试

```bash
python -m pip install pytest
python -m pytest -q .agents/skills/academic-manuscript-precheck/examples/test_skill.py
```

## 数据与隐私

本仓库只存放通用技能文件和虚构的测试示例。**不应将尚未发表的论文、数据集、评审报告或账号密钥上传到公开仓库。** 处理实际论文时在本地或已获授权的环境中执行。

## License

尚未指定开源许可证。如计划公开发布并允许他人复用，请自行选择许可证并添加 LICENSE 文件。
