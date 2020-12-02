#!/usr/bin/env bash
# vim: et:sw=4:ts=4
read -r -d '' USAGE << EOI
Usage:

$0 proxied-target [[[[[proxied-target] proxy] local-port] dest-port] user]

    Initiates an ssh-forwarded connection to host proxied-target through host
    proxy through local port local-port. If no arguments, the default values
    are:

        proxied-target: vclogin
        proxy:          trevslurm
        local-port:     4222
        dest-port:      22
        user:           trevor

    The constructed command will look like:

        ssh -L local-port:proxied-target:dest-port user@proxy cat

    Parameters:

        proxied-target Host reachable by proxy. This is the ultimate
                       destination.

        proxy          Host to proxy ssh connection connection will be:
                       local <-> proxy <-> proxied-target

        local-port     Port to bind locally. Connection is initiated through
                       this port.

        dest-port      Port to connect with to proxied-target.

        user           Username to connect with.
EOI

if [ "$1" = "-h" -o "$1" = "--help" ]; then
    echo "$USAGE"
    exit 0
fi

proxied_target=${1:-"vclogin"}
proxy=${2:-"trevslurm"}
local_port=${3:-4222}
dest_port=${4:-22}
user=${5:-"trevor"}

ssh -L ${local_port}:${proxied_target}:${dest_port} ${user}@${proxy} cat
res=$?
if [ $res != 0 ]; then
    echo "$USAGE"
    exit 1
fi
