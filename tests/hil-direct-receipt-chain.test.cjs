// HIL direct receiver receipts (StegVerse-Labs/.github#3106): the restored receiver Worker returns a verified
// HIL-RECEIVER-RECEIPT-v2 without an InTr receipt chain. The upload and retry pages must accept that receipt and
// record the chain as not issued, while still fully validating any chain that is present.
const fs = require('fs'); const path = require('path'); const vm = require('vm');
const root = path.join(__dirname, '..');
let n = 0; function check(ok, msg) { n++; if (!ok) throw new Error(msg); }
(async () => {
  const worker = fs.readFileSync(path.join(root, 'src/worker.js'), 'utf8');
  check(!/intr_receipt_chain/.test(worker), 'the direct receiver issues no InTr receipt chain (premise of this contract)');

  const upload = fs.readFileSync(path.join(root, 'assets/hil-direct-upload-v1.js'), 'utf8');
  const guarded = upload.match(/if \(result\.intr_receipt_chain != null\) \{([\s\S]*?)\} else \{([\s\S]*?)\}\n\s*return \{ receipt: result/);
  check(guarded, 'upload validates the chain only when one is present');
  check(/validateIntrReceiptChain\(result\.intr_receipt_chain, envelope\)/.test(guarded[1]) && /HIL_CUSTODY_TVC_INTERLOCK_ADMISSION/.test(guarded[1]), 'a present chain is still fully validated with its next transition');
  check(/intr_receipt_chain_state = 'NOT_ISSUED_BY_DIRECT_RECEIVER'/.test(guarded[2]), 'an absent chain is recorded as not issued');
  check(!/hop_receipt|receipt_hash\s*=/.test(guarded[2]), 'no hop receipts are synthesized for an absent chain');
  check((upload.match(/validateIntrReceiptChain\(/g) || []).length === 2, 'chain validation is not called unconditionally elsewhere');
  check(/EXACT_BYTES_PERSISTED/.test(upload.slice(upload.indexOf('ingress_custody_not_durable') - 200, upload.indexOf('ingress_custody_not_durable'))), 'durable custody is still required before accepting');

  const receipt = fs.readFileSync(path.join(root, 'hil-receipt.html'), 'utf8');
  check(receipt.includes("const chainState=result.intr_receipt_chain!=null?(await validateChain(result.intr_receipt_chain,intent),'VERIFIED'):'NOT_ISSUED_BY_DIRECT_RECEIVER';"), 'retry validates the chain only when present');
  check(receipt.includes('intr_receipt_chain_state:chainState,'), 'retry records the chain state on the accepted record');
  check((receipt.match(/validateChain\(/g) || []).length === 2, 'retry has no other unconditional chain validation');
  const order = ['EXACT_BYTES_PERSISTED', 'const chainState=', "location.assign('hil-accepted.html"].map(s => receipt.indexOf(s));
  check(order.every((v, i) => v > 0 && (i === 0 || v > order[i - 1])), 'retry checks custody, then the chain, before redirecting');

  // The retry validator itself is unchanged: it still rejects a malformed chain.
  const fn = receipt.match(/async function validateChain\(chain,intent\)\{[\s\S]*?return chain\}/)[0];
  const ctx = { canonical: JSON.stringify, digestJsonUri: async () => 'x' }; vm.createContext(ctx);
  vm.runInContext(fn + ';globalThis.validateChain=validateChain', ctx);
  for (const bad of [{}, { schema: 'other' }]) {
    let err = null; try { await ctx.validateChain(bad, {}); } catch (e) { err = e.message; }
    check(err === 'intr_receipt_chain_invalid', 'a present but malformed chain is still rejected');
  }
  console.log('HIL_DIRECT_RECEIPT_CHAIN=PASS checks=' + n);
})().catch(e => { console.error('HIL_DIRECT_RECEIPT_CHAIN=FAIL ' + e.message); process.exit(1); });
