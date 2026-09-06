#!/usr/bin/env python3
from pathlib import Path
import base64
import hashlib
import re
import zlib

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "news-releases.html"
ARTICLE = ROOT / "news-releases" / "ai-is-becoming-infrastructure-sovereignty-must-go-further.html"
COHERENT_LIFE = ROOT / "papers" / "coherent-life-and-admissible-existence" / "index.html"
COHERENT_LIFE_ARTIFACT = ROOT / "papers" / "coherent-life-and-admissible-existence" / "artifact" / "index.html"
COHERENT_LIFE_ARTIFACT_DIR = COHERENT_LIFE_ARTIFACT.parent
COMPANION = ROOT / "papers" / "coherent-life-companion" / "index.html"
EMPIRICAL_ADDENDUM = ROOT / "papers" / "coherent-life-and-admissible-existence" / "empirical-addendum-i.html"
ENTITY_ECONOMY = ROOT / "papers" / "stegverse-entity-economy" / "index.html"
ENTITY_ECONOMY_PDF = ROOT / "papers" / "stegverse-entity-economy" / "stegverse-entity-economy.pdf"
ENTITY_ECONOMY_VOLUME_II_ARTIFACT = ROOT / "papers" / "stegverse-entity-economy-volume-ii" / "artifact" / "index.html"
ENTITY_ECONOMY_VOLUME_II_ARTIFACT_DIR = ENTITY_ECONOMY_VOLUME_II_ARTIFACT.parent
DISCOVERY = ROOT / "Papers.html"

