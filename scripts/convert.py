#!/usr/bin/env python3
"""
Loon → Surge 自动转换脚本
使用 Script-Hub API 将 Loon 插件转换为 Surge 模块
"""
import yaml
import requests
import os
import re
import sys
import time
from pathlib import Path

SCRIPT_HUB_URL = os.environ.get("SCRIPT_HUB_URL", "http://127.0.0.1:9100")
CONFIG_FILE = "config.yml"
OUTPUT_DIR = "modules"

def sanitize_filename(name: str) -> str:
    """将中文名称转为安全的文件名"""
    return re.sub(r'[^\w\-]', '_', name) + ".sgmodule"

def convert_plugin(name: str, url: str, max_retries: int = 3):
    """调用 Script-Hub API 转换单个插件，带重试"""
    filename = sanitize_filename(name)
    api_url = f"{SCRIPT_HUB_URL}/file/_start_/{url}/_end_/{filename}"
    params = {
        "type": "loon-plugin",
        "target": "surge-module"
    }
    
    for attempt in range(max_retries):
        try:
            resp = requests.get(api_url, params=params, timeout=60)
            if resp.status_code == 200 and len(resp.text) > 50:
                return resp.text
            else:
                if attempt < max_retries - 1:
                    print(f"  ⚠️ HTTP {resp.status_code}, 重试 {attempt + 2}/{max_retries}...")
                    time.sleep(3 * (attempt + 1))
                    continue
                print(f"  ⚠️ 转换失败: HTTP {resp.status_code}, 响应: {resp.text[:100]}")
                return None
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️ 请求错误, 重试 {attempt + 2}/{max_retries}...")
                time.sleep(3 * (attempt + 1))
                continue
            print(f"  ❌ 请求错误: {e}")
            return None
    return None

def main():
    # 读取配置
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    plugins = config.get("plugins", [])
    print(f"📦 共 {len(plugins)} 个插件待转换\n")
    
    # 创建输出目录
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    success = 0
    failed = []
    
    for i, plugin in enumerate(plugins, 1):
        name = plugin["name"]
        url = plugin["url"]
        filename = sanitize_filename(name)
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"[{i}/{len(plugins)}] 🔄 {name}")
        
        content = convert_plugin(name, url)
        
        if content:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ → {filename} ({len(content)} bytes)")
            success += 1
        else:
            failed.append(name)
            print(f"  ❌ 跳过")
        
        # 避免请求过快
        time.sleep(1)
    
    # 生成汇总
    print(f"\n{'='*50}")
    print(f"✅ 成功: {success}/{len(plugins)}")
    if failed:
        print(f"❌ 失败: {', '.join(failed)}")
    
    # 生成 README
    generate_readme(plugins, failed)
    
    return 0 if not failed else 1

def generate_readme(plugins, failed):
    """生成 README.md"""
    lines = [
        "# Loon → Surge 自动转换\n",
        "",
        "将可莉的 Loon 插件自动转换为 Surge 模块，每日凌晨 2 点自动更新。",
        "",
        "## 📦 使用方法",
        "",
        "在 Surge 中添加远程模块，使用以下链接：",
        "",
        "| 插件 | Surge 模块链接 |",
        "|------|---------------|",
    ]
    
    for plugin in plugins:
        name = plugin["name"]
        filename = sanitize_filename(name)
        raw_url = f"https://raw.githubusercontent.com/zkwcw/loon-to-surge/main/modules/{filename}"
        status = "✅" if name not in failed else "❌"
        lines.append(f"| {status} {name} | `{raw_url}` |")
    
    lines.extend([
        "",
        "## 🔄 更新频率",
        "",
        "- **自动更新**: 每天凌晨 2:00 (UTC+8)",
        "- **手动触发**: 在 Actions 页面点击 'Run workflow'",
        "",
        "## 📋 插件来源",
        "",
        "所有插件来自 [可莉的Loon插件中心](https://hub.kelee.one/)",
        "转换工具: [Script-Hub](https://github.com/Script-Hub-Org/Script-Hub)",
        "",
        "## ⚠️ 注意事项",
        "",
        "- 部分插件可能需要 MitM 或特定 Surge 版本",
        "- 如遇问题请查看原插件说明",
        "",
        f"---\n\n*最后更新: 自动生成*",
    ])
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("📝 README.md 已生成")

if __name__ == "__main__":
    sys.exit(main())
