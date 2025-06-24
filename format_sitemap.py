from pathlib import Path
import xml.dom.minidom

# 入力ファイルと出力ファイルのパス
input_path = Path("sitemap-0.xml")
output_path = Path("sitemap-manual.xml")

# ファイルが存在するかチェック
if not input_path.exists():
    print(f"❌ 入力ファイルが見つかりません: {input_path.resolve()}")
    exit(1)

# sitemap.xml を読み込む
with input_path.open(encoding="utf-8") as f:
    raw_xml = f.read()

# 整形処理
try:
    dom = xml.dom.minidom.parseString(raw_xml)
    pretty_xml = dom.toprettyxml(indent="  ")

    # 整形後の内容を書き出し
    with output_path.open("w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"✅ 整形済みの sitemap を保存しました: {output_path.resolve()}")

except Exception as e:
    print(f"❌ XML の整形中にエラーが発生しました: {e}")

