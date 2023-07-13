import time
from multiprocessing import Pool, cpu_count


def factorize(n) -> list:
        i = 1
        lst = []
        while i ** 2 <= n:
            if n % i == 0:
                lst.append(i)
                if i != n // i:
                    lst.append(n // i)
            i += 1
        lst.sort()
        return lst   

def callback(result):
     print(result)

if __name__ == "__main__":

    nums = [128, 255, 99999, 10651060, 5632145, 7836523266965412, 2314, 74102589632, 98, 123, 7532156, 127, 24, 89632]
    
    timeLast = time.time()

    print(f'Count CPU: {cpu_count()}')

    with Pool(cpu_count()) as p:
        p.map_async(factorize, nums, callback=callback)
        p.close()
        p.join()

    timeDelta = time.time() - timeLast
    td = float("{0:.6f}".format(timeDelta))
    print(f"Time: {td}")

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
