# loginspect

It is recommended to save your flask output to some file, like `log.txt`, and then you can use loginspect like this:

`cat log.txt | ./loginspect.py`

```
$ ./loginspect.py --help
usage: loginspect [-h] [--filter IP] [--min AMOUNT] [--method {GET,POST}]

options:
  -h, --help           show this help message and exit
  --filter IP          filter by ip address
  --min AMOUNT         minimum occurences
  --method {GET,POST}  filter by method
```
