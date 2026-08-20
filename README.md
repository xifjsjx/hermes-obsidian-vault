# hermes-obsidian-vault

Hermes agent 管理 Obsidian 库的通用 Skill：把各类输入（聊天记录、网页摘录、口述内容等）**提炼、去重、结构化**地写入 Obsidian 库，并维护库的组织性与连接性。

## 功能

- **信息入库**：提炼核心结论，先查重再写入（合并优先于新建），自动登记到当日日记
- **主题整理**：合并重复条目、补齐互链、按需生成 MOC 导航
- **库级维护**：Inbox 清零、孤立笔记检测、全库索引自动重建
- **治理铁律**：只沉淀不抄录、不删笔记只归档、重大结构调整先确认

## 库结构约定

```
Inbox/    待分拣暂存
Notes/    主题笔记（按主题建子目录）
Daily/    每日笔记（脚本自动维护）
MOC/      索引地图（脚本自动生成）
Archive/  不再活跃的笔记
```

## 目录结构

```
SKILL.md                  skill 主文件（触发规则 + 铁律 + 快速操作）
references/workflows.md   三类任务（入库 / 主题整理 / 库级维护）的完整细则
scripts/vault.py          Obsidian 库操作脚本（仅标准库）：new / find / daily / index / orphans
```

## 脚本用法

```bash
python3 scripts/vault.py find   <vault> <关键词>        # 写入前查重
python3 scripts/vault.py new    <vault> <路径.md> --type 概念 --tags "..." --source web
python3 scripts/vault.py daily  <vault> --text "..."   # 追加今日日记
python3 scripts/vault.py index  <vault>                # 重建 MOC 索引
python3 scripts/vault.py orphans <vault>               # 检测孤立笔记
```

## 安装

将本仓库整个目录作为 skill 文件夹放入 agent 的 skills 目录（保持 `SKILL.md` 在根），或打包为 `.skill`（zip 格式）后导入支持 Skill 的 agent 环境。
