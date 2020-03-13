import hashlib
import requests
import time
from multiprocessing import Queue, Process
import os
import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof, rand_step=1):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = int(time.time())
    while valid_proof(last_proof, proof) is False:
        proof += random.randint(1, rand_step)

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    current_guess = f'{proof}'.encode()
    last_guess = f'{last_proof}'.encode()
    guess_hash = hashlib.sha256(current_guess).hexdigest()
    last_hash = hashlib.sha256(last_guess).hexdigest()
    return guess_hash[:6] == last_hash[-6:]


def proof_of_work_helper(last_proof, rand_step, q):
    while True:
        proof = proof_of_work(last_proof, rand_step)
        q.put(proof)
        return


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1 and sys.argv[1] != 'none':
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    if len(sys.argv) > 2:
        random_step = int(sys.argv[2])
    else:
        random_step = 1

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()

        # Begin multi
        q = Queue()
        jobs = []
        random_offset = random.randint(0, 99)
        for i in range(os.cpu_count() - 1):
            p = Process(
                target=proof_of_work_helper,
                args=(data.get('proof'), random_step, q)
                )
            jobs.append(p)
            p.start()
        new_proof = q.get(True)
        for p in jobs:
            p.kill()

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
