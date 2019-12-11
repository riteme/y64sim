## 依赖项

操作系统：Ubuntu 18.04

模拟器：

* Python 3 (3.6.8)
* colorama (0.4.1)

后端:

* Flask (1.1.1)
* flask-cors (3.0.8)

前端:

* npm (6.11.3)
* React (16.12.0)

前端的 NPM 依赖包：

* @material-ui/core (4.7.2)
* @material-ui/icons (4.5.1)
* typeface-roboto (0.0.75)
* react-monaco-editor (0.32.1)
* monaco-editor (0.18.1)
* react-cookie (4.0.1)
* responsive-react-monaco-editor (0.1.3)

## 准备运行环境
### 模拟器

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install colorama==0.4.1
```

运行模拟器：

```shell
python3 sim.py test/prog1.yo
```

对于每个时钟周期，会先输出当前流水线上的所有指令，之后输出时钟周期结束时所有寄存器的值（寄存器文件、条件代码、处理器状态和 PC）。

如果要观察流水线内部的详细运作情况，需要使用 “`-v`” 开关：

```shell
python3 sim.py test/prog1.yo -v
```

可以将所有输出重定向至某个文件：

```shell
python3 sim.py test/prog1.yo -v > output.log
```

如果输出过长，只想查看最后的寄存器结果，可以使用 `tail` 命令：

```shell
python3 sim.py test/asumi.yo | tail -4
```

退出 Virtualenv 环境：

```shell
deactivate
```

### 后端
安装 Flask：

```shell
source .venv/bin/activate
pip install Flask==1.1.1 flask-cors==3.0.8
```

之后使用

```shell
./backend/run-development.sh
```

来启动后端服务器。默认服务器地址在 `http://localhost:5000/`。

### 前端
安装完 NPM 后，进入 `frontend` 目录，使用以下命令编译前端：

```shell
npm run build
```

编译成功后，在本地运行前端服务器：

```shell
npm install -g serve
serve -s build -l 3000
```

打开 Chrome/Firefox，进入 `http://localhost:3000/` 即可看到前端页面。