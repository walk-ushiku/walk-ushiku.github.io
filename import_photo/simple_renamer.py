import os
import shutil
import difflib
from tkinter import *
from PIL import Image, ImageTk

from config import user_dict

max_size = (600, 600)
window_size = (800, 800)
processed_file = "processed.txt"

def resize_by_longest_edge(img, max_length):
    w, h = img.size
    if w >= h:
        scale = max_length / float(w)
    else:
        scale = max_length / float(h)
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.LANCZOS)

def gather_target_files(base_folder="raw_photo"):
    target_files = []
    if not os.path.isdir(base_folder):
        print(f"{base_folder} が存在しません")
        return target_files

    for user in os.listdir(base_folder):
        user_folder = os.path.join(base_folder, user)
        if not os.path.isdir(user_folder):
            continue
        for filename in os.listdir(user_folder):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                target_files.append((user, filename))
    return target_files

def load_valid_spot_names(spot_folder="../src/content/spot_note"):
    spot_names = []
    if os.path.isdir(spot_folder):
        for filename in os.listdir(spot_folder):
            if filename.endswith(".mdx"):
                spot_names.append(filename.removesuffix(".mdx"))
    return spot_names

def main(file_list):
    if not file_list:
        print("画像が見つかりません。")
        return

    spot_name_candidates = load_valid_spot_names()

    if os.path.exists(processed_file):
        with open(processed_file, "r", encoding="utf-8") as f:
            processed_set = set(line.strip() for line in f)
    else:
        processed_set = set()

    index = 0

    def show_image():
        nonlocal index
        user, filename = file_list[index]
        folder = os.path.join("raw_photo", user)
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path)
        img = resize_by_longest_edge(img, min(max_size))
        photo = ImageTk.PhotoImage(img)
        panel.config(image=photo)
        panel.image = photo
        entry.delete(0, END)
        label.config(text=f"{filename} ({index+1}/{len(file_list)})\n{folder}")

    def rename():
        nonlocal index
        user, old_name = file_list[index]
        folder = os.path.join("raw_photo", user)
        old_path = os.path.join(folder, old_name)
        _, ext = os.path.splitext(old_name)

        if old_path in processed_set:
            print(f"Skipped (already processed): {old_path}")
            next_image()
            return

        raw_input = entry.get().strip()
        if not raw_input:
            print("スキップ：名前を入力してください")
            return

        if raw_input.count("-") > 1:
            print("⚠ エラー：'-'が2個以上含まれています。形式は spot-photo です")
            return

        if raw_input.count("-") == 1:
            spot, _ = raw_input.split("-", 1)
            if spot not in spot_name_candidates:
                print(f"⚠ 不明なスポット名: '{spot}'")
                close = difflib.get_close_matches(spot, spot_name_candidates, n=5, cutoff=0.6)
                if close:
                    print("👉 もしかして:", ", ".join(close))
                else:
                    print("👉 該当する候補は見つかりませんでした")
                return

        # 重複チェック
        public_img_path = os.path.join("../public/images/photos", user_dict[user], raw_input + ".jpg")
        if os.path.exists(public_img_path):
            print(f"❌ エラー：すでに画像が存在します: {public_img_path}")

            existing_files = os.listdir(os.path.join("../public/images/photos", user_dict[user]))
            png_files = [f.removesuffix(".jpg") for f in existing_files if f.endswith(".jpg")]

            suggestions = difflib.get_close_matches(raw_input, png_files, n=5, cutoff=0.7)
            if suggestions:
                print("🔍 似たファイル名:", ", ".join(suggestions))
            return

        new_folder = os.path.join("named_photo", user)
        os.makedirs(new_folder, exist_ok=True)
        new_path = os.path.join(new_folder, raw_input + ext)

        if os.path.exists(new_path):
            print(f"⚠ Warning: すでに存在します: {new_path}")
            return

        print("✅ copy:", old_path, "->", new_path)
        shutil.copy2(old_path, new_path)

        # 処理済みに記録
        processed_set.add(old_path)
        with open(processed_file, "a", encoding="utf-8") as f:
            f.write(old_path + "\n")

        next_image()

    def next_image():
        nonlocal index
        index += 1
        if index < len(file_list):
            show_image()
        else:
            root.quit()

    # GUI setup
    root = Tk()
    root.title("画像コピー＋検証ツール")
    root.geometry(f"{window_size[0]}x{window_size[1]}")

    panel = Label(root)
    panel.pack(pady=10)

    label = Label(root, text="")
    label.pack()

    entry = Entry(root, width=100, font=("Arial", 16))
    entry.pack(pady=10)

    btn = Button(root, text="保存して次へ", command=rename, font=("Arial", 14))
    btn.pack()

    root.bind("<Return>", lambda event: rename())

    show_image()
    root.mainloop()

if __name__ == '__main__':
    print("入力パターン：spot_name-photo_name")

    processed = set()
    if os.path.exists("processed.txt"):
        with open("processed.txt", "r", encoding="utf-8") as f:
            for line in f:
                processed.add(line.strip())

    target_files = []
    raw_root = "raw_photo"

    for user in os.listdir(raw_root):
        user_path = os.path.join(raw_root, user)
        if not os.path.isdir(user_path):
            continue

        assert user in user_dict, \
                f"未知のユーザーです：{user}"

        for filename in os.listdir(user_path):
            if os.path.join(user_path, filename) not in processed:
                target_files.append((user, filename))

    if not target_files:
        print("処理対象の画像がありません") 
    else:
        main(target_files)

