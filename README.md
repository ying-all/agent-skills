# agent-skills

一组给 AI 用的技能包，按分类存放。

## 什么是 skill

一个技能 = 一个文件夹 + 一份 `SKILL.md`。

`SKILL.md` 是写给 AI 的操作手册：什么时候用、按什么步骤做、做到什么程度算合格。AI 读到就照着执行，人读到也知道这件事该怎么做。

提示词聊完就忘；技能是能版本管理、能复用、能分享的文件。

## 技能

| 分类 | 技能 | 一句话 |
|---|---|---|
| 文档 | [deepdoc](docs/deepdoc/) | 主题 → 可离线阅读的交互式 HTML 文档 |

每个技能怎么用，看它自己目录里的 `README.md`。

## 结构

```
agent-skills/
├── docs/              # 分类
│   └── deepdoc/       # 技能
│       ├── SKILL.md   # 给 AI 的指令
│       ├── README.md  # 给人的说明
│       └── assets/    # 脚本与模板
└── README.md
```

一级目录是分类，二级目录是技能。每个技能都能单独拿走用，互不依赖。

## 加一个技能

1. 在对应分类下建目录（没有合适的分类就新建一个）
2. 放 `SKILL.md` 和 `README.md`，脚本放 `assets/`
3. 在上面的技能表加一行
4. 提 PR，或直接 commit

## License

MIT
