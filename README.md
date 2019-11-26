## Runtime
Setup virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install prerequisites:

```shell
pip install colorama==0.4.1
```

Launch simulator:

```shell
python main.py test/prog1.yo
```

Launch simulator with full debug information:

```shell
python main.py test/prog1.yo -v
```

Redirect output to file:

```shell
python main.py test.prog1.yo -v > output.log
```

Exit virtual environment:

```shell
deactivate
```

## TODO
* [ ] Instruction implementations
* [ ] Data forwarding