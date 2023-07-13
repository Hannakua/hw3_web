import time


flst = []

def factorize(nums) -> list:
    for num in nums:
        i = 1
        lst = []
        while i ** 2 <= num:
            if num % i == 0:
                lst.append(i)
                if i != num // i:
                    lst.append(num // i)
            i += 1
        lst.sort()
        flst.append(lst)
    return flst   

if __name__ == "__main__":

    nums = nums = [128, 255, 99999, 10651060, 5632145, 7836523266965412, 2314, 74102589632, 98, 123, 7532156, 127, 24, 89632]

    timeLast = time.time()

    res = factorize(nums)
    

    timeDelta = time.time() - timeLast
    td = float("{0:.6f}".format(timeDelta))
    print(res)
    print(f"Time: {td}")
    

    # print(a, b, c, d)

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


