import logging
import queue
import threading

# Set up logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DatabaseInsertionThreadPool:
    def __init__(self, max_workers=5, database_connection=None):
        self.max_workers = max_workers
        self.database_connection = database_connection
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.workers = []
        self._shutdown = False
        # start the worker threads
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker)
            worker.start()
            self.workers.append(worker)

    def _worker(self):
        while not self._shutdown:
            # get a task from the queue and execute it
            try:
                task, args, kwargs = self.queue.get(timeout=1)
                try:
                    task(*args, **kwargs)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                continue

    def submit(self, task, *args, **kw):
        """submit a task to the thread pool"""
        with self.lock:
            self.queue.put((task, args, kw))

    def shutdown(self):
        """shutdown the thread pool"""
        with self.lock:
            self._shutdown = True
            self.queue.join()
            for worker in self.workers:
                worker.join()
