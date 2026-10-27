#!/usr/bin/env python3
"""Offline DOCX/PDF/Markdown/TXT -> source blocks with stable IDs.

Does NOT generate AI judgments. Exact extracted quotes can be verified later.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

HEADING_RE = re.compile(r"^(?:[1-9]\d*(?:\.\d+)*\.?\s+|(?:abstract|introduction|conclusion|results|discussion|references|methods|摘要|引言|结论|结果|讨论|参考文献)\b)", re.I)


def squeeze(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def get_blocks(path: Path):
    suf = path.suffix.lower()
    warnings = []
    if suf == '.docx':
        try:
            from docx import Document
        except ImportError as e:
            raise RuntimeError("For DOCX: pip install python-docx") from e
        doc = Document(path)
        for index, item in enumerate(doc.iter_inner_content(), 1):
            if hasattr(item, 'rows'):
                rows = []
                for row in item.rows:
                    rows.append(' | '.join(squeeze(cell.text) for cell in row.cells))
                val = '\n'.join(r for r in rows if r.strip('| '))
                if val:
                    yield {'type': 'table', 'locator': f'table/element {index}', 'page': None, 'text': val}
            else:
                val = squeeze(item.text)
                if not val:
                    continue
                style = getattr(getattr(item,'style',None),'name','') or ''
                is_heading = bool(re.search(r'heading|标题',style,re.I) or HEADING_RE.match(val))
                yield {'type': 'heading' if is_heading else 'paragraph', 'locator': f'element {index}', 'page': None, 'text': val}
        warnings.append('DOCX does not provide reliable page numbers; use element IDs and headings. Word layout requires visual verification.')
    elif suf == '.pdf':
        try:
            import fitz
            with fitz.open(path) as doc:
                if doc.is_encrypted:
                    raise RuntimeError('Encrypted PDF: provide a readable file.')
                for pn, page in enumerate(doc, 1):
                    raw = page.get_text('blocks', sort=True)
                    found = 0
                    for b in raw:
                        if len(b) < 7 or b[6] != 0:
                            continue
                        val = squeeze(str(b[4]))
                        if not val: continue
                        found += 1
                        yield {'type': 'heading' if HEADING_RE.match(val) and len(val)<180 else 'paragraph', 'locator': f'PDF page {pn}, text block {found}', 'page':pn, 'text':val}
                    if not found:
                        warnings.append(f'PDF page {pn} had no extractable text; scan or figures may need visual review.')
        except ImportError as e:
            raise RuntimeError('For PDF: pip install PyMuPDF') from e
    elif suf in ('.md', '.txt'):
        content = path.read_text(encoding='utf-8-sig')
        if suf == '.md':
            parts = re.split(r'\n\s*\n', content)
        else:
            parts = re.split(r'\n\s*\n', content)
        for index, part in enumerate(parts, 1):
            val = squeeze(part)
            if val:
                yield {'type':'heading' if val.startswith('#') or HEADING_RE.match(val) and len(val)<160 else 'paragraph', 'locator':f'text block {index}', 'page':None, 'text':val}
    else:
        raise RuntimeError('Input must be .pdf, .docx, .txt, or .md')
    # generator return is not available to the caller, warnings assigned at top only


def extract(path: Path):
    raw = list(get_blocks(path))
    if not raw:
        raise RuntimeError('No readable text extracted. Check scanned PDF, encrypted file or empty input.')
    blocks=[]; section='Unspecified'
    for i, r in enumerate(raw,1):
        if r['type']=='heading':
            section = r['text'][:160]
        blocks.append({'block_id':f'B{i:04}', 'type':r['type'], 'section': section, 'locator':r['locator'], 'page':r['page'], 'text':r['text']})
    chars=sum(len(v['text']) for v in blocks)
    words=sum(len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*|[\u4e00-\u9fa5]",v['text'])) for v in blocks)
    pdf_pages = None
    if path.suffix.lower()=='.pdf':
        import fitz
        with fitz.open(path) as doc:pdf_pages=len(doc)
    return {'source_file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'format':path.suffix.lower().lstrip('.'), 'pdf_page_count':pdf_pages,
            'note':'For DOCX there are no reliable page numbers; for PDF visual inspection is needed for images/equations.',
            'character_count':chars,'approx_tokens_words':words,'block_count':len(blocks),'blocks':blocks}


def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('input', type=Path)
    pa.add_argument('--output','-o',type=Path,default=None)
    a=pa.parse_args()
    if not a.input.is_file(): pa.error('Input does not exist')
    try: data=extract(a.input)
    except Exception as e: print('Extraction failed:',str(e),file=sys.stderr);return 2
    out=a.output or a.input.with_suffix('.source.json')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Extracted {len(data["blocks"])} blocks from {a.input.name} => {out}')
    if data['format']=='docx': print('Note: Word page numbers are not inferred; use block IDs / headings.')
    return 0

if __name__=='__main__':raise SystemExit(main())
