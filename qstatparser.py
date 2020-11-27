#!/usr/bin/env python3
# qstatparser.py
#
# WRITTEN: 5 Nov 2020
# AUTHOR:  Trevor Bautista
#
# The purpose of this script is to parse the results of Steven Senator's `qpat'
# Slurm queue example trace generator.

import json

ERR_INVALID_FILE = 1


def parseFileDict(file):
    """ Take a qstats log file and parse it into a Python dictionary.
    """
    result = {}
    with open(file,'r') as f:
        # First line = cluster's name
        curr_line = f.readline().rstrip()
        # Err if first line not valid
        if "CLUSTERNAME" not in curr_line:
            return ERR_INVALID_FILE
        result["clustername"] = curr_line.split(' ')[-1]
        #
        # Parse possible items in blocked queue
        #
        qblocked = []
        curr_line = f.readline()
        # Until we reach a qblocked QUEUELENGTH line,
        while "QUEUELENGTH" not in curr_line:
            # Placeholder for current job
            curr_job = {}
            # If heading line, read the next line (since we know the headers already)
            if "JobID" in curr_line:
                curr_line = f.readline()
            # Parse the current job's attributes
            jobid, reason = curr_line.split()
            curr_job["JobId"] = jobid
            curr_job["Reason"] = reason
            # Add current job to blocked queue
            qblocked.append(curr_job)
            curr_line = f.readline()
        result["qblocked"] = qblocked
        #
        # Parse possible number of items in the blocked queue
        #
        qlen = {}
        qlen["blocked"] = curr_line.split()[-1].rstrip()
        #
        # Parse possible number of items in the pending queue
        #
        qlen["pending"] = f.readline().split()[-1].rstrip()
        #
        # Parse possible items in pending queue
        #
        qpending = []
        # If we counted any jobs in this queue,
        if int(qlen["pending"]) > 0:
            # Read in the header line
            curr_line = f.readline()
            # Parse the headers
            pend_headings = curr_line.split()[1:]
            # Read next possible job line
            curr_line = f.readline()
            # Until we reach the qrunning QUEUELENGTH line,
            while "QUEUELENGTH" not in curr_line:
                # Placeholder dictionary for current parsed job
                curr_job = {}
                # Get the job ID (since it is space separated)
                vals = [ curr_line.split()[0] ]
                # Get the rest of the (comma separated) values
                vals.extend(curr_line.split()[-1].split(','))
                # This is a necessary evil, since for some reason, the current
                # version of qstats adds extra fields to the job attributes with
                # the value 'Makefile'.
                vals = [ v for v in vals if v != "Makefile" ]
                # Parse keys/values of job attributes
                # This must do for now (the min()), until the qstats output is fixed (TODO)
                for i in range(min(len(pend_headings), len(vals))):
                    curr_job[pend_headings[i]] = vals[i]
                # Add job to pending queue
                qpending.append(curr_job)
                # Read next potential job line
                curr_line = f.readline()
        # Add all parsed pending jobs to the qpending queue
        result["qpending"] = qpending
        #
        # Parse possible number of items in the running queue
        #
        qlen["running"] = curr_line.split()[-1].rstrip()
        qrunning = []
        # If we counted any jobs in this queue,
        if int(qlen["running"]) > 0:
            # Parse possible items in running queue
            curr_line = f.readline()
            pend_headings = curr_line.split()[:]
            curr_line = f.readline()
            while curr_line:
                curr_job = {}
                vals = [ curr_line.split()[0] ]
                vals.extend(curr_line.split()[-1].split(','))
                # This is a necessary evil, since for some reason, the current
                # version of qstats adds extra fields to the job attributes with
                # the value 'Makefile'.
                vals = [ v for v in vals if v != "Makefile" ]
                # This must do for now, until the qstats output is fixed (TODO)
                for i in range(min(len(pend_headings), len(vals))):
                    curr_job[pend_headings[i]] = vals[i]
                qrunning.append(curr_job)
                curr_line = f.readline()
        # Add running queue to main data structure
        result["qrunning"] = qrunning
        # Add queue lengths to main data structure
        result["qlen"] = qlen

    return result


def parseFilename(infile, outfile):
    result = parseFileDict("sample-files/qpat/logs/" + infile)
    result_json = json.dumps(result)
    with open("static/" + outfile, "w") as f:
        f.write(result_json)


if __name__ == "__main__":
    #result = parseFile("sample-files/qpat/logs/201005.1648/2.small-short-full")
    result = parseFileDict("sample-files/qpat/logs/201005.1648/5.large-head-long-small-tail-backfill-gap-filled-jobs-running")
    print(result)
    result_json = json.dumps(result)
    with open("static/testout.json", "w") as f:
        f.write(result_json)

