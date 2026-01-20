import os
import re

VAULT_PATH = r"C:\Users\fogpost\Documents\Obsidian Vault\blog\source"
RENAME_TO_CRATED = False  # True 就改名为 crated，False 就删除

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
            match = re.match(r'^\s*updated:\s*(.*)', line)
            if match:
                modified = True
                if RENAME_TO_CRATED:
                    new_lines.append(f'created: {match.group(1)}\n')
                # 如果不改名，就删除
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
