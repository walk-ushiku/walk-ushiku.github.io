import frontmatter

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
    return post

def write(path, post):
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
