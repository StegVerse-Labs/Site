(function(root){
  "use strict";
  if(!root.document || root.document.readyState!=="loading") throw new Error("STEGOS_NODE_SCHEMA_BOOTSTRAP_REQUIRES_PARSER_LOAD");
  root.document.write('<script src="/assets/stegos-node-idb-schema-compat.js?v=20260911-v3"><\/script>');
  root.document.write('<script src="/stegos-bootstrap/sv001-native-resident-activation-impl.js?v=20260911-v3"><\/script>');
}(window));
