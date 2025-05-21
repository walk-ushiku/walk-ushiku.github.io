import os
import subprocess as sp
from tqdm import tqdm

in_dir = "../raw"
out_dir = "../"

for fname in tqdm(os.listdir(in_dir)):
    cmd = " ".join([
        "convert",
        os.path.join(in_dir, fname),
        "-resize",
        "128x128",
        os.path.join(out_dir, fname)
    ])
    sp.run(cmd, shell=True)



