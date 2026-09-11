(function(root){
  "use strict";

  var DB_NAME="stegos-node-v1";
  var CANONICAL_VERSION=3;
  var STORES=Object.freeze({
    meta:{keyPath:"key"},
    receipts:{keyPath:"receipt_number"},
    intr_outbox:{keyPath:"materialization_id"}
  });

  function fail(message){throw new Error("STEGOS_NODE_IDB_SCHEMA_COMPAT: "+message);}
  function ensureStore(db,name,options){
    if(!db.objectStoreNames.contains(name)) db.createObjectStore(name,options);
  }
  function ensureCanonicalStores(db){
    Object.keys(STORES).forEach(function(name){ensureStore(db,name,STORES[name]);});
  }

  if(!root||!root.indexedDB||!root.IDBFactory||!root.IDBFactory.prototype) fail("IndexedDB unavailable");
  var proto=root.IDBFactory.prototype;
  var nativeOpen=proto.open;
  if(typeof nativeOpen!=="function") fail("IDBFactory.open unavailable");
  if(nativeOpen.__stegverseNodeSchemaCompat===true){
    root.StegVerseNodeDbSchemaCompatState=Object.freeze({schema:"stegverse.site.node-idb-schema-compat/v1",database:DB_NAME,canonical_version:CANONICAL_VERSION,installed:true,already_installed:true,authority_effect:"NONE_STORAGE_COMPAT_ONLY"});
    return;
  }

  function compatibleOpen(name,version){
    var args=Array.prototype.slice.call(arguments);
    var isNodeDb=String(name)===DB_NAME;
    if(!isNodeDb) return nativeOpen.apply(this,args);

    var requested=(version===undefined||version===null)?CANONICAL_VERSION:Number(version);
    if(!Number.isInteger(requested)||requested<1) return nativeOpen.apply(this,args);
    var effective=Math.max(requested,CANONICAL_VERSION);
    var request=nativeOpen.call(this,name,effective);
    request.addEventListener("upgradeneeded",function(){ensureCanonicalStores(request.result);});
    return request;
  }
  Object.defineProperty(compatibleOpen,"__stegverseNodeSchemaCompat",{value:true});
  Object.defineProperty(compatibleOpen,"__stegverseNodeSchemaNativeOpen",{value:nativeOpen});
  proto.open=compatibleOpen;
  if(proto.open!==compatibleOpen) fail("IDBFactory.open compatibility hook unavailable");

  root.StegVerseNodeDbSchemaCompatState=Object.freeze({
    schema:"stegverse.site.node-idb-schema-compat/v1",
    database:DB_NAME,
    canonical_version:CANONICAL_VERSION,
    required_stores:Object.keys(STORES),
    migration_mode:"ADDITIVE_VERSION_UPGRADE_ONLY",
    deletes_database:false,
    deletes_store:false,
    preserves_existing_rows:true,
    installed:true,
    authority_effect:"NONE_STORAGE_COMPAT_ONLY"
  });
}(window));
