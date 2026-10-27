import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_offline_pipeline(tmp_path):
    manuscript=ROOT/'examples'/'fictional-manuscript.md'
    out=tmp_path/'source.json'
    subprocess.run([sys.executable,str(ROOT/'scripts'/'extract_manuscript.py'),str(manuscript),'--output',str(out)],check=True)
    doc=json.loads(out.read_text())
    assert doc['block_count']>=4
    review=json.loads((ROOT/'assets'/'review-report-example.json').read_text())
    match=[b['block_id'] for b in doc['blocks'] if 'The dataset includes 200 samples.' in b['text']]
    assert match
    review['issues'][0]['block_id']=match[0]
    reviewfile=tmp_path/'review.json'
    reviewfile.write_text(json.dumps(review),encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'scripts'/'verify_review.py'),'--source',str(out),'--review',str(reviewfile)],check=True)
    report=tmp_path/'review.md'
    subprocess.run([sys.executable,str(ROOT/'scripts'/'render_review.py'),'--source',str(out),'--review',str(reviewfile),'--output',str(report)],check=True)
    assert 'A1' in report.read_text()
