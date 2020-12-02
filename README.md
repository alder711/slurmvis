# SlurmVis

## Brief Description

This project attempts to explore the behavior of SLURM visually. Currently, the project is in the prototyping phase and consists of several parts:

1. D3.js -> A visualization library written in Javascript used to actually visualize data.
2. Webserver -> A lightweight Python webserver to serve a D3.js application.
3. Data parser -> Parses data from `qstats.sh` into JSON for use with D3.js.
4. Data Transfer Channel -> (NOT IMPLEMENTED YET) A remote channel used to gather the current state of a SLURM cluster via `qstat.sh` (e.g., SSH).
5. `qstat.sh` -> A shell script utility written by Steven Senator for parsing the output of SLURM commands into comma (and sometimes space) separated values. This is located at the SLURM cluster and is not implemented here. This is not implemented in this project.
6. SLURM cluster -> The cluster to visualize. Not implemented in this project.

## Requirements

 - Python 3.x

## Quickstart

Make sure the prerequisites are met and the environment is set up (including the Python virtual environment):

```bash
$ make prereq
```

If using a [virtual Slurm cluster](https://github.com/hpc/hpc-collab) (see below), start an SSH forwarding process:

```bash
$ make relay
```

or

```bash
$ ./relay.sh <custom-params>
```

Now start a Flask webserver on port 5000:

```bash
$ make run
```

### Using a Slurm Cluster For Data
Currently, the interface allows you to visualize several sample files pre-generated by `qstat.sh`. However, if a [virtual Slurm cluster](https://github.com/hpc/hpc-collab) is being used, the `relay.sh` script may be useful. The script runs the equivalent of a `ssh -L ...` command to forward SSH connections to the virtual cluster. Run `./relay.sh -h` for usage. The default values can be used by running `make relay`.
