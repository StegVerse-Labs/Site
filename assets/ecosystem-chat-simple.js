(()=>{
  const form=document.getElementById('chatForm');
  const input=document.getElementById('messageInput');
  const log=document.getElementById('chatLog');
  if(!form||!input||!log)return;

  function append(kind,text){
    const item=document.createElement('div');item.className='chat-message '+kind;
    const body=document.createElement('div');body.className='body';body.textContent=text;
    item.appendChild(body);log.appendChild(item);log.scrollTop=log.scrollHeight;
  }
  function usePrompt(text){input.value=text;input.focus()}

  document.querySelectorAll('[data-chat-prompt]').forEach(button=>{
    button.addEventListener('click',()=>{usePrompt(button.dataset.chatPrompt||'')});
  });

  form.addEventListener('submit',event=>{
    const message=input.value.trim();
    if(!message)return;
    if(window.EcosystemVARuntime?.isVA?.(message))return;
    event.preventDefault();
    append('user',message);input.value='';
    append('system','I can currently give live conversational help with VA benefits and claims here. For another StegVerse service, tell me what you are trying to do and I’ll point you to the simplest available path.');
  });
})();
