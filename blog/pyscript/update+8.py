import os
import re
import shutil

# ===== 配置 =====
VAULT_PATH = r"C:\Users\fogpost\Documents\Obsidian Vault\blog\source"
BACKUP_PATH = VAULT_PATH + "_backup"

# ===== 备份 =====
if not os.path.exists(BACKUP_PATH):
    shutil.copytree(VAULT_PATH, BACKUP_PATH)
    print(f"已备份原始文件到 {BACKUP_PATH}")

def fix_updated(front_matter: str) -> str:
    """
    把：
      updated: 2024-09-12 14:59:07
    改成：
      updated: 2024-09-12T14:59:07+08:00
    """
    def repl(match):
        raw = match.group(1).strip()
        # 已经有时区的，直接跳过
        if '+' in raw or raw.endswith('Z'):
            return f"updated: {raw}"
        # 空格 → T，加上 +08:00
        fixed = raw.replace(' ', 'T') + "+08:00"
        return f"updated: {fixed}"

    return re.sub(
        r'^updated:\s*(.+)$',
        repl,
        front_matter,
        flags=re.MULTILINE
    )

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return

    front_matter = fm_match.group(1)
    body = content[fm_match.end():]

    if not re.search(r'^updated:', front_matter, re.MULTILINE):
        return

    new_fm = fix_updated(front_matter)

    if new_fm != front_matter:
        new_content = f"---\n{new_fm}\n---\n{body}"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 修复 updated 时区: {file_path}")

def traverse_posts():
    for root, _, files in os.walk(VAULT_PATH):
        if "_backup" in root:
            continue
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    traverse_posts()
    print("\n✨ 所有 updated 已修复（仅补时区，不改时间点）")
