# ChatGPT Session Launcher

## Purpose

`chat-session-launcher.html` provides a Site-owned browser surface that can reopen one specific existing web ChatGPT conversation for the authenticated operator.

## Supported behavior

```text
operator enters private https://chatgpt.com/c/<conversation-id> URL
-> URL is validated in the browser
-> query parameters and fragments are removed
-> normalized URL is stored in browser localStorage only
-> operator presses Open
-> browser opens the conversation in a new tab
```

## Explicit non-behavior

The launcher does not:

- commit or embed the conversation URL in the repository;
- transmit the URL to StegVerse infrastructure;
- place the conversation identifier in Site receipts, analytics, or query parameters;
- authenticate the operator to ChatGPT;
- share access to the private conversation;
- inject, prefill, or submit a prompt;
- control the opened ChatGPT page;
- claim execution, custody, continuity, admissibility, publication, or activation authority.

## Accepted URL contract

Only URLs satisfying all of the following are accepted:

```text
scheme = https
hostname = chatgpt.com OR www.chatgpt.com
path = /c/<letters, digits, underscore, or hyphen>
query = removed before storage
fragment = removed before storage
```

## Storage contract

```text
key = stegverse.chatgpt.session-launcher.v1
storage = window.localStorage
scope = current browser profile and Site origin
server persistence = none
repository persistence = none
Master-Records custody = none
```

Browser local storage is convenience state only. It is not secure credential storage and must not be treated as durable ecosystem custody.

## Operational requirement

The operator must already be signed into the ChatGPT account that owns the target conversation. A different account, signed-out browser, deleted conversation, or changed ChatGPT routing behavior may prevent access.

## Relationship to Ecosystem Chat

The launcher is a continuation convenience surface adjacent to `ecosystem-chat.html`. It does not replace the governed Ecosystem Chat gateway, provider response, custody, reconstruction, immutable receipt, activation, or downstream propagation path defined in `docs/SITE_MIRROR_HANDOFF.md`.

## Current implementation state

```text
page implemented = true
browser-local validation = true
browser-local persistence = true
private URL committed = false
prompt injection = false
Site execution authority = false
main Ecosystem Chat activation blocker changed = false
```
