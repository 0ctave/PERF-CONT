import grequests
import matplotlib.pyplot as plt

from custom_time import timeit

urls = {
    '4services':'http://localhost:8000',
    '9services':'http://localhost:8001',
    '9services_lc':'http://localhost:8002',
}

@timeit(verbose=False)
def getX(url,nb):
    """
    It creates a generator that will create nb requests to the url passed as argument
    
    Args:
      url: the url to be requested
      nb: number of requests
    """
    rs = (grequests.get(url) for _ in range(nb))
    grequests.map(rs)


def compareTimes(url):
    """
    It takes a url as input and returns a list of the execution times for the function getX for
    different values of n
    
    Args:
      url: the url of the website you want to test
    
    Returns:
      A list of the execution times for each n in N.
    """
    N = [x**3 for x in range(1,10)]
    execution_times = [getX(url,n) for n in N]
    return N,execution_times
  
def main():
    """
    It gets the times for the 4 services and 9 services, and then plots them
    """
    print("Getting times for 4 services being loadbalanced")
    N,T = compareTimes(urls['4services'])
    print("Done.")

    print("Getting times for 9 services being loadbalanced")
    N2,T2 = compareTimes(urls['9services'])
    print("Done.")

    print("Getting times for 9 services being loadbalanced w/ least-conn algorithm")
    N3,T3 = compareTimes(urls['9services_lc'])
    print("Done.")
    
    # Plotting things
    plt.plot(N,T,label="4")
    plt.plot(N,T2,label="9")
    plt.plot(N,T3,label="9 least_conn")

    plt.ylabel('ellapsed time')
    plt.yscale('linear')
    plt.legend(loc='upper left')

    plt.show()



if __name__ == '__main__':
    main()