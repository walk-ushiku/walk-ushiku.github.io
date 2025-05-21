import os
import subprocess
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import re

input_root = Path("./raw_photo")
output_image_dir = Path("../public/images/photos")
output_mdx_dir = Path("../src/content/photo_pages/")
template_path = Path("template.mdx")

# 読み込みテンプレート
template_text = template_path.read_text()

output_ext = "jpg"

# exiftoolからlat/lngを抽出
def get_gps_info(img_path):
    try:
        lat = subprocess.check_output(["exiftool", "-n", "-GPSLatitude", str(img_path)])
        lon = subprocess.check_output(["exiftool", "-n", "-GPSLongitude", str(img_path)])
        lat = lat.decode().strip().split(": ")[-1]
        lon = lon.decode().strip().split(": ")[-1]
        if lat and lon:
            return lat, lon
    except subprocess.CalledProcessError:
        pass
    return None, None

# 出力ファイル名とrelated_placeを決める
def parse_filename(original_name):
    name = original_name
    related_place = None
    if name[0] in ["-", "_"]:
        name = name[1:]
    elif "-" in name:
        related_place = name.split("-")[0]
    return name, related_place

def convert_image(input_path, output_path):
    with Image.open(input_path) as img:
        width, height = img.size
        if width >= height:
            new_width = 1080
            new_height = int((1080 / width) * height)
        else:
            new_height = 1080
            new_width = int((1080 / height) * width)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        resized_img.save(output_path, quality=70, optimize=True)

def create_mdx(filename_base, image_ext, contributor, related_place, lat, lon):
    mdx_path = output_mdx_dir / f"{filename_base}.mdx"
    mdx_path.parent.mkdir(parents=True, exist_ok=True)

    image_filename = f"{filename_base}.{image_ext}"

    # テンプレート読み込み
    text = template_text.replace("HOGEHOGE", image_filename)
    text = text.replace("調査中", contributor)

    # フロントマターを分解
    match = re.match(r'(?s)^---\n(.*?)\n---\n(.*)$', text)
    if not match:
        print(f"テンプレートのフロントマターが不正: {mdx_path}")
        return

    frontmatter, body = match.groups()
    lines = frontmatter.strip().splitlines()

    # 追記対象
    if related_place:
        lines.append(f"related_place: {related_place}")
    if lat and lon:
        lines.append(f"lat: {lat}")
        lines.append(f"lng: {lon}")

    # 再構築
    new_frontmatter = "\n".join(lines)
    new_text = f"---\n{new_frontmatter}\n---\n{body}"

    with open(mdx_path, "w", encoding="utf-8") as f:
        f.write(new_text)

    print(f"mdx生成完了: {mdx_path}")

def get_img_items(user_dir):
    valid_exts = [".jpg", ".jpeg", ".png", ".jpg_large", ".jfif"]
    contributor = user_dir.name
    items = []

    for entry in user_dir.iterdir():
        if entry.is_file():
            img_path = entry
            if img_path.suffix.lower() not in valid_exts:
                continue

            base_name = img_path.stem
            new_name, related_place = parse_filename(base_name)
            output_img_path = output_image_dir / f"{new_name}.{output_ext}"

            items.append({
                "img_path": img_path,
                "output_img_path": output_img_path,
                "new_name": new_name,
                "related_place": related_place,
                "contributor": contributor,
            })

        elif entry.is_dir():
            related_place = entry.name
            if related_place.lower() in ["null", "_", "none"]:
                related_place = None

            for img_path in entry.iterdir():
                if not img_path.is_file() or img_path.suffix.lower() not in valid_exts:
                    continue

                base_name = img_path.stem
                joined_name = base_name if related_place is None else f"{related_place}-{base_name}"
                new_name, _ = parse_filename(joined_name)
                output_img_path = output_image_dir / f"{new_name}.{output_ext}"

                items.append({
                    "img_path": img_path,
                    "output_img_path": output_img_path,
                    "new_name": new_name,
                    "related_place": related_place,
                    "contributor": contributor,
                })

    return items


# メイン処理
for user_dir in input_root.iterdir():
    if not user_dir.is_dir():
        continue
    user = user_dir.name
    print("user:", user)

    img_items = get_img_items(user_dir)

    for img_item in tqdm(img_items):
        # 変数を読み込み
        img_path = img_item["img_path"]
        output_img_path = img_item["output_img_path"]
        new_name = img_item["new_name"]
        related_place = img_item.get("related_place", None)
        assert user == img_item["contributor"]

        output_filename = f"{new_name}.{output_ext}"

        # 画像出力先
        output_img_path = output_image_dir / output_filename
        output_img_path.parent.mkdir(parents=True, exist_ok=True)

        # ダウンサンプリング
        convert_image(img_path, output_img_path)

        # EXIF GPS抽出
        lat, lon = get_gps_info(img_path)

        # mdx作成
        create_mdx(new_name, output_ext, user, related_place, lat, lon)

print("すべて完了！")

