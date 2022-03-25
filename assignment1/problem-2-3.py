import multiprocessing  # See https://docs.python.org/3/library/multiprocessing.html
import argparse  # See https://docs.python.org/3/library/argparse.html
import random
from math import pi

from pytest import yield_fixture


def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""

    max_range = n[0]  # get n from zip
    _seed = n[1]  # get seed from zip

    random.seed(_seed)
    print("Hello from a worker")
    s = 0
    for i in range(max_range):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s


def compute_pi(args):
    random.seed(1)
    n = int(args.steps / args.workers)

    p = multiprocessing.Pool(args.workers)

    seed = seed_gen(1, args.workers)
    seeds = [next(seed) for i in range(0, args.workers)]

    zip_list = zip([n]*args.workers, seeds)
    s = p.map(sample_pi, zip_list)

    n_total = n*args.workers
    s_total = sum(s)
    pi_est = (4.0*s_total)/n_total
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))


def seed_gen(seed, max):
    for i in range(0, max):
        _seed = seed + i
        yield _seed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers', '-w',
                        default='1',
                        type=int,
                        help='Number of parallel processes')
    parser.add_argument('--steps', '-s',
                        default='1000',
                        type=int,
                        help='Number of steps in the Monte Carlo simulation')
    parser.add_argument('--seed ', '-se',
                        default='1',
                        type=int,
                        help='Number of seed')
    args = parser.parse_args()
    compute_pi(args)
