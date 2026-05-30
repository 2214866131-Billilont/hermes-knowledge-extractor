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

## Sample Output

> Below is a preview of the extracted knowledge report. The full Chinese/English examples are in the `examples/` directory.

```markdown
# 📚 对话知识提取报告

**提取时间**：2025-06-01 10:30:00
**来源消息数**：8
**提取知识点**：10

---

## #Python优化

- ⭐ Python性能优化应先使用cProfile定位瓶颈，90%的性能问题集中在10%的代码中
  > 首先用cProfile做性能分析，找到真正的瓶颈，不要凭直觉优化...

- ⭐ 大规模数据使用NumPy向量化操作替代Python for循环，可获得10-50倍速度提升
  > 用NumPy的数组运算替代Python的for循环，能快几十倍...

- ⭐ CPU密集型任务使用multiprocessing而非多线程，因GIL限制多线程对CPU任务无效
  > 多线程在Python里因为GIL的存在，对CPU密集型任务帮助不大...

- ⭐ 使用functools.lru_cache缓存重复计算结果可显著提升性能
  > 用functools.lru_cache缓存重复计算的函数结果，很多时候能带来显著提升...

## #AI-Agent开发

- ⭐ AI Agent四大核心组件：规划（Planning）、工具使用（Tool Use）、记忆（Memory）、执行（Action）
  > 核心要理解Agent的四个组件：规划、工具使用、记忆、执行...
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
