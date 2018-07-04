*How to run*

`python main.py <module> [options]`
* `module` - python module name. Should contain a coroutine named `coroutine`. Also might specify `session_setup` function, that should return the dict of aiohttp session options.
Coroutine should return any hashable data - int, string, tuple, etc.
* `-c --count <int>` - max number of requests
* `-d --duration <int>` - max duration in seconds
* `-w --workers <int>` - number of parallel workers
* `--count-per-worker <int>` - max number of requests per worker

In case multiple options specified testing will run until any of the exit conditions is reached