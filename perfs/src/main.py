import grequests

urls = [
    'http://httpbin.org',
    'http://python-requests.org',
    'http://kennethreitz.com'
]

if __name__ == "__main__":

    timer = [3][100]
    for i in range(0, 100):
        rs = (grequests.get(u) for u in urls)
        u = 0
        for response in grequests.map(rs):
            timer[u][i] = response.elapsed.total_seconds()
            u += 1

    print(timer)

