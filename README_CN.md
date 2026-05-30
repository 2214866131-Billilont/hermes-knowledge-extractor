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
git clone https://github.com/221486613131-Billilont/hermes-knowledge-extractor.git
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

## 效果示例

> 以下是从中文对话中提取的结果预览。完整的中英文示例见 `examples/` 目录。

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
