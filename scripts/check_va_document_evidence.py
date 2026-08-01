#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'data/va-claim-assistant/fixtures/document-evidence-session.json'


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    bundle=json.loads(FIXTURE.read_text())
    index=bundle['document_index']; assessment=bundle['assessment']
    assert index['session_id']==assessment['session_id']
    assert not any(index['authority_flags'].values())
    assert not any(assessment['authority_flags'].values())
    docs={d['document_id']:d for d in index['documents']}
    anchors={(d['document_id'],a['anchor_id']):a for d in index['documents'] for a in d.get('page_anchors',[])}
    facts={}
    postures=set()
    for fact in assessment['facts']:
        assert fact['fact_id'] not in facts
        assert fact['document_id'] in docs
        assert (fact['document_id'],fact['anchor_id']) in anchors
        assert anchors[(fact['document_id'],fact['anchor_id'])]['page']==fact['page']
        facts[fact['fact_id']]=fact; postures.add(fact['posture'])
    assert 'FAVORABLE' in postures and ('UNFAVORABLE' in postures or 'CONFLICTING' in postures)
    for inf in assessment['inferences']:
        assert inf['supported_by'] and all(fid in facts for fid in inf['supported_by'])
    for contradiction in assessment['contradictions']:
        assert len(contradiction['fact_ids'])>=2
        assert all(fid in facts for fid in contradiction['fact_ids'])
    assert assessment['missing_evidence']
    unhashed={k:v for k,v in assessment.items() if k!='assessment_hash'}
    assert assessment['assessment_hash']==canonical_hash(unhashed)
    print(json.dumps({'result':'PASS','facts':len(facts),'contradictions':len(assessment['contradictions']),'missing_evidence':len(assessment['missing_evidence']),'assessment_hash':assessment['assessment_hash']}))

if __name__=='__main__':
    main()
