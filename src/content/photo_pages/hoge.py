import os

# カレントディレクトリのパスを取得
current_dir = os.getcwd()

# カレントディレクトリ内のすべてのファイルを取得
for filename in os.listdir(current_dir):
    file_path = os.path.join(current_dir, filename)

    # 通常のファイルのみ対象（ディレクトリなどを除く）
    if os.path.isfile(file_path):
        if ".py" in file_path:
            continue

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if "ibaido" not in content:
            continue
        print("replace:", file_path)

        # 置換を行う
        new_content = content.replace('related_place: ibaido', 'related_place: ibaraido')

        # 内容が変更されていれば上書き保存
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated: {filename}")

