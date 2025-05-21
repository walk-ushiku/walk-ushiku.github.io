import os
import glob
from tkinter import *
from PIL import Image, ImageTk

max_size = (600, 600)
window_size = (800, 800)

def resize_by_longest_edge(img, max_length):
    w, h = img.size
    if w >= h:
        scale = max_length / float(w)
    else:
        scale = max_length / float(h)
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.LANCZOS)


def main(folders):
    if isinstance(folders, str):
        folders = [folders]  # 単一フォルダでもリスト化

    all_files = []
    file_map = []

    # 全フォルダから画像ファイルを収集
    for folder in folders:
        files = [f for f in os.listdir(folder) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
        for f in files:
            all_files.append(f)
            file_map.append((folder, f))

    if not all_files:
        print("画像が見つかりません。")
        return

    index = 0

    def show_image():
        nonlocal index
        folder, filename = file_map[index]
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path)
        img = resize_by_longest_edge(img, min(max_size))
        photo = ImageTk.PhotoImage(img)
        panel.config(image=photo)
        panel.image = photo
        entry.delete(0, END)
        label.config(text=f"{filename} ({index+1}/{len(file_map)})\n{folder}")

    def rename():
        nonlocal index
        basename = entry.get().strip()
        folder, old_name = file_map[index]
        old_path = os.path.join(folder, old_name)
        _, ext = os.path.splitext(old_name)

        if basename:
            new_path = os.path.join(folder, basename + ext)
            if os.path.exists(new_path):
                print("Warning: Path exists.")
                return
            print("rename:", os.path.basename(old_path), "->", os.path.basename(new_path))
            os.rename(old_path, new_path)

        index += 1
        if index < len(file_map):
            show_image()
        else:
            root.quit()

    # GUI setup
    root = Tk()
    root.title("複数フォルダ対応画像リネームツール")
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
    folders = glob.glob("raw_photo/*/*")
    main(folders)

