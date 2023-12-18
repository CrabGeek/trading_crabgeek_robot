# trading_crabgeek_robot

## Binance 自动化交易策略 Robot

该项目为基于官方binance API, 自动化执行交易策略机器人

不要将API_KEY, API secert 上传至github!!!!

技术指标计算依赖于TA-Lib, TA-Lib基于C语言实现，不同操作系统平台需要安装的依赖不同，具体请参考https://github.com/TA-Lib/ta-lib-python

### 如何运行

1. python version need >= 3.10.13
2. pip install -r requirements.txt
4. https://github.com/TA-Lib/ta-lib-python，根据官方文档和自身所使用的操作系统安装TA-Lib
3. 配置 binance api_key & api_secret, 邮箱email_key
4. Ready to go 