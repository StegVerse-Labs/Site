"""Default pytest collection for Site tests."""

# test_stegmusic_browser.py is a Playwright script (no test functions) that stegmusic-browser-execution.yml
# runs directly after installing its browser; default collection must not require that framework.
collect_ignore = ["test_stegmusic_browser.py"]
