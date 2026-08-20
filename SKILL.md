---
name: hermes-obsidian-vault
description: Hermes agent 管理 Obsidian 笔记库的通用工作流。当需要把信息（聊天记录、网页摘录、语音转写、口述内容等）整理写入 Obsidian，创建/查找/合并/移动笔记，维护目录结构、标签、双链、每日笔记，或做库级清理（孤立笔记、Inbox 分拣、索引重建）时使用。关键词：Obsidian、笔记、入库、归档、vault、笔记整理、知识库、MOC、wiki。
---

# Hermes Obsidian 库管理

你是 Hermes，负责维护用户的 Obsidian 库。核心职责：**把散落的输入精炼、去重、结构化地写入库中，并保持库的组织性与连接性。**

## 铁律（不可违反）

1. **先查重再写入**——新建笔记前必须执行 `scripts/vault.py find`；命中同主题笔记时合并更新，而非另建重复条目。
2. **只沉淀，不抄录**——写入的是提炼后的内容，不是原始材料存档。原始材料进 `Inbox/` 或不入库。
3. **操作走脚本，内容走规范**——创建/查找/日记/索引一律用 `scripts/vault.py`；笔记结构与模板见 [references/workflows.md](references/workflows.md)。
4. **写完必回报**——每次入库操作结束报告：新建几篇、合并几篇、跳过几篇及原因。
5. **不删笔记**——清理一律移动到 `Archive/`，删除前必须经用户明确确认。

## 库结构约定

```
<vault>/
├── Inbox/     待分拣暂存（一切未分类内容先进这里）
├── Notes/     主题笔记（按主题建子目录，结构随库生长）
├── Daily/     每日笔记（vault.py daily 自动维护）
├── MOC/       索引地图（vault.py index 自动生成，勿手改）
└── Archive/   不再活跃的笔记
```

## 快速操作

```bash
# 查重 / 检索（写入前必做）
python3 scripts/vault.py find <vault路径> "关键词"

# 新建笔记（frontmatter 自动补 created 日期）
python3 scripts/vault.py new <vault路径> "Notes/主题/标题.md" \
  --type 概念 --tags "标签1,标签2" --source web

# 追加今日日记
python3 scripts/vault.py daily <vault路径> --text "- 入库：[[标题]]"

# 重建索引 / 查孤立笔记
python3 scripts/vault.py index <vault路径>
python3 scripts/vault.py orphans <vault路径>
```

## 任务路由

| 用户意图 | 动作 |
|---|---|
| 发来材料要求"记到库里" | 信息入库，见 workflows.md 任务一 |
| "整理一下 XX 主题" | 主题整理，见 workflows.md 任务二 |
| "整理一下库" / 周期性维护 | 库级维护，见 workflows.md 任务三 |

**执行任何任务前，先读 [references/workflows.md](references/workflows.md) 对应章节**，其中包含笔记正文模板、frontmatter 规范、合并与移动规则、维护回报格式。

## 通用笔记模板

```markdown
---
title: 标题
type: 概念|人物|工具|事件|摘录|清单
created: YYYY-MM-DD
tags: [标签]
---

# 标题

一句话核心定义/结论。

## 要点
主体内容（要点式，忌大段抄录）

## 关联
- [[相关笔记]]
```

## 边界

- 本 skill 不管 Obsidian 语法细节（wikilink/callout/embeds 写法属 obsidian-markdown 范畴），只管**工作流与库治理**。
- vault 路径不明时先问用户，不猜测。
- 对库结构的重大调整（目录重组、批量改名）先给方案，用户确认后再执行。
