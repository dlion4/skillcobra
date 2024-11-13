
import logging
import queue
import threading

# Configure logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler)



class MainThreadPool:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.workers = []
        self._shutdown = False

        # Start worker threads
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker)
            worker.start()
            self.workers.append(worker)

    def _worker(self):
        while not self._shutdown:
            try:
                # Get a task from the queue and execute it
                task, args, kwargs = self.task_queue.get(timeout=1)  # Wait for a task
                try:
                    task(*args, **kwargs)
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, task, *args, **kwargs):
        """Submit a new task to the thread pool."""
        with self.lock:
            self.task_queue.put((task, args, kwargs))

    def shutdown(self):
        """Shutdown the thread pool and wait for all tasks to finish."""
        self._shutdown = True
        for worker in self.workers:
            worker.join()


# # Example usage
# def send_notification(user_id, message):
#     # Simulate sending notification (e.g., via email or SMS)
#     print(f"Sending notification to user {user_id}: {message}")
#     time.sleep(2)  # Simulate delay in sending
#     print(f"Notification sent to user {user_id}.")


# # Create the thread pool
# thread_pool = MainThreadPool(max_workers=5)
# # Submit some tasks
# for i in range(10):
#     thread_pool.submit(send_notification, user_id=i, message="You have a new message!")

# # Wait for all tasks to complete
# thread_pool.task_queue.join()

# # Shutdown the thread pool
# thread_pool.shutdown()
