#!/usr/bin/env python3
import copy
import random
from datetime import datetime, timedelta

JOBID_START = 100200
JOBID_END   = 199999

JSON_TEMPLATE = {
    "clustername": "",
    "qlen": {
        "blocked": 0,
        "pending": 0,
        "running": 0
    },
    "qblocked": {},
    "qpending": {},
    "qrunning": {}
}




def genRunJobs(n, clstr_name="vc", data=None):
    """! Generate JSON corresponding to having jobs in the run queue.

    Specifically, generate JSON that includes various jobs with random
    data in .qrunning.

    @param n          Number of jobs to create.
    @param clstr_name Name of the cluster.
    @param data       Optional existing JSON to modify
    """
    # Get initial JSON to work with
    result = data
    if not data:
        result = copy.deepcopy(JSON_TEMPLATE)

    for job in range(n):
        jobid_s = str(random.randint(JOBID_START, JOBID_END))
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = "{:>04}-{:>02}-{:>02}T{:>02}:{:>02}:{:>02}".format(
                yesterday.year,
                yesterday.month,
                yesterday.day,
                yesterday.hour,
                yesterday.minute,
                yesterday.second)
        accrue_time = yesterday
        accrue_time_str = yesterday_str
        start_time = yesterday + timedelta(seconds=1)
        start_time_str = "{:>04}-{:>02}-{:>02}T{:>02}:{:>02}:{:>02}".format(
                start_time.year,
                start_time.month,
                start_time.day,
                start_time.hour,
                start_time.minute,
                start_time.second)
        end_time = start_time + timedelta(
                seconds=random.randint(0,60))
        end_time_str = "{:>04}-{:>02}-{:>02}T{:>02}:{:>02}:{:>02}".format(
                end_time.year,
                end_time.month,
                end_time.day,
                end_time.hour,
                end_time.minute,
                end_time.second)
        preempt_eligible_time = start_time + timedelta(minutes=30)
        preempt_eligible_time_str = "{:>04}-{:>02}-{:>02}T{:>02}:{:>02}:{:>02}".format(
                preempt_eligible_time.year,
                preempt_eligible_time.month,
                preempt_eligible_time.day,
                preempt_eligible_time.hour,
                preempt_eligible_time.minute,
                preempt_eligible_time.second)
        result["qrunning"][jobid_s] = {}
        result["qrunning"][jobid_s]["JobName"]             = "randjob" + str(job)
        result["qrunning"][jobid_s]["UserId"]              = "randuser(1000)"
        result["qrunning"][jobid_s]["GroupId"]             = "randuser(1000)"
        result["qrunning"][jobid_s]["MCS_label"]           = "N/A"
        result["qrunning"][jobid_s]["Priority"]            = 1440
        result["qrunning"][jobid_s]["Nice"]                = 0
        result["qrunning"][jobid_s]["Account"]             = "default" 
        result["qrunning"][jobid_s]["QOS"]                 = "normal"
        result["qrunning"][jobid_s]["WCKey"]               = "randjob"
        result["qrunning"][jobid_s]["JobState"]            = "RUNNING"
        result["qrunning"][jobid_s]["Reason"]              = "None"
        result["qrunning"][jobid_s]["Dependency"]          = "(null)"
        result["qrunning"][jobid_s]["Requeue"]             = 1
        result["qrunning"][jobid_s]["Restarts"]            = 0
        result["qrunning"][jobid_s]["BatchFlag"]           = 1
        result["qrunning"][jobid_s]["Reboot"]              = 0
        result["qrunning"][jobid_s]["ExitCode"]            = "0:0"
        result["qrunning"][jobid_s]["Runtime"]             = "00:00:{:>02}".format(random.randint(0,10))
        result["qrunning"][jobid_s]["TimeLimit"]           = "00:01:00"
        result["qrunning"][jobid_s]["TimeMin"]             = "N/A"
        result["qrunning"][jobid_s]["SubmitTime"]          = yesterday_str
        result["qrunning"][jobid_s]["EligibleTime"]        = result["qrunning"][jobid_s]["SubmitTime"]
        result["qrunning"][jobid_s]["AccrueTime"]          = accrue_time_str
        result["qrunning"][jobid_s]["StartTime"]           = start_time_str
        result["qrunning"][jobid_s]["EndTime"]             = end_time_str
        result["qrunning"][jobid_s]["Deadline"]            = "N/A"
        result["qrunning"][jobid_s]["PreemptEligibleTime"] = preempt_eligible_time_str
        result["qrunning"][jobid_s]["PreemptTime"]         = "None"
        result["qrunning"][jobid_s]["SuspendTime"]         = "None"
        result["qrunning"][jobid_s]["SecsPreSuspend"]      = 0 
        result["qrunning"][jobid_s]["LastSchedEval"]       = start_time_str
        result["qrunning"][jobid_s]["Partition"]           = "shared"
        result["qrunning"][jobid_s]["AllocNode:Sid"]       = "vclogin:29061"
        result["qrunning"][jobid_s]["RegNodeList"]         = "(null)"
        result["qrunning"][jobid_s]["ExcNodeList"]         = "(null)"
        result["qrunning"][jobid_s]["NodeList"]            = "vc1"
        result["qrunning"][jobid_s]["BatchHost"]           = "vc1"
        result["qrunning"][jobid_s]["NumNodes"]            = 1
        result["qrunning"][jobid_s]["NumCPUs"]             = 1
        result["qrunning"][jobid_s]["NumTasks"]            = 1
        result["qrunning"][jobid_s]["CPUs/Task"]           = 1
        result["qrunning"][jobid_s]["RegB:S:C:T"]          = "0:0:*:*"
        result["qrunning"][jobid_s]["TRES"]                = 1
        # TODO: Finish this when rest of fields are known

    return result

if __name__ == "__main__":
    data = genRunJobs(10)
    print(data)
