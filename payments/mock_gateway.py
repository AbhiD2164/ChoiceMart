import time
import random


def process_payment():

    # simulate payment gateway processing
    processing_time = random.randint(1, 7)

    time.sleep(processing_time)

    if processing_time > 5:
        return False
    else:
        return True