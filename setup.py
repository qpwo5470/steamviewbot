import os
import sys
import subprocess

from multiprocessing import Process

import time
import os



def launchTor(n):
    print('TOR %d' %i)
    command = 'tor -f /etc/tor/torrc.' + str(i)
    subprocess.check_call(command.split())


if __name__ == '__main__':
    process_count = int(input("How Many Process?"))
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'shared_preferences')
    shared = open(filename, 'w')
    shared.write(str(process_count))
    shared.close()

    if os.geteuid() == 0:
        print("We're root!")
    else:
        print("We're not root.")
        subprocess.call(['sudo', 'python3', *sys.argv])
        sys.exit()
    for i in range(process_count):
        f = open("/etc/tor/torrc.%s" % str(i), "w")
        f.write("SOCKSPort 90%s\n" % str(52 + i * 2))
        f.write("ControlPort 90%s\n" % str(53 + i * 2))
        f.write("DataDirectory /var/lib/tor%s\n" % str(i))
        f.write("HashedControlPassword 16:709DFABE7ED51F94606AE3C626FAEC7FD9E4ABCD2B999239FB5C29D200\n")
        f.write("CookieAuthentication 1\n")
        f.close()

    print('Config files created.')
    time.sleep(1)
    print('Executing tors')

    torProcess = []
    for i in range(process_count):
        torProcess.append(Process(target=launchTor, args=(i, )))
        torProcess[i].start()


    try:
        while True:
            pass
    except KeyboardInterrupt:
        for i in range(0, process_count):
            torProcess[i].join()