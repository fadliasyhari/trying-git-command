import unittest
from fastapi import FastAPI
import os
import subprocess
from datetime import datetime

app = FastAPI()

@app.get("/")
async def read_root():
    # run git commands to get info
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except subprocess.CalledProcessError:
        git_commit = ""
    
    try:
        git_tag = subprocess.check_output(["git", "tag", "-l", "--sort=-creatordate", "--format=%(refname:short)", "v*"]).decode().strip().split("\n")[0]
    except subprocess.CalledProcessError:
        git_tag = ""
    
    try:
        git_build_date = subprocess.check_output(["git", "log", "-1", "--format=%ct"]).decode().strip()
        git_build_date = datetime.utcfromtimestamp(int(git_build_date)).strftime('%Y-%m-%dT%H:%M:%S.%dZ')
    except (subprocess.CalledProcessError, ValueError):
        git_build_date = ""

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

if __name__ == "__main__":
    print("\n*** EXECUTING UNIT TEST ***")
    unittest.main(module='test_module', verbosity=2, exit=False)
    print("*** UNIT TEST EXECUTED ***\n")
    
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080, reload=True)#, log_level="critical")
