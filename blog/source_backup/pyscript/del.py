import os
import re
import shutil

# ===== 配置部分 =====
VAULT_PATH = r"C:\Users\fogpost\Documents\Obsidian Vault\blog\source"  # 改成你的笔记库路径
BACKUP_PATH = VAULT_PATH + "_backup"

# ===== 备份文件 =====
if not os.path.exists(BACKUP_PATH):
    shutil.copytree(VAULT_PATH, BACKUP_PATH)
    print(f"已备份笔记库到 {BACKUP_PATH}")

# ===== 处理函数 =====
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    inside_front_matter = False
    modified = False

    for line in lines:
        if line.strip() == '---':
            inside_front_matter = not inside_front_matter
            new_lines.append(line)
            continue

        if inside_front_matter:
            # 匹配 updated 字段，允许行首空格
            if re.match(r'^\s*updated:\s*.*', line):
                modified = True
                continue  # 删除该行
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"已删除 updated: -> {file_path}")

# ===== 遍历笔记库 =====
def traverse_vault():
    for root, dirs, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    traverse_vault()
    print("处理完成！")
