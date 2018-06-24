import argparse
import asyncio
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
import sys
import os

from runner import Runner


def main():
    parser = argparse.ArgumentParser(description='Simple load testing tool')
    parser.add_argument('module', help='Module with coroutine to run')
    parser.add_argument('-w', '--workers', type=int, help='Number of workers', default=10)
    parser.add_argument('-d', '--duration', type=int, help='Duration of testing', default=120)
    parser.add_argument('-c', '--count', type=int, help='Max number of runs')
    parser.add_argument('-t', '--timeout', type=int, help='Request timeout')
    parser.add_argument('--count-per-worker', dest='count_per_worker', type=int, help='Max number of runs per worker')
    args = parser.parse_args()

    if os.path.exists(args.module):
        spec = spec_from_file_location("loadtest", args.module)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        try:
            module = import_module(args.module)
        except (ImportError, ValueError) as e:
            print('Error: Cannot import %r' % args.module)
            sys.exit(1)

    coroutine = getattr(module, 'coroutine', None)
    if not asyncio.iscoroutinefunction(coroutine):
        print('Error: "coroutine" should be a coroutine')
        sys.exit(1)

    session_setup = getattr(module, 'session_setup', None)
    if session_setup is not None and not callable(session_setup):
        print('Error: "session_setup" should be a function')
        sys.exit(1)

    runner = Runner(args.workers,
                    module.coroutine,
                    duration=args.duration,
                    max_runs=args.count,
                    max_runs_per_worker=args.count_per_worker,
                    timeout=args.timeout,
                    session_setup=session_setup
                    )
    result = runner.run()

    print(result.full_stats())


if __name__ == '__main__':
    main()
