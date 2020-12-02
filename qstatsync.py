
import paramiko


QSS_SLURM_CLSTR_HOST="localhost"
QSS_SLURM_CLSTR_PORT=4222
QSS_CLSTR_USER="trevor"
QSS_CLSTR_PASS=""
QSS_DEBUG=True
QSS_QPAT_DIR="/home/trevor/qpat"


def connectToServer():
    """ Connect to a Slurm cluster, returning the connection object
    """
    # Create SSH client object to connect and run commands with
    client = paramiko.SSHClient()
    # Load this system's host keys
    client.load_system_host_keys()
    try:
        # Connect to the server
        client.connect(QSS_SLURM_CLSTR_HOST,
                port=QSS_SLURM_CLSTR_PORT,
                username=QSS_CLSTR_USER,
                password=QSS_CLSTR_PASS)
    except:
        # Err if error
        if QSS_DEBUG:
            print(f"Error connecting to server: {QSS_CLSTR_USER}@{QSS_SLURM_CLSTR_HOST}:{str(QSS_SLURM_CLSTR_PORT)}")
        return None
    return client


def remoteExec(client, command):
    """ Run a remote command, blocking until it returns and returning
        exit status, stdin, stdout, and stderr
    """
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    return exit_status, stdin, stdout, stderr


def getNewData(filename):
    """ Generate new data from qstats, returning the data for the logs
        given by filename
    """
    new_data = None
    # Make new SSH connection
    client = connectToServer()
    # Gen next date folder to query after call to make
    _, _, stdout, _ = remoteExec(client, "date +%y%m%d.%H%M")
    next_qstat_logdir = stdout.readline().strip("\n")
    # Make new data
    exit_status, stdin, stdout, stderr = remoteExec(client, "cd " + \
            QSS_QPAT_DIR + \
            " ; make")
    if exit_status == 0:
        new_data = ""
        # Get new data
        exit_status, stdin, stdout, stderr = remoteExec(client, 
                "cat " + \
                QSS_QPAT_DIR + \
                "/logs/" + \
                next_qstat_logdir + \
                "/" + \
                filename)
        for line in stdout:
            new_data += line

    client.close()
    return new_data
