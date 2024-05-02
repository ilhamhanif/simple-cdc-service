import subprocess
import os

gh_url = subprocess.Popen("git config --get remote.origin.url".split(), stdout=subprocess.PIPE).communicate()[0].decode().replace("\n", "").strip()
gh_url = gh_url.replace(".git", "")
script_dir = os.path.dirname(__file__)

new_lines = []
with open("README.md", "r") as r:
    lines = r.readlines()
    for line in lines:
        line = line.replace(".png)", ".png?raw=true)")
        line = line.replace("(./", f"({gh_url}/blob/main/")
        line = line.replace("<br>", "")
        new_lines.append(line)

gist_dir = os.path.join(script_dir, "docs", "gist")
if not os.path.exists(gist_dir):
    os.makedirs(gist_dir)

with open(os.path.join(gist_dir, "README-med.md"), "w") as w:
    w.writelines(new_lines)
