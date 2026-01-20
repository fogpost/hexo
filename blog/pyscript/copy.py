import os
import re
import shutil

# ===== 配置 =====
VAULT_PATH = r"C:\Users\fogpost\Documents\Obsidian Vault\blog\source"
BACKUP_PATH = VAULT_PATH + "_backup"

# ===== 备份整个 _posts =====
if not os.path.exists(BACKUP_PATH):
    shutil.copytree(VAULT_PATH, BACKUP_PATH)
    print(f"已备份 _posts 到 {BACKUP_PATH}")

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    inside_front_matter = False
    date_value = None
    modified = False

    for line in lines:
        if line.strip() == '---':
            inside_front_matter = not inside_front_matter
            new_lines.append(line)
            continue

        if inside_front_matter:
            # 先抓 date 的值
            date_match = re.match(r'^\s*date:\s*(.*)', line)
            if date_match:
                date_value = date_match.group(1).strip()
                new_lines.append(line)
                continue

            # 找到 updated 字段，把值替换成 date
            updated_match = re.match(r'^\s*updated:\s*(.*)', line)
            if updated_match:
                if date_value:
                    new_lines.append(f"updated: {date_value}\n")
                    modified = True
                else:
                    # 如果没找到 date，就保留原值
                    new_lines.append(line)
                continue

            new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"已更新 updated: -> date 的值 -> {file_path}")

def traverse_posts():
    for root, dirs, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    traverse_posts()
    print("处理完成！")
