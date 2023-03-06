#  Copyright (c) 2019-2020, Steckley & Associates
#  All rights reserved.

################################################################
# Progress
import sys
import threading

import progressbar

def synchronized_method(method):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"
    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)
    return sync_method


class ProgressBar:
    active = True

    def __init__(self):
        self.last_value = 0
        return

    @synchronized_method
    def start(self, max_value, label=""):
        __widgets = [label+'... [', progressbar.Timer(format='Elapsed: %(elapsed)s'), '] ', progressbar.Bar(), ' (', progressbar.ETA(format_finished='Took: %(elapsed)8s'), ') ', ]
        if ProgressBar.active:
            if max_value <= 0:
                max_value = progressbar.UnknownLength
            self.progress = progressbar.ProgressBar(min_value=0, max_value=max_value, widgets=__widgets).start()
            sys.stdout.flush()

    @synchronized_method
    def update(self, value=None, force=False, **kwargs):
        if ProgressBar.active:
            self.last_value = value
            self.progress.update(self.last_value, force, **kwargs)

    @synchronized_method
    def increment(self, value=1, force=False, **kwargs):
        if ProgressBar.active:
            self.last_value += value
            self.progress.update(self.last_value, force, **kwargs)


    @synchronized_method
    def finish(self, end='\n'):
        if ProgressBar.active:
            self.progress.finish(end)



################################################################

