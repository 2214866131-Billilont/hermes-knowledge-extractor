# Hermes 对话知识提取器

[English Docs](README.md) | [示例](examples/)

**一键把 AI 对话记录变成结构化个人知识库。**

> 你跟 ChatGPT、Claude 等 AI 助手聊了成百上千轮。那些对话里藏着宝贵的洞察、巧妙的解决方案、反复试错得出的经验。但想找回它们比大海捞针还难。这个工具就是来解决这个问题的。

## 它能做什么

1. **导入** — 加载 ChatGPT 或 Claude 的对话导出文件（JSON）
2. **提取** — AI 自动识别有价值的知识点，过滤掉闲聊和死胡同
3. **去重** — 语义去重合并跨对话的相似内容
4. **整理** — 输出结构化的 Markdown 报告，按主题标签分类

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/hermes-knowledge-extractor.git
cd hermes-knowledge-extractor

# 安装依赖
pip install -r requirements.txt

# 设置 API Key
export OPENAI_API_KEY="你的密钥"  # 支持 DeepSeek、OpenAI 等

## 使用示例

```python
from openai import OpenAI
from extractor import KnowledgeExtractor

# 使用任意 OpenAI 兼容的客户端
client = OpenAI(
    api_key="你的密钥",
    base_url="https://api.deepseek.com/v1"  # 示例：DeepSeek
)

# 创建提取器并运行
extractor = KnowledgeExtractor(
    llm_client=client,
    lang='auto'  # 自动检测中文或英文
)

result = extractor.run("路径/你的/chatgpt_导出文件.json")

## 作为 Hermes Skill 使用

```python
from skill import register

# 一行代码注册到你的 Hermes 实例
skill = register(hermes)

# 然后直接说：
# "整理一下我最近的对话"
# 或
# "Extract knowledge from my conversations"
```

## 项目结构

```
hermes-knowledge-extractor/
├── extractor.py              # 核心提取引擎
├── skill.py                  # Hermes Agent Skill 封装
├── prompts/
│   ├── extract_prompt.txt    # 中文提取 Prompt
│   └── extract_prompt_en.txt # 英文提取 Prompt
├── examples/
│   ├── sample_input.json     # 中文示例输入
│   ├── sample_input_en.json  # 英文示例输入
│   ├── sample_output.md      # 中文示例输出
│   └── sample_output_en.md   # 英文示例输出
├── storage/                  # 提取后的知识库（JSON）
└── tests/                    # 单元测试
```
