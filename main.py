from fastapi import FastAPI
import os
import subprocess
from datetime import datetime

app = FastAPI()

@app.get("/")
async def read_root():
    # Get Git Commit
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

    # Get Git Tag
    git_tag = subprocess.check_output(["git", "tag", "-l", "--sort=-creatordate", "--format=%(refname:short)", "v*"]).decode().strip().split("\n")[0]

    # Get Git Build Date
    git_build_date = subprocess.check_output(["git", "log", "-1", "--format=%ct"]).decode().strip()
    git_build_date_formatted = datetime.utcfromtimestamp(int(git_build_date)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Set environment variables
    os.environ["GIT_COMMIT"] = git_commit
    os.environ["GIT_TAG"] = git_tag
    os.environ["GIT_BUILD_DATE"] = git_build_date_formatted

    return {
        "message": "FastAPI with Git Info",
        "git_commit": git_commit,
        "git_tag": git_tag,
        "git_build_date": git_build_date_formatted,
    }
