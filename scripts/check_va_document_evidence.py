#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'data/va-claim-assistant/fixtures/document-evidence-session.json'
AWARENESS_FIXTURE=ROOT/'data/va-claim-assistant/fixtures/veteran-record-awareness-session.json'


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def validate_awareness():
    awareness=json.loads(AWARENESS_FIXTURE.read_text())
    assert awareness['scope']=='VETERAN_RECORD_AWARENESS'
    assert awareness['findings']
    assert not any(awareness['authority_flags'].values())
    boundary=awareness['claim_boundary']
    assert boundary['automatically_include_in_claim'] is False
    assert boundary['requires_separate_relevance_determination'] is True
    assert boundary['veteran_controls_escalation'] is True
    ids=set()
    for finding in awareness['findings']:
        assert finding['finding_id'] not in ids
        ids.add(finding['finding_id'])
        assert finding['evidence_refs']
        assert finding['observed_facts']
        assert finding['claim_relevance'] in {'NOT_EVALUATED','NOT_RELEVANT','POTENTIALLY_RELEVANT','RELEVANT'}
        assert finding['veteran_action']
    unhashed={k:v for k,v in awareness.items() if k!='awareness_hash'}
    assert awareness['awareness_hash']==canonical_hash(unhashed)
    return {'findings':len(ids),'awareness_hash':awareness['awareness_hash'],'claim_auto_include':False}


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
    awareness=validate_awareness()
    print(json.dumps({'result':'PASS','facts':len(facts),'contradictions':len(assessment['contradictions']),'missing_evidence':len(assessment['missing_evidence']),'assessment_hash':assessment['assessment_hash'],'veteran_record_awareness':awareness}))

if __name__=='__main__':
    main()
