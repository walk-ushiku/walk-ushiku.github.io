import glob

for f in glob.glob("*/*.mdx"):
    content = open(f, "r").read()
    if "contributor_id" not in content:
        cid = f.split("/")[0]
        content = content.replace(
            "\n---",
            "\n" + 
            "contributor_id: " + cid + "\n" + 
            "---",
        )
        with open(f, "w") as f:
            print(content, end="", file=f)
