from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
ORG = (ROOT / "organizational-kv.html").read_text(encoding="utf-8")


class HomepageChatTests(unittest.TestCase):
    def test_three_expected_starters_exist(self):
        for prompt in (
            "How do I use this chat?",
            "What is StegVerse?",
            "What is My KV?",
        ):
            self.assertIn(f'data-chat-prompt="{prompt}"', INDEX)
        self.assertEqual(INDEX.count("data-chat-prompt="), 3)

    def test_homepage_reuses_canonical_chat_runtime(self):
        for script in (
            "assets/semantic-command-router.js",
            "assets/ecosystem-chat-semantic-commands.js",
            "assets/ecosystem-chat-va-runtime.js",
            "assets/ecosystem-chat-simple.js",
        ):
            self.assertIn(script, INDEX)
        for element_id in ("chatForm", "messageInput", "chatLog"):
            self.assertIn(f'id="{element_id}"', INDEX)

    def test_homepage_navigation_is_kv_focused(self):
        self.assertIn('href="my-kv.html">My KV</a>', INDEX)
        self.assertIn('href="organizational-kv.html">Organizational KV</a>', INDEX)
        self.assertNotIn("Version &amp; Status", INDEX)
        self.assertNotIn("StegWallet", INDEX)
        self.assertNotIn("Thought Experiments", INDEX)

    def test_organizational_kv_is_non_authorizing(self):
        self.assertIn("NOT CONNECTED", ORG)
        self.assertIn("grants none of them", ORG)
        self.assertNotIn("CONNECTED</span>", ORG)
        self.assertNotIn('type="password"', ORG)


if __name__ == "__main__":
    unittest.main()
