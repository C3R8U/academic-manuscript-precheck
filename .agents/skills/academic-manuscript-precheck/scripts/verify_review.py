#!/usr/bin/env python3
"""Validate review JSON evidence anchors against an extracted manuscript source JSON."""
import argparse,json,re,sys
from pathlib import Path

def norm(s): return re.sub(r'\s+',' ',str(s)).strip().casefold()

def verify(source, review):
    errs=[]; warnings=[]
    blocks={b.get('block_id'):b for b in source.get('blocks',[])}
    issues=review.get('issues',[])
    if not isinstance(issues,list): return ['review.issues must be an array'],[]
    seen=set()
    for n, issue in enumerate(issues,1):
        ident=issue.get('id') or f'issue {n}'
        if ident in seen: errs.append(f'{ident}: duplicate id')
        seen.add(ident)
        if issue.get('severity') not in ('A','B','C'): errs.append(f'{ident}: severity must be A, B, C')
        key=issue.get('block_id'); quote=issue.get('evidence_quote')
        if key not in blocks: errs.append(f'{ident}: unknown/missing block_id {key!r}');continue
        if not quote: errs.append(f'{ident}: empty evidence_quote');continue
        if norm(quote) not in norm(blocks[key].get('text','')):
            errs.append(f'{ident}: evidence_quote NOT found in {key}; do not invent or paraphrase a verbatim quotation')
        if len(quote)>450:warnings.append(f'{ident}: quote is long; consider <=450 characters')
        for field in ('issue','impact','minimal_action'):
            if not str(issue.get(field,'')).strip(): errs.append(f'{ident}: missing {field}')
    if not issues:warnings.append('No issues found; check if report is intentionally empty')
    return errs,warnings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--review',type=Path,required=True)
    a=p.parse_args()
    source=json.loads(a.source.read_text(encoding='utf-8'))
    review=json.loads(a.review.read_text(encoding='utf-8'))
    errs,warn=verify(source,review)
    for w in warn: print('WARNING:',w)
    for e in errs: print('ERROR:',e,file=sys.stderr)
    print('Evidence check:', 'PASS' if not errs else 'FAIL',f'({len(review.get("issues",[]))} issues, {len(errs)} errors)')
    return 1 if errs else 0
if __name__=='__main__':raise SystemExit(main())
