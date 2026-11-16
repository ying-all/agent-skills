# agent-skills

一组给 AI 用的「技能包」：把某件事的标准做法写成文件，让 AI 按固定流程干活，而不是每次自由发挥。

## 什么是 skill

一个技能 = 一个文件夹 + 一份 `SKILL.md`。

`SKILL.md` 是写给 AI 的操作手册：什么时候用、按什么步骤做、做到什么程度算合格。AI 读到就照着执行，人读到也知道这件事该怎么做。

和提示词的区别：提示词聊完就忘；技能是能版本管理、能复用、能分享的文件。

## 快速开始

**1. 下载**

[ZIP 打包下载](https://github.com/ying-all/agent-skills/archive/refs/heads/main.zip) · 或 `git clone https://github.com/ying-all/agent-skills.git`

**2. 用**

把技能目录放到任意位置，然后跟 AI 说：

```
读 <路径>/docs/deepdoc/SKILL.md，按里面流程写一篇「你的主题」
```

技能里带的脚本也可以直接跑：

```bash
python docs/deepdoc/assets/build.py --input note.md --output note.html --title "标题"
```

## 技能列表

| 分类 | 技能 | 作用 |
|---|---|---|
| 文档 | [deepdoc](docs/deepdoc/) | 给一个主题，生成可离线阅读的交互式 HTML 文档（目录 / 搜索 / 深色模式 / 代码高亮） |

## 仓库结构

```
agent-skills/
├── docs/              # 分类：文档生成
│   └── deepdoc/       # 技能
│       ├── SKILL.md   # 给 AI 的指令
│       ├── README.md  # 给人的说明
│       └── assets/    # 脚本与模板
└── security/          # 分类：安全（待添加）
```

一级目录是分类，二级目录是技能。每个技能都能独立拿走用，互不依赖。

## 加一个技能

1. 在对应分类下建目录（没有合适的分类就新建一个分类目录）
2. 放 `SKILL.md` 和 `README.md`，脚本放 `assets/`
3. 在上面的技能列表加一行
4. 提 PR，或直接 commit

## 说明

部分技能涉及安全测试，请只在自有靶场、明确授权的测试、CTF 和内部评估中使用。

## License

MIT
