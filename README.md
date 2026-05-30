# Hermes Knowledge Extractor

[中文文档](README_CN.md) | [Examples](examples/)

**Turn your AI chat history into a structured personal knowledge base with one click.**

> You've had hundreds of conversations with ChatGPT, Claude, and other AI assistants. Somewhere in those chats are golden insights, clever solutions, and hard-won lessons. But finding them again is impossible. This tool fixes that.

## What It Does

1. **Import** — Load ChatGPT or Claude export files (JSON)
2. **Extract** — AI automatically identifies valuable knowledge points, filtering out small talk and dead ends
3. **Deduplicate** — Semantic deduplication merges similar ideas across conversations
4. **Organize** — Output a structured Markdown report, grouped by topic tags

## Quick Start

```bash
# Clone the repo
git clone https://github.com/221486613131-Billilont/hermes-knowledge-extractor.git
cd hermes-knowledge-extractor

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-key"  # Works with DeepSeek, OpenAI, etc.

## Usage Example

```python
from openai import OpenAI
from extractor import KnowledgeExtractor

# Initialize with any OpenAI-compatible client
client = OpenAI(
    api_key="your-key",
    base_url="https://api.deepseek.com/v1"  # Example: DeepSeek
)

# Create extractor and run
extractor = KnowledgeExtractor(
    llm_client=client,
    lang='auto'  # Auto-detect Chinese or English
)

result = extractor.run("path/to/your/chatgpt_export.json")
```

## Use as a Hermes Skill

```python
from skill import register

# One line to register with your Hermes instance
skill = register(hermes)

# Then simply say:
# "整理一下我最近的对话"
# or
# "Extract knowledge from my conversations"
```

## Project Structure

```
hermes-knowledge-extractor/
├── extractor.py              # Core extraction engine
├── skill.py                  # Hermes Agent skill wrapper
├── prompts/
│   ├── extract_prompt.txt    # Chinese extraction prompt
│   └── extract_prompt_en.txt # English extraction prompt
├── examples/
│   ├── sample_input.json     # Chinese example input
│   ├── sample_input_en.json  # English example input
│   ├── sample_output.md      # Chinese example output
│   └── sample_output_en.md   # English example output
├── storage/                  # Extracted knowledge base (JSON)
└── tests/                    # Unit tests
```
