import grequests
import grpc
from concurrent import futures
from protos import movie_pb2
from protos import movie_pb2_grpc
from google.protobuf.json_format import MessageToJson
import numpy as np

import json
import time

EPOCH = 100
def call_rest():
    rs = (grequests.get("http://127.0.0.1:3001/movies/39ab85e5-5e8e-4dc5-afea-65dc368bd7ab") for i in range(EPOCH))
    times = list(map(lambda response: response.elapsed.total_seconds(),grequests.map(rs)))
    return times

def call_grpc():
    times = [0] * EPOCH
    counter = 0

    def callback_grpc(call_future):
        nonlocal counter
        times[counter] = time.time() - times[counter]
        #print(times[counter], ":", counter)
        counter += 1

    for i in range(EPOCH):
        times[i] = time.time()

        stub = movie_pb2_grpc.MovieStub(grpc.insecure_channel('127.0.0.1:3002'))

        movieid = movie_pb2.MovieID(id="39ab85e5-5e8e-4dc5-afea-65dc368bd7ab")
        movie = stub.GetMovieByID.future(movieid)
        movie.add_done_callback(callback_grpc)
        #times[i] = time.time() - timer

    time.sleep(3)
    return times

def call_graphql():
    query = {
        "query": "query { movie_with_id(_id:\"39ab85e5-5e8e-4dc5-afea-65dc368bd7ab\") {title rating director }}"
    }
    rs = (grequests.post("http://127.0.0.1:3003/graphql", data=query) for i in range(EPOCH))
    times = list(map(lambda response: response.elapsed.total_seconds(),grequests.map(rs)))
    return times

if __name__ == "__main__":
    time_rest = call_rest()
    print("REST mean time for 100 parallel resquests : ", np.mean(time_rest))

    time_grpc = call_grpc()
    print("gRPC mean time for 100 parallel resquests : ", np.mean(time_grpc))

    time_graphql = call_graphql()
    print("GraphQL mean time for 100 parallel resquests : ", np.mean(time_graphql))



