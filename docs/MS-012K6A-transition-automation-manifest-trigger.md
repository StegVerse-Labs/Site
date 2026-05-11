# MS-012K.6A Transition Automation Manifest Trigger

This bundle intentionally exists to trigger the installed transition automation controller through `bundle-manifest.json`.

```text
post_install_tasks:
  - data/headless-tasks/transition-automation-controller-v1.json
```

It contains no workflow files and no execution logic.
