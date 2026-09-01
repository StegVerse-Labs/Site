const fs=require('fs');const path=require('path');
const root=path.join(__dirname,'..');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
const bridge=fs.readFileSync(path.join(root,'assets/workspace-kv-bridge.js'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const claim=JSON.parse(fs.readFileSync(path.join(root,'data/session-work-claims.d/site-workspace-interoperability-20260831.json'),'utf8')).claims[0];
function has(text,value){if(!text.includes(value))throw new Error('missing '+value)}
for(const required of ['assets/stegverse-node-continuity.js','assets/generated/site-browser-intr-connectors.js','assets/hb-intr-carrier.js','stegos-node/device-kv-intr-sync.js','assets/workspace-kv-bridge.js'])has(page,required);
for(const required of ['WORKSPACE_PERSONAL_PROJECTION','Site",component:"Workspace','workspace_type:"PERSONAL','NONE_RESULT_LOOKUP_ONLY','DEVICE_KV_QUERY_RETURN','recoverSignal','workspace_grants_authority===false'])has(bridge,required);
for(const required of ['StegVerseWorkspaceKVBridge','Personal KV connected; Workspace registry is empty.','Personal KV data is never substituted for Org-KV or Org-Emp-KV.','No Workspace Assistant identity is admitted'])has(ui,required);
if(ui.includes('localStorage.getItem("stegverse.workspace.'))throw new Error('Workspace must not substitute browser localStorage for canonical KV data');
if(!claim.next_task_after_release)throw new Error('Workspace claim missing next_task_after_release');
if((claim.dependency_surface_keys||[]).includes('site:ecosystem-chat'))throw new Error('Workspace claim collides with existing Ecosystem Chat owner');
console.log('WORKSPACE_KV_BINDING_PASS');
