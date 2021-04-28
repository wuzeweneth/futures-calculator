# 合约爆仓价格计算器

## 参数
| 名称 | 参数 | 参数类型 | 示例 | 默认值 | 描述 | 
| ---- | ---- | ---- | ---- | ---- | ---- |
| 保证金类型 | --mgnType | `int` | `0` \ `1` | 0 | `0` PA：币本位, `1` BS：美元本位 |
| 保证金模式 | --mgnMode | `int` | `0` \ `1` | 0 | `0` cross：全仓, `1` isolated：逐仓 |
| 挂单手续费 | --makerFee | `float` | 0.02 | 0.02 | 百分比，[详情参考](https://www.okex.com/fees.html) |
| 吃单手续费 | --takerFee | `float` | 0.05 | 0.05 | 百分比，[详情参考](https://www.okex.com/fees.html) |
| 购入价格 | --buyPrice | `float` | 6666.66 | 100 | 合约成交价 |
| 购入数 | --buyCount | `float` | 222.2 | 1 | 购入量 |
| 杠杆 | --lever | `int` | 10 | 1 | 杠杆 |
| 保证金余额 | --availEq | `float` | 10.0 | 0 | 若不传参，则按最低初始保证金率计算 |
| 持仓方向 | --posSide | `string` | 'long' | 'long' | 持仓方向，`long`（做多）或者`short`（做空） |

## 示例
```
python main.py --buyPrice 58000 --buyCount 10 --lever 10 --posSide 'long'
```