PARENT_TITLE = "Coherent Life and Admissible Existence"
COMPANION_TITLE = "Coherent Life and Admissible Existence — Companion Extensions"
ADDENDUM_TITLE = "Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary"
ENTITY_TITLE = "The StegVerse Entity Economy"
SOUTH_KOREA_TITLE = "AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model."
PARENT_ROUTE = 'href="papers/coherent-life-and-admissible-existence/"'
COMPANION_ROUTE = 'href="papers/coherent-life-companion/"'
ADDENDUM_ROUTE = 'href="papers/coherent-life-and-admissible-existence/empirical-addendum-i.html"'
ARTIFACT_PARTS = [f"coherent-life-36-page.part{i:02d}.b64" for i in range(9)]
APPROVED_ARTIFACT_SHA256 = "6afed983e236b260718df548f40cac2e1a8c12cd9c8f82a28c7a5f757eefe918"
APPROVED_ARTIFACT_BYTES = 413092
VOLUME_II_PREFIX_PARTS = [f"volume-ii.part{i:02d}.b64" for i in range(17)]
VOLUME_II_COMPRESSED_TAIL = "volume-ii.tail-after-part16.deflate"
VOLUME_II_COMPRESSED_TAIL_GIT_BLOB_SHA = "aaa5cd39648f065c3f3ed52c9eabdf66b7a3d8b6"
VOLUME_II_SHA256 = "129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f"
VOLUME_II_BYTES = 132330


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def reconstruct_base64_parts(directory: Path, parts: list[str], failures: list[str], label: str) -> bytes | None:
    encoded = []
    for part in parts:
        path = directory / part
        if not path.exists():
            failures.append(f"missing {label} part: {part}")
            return None
        encoded.append(re.sub(r"\s+", "", path.read_text(encoding="utf-8")))
    try:
        return base64.b64decode("".join(encoded), validate=True)
    except Exception as exc:
        failures.append(f"{label} base64 reconstruction failed: {exc}")
        return None


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main():
    failures = []
    volume_ii_tail_path = ENTITY_ECONOMY_VOLUME_II_ARTIFACT_DIR / VOLUME_II_COMPRESSED_TAIL
    required_files = [
        (INDEX, "missing news-releases.html"),
        (ARTICLE, "missing inaugural news release"),
        (COHERENT_LIFE, "missing Coherent Life working-paper projection"),
        (COHERENT_LIFE_ARTIFACT, "missing complete Coherent Life 36-page artifact loader"),
        (COMPANION, "missing Coherent Life attached companion projection"),
        (EMPIRICAL_ADDENDUM, "missing legacy Empirical Addendum I deep-link projection"),
        (ENTITY_ECONOMY, "missing Entity Economy paper landing page"),
        (ENTITY_ECONOMY_PDF, "missing Entity Economy PDF"),
        (ENTITY_ECONOMY_VOLUME_II_ARTIFACT, "missing Entity Economy Volume II artifact loader"),
        (volume_ii_tail_path, "missing Entity Economy Volume II compressed canonical tail"),
        (DISCOVERY, "missing Papers.html discovery surface"),
    ]
    required_files.extend((COHERENT_LIFE_ARTIFACT_DIR / part, f"missing Coherent Life artifact part: {part}") for part in ARTIFACT_PARTS)
    required_files.extend((ENTITY_ECONOMY_VOLUME_II_ARTIFACT_DIR / part, f"missing Entity Economy Volume II prefix part: {part}") for part in VOLUME_II_PREFIX_PARTS)
    for path, message in required_files:
        require(path.exists(), message, failures)
    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for failure in failures:
            print(failure)
        return 1

    index = INDEX.read_text(encoding="utf-8")
    article = ARTICLE.read_text(encoding="utf-8")
    coherent_life = COHERENT_LIFE.read_text(encoding="utf-8")
    artifact = COHERENT_LIFE_ARTIFACT.read_text(encoding="utf-8")
    companion = COMPANION.read_text(encoding="utf-8")
    addendum = EMPIRICAL_ADDENDUM.read_text(encoding="utf-8")
    entity = ENTITY_ECONOMY.read_text(encoding="utf-8")
    volume_ii_artifact = ENTITY_ECONOMY_VOLUME_II_ARTIFACT.read_text(encoding="utf-8")
    discovery = DISCOVERY.read_text(encoding="utf-8")

    require("Current News Releases" in index, "landing title missing", failures)
    entries = re.findall(r'data-published="(\d{4}-\d{2}-\d{2})" data-sequence="(\d+)"', index)
    require(entries, "machine-readable publication ordering missing", failures)
    keys = [(date, int(sequence)) for date, sequence in entries]
    require(keys == sorted(keys, reverse=True), "news releases not reverse chronological/sequence order", failures)

    require('id="edition"' in index, "edition selector missing", failures)
    require('aria-describedby="edition-note"' in index, "edition selector accessibility description missing", failures)
    require('<option value="2026-09-05" selected>9/5/2026</option>' in index, "latest edition must be selected by default", failures)
    require('<option value="2026-09-04">9/4/2026</option>' in index, "September 4 edition missing", failures)
    require('<option value="2026-09-03">9/3/2026</option>' in index, "September 3 edition missing", failures)
    require('<option value="all">All releases</option>' in index, "all-releases option missing", failures)
    require('id="show-all"' in index, "show-all release control missing", failures)
    require("release.dataset.published===value" in index, "edition filtering must resolve from data-published", failures)
    require("value==='all'||" in index, "all-releases filtering path missing", failures)
    require("reconstruct an earlier publication date" in index, "historical-edition reconstruction description missing", failures)

    for title in (PARENT_TITLE, ENTITY_TITLE, SOUTH_KOREA_TITLE):
        require(title in index, f"news release entry missing: {title}", failures)
    require(PARENT_ROUTE in index, "Current News Releases must point to the Coherent Life parent paper", failures)
    require(COMPANION_ROUTE not in index, "Current News Releases must not promote the companion as a peer release", failures)
    require(ADDENDUM_ROUTE not in index, "Current News Releases must not expose a separate Empirical Addendum I release", failures)
    require(COMPANION_TITLE not in index, "Current News Releases must not present the companion as a second publication identity", failures)
    require(ADDENDUM_TITLE not in index, "Current News Releases must not expose the former standalone Empirical Addendum I title", failures)
    require("Working Formal Paper / Attached Companion Extensions" in index, "attached-companion release classification missing", failures)
    if all(title in index for title in (PARENT_TITLE, ENTITY_TITLE, SOUTH_KOREA_TITLE)):
        require(index.index(PARENT_TITLE) < index.index(ENTITY_TITLE) < index.index(SOUTH_KOREA_TITLE), "required Coherent Life -> Entity Economy -> South Korea ordering not preserved", failures)

    require(PARENT_TITLE in coherent_life, "Coherent Life parent title missing", failures)
    require("Working Formal Paper" in coherent_life, "Coherent Life parent working-paper marker missing", failures)
    require("Conjoined Working Formal Paper" not in coherent_life, "Coherent Life parent must not remain over-integrated", failures)
    require("Empirical Application I" not in coherent_life, "Coherent Life parent must not embed Addendum I", failures)
    require("Attached companion materials" in coherent_life, "Coherent Life parent attached-companion section missing", failures)
    require('href="../coherent-life-companion/"' in coherent_life, "Coherent Life parent does not link its attached companion", failures)
    require('href="artifact/"' in coherent_life, "Coherent Life parent does not link the complete 36-page artifact", failures)
    require("Complete paper — 36 pages" in coherent_life, "Coherent Life parent complete-artifact marker missing", failures)
    require("original 22-page working paper" in coherent_life, "Coherent Life parent does not preserve original-paper page boundary", failures)
    require("14 pages of companion material" in coherent_life, "Coherent Life parent does not describe attached companion page boundary", failures)
    require("subordinate to and attached to this working paper" in coherent_life, "parent/companion hierarchy boundary missing", failures)

    require("Complete 36-page Coherent Life paper" in artifact, "complete artifact loader title missing", failures)
    require("Pages 1–22" in artifact and "Pages 33–36" in artifact, "complete artifact page partition missing", failures)
    require("crypto.subtle.digest('SHA-256',bytes)" in artifact, "complete artifact SHA-256 verification missing", failures)
    require("head.startsWith('%PDF-')" in artifact, "complete artifact PDF header fail-closed check missing", failures)
    require("tail.includes('%%EOF')" in artifact, "complete artifact PDF end-marker fail-closed check missing", failures)
    require("catalogSample.includes('/Count 36')" in artifact, "complete artifact 36-page catalog fail-closed check missing", failures)
    require("Artifact unavailable:" in artifact, "complete artifact fail-closed error posture missing", failures)
    require(APPROVED_ARTIFACT_SHA256 in artifact, "complete artifact approved SHA-256 binding missing", failures)
    require(f"EXPECTED_SIZE={APPROVED_ARTIFACT_BYTES}" in artifact, "complete artifact approved byte-length binding missing", failures)
    require("bytes.length!==EXPECTED_SIZE" in artifact, "complete artifact byte-length mismatch fail-closed check missing", failures)
    require("sha!==EXPECTED_SHA" in artifact, "complete artifact SHA-256 mismatch fail-closed check missing", failures)
    require("Verified exact approved 36-page PDF" in artifact, "complete artifact exact-identity success posture missing", failures)
    for part in ARTIFACT_PARTS:
        require(part in artifact, f"complete artifact loader does not reference {part}", failures)

    require(COMPANION_TITLE in companion, "Coherent Life companion title missing", failures)
    require("does not replace or rewrite the original Coherent Life working paper" in companion, "companion parent-preservation boundary missing", failures)
    require("Notation Table and Theorem Witnesses" in companion, "companion notation/theorem component missing", failures)
    require("Unknown-Class Transformation at the Quantum-Gravitational Boundary" in companion, "companion Addendum I component missing", failures)
    require("Recoverable Capacity Across Representational Boundaries" in companion, "companion Addendum II component missing", failures)
    require("Observation ≠ Interpretation ≠ Established knowledge" in companion, "companion Addendum I preservation relation missing", failures)
    require("transition-then-project ≈ project-then-transition" in companion, "companion Addendum II representation-coherence relation missing", failures)

    require("Unknown-Class Transformation at the Quantum-Gravitational Boundary" in addendum, "legacy Empirical Addendum I deep link title missing", failures)
    require(SOUTH_KOREA_TITLE in article, "headline missing", failures)
    require("StegVerse LLC" in article, "company attribution missing", failures)
    require("sovereignty all the way down" in article, "key differentiator missing", failures)
    require(ENTITY_TITLE in entity, "Entity Economy title missing", failures)
    require('href="stegverse-entity-economy.pdf"' in entity, "Entity Economy PDF link missing", failures)

    require("Identity, Agency, Labor, Autonomy, and Legal Standing" in volume_ii_artifact, "Volume II artifact title missing", failures)
    require(VOLUME_II_SHA256 in volume_ii_artifact, "Volume II artifact canonical SHA-256 binding missing", failures)
    require(str(VOLUME_II_BYTES) in volume_ii_artifact, "Volume II artifact canonical byte-length binding missing", failures)
    require("head.startsWith('%PDF-')" in volume_ii_artifact, "Volume II artifact PDF header fail-closed check missing", failures)
    require("tail.includes('%%EOF')" in volume_ii_artifact, "Volume II artifact PDF end-marker fail-closed check missing", failures)
    require("sample.includes('/Count 7')" in volume_ii_artifact, "Volume II artifact seven-page catalog check missing", failures)
    require("bytes.length!==expectedSize" in volume_ii_artifact, "Volume II artifact byte-length mismatch check missing", failures)
    require("sha!==expectedSha" in volume_ii_artifact, "Volume II artifact SHA-256 mismatch check missing", failures)
    require("DecompressionStream('deflate')" in volume_ii_artifact, "Volume II artifact compressed-tail decompression missing", failures)
    require(VOLUME_II_COMPRESSED_TAIL in volume_ii_artifact, "Volume II artifact compressed canonical tail binding missing", failures)
    require("Verified: canonical seven-page Volume II PDF reconstructed successfully." in volume_ii_artifact, "Volume II artifact success posture missing", failures)
    for part in VOLUME_II_PREFIX_PARTS:
        require(part in volume_ii_artifact, f"Volume II artifact loader does not reference prefix {part}", failures)

    prefix_bytes = reconstruct_base64_parts(ENTITY_ECONOMY_VOLUME_II_ARTIFACT_DIR, VOLUME_II_PREFIX_PARTS, failures, "Entity Economy Volume II prefix")
    compressed_tail = volume_ii_tail_path.read_bytes()
    require(git_blob_sha(compressed_tail) == VOLUME_II_COMPRESSED_TAIL_GIT_BLOB_SHA, "Volume II compressed tail Git blob identity mismatch", failures)
    tail_bytes = None
    try:
        tail_bytes = zlib.decompress(compressed_tail)
    except zlib.error as exc:
        failures.append(f"Volume II compressed tail decompression failed: {exc}")
    if prefix_bytes is not None and tail_bytes is not None:
        volume_ii_bytes = prefix_bytes + tail_bytes
        require(volume_ii_bytes.startswith(b"%PDF-"), "Volume II reconstructed bytes do not have a PDF header", failures)
        require(b"%%EOF" in volume_ii_bytes[-2048:], "Volume II reconstructed bytes do not contain a PDF EOF marker", failures)
        require(b"/Count 7" in volume_ii_bytes[:65536], "Volume II reconstructed bytes do not declare seven pages", failures)
        require(len(volume_ii_bytes) == VOLUME_II_BYTES, f"Volume II reconstructed byte length mismatch: {len(volume_ii_bytes)}", failures)
        observed_sha = hashlib.sha256(volume_ii_bytes).hexdigest()
        require(observed_sha == VOLUME_II_SHA256, f"Volume II reconstructed SHA-256 mismatch: {observed_sha}", failures)

    require(PARENT_TITLE in discovery, "Coherent Life parent missing from Papers index", failures)
    require(PARENT_ROUTE in discovery, "Coherent Life parent Papers route missing", failures)
    require(COMPANION_ROUTE not in discovery, "Papers index must not promote companion to peer publication card", failures)
    require(COMPANION_TITLE not in discovery, "Papers index must expose one Coherent Life publication identity", failures)
    require(ADDENDUM_ROUTE not in discovery, "Papers index must not expose Addendum I as a peer publication", failures)
    require(ADDENDUM_TITLE not in discovery, "Papers index must not expose standalone Addendum I title", failures)
    require("Attached companion materials:" in discovery, "Papers index must describe attached companion under parent", failures)
    require("CURRENT FEATURED" in discovery, "Papers index featured publication marker missing", failures)
    require('href="news-releases.html"' in discovery, "public discovery link missing", failures)

    if failures:
        print("CURRENT_NEWS_RELEASES_FAIL")
        for failure in failures:
            print(failure)
        return 1
    print("ENTITY_ECONOMY_VOLUME_II_ARTIFACT_EXACT=PASS")
    print(f"ENTITY_ECONOMY_VOLUME_II_ARTIFACT_BYTES={VOLUME_II_BYTES}")
    print(f"ENTITY_ECONOMY_VOLUME_II_ARTIFACT_SHA256={VOLUME_II_SHA256}")
    print(f"ENTITY_ECONOMY_VOLUME_II_COMPRESSED_TAIL_BLOB={VOLUME_II_COMPRESSED_TAIL_GIT_BLOB_SHA}")
    print("CURRENT_NEWS_RELEASES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
