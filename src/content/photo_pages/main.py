import os
import shutil
from tqdm import tqdm
import glob

cdict = {
    "ナト": "nato_blooming",
    "はみゅ": "hamyu044",
    "地底人かきたま": "poketc_meganest",
    "吹雪": "hubuki_ma36s",
    "ボケ人間ステークス": "sa_16807",
    "こめつぶ": "aqours_forever_",
}

def get_contributor(fname):
    cname = None
    for l in open(fname, "r").readlines():
        if l.startswith("contributor"):
            cname = l.split(":")[1]
            cname = cname.strip(" ")
            cname = cname.strip("\n")
            break

    assert cname is not None, f"contributor not found: {fname}"
    assert cname in cdict, f"unknown contributor: {cname}"

    return cname


for f in glob.glob("*.mdx"):
    cname = get_contributor(f)
    cid = cdict[cname]
    ofname = os.path.join(cid, f)

    content = open(f, "r").read()
    content = content.replace(
        "\n---",
        "\n" + 
        "contributor_id: " + cid + "\n" + 
        "---",
    )
    bname = os.path.basename(f).split(".")[0] + ".jpg"
    content = content.replace(
            bname,
            os.path.join(cid, bname)
    )

    with open(ofname, "w") as f:
        print(content, end="", file=f)


"""
for 
photo_dir = "photos"
pages_dir = "../../src/content/photo_pages"

# print(get_contributor("ibaraido-map"))
for bname in tqdm(os.listdir(photo_dir)):
    if bname.endswith(".jpg"):
        mbname, cname, cid = get_contributor(bname)

        photo_output_dir = os.path.join(photo_dir, cid)
        pages_output_dir = os.path.join(pages_dir, cid)

        os.makedirs(photo_output_dir, exist_ok=True)
        os.makedirs(pages_output_dir, exist_ok=True)

        shutil.copy(
            os.path.join(photo_dir, bname),
            os.path.join(photo_output_dir, bname)
        )

        mdx = open(os.path.join(pages_dir, mbname), "r").read()
        mdx = mdx.replace(
                "description",
                "contributor_id: " + cid + "\n" + 
                "description"
        )
        mdx = mdx.replace(
                bname,
                os.path.join(cid, bname)
        )
        with open(os.path.join(pages_output_dir, mbname), "w") as f:
            print(mdx, file=f, end="")
        
"""
