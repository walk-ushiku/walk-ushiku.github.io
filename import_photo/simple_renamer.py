import os
import shutil
import difflib
from tkinter import *
from PIL import Image, ImageTk

from config import user_dict

max_size = (600, 600)
window_size = (800, 850)
processed_file = "processed.txt"

def resize_by_longest_edge(img, max_length):
    w, h = img.size
    scale = max_length / float(max(w, h))
    return img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

def load_valid_spot_names(spot_folder="../src/content/spot_note"):
    if not os.path.isdir(spot_folder):
        return []
    return [
        f.removesuffix(".mdx") for f in os.listdir(spot_folder)
        if f.endswith(".mdx")
    ]

def check_spot_validity(spot, spot_name_candidates):
    if spot in spot_name_candidates:
        return True

    close = difflib.get_close_matches(spot, spot_name_candidates, n=5, cutoff=0.6)
    prefix = [name for name in spot_name_candidates if name.startswith(spot) and name not in close]
    suggestions = close + prefix

    return suggestions

def gather_target_files(base_folder="raw_photo"):
    targets = []
    for user in os.listdir(base_folder):
        path = os.path.join(base_folder, user)
        if not os.path.isdir(path):
            continue
        for filename in os.listdir(path):
            if filename.lower().endswith((".jpg_large", ".jpg", ".jpeg", ".png", ".jfif")):
                full = os.path.join(path, filename)
                if not os.path.exists(processed_file) or full not in open(processed_file).read():
                    targets.append((user, filename))
    return targets

def main(file_list):
    if not file_list:
        print("画像が見つかりません。")
        return

    spot_name_candidates = load_valid_spot_names()
    processed_set = set()
    if os.path.exists(processed_file):
        with open(processed_file, "r", encoding="utf-8") as f:
            processed_set = set(line.strip() for line in f)

    index = 0

    def show_image():
        nonlocal index
        user, filename = file_list[index]
        img_path = os.path.join("raw_photo", user, filename)
        img = Image.open(img_path)
        img = resize_by_longest_edge(img, min(max_size))
        photo = ImageTk.PhotoImage(img)
        panel.config(image=photo)
        panel.image = photo
        entry.delete(0, END)
        label.config(text=f"{filename} ({index+1}/{len(file_list)})\n{user}")

    def next_image():
        nonlocal index
        index += 1
        if index < len(file_list):
            show_image()
        else:
            root.quit()

    def skip():
        nonlocal index
        print(f"⏩ スキップ: {file_list[index]}")
        next_image()
        return

    def rename():
        nonlocal index
        user, old_name = file_list[index]
        old_path = os.path.join("raw_photo", user, old_name)
        _, ext = os.path.splitext(old_name)

        if old_path in processed_set:
            print(f"スキップ（処理済）: {old_path}")
            next_image()
            return

        raw_input = entry.get().strip()
        if not raw_input:
            print("❌ 入力が空です")
            return

        if raw_input.count("-") > 1:
            print("⚠ エラー：'-'が2個以上あります。形式: spot-photo")
            return

        if "-" in raw_input:
            spot, _ = raw_input.split("-", 1)
            result = check_spot_validity(spot, spot_name_candidates)
            if result is not True:
                print(f"⚠ 不明なスポット名: '{spot}'")
                if result:
                    print("👉 候補:", ", ".join(result))
                else:
                    print("👉 該当する候補は見つかりません")
                return

        public_path = os.path.join("../public/images/photos", user_dict[user], raw_input + ".jpg")
        if os.path.exists(public_path):
            print(f"❌ 既に画像が存在します: {public_path}")
            existing = os.listdir(os.path.dirname(public_path))
            name_only = [f.removesuffix(".jpg") for f in existing if f.endswith(".jpg")]
            suggestions = difflib.get_close_matches(raw_input, name_only, n=5, cutoff=0.7)
            if suggestions:
                print("🔍 似たファイル名:", ", ".join(suggestions))
            return

        dst_folder = os.path.join("named_photo", user)
        os.makedirs(dst_folder, exist_ok=True)
        new_path = os.path.join(dst_folder, raw_input + ext)

        if os.path.exists(new_path):
            print(f"⚠ すでに存在します: {new_path}")
            return

        print("✅ コピー:", old_path, "→", new_path)
        shutil.copy2(old_path, new_path)

        with open(processed_file, "a", encoding="utf-8") as f:
            f.write(old_path + "\n")

        next_image()

    def check_spot_button():
        raw_input = entry.get().strip()
        if not raw_input:
            print("⚠ 入力が空です")
            return

        if "-" in raw_input:
            spot = raw_input.split("-", 1)[0]
        else:
            spot = raw_input

        result = check_spot_validity(spot, spot_name_candidates)
        if result is True:
            print(f"✅ スポット名は有効: {spot}")
        else:
            print(f"❌ 不明なスポット名: {spot}")
            if result:
                print("👉 候補:", ", ".join(result))
            else:
                print("👉 候補なし")

    def on_tab(event):
        raw_input = entry.get().strip()
        if not raw_input:
            return "break"  # 無効化

        if "-" in raw_input:
            spot, rest = raw_input.split("-", 1)
        else:
            spot, rest = raw_input, ""

        matches = [name for name in spot_name_candidates if name.startswith(spot)]
        if len(matches) == 1:
            new_input = matches[0] + ("-" + rest if rest else "-")
            entry.delete(0, END)
            entry.insert(0, new_input)
            print(f"✅ 補完: {raw_input} → {new_input}")
        elif len(matches) > 1:
            print(f"🔍 複数候補: {', '.join(matches)}")
        else:
            print("❌ 補完候補がありません")

        return "break"  # EntryのデフォルトTab動作（フォーカス移動）を防止

    # --- GUI ---
    root = Tk()
    root.title("画像検証ツール")
    root.geometry(f"{window_size[0]}x{window_size[1]}")

    panel = Label(root)
    panel.pack(pady=10)

    label = Label(root, text="")
    label.pack()

    entry = Entry(root, width=100, font=("Arial", 16))
    entry.pack(pady=10)

    Button(root, text="保存して次へ", command=rename, font=("Arial", 14)).pack()
    Button(root, text="候補を確認", command=check_spot_button, font=("Arial", 12)).pack(pady=5)
    Button(root, text="スキップ", command=skip, font=("Arial", 12)).pack(pady=5)

    root.bind("<Return>", lambda e: rename())
    root.bind("<Tab>", on_tab)

    show_image()
    root.mainloop()

if __name__ == '__main__':
    print("入力パターン：spot_name-photo_name")

    targets = gather_target_files()
    if not targets:
        print("処理対象の画像がありません")
    else:
        main(targets)

