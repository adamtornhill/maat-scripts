# Combine the History of Multiple Repositories

`combine_repos.py` combines a number of git history files into a single git history file.

The program sorts the aggregated commits by date in descending order before writing the result.

For usage instructions, call

```shell
combine_repos.py -h
```

The tests in [test_combine_repos.py](test_combine_repos.py) and the [test-data](test-data) give examples of what the
program does.
