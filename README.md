# agent-skills

给 AI 用的技能包集合。按分类分文件夹，同类技能放一起。

## 下载

- [ZIP 打包下载](https://github.com/ying-all/agent-skills/archive/refs/heads/main.zip)
- 或 `git clone https://github.com/ying-all/agent-skills.git`

## 使用

把技能目录放到任意位置，然后跟 AI 说：

```
读 <路径>/docs/deepdoc/SKILL.md，按里面流程写一篇「某某某方法论」
```

自己跑构建：

```bash
python docs/deepdoc/assets/build.py --input note.md --output note.html --title "标题"
```

## 目录

| 文件夹 | 分类 | 技能 |
|---|---|---|
| [docs](docs/) | 文档生成 | [deepdoc](docs/deepdoc/) |

## 约定

- **一级目录 = 分类**：`docs` 文档、`security` 安全、`dev` 开发、`workflow` 工作流
- **二级目录 = 技能名**，小写短横线，如 `docs/deepdoc`
- 每个技能自带 `SKILL.md`（给 AI）和 `README.md`（给人）
- 新技能先归到已有分类；没有合适的再新建分类

## 新增技能

1. 在对应分类目录下建技能目录
2. 放 `SKILL.md` 和 `README.md`
3. 上面的表格加一行
4. `git add . && git commit -m "add xxx" && git push`

