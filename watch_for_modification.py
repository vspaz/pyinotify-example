import multiprocessing

import pyinotify


def worker(watched_path):
    def on_close():
        pass

    def update_something():
        pass

    def check_status():
        pass

    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            # it's better to watch if writable file was closed after being modified.
            # otherwise multiple events might be triggered if we use IN_MODIFY.
            on_close()
            update_something()
            check_status()

    event_handler = EventHandler()
    manager = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(manager, event_handler)
    # rec=False means watch only the current directory exluding nested dirs.
    manager.add_watch(watched_path, pyinotify.IN_CLOSE_WRITE, rec=False)
    notifier.loop()


if __name__ == "__main__":
    path = "/path/to/required/dir"
    # watch in a separate process.
    proc = multiprocessing.Process(target=worker, args=(path, ))
    proc.start()
