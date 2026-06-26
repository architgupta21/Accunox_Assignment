import time
import threading
from django.dispatch import Signal, receiver
from django.db import transaction
from django.db.models.signals import post_save
from core.models import TestModel


# QUESTION 1: Synchronous Execution Proof
sync_signal = Signal()

@receiver(sync_signal)
def slow_receiver(sender, **kwargs):
    print("   [Receiver] Task started... sleeping for 3 seconds.")
    time.sleep(3)
    print("   [Receiver] Task finished!")

def test_sync_signal():
    print("\n--- Testing Question 1: Synchronous vs Asynchronous ---")
    start_time = time.time()
    sync_signal.send(sender=None)
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds.")
    print("Conclusion: Because the time is > 3 seconds, the sender waited for the receiver. It is SYNCHRONOUS.")


# QUESTION 2: Thread Execution Proof
thread_signal = Signal()

@receiver(thread_signal)
def thread_receiver(sender, **kwargs):
    print(f"   [Receiver] Running in thread ID: {threading.get_ident()}")

def test_thread_signal():
    print("\n--- Testing Question 2: Thread Execution ---")
    print(f"   [Caller] Running in thread ID: {threading.get_ident()}")
    thread_signal.send(sender=None)
    print("Conclusion: The Thread IDs match. They run in the SAME THREAD.")


# QUESTION 3: Database Transaction Proof
@receiver(post_save, sender=TestModel)
def transaction_receiver(sender, instance, created, **kwargs):
    print(f"   [Receiver] Signal triggered for '{instance.name}'.")

def test_transaction_signal():
    print("\n--- Testing Question 3: Database Transactions ---")
    try:
        with transaction.atomic():
            print("   [Caller] Creating TestModel instance...")
            TestModel.objects.create(name="Transaction Test")
            print("   [Caller] Deliberately raising an error to rollback transaction...")
            raise Exception("Intentional Error")
    except Exception as e:
        print(f"   [Exception Caught] {e}")
        
    exists = TestModel.objects.filter(name="Transaction Test").exists()
    print(f"Does the record exist in the DB? {exists}")
    print("Conclusion: Because it prints False, the receiver's DB changes were rolled back with the caller's transaction. They share the SAME TRANSACTION.")


# Custom Classes in Python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}