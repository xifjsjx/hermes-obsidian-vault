# hermes-obsidian-vault

Hermes agent 管理 Obsidian 学习库的 Skill：把 Kimi 聊天记录、复习总结、ima 笔记**精炼、去重、结构化**地写入 Obsidian 库，并维护库的连接性。

## 功能

- **盲区精炼入库**：从聊天记录/复盘中提取盲区，≤15 字核心短句锚定，先查重再写入（合并优先于新建）
- **ima 笔记同步**：逐条拆分、去重、按学科归档
- **焊链成果归档**：模块骨架笔记 + 盲区状态流转（待消化 → 待重默 → 已掌握）
- **周期维护**：孤立笔记检测、Inbox 清空、MOC 索引自动重建

## 目录结构

```
SKILL.md                  skill 主文件（触发规则 + 铁律 + 快速操作）
references/workflows.md   三类入库任务与周期维护的完整细则
scripts/vault.py          Obsidian 库操作脚本（仅标准库）：new / find / daily / index / orphans
```

## 脚本用法

```bash
python3 scripts/vault.py find   <vault> <关键词>        # 写入前查重
python3 scripts/vault.py new    <vault> <路径.md> --type 盲区 --subject 化学 ...
python3 scripts/vault.py daily  <vault> --text "..."   # 追加今日复盘
python3 scripts/vault.py index  <vault>                # 重建 MOC 索引
python3 scripts/vault.py orphans <vault>               # 检测孤立笔记
```

## 安装

将本仓库整个目录作为 skill 文件夹放入 agent 的 skills 目录（保持 `SKILL.md` 在根），或打包为 `.skill`（zip 格式）后导入支持 Skill 的 agent 环境。
