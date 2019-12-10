## Prerequisites

Simulator:

* Python 3 (3.6.8)
* colorama (0.4.1)

Backend:
* Flask (1.1.1)
* flask-cors (3.0.8)

Frontend:
* npm (6.11.3)
* React (16)
* Material-UI (core/icons)
* typeface-roboto
* react-monaco-editor
* monaco-editor

## 运行
在 Ubuntu 18.04 终端中，准备运行环境：

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install colorama==0.4.1
```

运行模拟器：

```shell
python3 main.py test/prog1.yo
```

对于每个时钟周期，会先输出当前流水线上的所有指令，之后输出时钟周期结束时所有寄存器的值（寄存器文件、条件代码、处理器状态和 PC）。

如果要观察流水线内部的详细运作情况，需要使用 “`-v`” 开关：

```shell
python3 main.py test/prog1.yo -v
```

可以将所有输出重定向至某个文件：

```shell
python3 main.py test/prog1.yo -v > output.log
```

如果输出过长，只想查看最后的寄存器结果，可以使用 `tail` 命令：

```shell
python3 main.py test/asumi.yo | tail -4
```

退出 Virtualenv 环境：

```shell
deactivate
```

## Runtime
Setup virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install prerequisites:

```shell
pip install colorama==0.4.1 Flask==1.1.1
```

Launch simulator:

```shell
python3 main.py test/prog1.yo
```

Launch simulator with full debug information:

```shell
python3 main.py test/prog1.yo -v
```

Redirect output to file:

```shell
python3 main.py test/prog1.yo -v > output.log
```

Exit virtual environment:

```shell
deactivate
```

## Backend
In virtual environment, run:

```shell
./backend/server.py
```

to start backend server in development mode.

## TODO
* [x] Instruction implementations
* [x] Data forwarding