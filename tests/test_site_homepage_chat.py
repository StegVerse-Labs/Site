from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
ECOSYSTEM_CHAT = (ROOT / "ecosystem-chat.html").read_text(encoding="utf-8")
CHAT_JS = (ROOT / "assets/ecosystem-chat-simple.js").read_text(encoding="utf-8")
NODE_JS = (ROOT / "assets/stegverse-node-continuity-impl.js").read_text(encoding="utf-8")
RUNTIME_JS = (ROOT / "assets/ecosystem-chat-va-runtime.js").read_text(encoding="utf-8")
SDK_CLIENT_JS = (ROOT / "assets/ecosystem-chat-sdk-client.js").read_text(encoding="utf-8")
ADMITTED_INFERENCE_JS = (ROOT / "stegos-bootstrap/admitted-inference.js").read_text(encoding="utf-8")
ORG = (ROOT / "organizational-kv.html").read_text(encoding="utf-8")
SHARED_CSS = (ROOT / "sv-shared.css").read_text(encoding="utf-8")


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

    def test_homepage_navigation_is_kv_focused_and_personal_kv_is_governed(self):
        self.assertIn('id="kv-entry-launcher"', INDEX)
        self.assertNotIn('href="my-kv.html">My KV</a>', INDEX)
        self.assertIn('assets/kv-entrypoint-intr-launcher.js', INDEX)
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
        self.assertIn("nodeRegister.hidden=true", CHAT_JS)
        self.assertIn("[hidden] { display: none !important; }", SHARED_CSS)

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

    def test_named_products_use_canonical_definition_discovery_before_model(self):
        for product_marker in (
            "canonical_product_definition_sdk",
            "canonical_product_definition_steggate",
            "canonical_product_definition_stegcore",
            "canonical_product_definition_knowledgevault",
            "StegVerse-org/StegVerse-SDK/README.md",
            "StegVerse-Labs/StegCore/README.md",
            "StegVerse-Labs/continuity-vault-kit/README.md",
        ):
            self.assertIn(product_marker, RUNTIME_JS)
        self.assertIn("canonicalProductDefinitionCapability(message)", RUNTIME_JS)
        self.assertIn('schema:"stegverse.canonical-product-definition-deterministic-execution.v1"', RUNTIME_JS)
        self.assertIn('source_grounding:"canonical_repository_contracts"', RUNTIME_JS)
        self.assertIn("model_execution:false", RUNTIME_JS)
        product_index = RUNTIME_JS.index("const productDefinition=await canonicalProductDefinitionCapability(message);")
        model_index = RUNTIME_JS.index("const result=await executeDeviceRaw(generalPrompt(message),'device-general');")
        self.assertLess(product_index, model_index)

    def test_sdk_definition_cannot_fall_through_to_generic_reference_model(self):
        self.assertIn('aliases:["sdk","stegverse sdk"]', RUNTIME_JS)
        self.assertIn("The StegVerse SDK is a public governance experiment and validation environment", RUNTIME_JS)
        product_index = RUNTIME_JS.index("const productDefinition=await canonicalProductDefinitionCapability(message);")
        deterministic_index = RUNTIME_JS.index("const deterministic=await deterministicGeneralCapability(message);")
        model_index = RUNTIME_JS.index("const result=await executeDeviceRaw(generalPrompt(message),'device-general');")
        self.assertLess(product_index, deterministic_index)
        self.assertLess(product_index, model_index)

    def test_registered_node_deterministic_invocation_emits_bound_exportable_observation(self):
        for marker in (
            "recordEcosystemChatObservation",
            "stegverse.ecosystem-chat-registered-node-observation.v1",
            "stegverse.ecosystem-chat-node-observation-commitment.v1",
            "ECOSYSTEM_CHAT_INVOCATION_OBSERVED",
            'capability: "ecosystem-chat-observation"',
            'registration_exported: false',
            'contains_credentials: false',
        ):
            self.assertIn(marker, NODE_JS)
        self.assertIn("DETERMINISTIC_CHAT_EVIDENCE_DIGEST_MISMATCH", NODE_JS)
        self.assertIn("REGISTERED_NODE_REQUIRED_FOR_CHAT_OBSERVATION", NODE_JS)
        self.assertIn("nodeApi.recordEcosystemChatObservation({message,result})", CHAT_JS)
        self.assertIn("if(current.registered)", CHAT_JS)
        self.assertIn("Export Node observation", CHAT_JS)
        self.assertIn("result?.model_execution===false&&result?.deterministic_execution===true", CHAT_JS)

    def test_starter_capabilities_bypass_llm_allowance_counting(self):
        starter_index = RUNTIME_JS.index("const starter=await homepageStarterCapability(message);")
        model_index = RUNTIME_JS.index("const result=await executeDeviceRaw(generalPrompt(message),'device-general');")
        self.assertLess(starter_index, model_index)
        self.assertIn("if(nodeApi&&result?.model_execution!==false){await nodeApi.recordLlmExecution()", CHAT_JS)

    def test_local_model_completion_ceiling_is_bounded_but_not_64_tokens(self):
        self.assertIn("max_tokens: 256", ADMITTED_INFERENCE_JS)
        self.assertNotIn("max_tokens: 64", ADMITTED_INFERENCE_JS)

    def test_weather_and_node_status_precede_reference_model(self):
        self.assertIn("const implicitCurrent=", RUNTIME_JS)
        self.assertIn("what(?:'s| is)?\\s+)?(?:the\\s+)?weather", RUNTIME_JS)
        self.assertIn("async function deviceRegistrationCapability(message)", RUNTIME_JS)
        self.assertIn("StegVerseNodeContinuity", RUNTIME_JS)
        self.assertIn("Yes. This device is registered", RUNTIME_JS)
        self.assertIn("I couldn't verify this device's Node registration state", RUNTIME_JS)
        device_index = RUNTIME_JS.index("const deviceStatus=await deviceRegistrationCapability(message);")
        weather_index = RUNTIME_JS.index("const weather=await liveWeatherCapability(message);")
        model_index = RUNTIME_JS.index("const result=await executeDeviceRaw(generalPrompt(message),'device-general');")
        self.assertLess(device_index, weather_index)
        self.assertLess(weather_index, model_index)

    def test_recognized_dynamic_status_intents_fail_closed_instead_of_model_fallback(self):
        self.assertIn("I couldn't reach the admitted live weather source just now", RUNTIME_JS)
        self.assertIn("I can't read this device's Node registration state from the current page", RUNTIME_JS)
        self.assertIn("capability:'node_registration_status'", RUNTIME_JS)
        self.assertIn("capability:'live_weather'", RUNTIME_JS)

    def test_organizational_kv_is_non_authorizing(self):
        self.assertIn("NOT CONNECTED", ORG)
        self.assertIn("grants none of them", ORG)
        self.assertNotIn('<span class="state">CONNECTED</span>', ORG)
        self.assertNotIn('type="password"', ORG)



    def test_ecosystem_chat_is_first_class_intent_separated_sdk_client(self):
        for source in (INDEX, ECOSYSTEM_CHAT):
            self.assertIn("assets/ecosystem-chat-sdk-client.js", source)
        for marker in ("EXPLAIN:'EXPLAIN'", "BUILD:'BUILD'", "VALIDATE:'VALIDATE'", "SUBMIT:'SUBMIT'", "REPORT:'REPORT'", "/api/sdk/contract", "/api/sdk/manifest/build", "/api/sdk/manifest/validate", "/api/sdk/manifest/submit", "SDK_STANDING_REQUIRED", "informational_questions_execute:false", "standing_is_never_synthesized:true"):
            self.assertIn(marker, SDK_CLIENT_JS)
        self.assertIn("async function sdkLifecycle(request)", RUNTIME_JS)
        self.assertIn("client.perform(request)", RUNTIME_JS)
        self.assertIn("public first-class conversational interface for the StegVerse ecosystem", RUNTIME_JS)

    def test_sdk_informational_stage_cannot_cross_execution_surfaces(self):
        start = SDK_CLIENT_JS.index("if(action===ACTIONS.EXPLAIN)")
        end = SDK_CLIENT_JS.index("if(action===ACTIONS.BUILD)", start)
        explain = SDK_CLIENT_JS[start:end]
        self.assertIn("execution_performed:false", explain)
        self.assertIn("sdk_crossing_performed:false", explain)
        self.assertNotIn("postSdk(", explain)
        self.assertNotIn("fetch(", explain)

    def test_sdk_submission_is_reported_as_handoff_not_runtime_result(self):
        for marker in ("result_is_a_handoff_not_a_runtime_result===true", "report_class:'SDK_MANIFEST_HANDOFF'", "runtime_result_observed:false", "HANDOFF_ONLY_DO_NOT_REPORT_RUNTIME_RESULT", "ADMITTED_RUNTIME_RESULT", "SDK_RUNTIME_DISPOSITION_REQUIRED", "REPORT_EXACT_DISPOSITION_AND_MANIFEST_REQUESTED_EVIDENCE_ONLY"):
            self.assertIn(marker, SDK_CLIENT_JS)
        self.assertIn("['ALLOW','DENY','FAIL_CLOSED']", SDK_CLIENT_JS)

    def test_sdk_client_does_not_create_authority_or_alternate_ingress(self):
        self.assertIn("authority_effect:'NONE_CLIENT_ONLY'", SDK_CLIENT_JS)
        self.assertIn("credentials:'same-origin'", SDK_CLIENT_JS)
        self.assertNotIn("/api/ecosystem-chat/sdk", SDK_CLIENT_JS)
        self.assertNotIn("Authorization", SDK_CLIENT_JS)
        self.assertNotIn("api_key", SDK_CLIENT_JS)

if __name__ == "__main__":
    unittest.main()


    def test_external_inference_session_projection_is_receipt_1_bound_and_non_authoritative(self):
        for marker in (
            "recordExternalInferenceSession",
            "stegverse.hybrid-collab.ecosystem-chat-external-inference-session/v1",
            "REGISTERED_NODE_REQUIRED_FOR_EXTERNAL_INFERENCE_OBSERVATION",
            "external inference session Receipt #1 binding mismatch",
            "comparison requires unique retained observation references",
            "ECOSYSTEM_CHAT_EXTERNAL_INFERENCE_SESSION_OBSERVED",
            "stegverse.ecosystem-chat-external-inference-node-observation.v1",
            "provider_output_grants_authority: false",
            'authority_effect: "NONE"',
        ):
            self.assertIn(marker, NODE_JS)

    def test_external_inference_projection_does_not_create_sdk_or_provider_transport(self):
        start = NODE_JS.index("function recordExternalInferenceSession")
        end = NODE_JS.index("root.StegVerseNodeContinuity", start)
        projection = NODE_JS[start:end]
        for forbidden in ("/api/sdk/", "/api/node-standing", "fetch(", "Authorization", "api_key"):
            self.assertNotIn(forbidden, projection)
