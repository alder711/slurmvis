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
        #
        # Parse possible number of items in the blocked queue
        #
        # NOTE: Parsed queue lengths are not used. Instead, we calculate them.
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
            pend_headings = curr_line.split()[:]
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

        #
        # Remove duplicate job entries
        #
        # Interestingly, qstats just spits out job information as it is available,
        # so jobs in the running queue will most likely also be in the pending
        # queue as well, according to qstats, which is incorrect. Thus, we must
        # fix this here.
        # Get IDs of running jobs
        qpending_real = []
        # For each pending job,
        for pendjob in qpending:
            duplicate=False
            # For each running job,
            for runjob in qrunning:
                # See if running job is in pending queue
                if pendjob["JobId"] == runjob["JobId"]:
                    duplicate=True
            # If current running job is in pending queue,
            if not duplicate:
                # Add it to real pending queue
                qpending_real.append(pendjob)
        qblocked_real = []
        # For each blocked job,
        for blockjob in qblocked:
            duplicate_running=False
            duplicate_pending=False
            # For each running job,
            for runjob in qrunning:
                # See if running job is in blocked queue
                if blockjob["JobId"] == runjob["JobId"]:
                    duplicate_running=True
            for pendjob in qpending:
                # See if pending job is in blocked queue
                if blockjob["JobId"] == pendjob["JobId"]:
                    duplicate_pending=True
            # If current running job is in pending queue,
            if not duplicate_running and not duplicate_pending:
                # Add it to real pending queue
                qblocked_real.append(blockjob)
        # Recalculate queue lengths
        qlen["blocked"] = len(qblocked_real)
        qlen["pending"] = len(qpending_real)
        qlen["running"] = len(qrunning)

        # Add all parsed blocked jobs to the qblocked queue
        result["qblocked"] = qblocked_real
        # Add all parsed pending jobs to the qpending queue
        result["qpending"] = qpending_real
        # Add running queue to main data structure
        result["qrunning"] = qrunning
        # Add queue lengths to main data structure
        result["qlen"] = qlen

    return result


def parseFileToFile(infile, outfile):
    """ Parse the contents of infile as a qstat logfile into json,
        writing into outfile.
    """
    result = parseFileDict("sample-files/qpat/logs/" + infile)
    result_json = json.dumps(result)
    with open("static/" + outfile, "w") as f:
        f.write(result_json)


def parseFile(infile):
    """ Parse the contents of infile as a qstat logfile into json,
        returning the result.
    """
    return json.dumps(parseFileDict("sample-files/qpat/logs/" + infile))


if __name__ == "__main__":
    #result = parseFile("sample-files/qpat/logs/201005.1648/2.small-short-full")
    result = parseFileDict("sample-files/qpat/logs/201005.1648/5.large-head-long-small-tail-backfill-gap-filled-jobs-running")
    print(result)
    result_json = json.dumps(result)
    with open("static/testout.json", "w") as f:
        f.write(result_json)

