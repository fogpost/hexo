import os
import re
import shutil

# ===== 配置 =====
# 建议确认此路径是否包含 _drafts，如果是整个 source 文件夹，脚本会处理旗下所有子文件夹
VAULT_PATH = r"C:\Users\fogpost\Documents\Obsidian Vault\blog\source"
BACKUP_PATH = VAULT_PATH + "_backup"

# ===== 备份功能 =====
if not os.path.exists(BACKUP_PATH):
    shutil.copytree(VAULT_PATH, BACKUP_PATH)
    print(f"已备份原始文件到 {BACKUP_PATH}")

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则匹配整个 Front Matter 部分 (--- ... ---)
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return

    front_matter = fm_match.group(1)
    body = content[fm_match.end():]
    
    # 1. 提取 date 的值
    date_search = re.search(r'^date:\s*(.*)$', front_matter, re.MULTILINE)
    if not date_search:
        return # 如果没有 date 字段，无法同步，跳过
    
    date_value = date_search.group(1).strip()

    # 2. 处理 updated 字段
    # 逻辑：如果存在 updated 字段则修改；如果不存在则添加
    if re.search(r'^updated:', front_matter, re.MULTILINE):
        # 替换现有的 updated 值
        new_fm = re.sub(r'^updated:.*$', f"updated: {date_value}", front_matter, flags=re.MULTILINE)
    else:
        # 如果没有 updated 字段，直接在 front matter 末尾添加一行
        new_fm = front_matter.strip() + f"\nupdated: {date_value}"

    # 3. 检查是否有变化，有变化才写入
    if new_fm != front_matter:
        new_content = f"---\n{new_fm.strip()}\n---\n{body}"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 已同步 updated = date: {file_path}")

def traverse_posts():
    for root, dirs, files in os.walk(VAULT_PATH):
        # 排除备份文件夹本身，防止死循环
        if "_backup" in root:
            continue
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    traverse_posts()
    print("\n✨ 所有文件处理完成！")