#!/usr/bin/env python3
# parser.py
#
# WRITTEN: 5 Nov 2020
# AUTHOR:  Trevor Bautista
#
# The purpose of this script is to parse the results of Steven Senator's `qpat'
# Slurm queue example trace generator.

import json

ERR_INVALID_FILE = 1

def parseFile(file):
    result = {}
    with open(file,'r') as f:
        # First line = cluster's name
        curr_line = f.readline().rstrip()
        if "CLUSTERNAME" not in curr_line:
            return ERR_INVALID_FILE
        result["clustername"] = curr_line.split(' ')[-1]
        # Parse possible items in blocked queue
        qblocked = {}
        curr_line = f.readline()
        while "QUEUELENGTH" not in curr_line:
            if "JobID" in curr_line:
                curr_line = f.readline()
            jobid, reason = curr_line.split()
            qblocked[jobid] = reason
            curr_line = f.readline()
        result["qblocked"] = qblocked
        # Parse possible number of items in the blocked queue
        qlen = {}
        qlen["blocked"] = curr_line.split()[-1].rstrip()
        # Parse possible number of items in the pending queue
        qlen["pending"] = f.readline().split()[-1].rstrip()
        # Parse possible items in pending queue
        qpending = {}
        curr_line = f.readline()
        pend_headings = curr_line.split()[1:]
        curr_line = f.readline()
        while "QUEUELENGTH" not in curr_line:
            job  = curr_line.split()[0]
            qpending[job] = {}
            vals = curr_line.split()[-1].split(',')
            # This is a necessary evil, since for some reason, the current
            # version of qstats adds extra fields to the job attributes with
            # the value 'Makefile'.
            #print(f"len(pend_headings)={len(pend_headings)}, len(vals)={len(vals)}")
            vals = [ v for v in vals if v != "Makefile" ]
            #print(pend_headings)
            #print(vals)
            #print(f"len(pend_headings)={len(pend_headings)}, len(vals)={len(vals)}")
            # This must do for now, until the qstats output is fixed (TODO)
            for i in range(min(len(pend_headings), len(vals))):
                qpending[job][pend_headings[i]] = vals[i]
            curr_line = f.readline()
        result["qpending"] = qpending
        # Parse possible number of items in the running queue
        qlen["running"] = curr_line.split()[-1].rstrip()
        # Parse possible items in running queue
        qrunning = {}
        curr_line = f.readline()
        pend_headings = curr_line.split()[1:]
        curr_line = f.readline()
        while curr_line:
            job  = curr_line.split()[0]
            qrunning[job] = {}
            vals = curr_line.split()[-1].split(',')
            # This is a necessary evil, since for some reason, the current
            # version of qstats adds extra fields to the job attributes with
            # the value 'Makefile'.
            vals = [ v for v in vals if v != "Makefile" ]
            # This must do for now, until the qstats output is fixed (TODO)
            for i in range(min(len(pend_headings), len(vals))):
                qrunning[job][pend_headings[i]] = vals[i]
            curr_line = f.readline()
        #print("[DEBUG]: Final qrunning:", qrunning)
        result["qrunning"] = qrunning
        result["qlen"] = qlen

    return result

if __name__ == "__main__":
    #result = parseFile("sample-files/qpat/logs/201005.1648/2.small-short-full")
    result = parseFile("sample-files/qpat/logs/201005.1648/2.small-short-full")
    print(result)
    result_json = json.dumps(result)
    with open("testout.json", "w") as f:
        f.write(result_json)

