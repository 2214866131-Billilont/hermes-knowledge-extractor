#!/usr/bin/env python3
"""Tests for Hermes Knowledge Extractor."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure the project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from extractor import KnowledgeExtractor


# ── Mock LLM client for unit tests ──────────────────────────────────────

def make_mock_llm(mock_data: list = None):
    """Create a callable mock LLM client.

    Returns a function (prompt, conversation) -> JSON string
    that can be passed as llm_client to KnowledgeExtractor.
    """
    if mock_data is None:
        mock_data = [
            {
                "knowledge": "Python性能优化应先用cProfile定位瓶颈",
                "evidence": "首先用cProfile做性能分析，找到真正的瓶颈",
                "tags": ["#Python"],
                "confidence": "high",
            }
        ]
    def mock_llm(prompt, conversation_text):
        return json.dumps(mock_data, ensure_ascii=False)
    return mock_llm


def make_mock_llm_dict(mock_data: list = None):
    """Mock that returns {knowledge_points: [...]}."""
    if mock_data is None:
        mock_data = [{"knowledge": "Test", "evidence": "E", "tags": ["#T"], "confidence": "high"}]
    def mock_llm(prompt, conversation_text):
        return json.dumps({"knowledge_points": mock_data}, ensure_ascii=False)
    return mock_llm


def make_mock_llm_points(mock_data: list = None):
    """Mock that returns {points: [...]}."""
    if mock_data is None:
        mock_data = [{"knowledge": "Test", "evidence": "E", "tags": ["#T"], "confidence": "medium"}]
    def mock_llm(prompt, conversation_text):
        return json.dumps({"points": mock_data}, ensure_ascii=False)
    return mock_llm


# ── Test data ──────────────────────────────────────────────────────────

CN_CONVERSATIONS = [
    {"role": "user", "content": "Python代码跑得慢，有什么优化技巧？"},
    {"role": "assistant", "content": (
        "首先用cProfile做性能分析，找到真正的瓶颈。\n"
        "用NumPy的数组运算替代Python for循环，能快几十倍。"
    )},
    {"role": "user", "content": "今天天气真好。"},
    {"role": "assistant", "content": "确实，好天气让人心情舒畅。"},
]

EN_CONVERSATIONS = [
    {"role": "user", "content": "My Python code is slow. Any optimization tips?"},
    {"role": "assistant", "content": (
        "Start with cProfile to find the real bottlenecks.\n"
        "Use NumPy vectorized operations instead of for loops for 10-50x speedup."
    )},
    {"role": "user", "content": "The weather is nice today."},
    {"role": "assistant", "content": "It is! Nice weather lifts the mood."},
]

MIXED_CONVERSATIONS = [
    {"role": "user", "content": "Question in English? No Chinese here."},
    {"role": "assistant", "content": "Answer in English too."},
]


# ── Tests ──────────────────────────────────────────────────────────────

class TestLanguageDetection(unittest.TestCase):
    """Test automatic language detection."""

    def setUp(self):
        self.extractor = KnowledgeExtractor(llm_client=make_mock_llm(), lang="auto")

    def test_detect_chinese(self):
        lang = self.extractor._detect_lang(CN_CONVERSATIONS)
        self.assertEqual(lang, "cn", "Should detect Chinese from first user message")

    def test_detect_english(self):
        lang = self.extractor._detect_lang(EN_CONVERSATIONS)
        self.assertEqual(lang, "en", "Should detect English from first user message")

    def test_detect_english_no_chinese(self):
        lang = self.extractor._detect_lang(MIXED_CONVERSATIONS)
        self.assertEqual(lang, "en", "Should detect English when no Chinese characters")

    def test_detect_empty_conversation(self):
        lang = self.extractor._detect_lang([])
        self.assertEqual(lang, "cn", "Empty conversation should default to Chinese")


class TestConversationFormatting(unittest.TestCase):
    """Test conversation text formatting."""

    def setUp(self):
        self.extractor = KnowledgeExtractor(llm_client=make_mock_llm(), lang="cn")

    def test_format_conversation(self):
        text = self.extractor._format_conversation(CN_CONVERSATIONS)
        self.assertIn("## USER", text)
        self.assertIn("## ASSISTANT", text)
        self.assertIn("Python代码跑得慢", text)
        self.assertIn("用NumPy的数组运算", text)

    def test_format_conversation_counts_messages(self):
        text = self.extractor._format_conversation(CN_CONVERSATIONS)
        # Should have 2 user + 2 assistant markers = 4
        self.assertEqual(text.count("## USER"), 2)
        self.assertEqual(text.count("## ASSISTANT"), 2)

    def test_format_empty_conversation(self):
        text = self.extractor._format_conversation([])
        self.assertEqual(text, "", "Empty conversation should produce empty string")


class TestInputLoading(unittest.TestCase):
    """Test input file loading and normalization."""

    def setUp(self):
        self.extractor = KnowledgeExtractor(llm_client=make_mock_llm(), lang="cn")

    def test_load_list_format(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(CN_CONVERSATIONS, f)
            tmp_path = f.name
        try:
            with open(tmp_path, "r") as f:
                data = json.load(f)
            # Should parse as-is for list format
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 4)
        finally:
            os.unlink(tmp_path)

    def test_load_dict_format(self):
        wrapped = {"conversations": CN_CONVERSATIONS}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(wrapped, f)
            tmp_path = f.name
        try:
            with open(tmp_path, "r") as f:
                data = json.load(f)
            convs = data.get("conversations", data.get("messages", data.get("history", [])))
            self.assertIsInstance(convs, list)
            self.assertEqual(len(convs), 4)
        finally:
            os.unlink(tmp_path)

    def test_load_dict_with_messages_format(self):
        wrapped = {"messages": CN_CONVERSATIONS}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(wrapped, f)
            tmp_path = f.name
        try:
            with open(tmp_path, "r") as f:
                data = json.load(f)
            convs = data.get("conversations", data.get("messages", data.get("history", [])))
            self.assertIsInstance(convs, list)
            self.assertEqual(len(convs), 4)
        finally:
            os.unlink(tmp_path)


class TestPromptLoading(unittest.TestCase):
    """Test prompt file loading."""

    def setUp(self):
        self.extractor = KnowledgeExtractor(llm_client=make_mock_llm())

    def test_load_cn_prompt(self):
        prompt = self.extractor._load_prompt("cn")
        self.assertIn("知识提取专家", prompt)
        self.assertIn("{conversation_content}", prompt)

    def test_load_en_prompt(self):
        prompt = self.extractor._load_prompt("en")
        self.assertIn("knowledge extraction", prompt.lower())
        self.assertIn("{conversation_content}", prompt)

    def test_load_auto_defaults_to_cn(self):
        prompt = self.extractor._load_prompt("auto")
        self.assertIn("知识提取专家", prompt)

    def test_prompt_has_placeholder(self):
        cn_prompt = self.extractor._load_prompt("cn")
        en_prompt = self.extractor._load_prompt("en")
        self.assertIn("{conversation_content}", cn_prompt)
        self.assertIn("{conversation_content}", en_prompt)


class TestLLMResponseParsing(unittest.TestCase):
    """Test parsing of different LLM response formats."""

    def test_parse_direct_list(self):
        mock_data = [
            {"knowledge": "Test knowledge", "evidence": "Test evidence",
             "tags": ["#Test"], "confidence": "high"}
        ]
        extractor = KnowledgeExtractor(llm_client=make_mock_llm(mock_data), lang="cn")
        prompt = extractor._load_prompt("cn")
        result = extractor._call_llm(prompt, "test conversation")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["knowledge"], "Test knowledge")

    def test_parse_knowledge_points_dict(self):
        mock_data = [
            {"knowledge": "Dict wrapped", "evidence": "Evidence",
             "tags": ["#Test"], "confidence": "high"}
        ]
        extractor = KnowledgeExtractor(llm_client=make_mock_llm_dict(mock_data), lang="cn")
        prompt = extractor._load_prompt("cn")
        result = extractor._call_llm(prompt, "test conversation")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["knowledge"], "Dict wrapped")

    def test_parse_points_dict(self):
        mock_data = [
            {"knowledge": "Points wrapped", "evidence": "Evidence",
             "tags": ["#Test"], "confidence": "medium"}
        ]
        extractor = KnowledgeExtractor(llm_client=make_mock_llm_points(mock_data), lang="cn")
        prompt = extractor._load_prompt("cn")
        result = extractor._call_llm(prompt, "test conversation")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["knowledge"], "Points wrapped")


class TestReportFormatting(unittest.TestCase):
    """Test Markdown report formatting."""

    def setUp(self):
        self.extractor = KnowledgeExtractor(llm_client=make_mock_llm(), lang="cn")
        self.points = [
            {"knowledge": "Point A", "evidence": "Evidence A",
             "tags": ["#Category1"], "confidence": "high"},
            {"knowledge": "Point B", "evidence": "Evidence B",
             "tags": ["#Category2"], "confidence": "medium"},
            {"knowledge": "Point C", "evidence": "Evidence C",
             "tags": ["#Category1"], "confidence": "high"},
        ]

    def test_report_has_header(self):
        report = self.extractor._format_report(self.points, 10)
        self.assertIn("📚 对话知识提取报告", report)
        self.assertIn("来源消息数", report)
        self.assertIn("提取知识点", report)
        self.assertIn("3", report)

    def test_report_has_tags_as_sections(self):
        report = self.extractor._format_report(self.points, 10)
        self.assertIn("#Category1", report)
        self.assertIn("#Category2", report)

    def test_report_has_generated_footer(self):
        report = self.extractor._format_report(self.points, 10)
        self.assertIn("Hermes Knowledge Extractor", report)

    def test_report_icons_by_confidence(self):
        high_points = [
            {"knowledge": "High", "evidence": "E", "tags": ["#T"], "confidence": "high"},
            {"knowledge": "Medium", "evidence": "E", "tags": ["#T"], "confidence": "medium"},
        ]
        report = self.extractor._format_report(high_points, 2)
        self.assertIn("⭐", report)   # high confidence
        self.assertIn("🌗", report)   # medium/low confidence

    def test_tag_string_handling(self):
        """Tags can be a string (single tag) instead of list."""
        points = [
            {"knowledge": "Single tag", "evidence": "E",
             "tags": "#OnlyTag", "confidence": "high"},
        ]
        report = self.extractor._format_report(points, 1)
        self.assertIn("#OnlyTag", report)


class TestEndToEnd(unittest.TestCase):
    """End-to-end test with mock LLM."""

    def test_e2e_with_sample_input(self):
        """Run full extraction pipeline on sample_input.json with mock client."""
        mock_data = [
            {"knowledge": "End-to-end test knowledge",
             "evidence": "Evidence text", "tags": ["#E2E"], "confidence": "high"},
        ]
        extractor = KnowledgeExtractor(llm_client=make_mock_llm_dict(mock_data), lang="cn")

        sample_path = Path(__file__).resolve().parent.parent / "examples" / "sample_input.json"
        self.assertTrue(sample_path.exists(), f"Sample input not found at {sample_path}")

        result = extractor.run(str(sample_path))
        self.assertIn("report", result)
        self.assertIn("points", result)
        self.assertEqual(len(result["points"]), 1)
        self.assertEqual(result["points"][0]["knowledge"], "End-to-end test knowledge")
        self.assertIn("📚", result["report"])

    def test_e2e_with_sample_input_en(self):
        """Run full extraction pipeline on sample_input_en.json with mock client."""
        mock_data = [
            {"knowledge": "E2E English test",
             "evidence": "Evidence text", "tags": ["#E2E"], "confidence": "high"},
        ]
        extractor = KnowledgeExtractor(llm_client=make_mock_llm_dict(mock_data), lang="en")

        sample_path = Path(__file__).resolve().parent.parent / "examples" / "sample_input_en.json"
        self.assertTrue(sample_path.exists(), f"Sample input EN not found at {sample_path}")

        result = extractor.run(str(sample_path))
        self.assertIn("report", result)
        self.assertIn("points", result)
        self.assertIn("📚", result["report"])


class TestEndToEndReal(unittest.TestCase):
    """End-to-end test with real LLM call (requires OPENAI_API_KEY).

    Skip if no API key is available.
    """

    @unittest.skipIf(
        not os.getenv("OPENAI_API_KEY"),
        "OPENAI_API_KEY not set, skipping real LLM test"
    )
    def test_real_extraction(self):
        extractor = KnowledgeExtractor(lang="auto")
        sample_path = Path(__file__).resolve().parent.parent / "examples" / "sample_input.json"
        result = extractor.run(str(sample_path))
        self.assertIn("report", result)
        self.assertIn("points", result)
        self.assertGreater(len(result["points"]), 0, "Should extract at least 1 knowledge point")


if __name__ == "__main__":
    unittest.main(verbosity=2)
