// KV entry points (Site#1509; canonical task STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001, BLK1 resolved in
// .github docs/STEGVERSE_WORKSPACE_ANY_DEVICE_KV_SURFACE_MIRROR_HANDOFF.md): WorkSpace is the shell and the KV pages
// remain their own canonical entry points. The shell links to each standalone KV page and carries nothing over:
// plain same-site links with no query, fragment, target or script, so no shell state can reach the KV page and no
// KV state is copied into the shell.
const fs=require('fs');const path=require('path');
const root=path.join(__dirname,'..');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
let n=0;function check(ok,msg){n++;if(!ok)throw new Error(msg);}
const start=page.indexOf('<nav class="kv-entry" aria-label="KV entry points">');
check(start>0&&start<page.indexOf('<main'),'KV entry points are a labelled landmark in the shell, before main content');
const block=page.slice(start,page.indexOf('</nav>',start));
const links=[...block.matchAll(/<a\b([^>]*)>([^<]*)<\/a>/g)];
const hrefs=links.map(m=>(m[1].match(/href="([^"]*)"/)||[])[1]);
check(JSON.stringify(hrefs)===JSON.stringify(['my-kv.html','organizational-kv.html']),'links to the standalone MyKV and Organizational KV pages: '+hrefs);
for(const f of hrefs)check(fs.existsSync(path.join(root,f)),'linked KV page exists: '+f);
for(const m of links){
  check(/^ href="[a-z-]+\.html"$/.test(m[1]),'plain link with no query, fragment, target or handler: '+m[1]);
  check(m[2].trim().length>0,'link has visible text');
}
check(!/<script|on[a-z]+=|<form|<input|<button/i.test(block),'the entry-point block holds no script, handler, form or control');
check(/Nothing from this Workspace is carried over/.test(block)&&/grants no authority/.test(block),'the block says it carries nothing over and grants no authority');
check(!/kv-entry/.test(ui),'workspace.js does not rewrite or augment the entry-point links');
console.log('PASS workspace KV entry points ('+n+' checks)');
