import threading, time

def my_threaded_func(arg, arg2):
    print('start thread')
    time.sleep(10)
    print('done')

thread = threading.Thread(target=my_threaded_func, args=("I'ma", "thread"))
thread.start()

print('hi, iam coder')