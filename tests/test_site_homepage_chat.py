from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
ECOSYSTEM_CHAT = (ROOT / "ecosystem-chat.html").read_text(encoding="utf-8")
CHAT_JS = (ROOT / "assets/ecosystem-chat-simple.js").read_text(encoding="utf-8")
RUNTIME_JS = (ROOT / "assets/ecosystem-chat-va-runtime.js").read_text(encoding="utf-8")
ADMITTED_INFERENCE_JS = (ROOT / "stegos-bootstrap/admitted-inference.js").read_text(encoding="utf-8")
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

    def test_chat_surfaces_do_not_render_literal_newline_escapes(self):
        for source in (INDEX, ECOSYSTEM_CHAT):
            self.assertNotIn('</p>\\n\\n', source)
            self.assertNotIn('</script>\\n', source)

    def test_chat_surfaces_offer_bounded_node_registration(self):
        for source in (INDEX, ECOSYSTEM_CHAT):
            self.assertIn('id="node-register-device"', source)
            self.assertIn('>Register this device</button>', source)
        self.assertIn("nodeRegister?.addEventListener('click'", CHAT_JS)
        self.assertIn("nodeRegister.textContent='Check current registration'", CHAT_JS)
        self.assertIn("const current=await nodeApi.status()", CHAT_JS)
        self.assertIn("registrationRecheckConfirmedUnregistered=true", CHAT_JS)
        self.assertIn("nodeRegister.dataset.action=registrationRecheckConfirmedUnregistered?'register':'check'", CHAT_JS)
        self.assertIn('await nodeApi.registerDevice()', CHAT_JS)
        self.assertIn("if(current.registered)", CHAT_JS)

    def test_homepage_starters_are_distinct_non_model_capabilities(self):
        self.assertIn('"how do i use this chat?"', RUNTIME_JS)
        self.assertIn('"what is stegverse?"', RUNTIME_JS)
        self.assertIn('"what is my kv?"', RUNTIME_JS)
        for phrase in (
            "Use the starter questions or type what you need in your own words.",
            "StegVerse is a governed, continuity-focused ecosystem",
            "My KV is your KnowledgeVault",
        ):
            self.assertIn(phrase, RUNTIME_JS)
        self.assertIn("homepageStarterCapability(message)", RUNTIME_JS)
        self.assertIn("model_execution:false", RUNTIME_JS)
        self.assertIn("deterministic_execution:true", RUNTIME_JS)
        self.assertIn('reconstruction_state:"PASS"', RUNTIME_JS)

    def test_starter_capabilities_bypass_llm_allowance_counting(self):
        starter_index = RUNTIME_JS.index("const starter=await homepageStarterCapability(message);")
        model_index = RUNTIME_JS.index("const result=await executeDeviceRaw(generalPrompt(message),'device-general');")
        self.assertLess(starter_index, model_index)
        self.assertIn("if(nodeApi&&result?.model_execution!==false){await nodeApi.recordLlmExecution()", CHAT_JS)

    def test_local_model_completion_ceiling_is_bounded_but_not_64_tokens(self):
        self.assertIn("max_tokens: 256", ADMITTED_INFERENCE_JS)
        self.assertNotIn("max_tokens: 64", ADMITTED_INFERENCE_JS)

    def test_organizational_kv_is_non_authorizing(self):
        self.assertIn("NOT CONNECTED", ORG)
        self.assertIn("grants none of them", ORG)
        self.assertNotIn('<span class="state">CONNECTED</span>', ORG)
        self.assertNotIn('type="password"', ORG)


if __name__ == "__main__":
    unittest.main()
