#!/usr/bin/env python3
"""Render an evidence-anchored review JSON as a Markdown report. Does not call an LLM."""
from pathlib import Path
import json,argparse

def safe(text): return str(text or '').replace('|','\\|')

def render(r,src):
    m={b['block_id']:b for b in src['blocks']}
    l=[f'# 论文初稿AI预审报告（非正式期刊审稿）', '', f'**标题：** {r.get("title", "未提供")}',
       f'**来源：** {src.get("source_file", "未提供")}', f'**阅读范围：** {r.get("scope", "稿件可提取文字")}',
       f'**PDF页数：** {src.get("pdf_page_count") or "不适用/未知"}；**文本块数：** {src.get("block_count")}',
       '', '## 整体评价','',r.get('summary','未填写'),'']
    issues=r.get('issues',[])
    for sev,label in [('A','主要问题（A）'),('B','重要问题（B）'),('C','次要问题（C）')]:
        s=[i for i in issues if i.get('severity')==sev]
        if not s: continue
        l.extend([f'## {label}',''])
        for i in s:
            block=m.get(i.get('block_id'),{})
            l.extend([f'### {i.get("id", "")}. {i.get("category", "具体问题")}',
                f'- **位置：** {i.get("block_id", "")}；{block.get("section", "")}；{block.get("locator", "")}',
                f'- **原文依据：** {i.get("evidence_quote", "")}',
                f'- **问题：** {i.get("issue", "")}',f'- **影响：** {i.get("impact", "")}',
                f'- **最小修改建议：** {i.get("minimal_action", "")}', ''])
    weights=[('contribution','研究贡献与定位',20),('methods','方法可靠性',25),('evidence','实验证据',25),('coherence','论证结构',15),('writing','语言与报告规范',15)]
    d=r.get('dimensions',{})
    if d:
        l.extend(['## 维度评分（仅供诊断，不代表录用概率）','','| 维度 | 权重 | 1—5分 |','|---|---:|---:|'])
        for key,name,w in weights:l.append(f'| {name} | {w}% | {safe(d.get(key,"未评价"))} |')
        l.append('')
    l.extend(['## 篇幅与修改顺序','',r.get('length_note','未指定投稿字数或页数标准。'),'','### 优先行动'])
    for a in r.get('priority_actions',[]):l.append('- '+str(a))
    l.extend(['','---','**性质说明：** 该报告为AI辅助的学术预审，不是正式编辑决定、匿名专家审稿或原始实验结果的独立验证。',''])
    return '\n'.join(l)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--review',required=True,type=Path)
    p.add_argument('--output','-o',type=Path,required=True)
    a=p.parse_args()
    src=json.loads(a.source.read_text(encoding='utf-8'))
    rev=json.loads(a.review.read_text(encoding='utf-8'))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(render(rev,src),encoding='utf-8')
    print('Created',a.output)
if __name__=='__main__':main()
