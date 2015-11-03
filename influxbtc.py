import schedule
import time
import os

#TODO make this thing a daemon
#import sys
#import grp
#import signal
#import daemon
#import lockfile

#from spam import (
#    initial_program_setup,
#    main,
#    program_cleanup,
#    reload_program_config,
#    )

#context = daemon.DaemonContext(
#    working_directory='.',
#    umask=0o002,
#    pidfile=lockfile.FileLock('./influxbtc.pid'),
#    )

#context.signal_map = {
#    signal.SIGTERM: program_cleanup,
#    signal.SIGHUP: 'terminate',
#    signal.SIGUSR1: reload_program_config,
#    }

#mail_gid = grp.getgrnam('mail').gr_gid
#context.gid = mail_gid

#important_file = open('spam.data', 'w')
#interesting_file = open('eggs.data', 'w')
#context.files_preserve = [important_file, interesting_file]

#initial_program_setup()

#with context:
#    main()

def main():
    config = __import__('config')
    
    sys.path.append('./accumulators/perpetual/')
    list = os.listdir('./accumulators/perpetual')
    
    modules = []
    for item in list:
        name = item.partition('.')[0]
        if name not in modules:
            modules.append(name)
    
    for item in modules:
        print "Loading module " + item
        module = __import__(item)
        module.init(config)
        
    while True: #TODO make this a daemon
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
    
    