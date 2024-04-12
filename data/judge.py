"""
Azukiiro Glue Judger Script (Python3)
Special environment variables:
- GLUE_PROBLEM_DATA: problem data file
- GLUE_SOLUTION_DATA: solution data file
- GLUE_REPORT: write status report to this file
- GLUE_DETAILS: write detailed report to this file

However, as in problem.yml, there will be two directories in cwd:
- problem: unzipped problem data
- solution: unzipped solution data
So you do not need to read GLUE_PROBLEM_DATA and GLUE_SOLUTION_DATA.

GLUE_REPORT supports the following status:
- score=<score>
  - score: float (0 <= score <= 100)
  - The current score of the solution
- status=<status>
  - status: str
  - The current status of the solution
  - A short phrase describing the status
  - Eg. Accepted, Wrong Answer, Runtime Error
- message=<message>
  - message: str
  - A brief message to the user about the judge
  - Eg. Running on case 1
- metrics=<metrics>
  - metrics: Dict[str, float]
  - A dictionary of metrics to be displayed in the report
  - Suggestions: cpu, mem
- commit
  - Commit the current status to the report

GLUE_DETAILS should be a json file defined as https://github.com/fedstackjs/azukiiro/blob/main/common/solution.go:
"""

import json
import os
import subprocess
from time import perf_counter
from typing import Dict, TypedDict

glue_report = os.getenv("GLUE_REPORT")
glue_details = os.getenv("GLUE_DETAILS")
assert glue_report is not None, "GLUE_REPORT is not set"
assert glue_details is not None, "GLUE_DETAILS is not set"

# since glue_report is a pipe, we need to open with mode "w" and disable buffering
glue_report_fp = open(glue_report, "w")
def report_raw(key: str, val: str):
  print(f"{key}={val}", file=glue_report_fp, flush=True)

def report_score(score: float):
  report_raw("score", str(score))

def report_status(status: str):
  report_raw("status", status)

def report_message(message: str):
  report_raw("message", message)

def report_metrics(metrics: Dict[str, float]):
  report_raw("metrics", json.dumps(metrics))

def commit():
  report_raw("commit", "1")

class SolutionDetailsTest(TypedDict):
  name: str
  score: float
  score_scale: float
  status: str
  summary: str

class SolutionDetailsJob(TypedDict):
  name: str
  score: float
  score_scale: float
  status: str
  tests: list[SolutionDetailsTest]
  summary: str

class SolutionDetails(TypedDict):
  version: int
  jobs: list[SolutionDetailsJob]
  summary: str

def write_details(details: SolutionDetails):
  with open(glue_details, "w") as fp:
    json.dump(details, fp)

start = perf_counter()
process = subprocess.Popen(["python3", "solution/main.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output, error = process.communicate("1\n", 1)
end = perf_counter()
time_ms = int((end - start) * 1000)

correct = output.strip() == "1"
if correct:
  report_score(100)
  report_status("Accepted")
  report_message("Correct")
  report_metrics({"cpu": time_ms})
  write_details({
    "version": 1,
    "jobs": [
      {
        "name": "main",
        "score": 100,
        "score_scale": 100,
        "status": "Accepted",
        "tests": [
          {
            "name": "main",
            "score": 100,
            "score_scale": 100,
            "status": "Accepted",
            "summary": "Correct"
          }
        ],
        "summary": "Correct"
      }
    ],
    "summary": "Correct"
  })
else:
  report_score(0)
  report_status("Wrong Answer")
  report_message("Incorrect")
  report_metrics({"cpu": time_ms})
  write_details({
    "version": 1,
    "jobs": [
      {
        "name": "main",
        "score": 0,
        "score_scale": 100,
        "status": "Wrong Answer",
        "tests": [
          {
            "name": "main",
            "score": 0,
            "score_scale": 100,
            "status": "Wrong Answer",
            "summary": "Incorrect"
          }
        ],
        "summary": "Incorrect"
      }
    ],
    "summary": "Incorrect"
  })
commit()
