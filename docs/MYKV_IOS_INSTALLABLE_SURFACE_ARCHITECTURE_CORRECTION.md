# MyKV iPhone Surface Architecture Correction

Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`

## Canonical distinction

The installable MyKV web surface is an optional owner-facing management UI. It is not the KnowledgeVault instance, not the storage host, and not the StegOS device substrate required to install or adopt a KV on an owner-selected storage endpoint.

Canonical runtime order is StegOS-first:

1. install/activate StegOS infrastructure on the current iPhone;
2. preserve or establish Node continuity and the Interlock/InTr-governed storage transition path;
3. select the KV storage host independently of KV identity;
4. install or adopt the KV on that host;
5. connect and verify the KV;
6. use MyKV as an optional management surface over the verified KV.

The device itself may be selected as a KV host. Cloud storage such as iCloud Drive or Google Drive may also be selected. Installing MyKV does not choose or create a host.

The existing `my-kv-install.html` source remains valid as a management UI and must remain non-authorizing. Runtime installation of that UI is optional and is not a prerequisite for installing StegOS infrastructure or for creating/adopting a KV through the governed storage path.
