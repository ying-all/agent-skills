# deepdoc

给一个主题，生成一篇能离线阅读的 HTML 文档：左侧目录、全文搜索、深色模式、代码高亮，单文件，双击就开。

## 用法

**直接说：**

```
用 deepdoc 写一篇「XSS 攻防方法论」，输出到桌面
```

**已经有 Markdown：**

```bash
python assets/build.py --input note.md --output note.html --title "XSS 攻防方法论"
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--input` | 是 | 源 Markdown |
| `--output` | 是 | 输出 HTML 路径 |
| `--title` | 是 | 文档标题 |
| `--subtitle` | | 首屏一句话简介 |
| `--chips` | | 首屏标签，用 `\|` 分隔，如 `18 章\|方法论` |
| `--intro` | | 开头说明块（Markdown 文件） |
| `--footer` | | 页脚声明 |

## Markdown 怎么写

- `## 1. 第一步`、`### 1.1 闭合` → 自动进左侧目录，数字变成小徽标
- 表格、围栏代码块（标语言）、`- [ ]` 清单、`>` 提示框都支持
- 不要自己写目录，脚本会生成

## 环境

Python 3.8+，Markdown 库已内置。想要代码高亮再装 Pygments：

```bash
pip install Pygments
```

## 边界

仅用于授权范围内的学习与测试。
