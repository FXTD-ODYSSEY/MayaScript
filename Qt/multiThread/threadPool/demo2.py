# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/15675043/multiprocessing-and-gui-updating-qprocess-or-multiprocessing
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-10-29 16:21:57'


from multiprocessing import Process, Queue
from PySide2 import QtCore
# from MyJob import job_function


# Runner lives on the runner thread

class Runner(QtCore.QObject):
    """
    Runs a job in a separate process and forwards messages from the job to the
    main thread through a pyqtSignal.

    """

    msg_from_job = QtCore.Signal(object)

    def __init__(self, start_signal):
        """
        :param start_signal: the pyqtSignal that starts the job

        """
        super(Runner, self).__init__()
        self.job_input = None
        start_signal.connect(self._run)

    def run(self,queue,job_input):
        queue.put(job_input)
        print('run')
    
    def _run(self):
        queue = Queue()
        p = Process(target=self.run, args=(queue, self.job_input))
        p.start()
        while True:
            msg = queue.get()
            self.msg_from_job.emit(msg)
            if msg == 'done':
                break


# Things below live on the main thread

def run_job(input):
    """ Call this to start a new job """
    runner.job_input = input
    runner_thread.start()


def handle_msg(msg):
    print(msg)
    if msg == 'done':
        runner_thread.quit()
        runner_thread.wait()


# Setup the OQ listener thread and move the OQ runner object to it
runner_thread = QtCore.QThread()
runner = Runner(start_signal=runner_thread.started)
runner.msg_from_job.connect(handle_msg)
runner.moveToThread(runner_thread)

run_job('test')
print("done")