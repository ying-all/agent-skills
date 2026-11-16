# agent-skills

给 AI 用的技能包集合。每个目录一个技能，独立可用。

## 下载

- [ZIP 打包下载](https://github.com/ying-all/agent-skills/archive/refs/heads/main.zip)
- 或 `git clone https://github.com/ying-all/agent-skills.git`

解压后每个目录就是一个技能，不用安装依赖。

## 使用

把技能目录放到任意位置，然后跟 AI 说：

```
读 <路径>/deepdoc/SKILL.md，按里面流程写一篇「 某某某方法论」
```

自己跑构建：

```bash
python deepdoc/assets/build.py --input note.md --output note.html --title "标题"
```

## 技能

| 技能 | 分类 | 作用 |
|---|---|---|
| [deepdoc](deepdoc/) | 文档 | 给一个主题，生成可离线阅读的交互式 HTML 文档（目录 / 搜索 / 深色模式 / 代码高亮） |

## 约定

- 目录名 = 技能名，小写短横线，如 `deepdoc`、`xss-notes`
- **扁平存放**，不按分类建子目录；分类写在上面的表格里
- 每个技能自带 `SKILL.md`（给 AI）和 `README.md`（给人）
- 技能超过 10 个、或某一类超过 5 个，再考虑拆目录（用 `git mv`，历史不会丢）

## 新增技能

1. 建目录，放 `SKILL.md` 和 `README.md`
2. 在上面的表格加一行，填上分类
3. `git add . && git commit -m "add xxx" && git push`
