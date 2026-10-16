from pathlib import Path
import subprocess
import pandas as pd
from datetime import datetime

message = datetime.now().strftime(
    "Student robots %Y-%m-%d %H:%M"
)

ROOT = Path(__file__).resolve().parents[1]

HPC = "kaiolae@fox.educloud.no"

REMOTE_PROJECT = "~/IN5490-evogym-builder"

EVOGYM_PATH = "~/evogym-bayesian-optimization"

SLURM_FILE = "in5490-job.sbatch"


def run(cmd, cwd=None):
    print(">", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


print("Downloading student robots...")
run(["python", "scripts/download_students.py"], cwd=ROOT)

print("Committing...")

run(["git", "remote", "set-url", "origin", "https://github.com/kaiolae/kaiSoftRobots.git"], cwd=ROOT)

run(
    ["git", "pull", "origin", "main", "--allow-unrelated-histories"],
    cwd=ROOT,
)

run(["git", "add", "experiments/robots.json"], cwd=ROOT)


run(
    [
        "git",
        "commit",
        "-m",
        message,
    ],
    cwd=ROOT,
)



print("Pushing...")

run(["git", "push"], cwd=ROOT)

print("Running on HPC...")

remote = f"""
cd {REMOTE_PROJECT}
git pull
cd {EVOGYM_PATH}
sbatch {SLURM_FILE}
"""

run(["ssh", HPC, remote])

print("Finished!")
