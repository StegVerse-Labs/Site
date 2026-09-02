importScripts("/assets/master-records-sv002-reconstruction.js?v=20260902-2258");
self.postMessage({type:"MASTER_RECORDS_READY"});
self.onmessage=function(event){
  var m=event.data||{};
  if(m.type!=="RECONSTRUCT_SV002")return;
  Promise.resolve(self.MasterRecordsSV002BrowserReconstruction.reconstruct(m.materialization))
    .then(function(receipt){self.postMessage({type:"MASTER_RECORDS_PASS",receipt:receipt});})
    .catch(function(err){self.postMessage({type:"MASTER_RECORDS_FAIL",error:String(err&&err.message||err)});});
};