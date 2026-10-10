// Mobile navigation acceptance (Site#1509 W6): iPhone-first, any-device navigation of the WorkSpace shell is
// deterministic and device-independent. Static checks only: the page declares a responsive viewport, every nav
// button targets a section that exists, the nav handler marks the active target and scrolls to it without any
// storage or device dependency, and the stylesheet collapses the two-column shell to one fluid column at phone
// widths with tap-sized controls and no fixed-width track that can force horizontal overflow.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
const css=fs.readFileSync(path.join(root,'assets/workspace.css'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
function assert(ok,msg){if(!ok)throw new Error(msg)}

// Viewport and accessible context controls.
assert(/<meta name="viewport" content="width=device-width,initial-scale=1">/.test(page),'responsive viewport meta required');
assert(!/user-scalable=no|maximum-scale=1/.test(page),'zoom must not be disabled');
assert(/<select id="workspaceSwitch"[^>]*aria-label="Workspace context"/.test(page),'context switch must be labelled');
assert(/id="workspaceRuntimeState"[^>]*role="status"[^>]*aria-live="polite"/.test(page),'runtime state must be a live region');

// Every nav button targets an existing section id; no target is duplicated.
const targets=[...page.matchAll(/<button[^>]*data-target="([^"]+)"/g)].map(m=>m[1]);
assert(targets.length>=8,'nav must expose the shell sections: '+targets.join(','));
assert(new Set(targets).size===targets.length,'duplicate nav targets');
for(const t of targets)assert(new RegExp('id="'+t+'"').test(page),'nav target missing in page: '+t);
assert(page.indexOf('class="nav"')<page.indexOf('<main'),'nav precedes main content for keyboard and screen-reader order');

// Phone layout: single fluid column, non-sticky sidebar, fluid nav tracks, tap-sized controls.
function mediaBlock(source,prefix){const i=source.indexOf(prefix);if(i<0)return '';let depth=0,j=i+prefix.length-1;for(;j<source.length;j++){if(source[j]==='{')depth++;else if(source[j]==='}'){depth--;if(depth===0)break;}}return source.slice(i+prefix.length,j);}
const mobile=mediaBlock(css,'@media(max-width:800px){');
assert(mobile.length>0,'phone media query required');
assert(/\.shell\{grid-template-columns:minmax\(0,1fr\)\}/.test(mobile),'phone shell must be one fluid column');
assert(/\.sidebar\{[^}]*position:relative[^}]*\}/.test(mobile)&&/\.sidebar\{[^}]*min-width:0[^}]*\}/.test(mobile),'phone sidebar must flow and shrink');
assert(/\.main\{[^}]*min-width:0[^}]*\}/.test(mobile),'main must be allowed to shrink');
assert(/\.nav\{grid-template-columns:repeat\(auto-fit,minmax\(min\(100%,\d+px\),1fr\)\)\}/.test(mobile),'nav tracks must be fluid, never a fixed count that forces overflow');
assert(!/\.nav\{[^}]*repeat\(\d+,1fr\)/.test(mobile),'fixed nav column count forbidden at phone width');
const navBtn=(mobile.match(/\.nav button\{([^}]*)\}/)||[])[1]||'';
assert(/min-width:0/.test(navBtn)&&/min-height:44px/.test(navBtn)&&/white-space:normal/.test(navBtn),'nav buttons must shrink, wrap and keep a 44px tap height');
assert(/\.workspace-switch\{[^}]*min-height:44px[^}]*\}/.test(mobile),'context switch must keep a 44px tap height');
assert(/\.card,\.card\.third\{grid-column:1\/-1\}/.test(mobile),'cards must span the single column');
assert(/\*\{box-sizing:border-box\}/.test(css),'border-box sizing required for fluid widths');
assert(/\.assistant\{[^}]*overflow-wrap:anywhere[^}]*\}/.test(css)&&/\.card\{[^}]*overflow-wrap:anywhere[^}]*\}/.test(css),'long predicate and schema tokens must wrap inside cards');
assert(!/position:fixed/.test(css),'no fixed-position chrome that can hide content on small screens');

// Nav handler: marks the chosen button active, scrolls to its target, touches no storage or device identity.
const els={};const listeners={};
const mk=(id,extra)=>Object.assign({id,classList:{list:new Set(id==='home'?['active']:[]),add(c){this.list.add(c)},remove(c){this.list.delete(c)}},dataset:{target:id},addEventListener(t,f){(listeners[id]=listeners[id]||{})[t]=f},scrolled:0,scrollIntoView(){this.scrolled++},innerHTML:'',textContent:'',className:'',value:''},extra||{});
const navButtons=targets.map(t=>mk(t));
const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities'];
ids.forEach(i=>els[i]=mk(i));
const sections={};targets.forEach(t=>sections[t]=mk(t));
const bootstrap=JSON.parse(fs.readFileSync(path.join(root,'data/workspace/bootstrap.json'),'utf8'));
const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:s=>s==='.nav button'?navButtons:[],getElementById:i=>sections[i]||els[i]||null,addEventListener(){}},console,
  fetch:()=>Promise.resolve({json:()=>Promise.resolve(bootstrap)}),window:{}};
vm.createContext(ctx);vm.runInContext(ui,ctx);
(async()=>{
  await new Promise(r=>setTimeout(r,10));
  const feedBtn=navButtons.find(b=>b.dataset.target==='feedCard');
  assert(listeners.feedCard&&listeners.feedCard.click,'nav buttons must be bound');
  listeners.feedCard.click();
  assert(feedBtn.classList.list.has('active')&&!navButtons[0].classList.list.has('active'),'click must move the active marker');
  assert(sections.feedCard.scrolled===1,'click must scroll to the target section');
  // The page still renders (fail-closed) with no KV bridge, no device registration and no stored state.
  assert(/FAIL_CLOSED|NOT_OBSERVED|unavailable/i.test(els.workspaceRuntimeState.textContent+els.assistant.innerHTML),'page must render fail-closed state without a device or bridge');
  assert(!/localStorage|sessionStorage|indexedDB|navigator\.userAgent|matchMedia|screen\./.test(ui),'navigation must not depend on storage, device or user-agent state');
  console.log('WORKSPACE_MOBILE_NAVIGATION_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
