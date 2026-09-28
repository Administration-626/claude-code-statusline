#!/usr/bin/env python3
import sys
import json
import os
import subprocess

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

# 模型信息
model_info = data.get("model") or {}
model = model_info.get("display_name") or model_info.get("id") or "Claude"

# 思考深度级别（使用灰色显示）
effort_info = data.get("effort") or {}
thinking_info = data.get("thinking") or {}
effort = effort_info.get("level") or thinking_info.get("effort")
if not effort:
    effort = "enabled" if thinking_info.get("enabled") else "default"

# 上下文窗口与使用量度量
cw = data.get("context_window") or {}
window_size = cw.get("context_window_size") or 200000
used_pct = cw.get("used_percentage") or 0.0

window_k = f"{window_size / 1000:.0f}k"
used_tokens = f"{(window_size * used_pct) / 100000:.1f}k"
used_pct_fmt = f"{used_pct:.1f}%"

# 工作区目录
ws = data.get("workspace") or {}
current_dir = ws.get("current_dir") or os.getcwd()
home = os.path.expanduser("~")
if current_dir.startswith(home):
    short_dir = "~" + current_dir[len(home):]
else:
    short_dir = current_dir

# Git 分支
branch = ""
try:
    res = subprocess.run(
        ["git", "-C", current_dir, "rev-parse", "--abbrev-ref", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=0.5
    )
    if res.returncode == 0:
        b = res.stdout.strip()
        if b:
            branch = f" | \033[35m {b}\033[0m"
except Exception:
    pass

# 单行状态栏：[模型] (灰色级别) | 目录 | 分支 | 百分比 已用量/总容量
status_line = (
    f"\033[36m[{model}]\033[0m \033[90m({effort})\033[0m"
    f" | \033[37m{short_dir}\033[0m{branch}"
    f" | \033[33m{used_pct_fmt}\033[0m \033[36m{used_tokens}/{window_k}\033[0m"
)

print(status_line)
