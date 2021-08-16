import time


def add_execution_time(func):

    def wrapper(*args, **kwargs):
        start_time = time.time()

        output = func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if type(output) == dict:
            output |= {
                'time': elapsed_time,
            }

        return output

    return wrapper

