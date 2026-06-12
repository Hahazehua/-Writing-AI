# Writing AI

Writing AI 是一个 Codex Skill。它可以读取指定文件夹中的 Word 文档，归纳用户稳定的写作风格，并根据主题、观点、篇幅和发布平台生成原创中文文章。

## 主要功能

- 递归读取文件夹内的全部 `.docx` 文档
- 自动忽略以 `~$` 开头的 Word 临时文件
- 分析句式节奏、段落结构、论证方式、情绪倾向和结尾习惯
- 按照指定主题、观点和字数生成原创文章
- 支持小红书文案、评论文章、个人随笔等中文写作场景
- 遇到新闻和时效性话题时，要求先核实最新事实
- 自动清除中英文双引号、破折号及同类横线符号
- 避免直接复制语料中的独特句子、姓名和私人信息

## 项目结构

```text
writing-ai/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── settings.md
│   └── style-analysis.md
└── scripts/
    ├── extract_docx_corpus.py
    └── sanitize_output.py
```

## 安装方法

将整个 `writing-ai` 文件夹复制到 Codex 的技能目录。

Windows：

```text
C:\Users\你的用户名\.codex\skills\writing-ai
```

macOS 或 Linux：

```text
~/.codex/skills/writing-ai
```

完成安装后，重新启动 Codex 或新建对话。

## 使用方法

在请求中指定 Word 文档所在的文件夹：

```text
使用 $writing-ai，学习 D:\我的文章 文件夹中的所有 Word 文档，
按照我的风格写一篇关于人工智能与个人成长的文章，800字左右。
```

也可以提供更完整的写作要求：

```text
使用 $writing-ai，根据我的写作风格写一篇小红书文章。

主题：努力却感觉退步，可能意味着正在进入新的阶段
观点：使用局部最优解释短期下滑
字数：800字左右
要求：结尾回到个人成长，不使用双引号和破折号
```

## 设置默认语料目录

默认语料目录位于：

```text
references/settings.md
```

可以将其中的路径改为自己的 Word 文档目录。若准备将项目上传到公开仓库，建议不要提交真实用户名、磁盘路径或私人文件位置。

也可以将默认设置改为：

```text
Default Word document folder: Ask the user to provide the folder.
```

这样技能会在没有指定目录时要求用户提供语料位置。

## 工作流程

每次执行写作任务时，Writing AI 会：

1. 提取指定目录中全部 Word 文档的文本
2. 分析多篇文章反复出现的稳定写作特征
3. 区分个人风格与单篇文章中的偶然表达
4. 根据当前主题和要求生成原创内容
5. 对时效性和高风险事实进行核实
6. 检查篇幅并清除禁用标点

Writing AI 不会训练或微调新的模型。新增 Word 文档后，只需再次调用技能，无需重新安装。

## 独立使用脚本

提取一个文件夹中的全部 Word 文档：

```bash
python scripts/extract_docx_corpus.py --source "你的文档目录" --output writing-ai-corpus.md
```

清理文章中的双引号和破折号：

```bash
python scripts/sanitize_output.py draft.md --output final.md
```

检查清理结果：

```bash
python scripts/sanitize_output.py final.md --check
```

脚本仅使用 Python 标准库，无需安装额外依赖。

## 隐私与安全

Word 文档只应保存在本地，不需要上传到 GitHub。公开仓库建议添加以下 `.gitignore` 规则：

```gitignore
*.docx
writing-ai-corpus.md
writing-ai-test/
```

请勿提交包含个人隐私、未公开文章或敏感信息的语料文件。

## 使用限制

- 语料数量和质量会影响风格归纳效果
- 技能学习的是稳定表达特征，不会逐句复制原文
- 生成结果仍需要作者进行事实检查和最终审阅
- 新闻、医疗、法律、金融等内容必须优先保证事实准确

## License

发布到 GitHub 前，可以根据需要添加 MIT License 或其他合适的开源许可证。

