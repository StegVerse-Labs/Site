(()=>{
  const form=document.getElementById('chatForm');
  const input=document.getElementById('messageInput');
  const log=document.getElementById('chatLog');
  if(!form||!input||!log)return;

  function append(kind,text){
    const item=document.createElement('div');item.className='chat-message '+kind;
    const body=document.createElement('div');body.className='body';body.textContent=text;
    item.appendChild(body);log.appendChild(item);log.scrollTop=log.scrollHeight;
    return item;
  }
  function usePrompt(text){input.value=text;input.focus()}

  document.querySelectorAll('[data-chat-prompt]').forEach(button=>{
    button.addEventListener('click',()=>{usePrompt(button.dataset.chatPrompt||'')});
  });

  form.addEventListener('submit',async event=>{
    const message=input.value.trim();
    if(!message)return;
    const runtime=window.EcosystemRuntime||window.EcosystemVARuntime;
    if(runtime?.isVA?.(message))return;
    event.preventDefault();
    append('user',message);input.value='';
    const pending=append('system','Thinking…');
    try{
      if(!runtime?.askGeneral)throw new Error('shared_runtime_unavailable');
      const result=runtime?.isMath?.(message)&&runtime?.askMath
        ? await runtime.askMath(message)
        : await runtime.askGeneral(message);
      pending.remove();append('system',result.text);
    }catch(_error){
      pending.remove();
      append('system','I could not complete that conversation locally just now. Please try again.');
    }
  });
})();
