import os
import re

# ===== 配置部分 =====
# 你的 Obsidian 笔记库路径
VAULT_PATH = r"C:\Users\fogpost\Documents\Obsidian Vault\blog\source"  # 改成你自己的路径

# 是否自动将 create 的值改成 crated，否则只是删除
RENAME_TO_CRATED = True

# ===== 脚本逻辑 =====
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    inside_front_matter = False
    modified = False

    for line in lines:
        # 检测 front matter 开始和结束
        if line.strip() == '---':
            inside_front_matter = not inside_front_matter
            new_lines.append(line)
            continue

        if inside_front_matter:
            # 找到 create: 字段
            match = re.match(r'^(crated:\s*)(.*)', line)
            if match:
                modified = True
                if RENAME_TO_CRATED:
                    # 改成 crated: 原值不变
                    new_lines.append(f'created: {match.group(2)}\n')
                # 如果不改名，只删除
                continue
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"修改: {file_path}")

def traverse_vault():
    for root, dirs, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    traverse_vault()
    print("处理完成！") 