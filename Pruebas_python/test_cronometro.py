import time
import threading

def met():
    initial = time.time()

    while(True):

        actual = time.time() - initial

        actual_int = int(actual)

        time.sleep(0.01)
        print(actual)
        print(actual_int)




t1 = threading.Thread(target=met)
t1.start()
