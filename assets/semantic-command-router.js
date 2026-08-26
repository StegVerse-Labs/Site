(()=>{
  const COMMANDS={
    help:{
      label:'Help',
      summary:'Show low-language-bandwidth starting points without guessing the user\'s intent.',
      topics:['Explain something','Compare options','Find evidence','Build a timeline','Visualize a concept','VA disability help']
    },
    disability:{
      label:'Disability',
      summary:'Expose a VA disability topic neighborhood before narrowing to a specific claim intent.',
      contexts:{
        VA_CLAIMS_CHAT:{
          heading:'VA disability topics',
          topics:[
            'Disability compensation',
            'Service connection',
            'Secondary conditions',
            'Individual unemployability (TDIU)',
            'Permanent & Total (P&T)',
            'Combined disability ratings',
            'Effective dates',
            'Claims, supplemental claims, and appeals',
            'C&P examinations',
            'Evidence and medical records',
            'Dependents',
            'Special Monthly Compensation (SMC)',
            'Common VA forms',
            'Common regulations and references',
            'I do not know which topic applies'
          ],
          boundary:'Topic discovery only. No diagnosis, rating prediction, representation, filing, or private-record activation.'
        },
        ECOSYSTEM_CHAT:{
          heading:'Disability topic routes',
          topics:['VA disability claims','Accessibility and assistive communication','Disability evidence and records','Disability policy or governance','I do not know which route applies'],
          boundary:'Route discovery only. The command exposes choices before any inferred route is committed.'
        }
      }
    },
    evidence:{
      label:'Evidence',
      summary:'Expose common evidence operations before selecting one.',
      topics:['Find evidence','Organize evidence','Check provenance','Find contradictions','Find missing evidence','Build an evidence timeline']
    },
    timeline:{
      label:'Timeline',
      summary:'Expose timeline operations before selecting one.',
      topics:['Build a timeline','Inspect a timeline','Reconcile conflicting dates','Find gaps','Separate event date from later recognition']
    },
    compare:{
      label:'Compare',
      summary:'Expose comparison choices before assuming what should be compared.',
      topics:['Compare two things','Compare evidence','Compare versions','Compare timelines','Compare governance states']
    },
    explain:{
      label:'Explain',
      summary:'Let the user choose the explanation style.',
      topics:['Simple explanation','Detailed explanation','Step-by-step','Visual explanation','Analogy','Definitions and references']
    },
    visualize:{
      label:'Visualize',
      summary:'Expose recognizable visual forms instead of requiring expert prompt vocabulary.',
      topics:['Blueprint','Exploded view','Timeline','Relationship map','State transition','Handwritten explainer','X-ray/internal view','Sticky-note summary']
    }
  };

  function parse(value){
    const text=String(value||'').trim();
    const match=text.match(/^\/([a-z0-9_-]+)(?:\s+(.*))?$/i);
    if(!match)return null;
    return {name:match[1].toLowerCase(),argument:(match[2]||'').trim(),raw:text};
  }

  function resolve(value,context='ECOSYSTEM_CHAT'){
    const parsed=parse(value);if(!parsed)return null;
    const spec=COMMANDS[parsed.name];
    if(!spec)return {recognized:false,command:parsed.name,argument:parsed.argument,available:Object.keys(COMMANDS)};
    const contextual=spec.contexts&&spec.contexts[context];
    const topics=(contextual&&contextual.topics)||spec.topics||[];
    return {
      recognized:true,
      command:parsed.name,
      argument:parsed.argument,
      label:spec.label,
      heading:(contextual&&contextual.heading)||`${spec.label} choices`,
      summary:spec.summary,
      topics:[...topics],
      boundary:(contextual&&contextual.boundary)||'Discovery only; selecting a shorthand command does not itself authorize execution.',
      commit_intent:false,
      authority_effect:false,
      activation_effect:false
    };
  }

  function renderText(result){
    if(!result)return null;
    if(!result.recognized)return `I do not recognize /${result.command}. Available shortcuts:\n- /${result.available.join('\n- /')}`;
    const suffix=result.argument?`\n\nYou added: ${result.argument}\nI will not treat that as a committed intent until you choose or clarify the applicable topic.`:'';
    return `${result.heading}\n\n${result.summary}\n\n- ${result.topics.join('\n- ')}\n\nBoundary: ${result.boundary}${suffix}`;
  }

  window.StegVerseSemanticCommands={parse,resolve,renderText,commands:Object.freeze(Object.keys(COMMANDS))};
})();
