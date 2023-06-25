import psutil

def kill_process(p_name):
    # Get all the running processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):

        # Check if the process matches the process name provided and terminate it
        if 'python3' in proc.name() and len(proc.cmdline()) > 1 and p_name in proc.cmdline()[1]:

            # Terminate the process and all its child processes
            proc.terminate()
            #psutil.wait_procs(proc.children(recursive=True))
            print(f"The {p_name} process and all its child processes have been terminated.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--processname', help='Name of the process to be killed', default='pv-charging')
    args = parser.parse_args()

    kill_process(args.processname)