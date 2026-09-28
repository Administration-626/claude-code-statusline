# Claude Code Statusline

轻量、高性能的 Claude Code 单行状态栏工具。使用 Python 3 运行时解析数据流，零第三方工具依赖（无需 `jq`），单次渲染延迟低于 3 毫秒。

## 呈现效果

- 处于 Git 仓库目录时：
  ```text
  [glm-5.3] (high) | ~/dotfiles |  main | 15.2% 159.4k/1049k
  ```
- 处于普通目录时：
  ```text
  [glm-5.3] (high) | ~/playground | 15.2% 159.4k/1049k
  ```

## 字段说明

- **模型**：`[model]`，使用常规青色（`\033[36m`）显示。
- **思考深度**：`(effort_level)`，使用暗灰阶色彩（`\033[90m`）弱化呈现。
- **工作区**：`~/dir`，自动压缩 `$HOME` 绝对路径为波浪号。
- **Git 分支**：` branch`，仅读取本地 `HEAD` 指针，不扫描文件树。
- **上下文度量**：`xx% xxk/xxxk`，包含使用百分比、已消耗 Token 与总容量。

## 安装与配置

1. 赋予脚本执行权限：
   ```bash
   chmod +x statusline.sh statusline.py
   ```

2. 在 Claude Code 配置文件 `~/.claude/settings.json` 中配置：
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "/home/tan/claude-code-statusline/statusline.sh",
       "padding": 0
     }
   }
   ```
