(()=>{
  const form=document.getElementById('chatForm');
  const input=document.getElementById('messageInput');
  const log=document.getElementById('chatLog');
  const mathImageInput=document.getElementById('mathImageInput');
  const mathImageName=document.getElementById('mathImageName');
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
  mathImageInput?.addEventListener('change',()=>{
    const file=mathImageInput.files?.[0]||null;
    if(mathImageName)mathImageName.textContent=file?file.name:'';
  });

  form.addEventListener('submit',async event=>{
    const message=input.value.trim();
    const mathImage=mathImageInput?.files?.[0]||null;
    if(!message&&!mathImage)return;
    const runtime=window.EcosystemRuntime||window.EcosystemVARuntime;
    if(!mathImage&&runtime?.isVA?.(message))return;
    event.preventDefault();
    if(message)append('user',message);
    if(mathImage)append('user','Math image: '+mathImage.name);
    input.value='';
    if(mathImageInput)mathImageInput.value='';
    if(mathImageName)mathImageName.textContent='';
    const pending=append('system',mathImage?'Reviewing the image…':'Thinking…');
    try{
      if(!runtime?.askGeneral)throw new Error('shared_runtime_unavailable');
      let result;
      if(mathImage){
        if(!runtime?.reviewMathImage)throw new Error('math_image_runtime_unavailable');
        result=await runtime.reviewMathImage(mathImage);
        if(message){
          result={...result,text:result.text+'\n\nYour question was not answered from the image because a mathematical transcription has not been produced or admitted yet.'};
        }
      }else{
        result=runtime?.isMath?.(message)&&runtime?.askMath
          ? await runtime.askMath(message)
          : await runtime.askGeneral(message);
      }
      pending.remove();
      const response=append('system',result.text);
      if(result.receipt){
        response.dataset.executionReceipt=result.receipt;
        response.dataset.reconstructionState=result.reconstruction_state||'';
        response.dataset.executionKind=result.model_execution===false?'deterministic-capability':'model';
      }
      if(result.attachment_hash)response.dataset.attachmentHash=result.attachment_hash;
      if(result.transcription_state)response.dataset.transcriptionState=result.transcription_state;
    }catch(_error){
      pending.remove();
      append('system',mathImage
        ? 'I could not admit that image through the governed Math intake just now. The image was not treated as mathematical source text.'
        : 'I could not complete that conversation locally just now. Please try again.');
    }
  });
})();
