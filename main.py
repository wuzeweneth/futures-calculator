# 计算交割合约逐仓模式下的爆仓触发价格

# 梯度保证金
# https://www.okex.win/trade-market/position/futures

import argparse

# 交割币本位
# [档位，最小张数，最大张数，维持保证金率，最低初始保证金率，最高可用杠杆倍数]
coinFpt = [
    [1, 0, 500, 0.40, 0.80, 125.00],
    [2, 501, 3000, 0.50, 1.00, 100.00],
    [3, 3001, 22000, 1.00, 1.50, 66.66],
    [4, 22001, 42000, 1.50, 2.00, 50.00],
    [5, 42001, 62000, 2.00, 2.50, 40.00],
    [6, 62001, 82000, 2.50, 3.00, 33.33],
    [7, 82001, 102000, 3.00, 3.50, 28.57],
    [8, 102001, 122000, 3.50, 4.00, 25.00],
    [9, 122001, 142000, 4.00, 4.50, 22.22],
    [10, 142001, 162000, 4.50, 5.00, 20.00],
    [11, 162001, 182000, 5.00, 5.50, 18.18],
    [12, 182001, 202000, 5.50, 6.00, 16.66],
    [13, 202001, 222000, 6.00, 6.50, 15.38],
    [14, 222001, 242000, 6.50, 7.00, 14.28],
    [15, 242001, 262000, 7.00, 7.50, 13.33],
    [16, 262001, 282000, 7.50, 8.00, 12.50],
    [17, 282001, 302000, 8.00, 8.50, 11.76],
    [18, 302001, 322000, 8.50, 9.00, 11.11],
    [19, 322001, 342000, 9.00, 9.50, 10.52],
    [20, 342001, 362000, 9.50, 10.00, 10.00]
]

# 交割美元本位
# [档位，最小张数，最大张数，维持保证金率，最低初始保证金率，最高可用杠杆倍数]
usdtFpt = [
    [1, 0, 200, 0.40, 0.80, 125.00],
    [2, 201, 1000, 0.50, 1.00, 100.00],
    [3, 1001, 11000, 1.00, 1.50, 66.66],
    [4, 11001, 21000, 1.50, 2.00, 50.00],
    [5, 21001, 31000, 2.00, 2.50, 40.00],
    [6, 31001, 41000, 2.50, 3.00, 33.33],
    [7, 41001, 51000, 3.00, 3.50, 28.57],
    [8, 51001, 61000, 3.50, 4.00, 25.00],
    [9, 61001, 71000, 4.00, 4.50, 22.22],
    [10, 71001, 81000, 4.50, 5.00, 20.00],
    [11, 81001, 91000, 5.00, 5.50, 18.18],
    [12, 91001, 101000, 5.50, 6.00, 16.66],
    [13, 101001, 111000, 6.00, 6.50, 15.38],
    [14, 111001, 121000, 6.50, 7.00, 14.28],
    [15, 121001, 131000, 7.00, 7.50, 13.33],
    [16, 131001, 141000, 7.50, 8.00, 12.50],
    [17, 141001, 151000, 8.00, 8.50, 11.76],
    [18, 151001, 161000, 8.50, 9.00, 11.11],
    [19, 161001, 171000, 9.00, 9.50, 10.52],
    [20, 171001, 181000, 9.50, 10.00, 10.00]
]

# 币本位所需保证金：(购入价格,购入张数,杠杆倍数,持仓方向,最新标记价格,吃单手续费)
def clacPAMgn(buyPrice, buyCount, lever, posSide, lastMarkPrice, takerFee):
    print("=========================================")
    print("币本位爆仓价格计算")
    print("购入价格: %f, 购入张数: %d, 杠杆倍数: %d, 持仓方向: %s, 最新标记价格: %f" %
          (buyPrice, buyCount, lever, posSide, lastMarkPrice))
    # 面值USDT
    onePrice = 100
    print("当前面值为: %fUSDT(%fBTC)" % (onePrice, onePrice/buyPrice))
    # 档位
    level = 0
    # 档位维持保证金率
    levelMgnRate = 0
    # 最低初始保证金率
    minLevelMgnRate = 0
    for item in coinFpt:
        if buyCount >= item[1] and buyCount <= item[2]:
            level = item[0]
            levelMgnRate = item[3]
            minLevelMgnRate = item[4]
    print("当前档位: %d, 档位维持保证金率: %f%%, 最低初始保证金率: %f%%" %
          (level, levelMgnRate, minLevelMgnRate))
    print("=========================================")
    # 平仓手续费率 (爆仓时按照吃单计算)
    clossFee = takerFee
    # 固定保证金 = 面值 * 张数 / (购入价格 * 杠杆倍数)
    fixMgn = onePrice * buyCount / (buyPrice * lever)
    print("固定保证金为：%fBTC(%fUSDT)" % (fixMgn, fixMgn*lastMarkPrice))
    # 当前所需维持保证金率 + 平仓手续费率
    keyRate = (levelMgnRate + clossFee) / 100
    # 计算开多的未实现盈亏
    # 未实现盈亏
    upl = 0
    if posSide == "long":
        # 未实现盈亏 (买入开多) = 面值 * 张数 / 开仓均价 - 面值 * 张数 / 最新标记价格
        upl = onePrice * buyCount / buyPrice - onePrice * buyCount / lastMarkPrice
    # 计算开空的未实现盈亏
    if posSide == "short":
        # 未实现盈亏 (卖出开空) = 面值 * 张数 / 最新标记价格 - 面值 * 张数 / 开仓均价
        upl = onePrice * buyCount / lastMarkPrice - onePrice * buyCount / buyPrice
    # 保证金率 = (固定保证金 + 未实现盈亏) / (面值 * 张数 / 最新标记价格)
    isolatedMgn = (fixMgn + upl) / (onePrice * buyCount / lastMarkPrice) * 100
    print("未实现盈亏为：%fBTC(%FUDST)" % (upl, upl*lastMarkPrice))
    print("保证金率为: %f%%" % (isolatedMgn))
    print("-----------------------------------------")
    # 当保证金率小于等于用户当前所需维持保证金率 + 平仓手续费率时，即触发爆仓
    if posSide == "long":
        # (当前所需维持保证金率 + 平仓手续费率)a = (固定保证金b + 面值c * 张数d / 开仓均价e - 面值c * 张数d / 最新标记价格f) / (面值c * 张数d / 最新标记价格f)
        # a = (b + c * d / e - c * d / f) / (c * d / f)
        # 求爆仓的变量f：最新标记价格
        # f = (a * c * d + c * d) / (b + c * d / e)
        # 最新标记价格(爆仓) = ((当前所需维持保证金率 + 平仓手续费率) * 面值 * 张数 + 面值 * 张数) / (固定保证金 + 面值 * 张数 / 开仓均价)
        explMarkPrice = (keyRate * onePrice * buyCount + onePrice *
                         buyCount) / (fixMgn + onePrice * buyCount / buyPrice)
        # 未实现盈亏 (买入开多) = 面值 * 张数 / 开仓均价 - 面值 * 张数 / 最新标记价格
        lastUpl = onePrice * buyCount / buyPrice - onePrice * buyCount / explMarkPrice
        expisolatedMgn = (fixMgn + lastUpl) / (onePrice *
                                               buyCount / explMarkPrice)
        print("当标记价格等于或小于: %f时" % (explMarkPrice))
        print("未实现盈亏为：%fBTC(%fUSDT)" % (lastUpl, lastUpl*explMarkPrice))
        closeFeeResult = onePrice * buyCount / explMarkPrice * clossFee / 100
        print("平仓手续费为：%fBTC(%fUSDT)" %
              (closeFeeResult, closeFeeResult*explMarkPrice))
        levelMgnResult = (onePrice * buyCount /
                          explMarkPrice) * (levelMgnRate / 100)
        print("档位最低维持保证金为：%fBTC(%fUSDT)" %
              (levelMgnResult, levelMgnResult*explMarkPrice))
        print("原先固定保证金为: %fBTC(%fUSDT)" % (fixMgn, fixMgn*explMarkPrice))
        tempResult = fixMgn + lastUpl - closeFeeResult
        print("当前保证金(加上未实现盈亏和减去平仓手续费)为：%fBTC(%fUSDT)" %
              (tempResult, tempResult*explMarkPrice))
        print("保证金率为: %f%%, 等于或小于当前档位维持保证金率+平仓手续费率%f%%触发爆仓" %
              (expisolatedMgn*100, keyRate*100))
    # 计算开空的未实现盈亏
    if posSide == "short":
        # (当前所需维持保证金率 + 平仓手续费率)a = (固定保证金b + 面值c * 张数d / 最新标记价格e - 面值c * 张数d / 开仓均价f) / (面值c * 张数d / 最新标记价格e)
        # a = (b + c * d / e - c * d / f) / (c * d / e)
        # 求爆仓的变量e：最新标记价格
        # e = (a * c * d - c * d) / (b - c * d / f)
        # 最新标记价格(爆仓) = ((当前所需维持保证金率 + 平仓手续费率) * 面值 * 张数 - 面值 * 张数) / (固定保证金 - 面值 * 张数 / 开仓均价)
        explMarkPrice = (keyRate * onePrice * buyCount - onePrice *
                         buyCount) / (fixMgn - onePrice * buyCount / buyPrice)
        # 未实现盈亏 (卖出开空) = 面值 * 张数 / 最新标记价格 - 面值 * 张数 / 开仓均价
        lastUpl = onePrice * buyCount / explMarkPrice - onePrice * buyCount / buyPrice
        expisolatedMgn = (fixMgn + lastUpl) / (onePrice *
                                               buyCount / explMarkPrice)
        print("当标记价格等于或大于: %f时" % (explMarkPrice))
        print("未实现盈亏为：%fBTC(%fUSDT)" % (lastUpl, lastUpl*explMarkPrice))
        closeFeeResult = onePrice * buyCount / explMarkPrice * clossFee / 100
        print("平仓手续费为：%fBTC(%fUSDT)" %
              (closeFeeResult, closeFeeResult*explMarkPrice))
        levelMgnResult = (onePrice * buyCount /
                          explMarkPrice) * (levelMgnRate / 100)
        print("档位最低维持保证金为：%fBTC(%fUSDT)" %
              (levelMgnResult, levelMgnResult*explMarkPrice))
        print("原先固定保证金为: %fBTC(%fUSDT)" % (fixMgn, fixMgn*explMarkPrice))
        tempResult = fixMgn + lastUpl - closeFeeResult
        print("当前保证金(加上未实现盈亏和减去平仓手续费)为：%fBTC(%fUSDT)" %
              (tempResult, tempResult*explMarkPrice))
        print("保证金率为: %f%%, 等于或小于档位维持保证金率+平仓手续费率%f%%触发爆仓" %
              (expisolatedMgn*100, keyRate*100))
    print("-----------------------------------------")

# USDT本位所需保证金：(购入价格,购入张数,杠杆倍数,持仓方向,最新标记价格,吃单手续费)
def clacBSMgn(buyPrice, buyCount, lever, posSide, lastMarkPrice, takerFee):
    print("=========================================")
    print("USDT本位爆仓价格计算")
    print("购入价格: %f, 购入张数: %d, 杠杆倍数: %d, 持仓方向: %s, 最新标记价格: %f" %
          (buyPrice, buyCount, lever, posSide, lastMarkPrice))
    # 面值BTC
    onePrice = 0.01
    print("当前面值为: %fBTC(%fUSDT)" % (onePrice, onePrice*buyPrice))
    # 档位
    level = 0
    # 档位维持保证金率
    levelMgnRate = 0
    # 最低初始保证金率
    minLevelMgnRate = 0
    for item in usdtFpt:
        if buyCount >= item[1] and buyCount <= item[2]:
            level = item[0]
            levelMgnRate = item[3]
            minLevelMgnRate = item[4]
    print("当前档位: %d, 档位维持保证金率: %f%%, 最低初始保证金率: %f%%" %
          (level, levelMgnRate, minLevelMgnRate))
    print("=========================================")
    # 平仓手续费率 (爆仓时按照吃单计算)
    clossFee = takerFee
    # 固定保证金 = 面值 * 张数 * 开仓价格 / 杠杆倍数
    fixMgn = onePrice * buyCount * buyPrice / lever
    print("固定保证金为：%fUSDT(%fBTC)" % (fixMgn, fixMgn/lastMarkPrice))
    # 当前所需维持保证金率 + 平仓手续费率
    keyRate = (levelMgnRate + clossFee) / 100
    # 计算开多的未实现盈亏
    # 未实现盈亏
    upl = 0
    if posSide == "long":
        # 未实现盈亏 (买入开多) = 面值 * 张数 * 最新标记价格 - 面值 * 张数 * 开仓均价
        upl = onePrice * buyCount * lastMarkPrice - onePrice * buyCount * buyPrice
    # 计算开空的未实现盈亏
    if posSide == "short":
        # 未实现盈亏 (卖出开空) = 面值 * 张数 * 开仓均价 - 面值 * 张数 * 最新标记价格
        upl = onePrice * buyCount * buyPrice - onePrice * buyCount * lastMarkPrice
    # 保证金率 = (固定保证金 + 未实现盈亏) / (面值 * 张数 * 最新标记价格)
    isolatedMgn = (fixMgn + upl) / (onePrice * buyCount * lastMarkPrice)
    print("未实现盈亏为：%fUSDT(%fBTC)" % (upl, upl/lastMarkPrice))
    print("保证金率为: %f%%" % (isolatedMgn*100))
    print("-----------------------------------------")
    # 当保证金率小于等于用户当前所需维持保证金率 + 平仓手续费率时，即触发爆仓
    if posSide == "long":
        # (当前所需维持保证金率 + 平仓手续费率)a = (固定保证金b + 面值c * 张数d * 最新标记价格e - 面值c * 张数d * 开仓均价f) / (面值c * 张数d * 最新标记价格e)
        # a = (b + c * d * e - c * d * f) / (c * d * e)
        # 求爆仓的变量e：最新标记价格
        # e = (b - c * d * f) / (a * c * d - c * d)
        # 最新标记价格(爆仓) = (固定保证金 - 面值 * 张数 * 开仓均价) / ((当前所需维持保证金率 + 平仓手续费率) * 面值 * 张数 - 面值 * 张数)
        explMarkPrice = (fixMgn - onePrice * buyCount * buyPrice) / \
            (keyRate * onePrice * buyCount - onePrice * buyCount)
        # 未实现盈亏 (买入开多) = 面值 * 张数 * 最新标记价格 - 面值 * 张数 * 开仓均价
        lastUpl = onePrice * buyCount * explMarkPrice - onePrice * buyCount * buyPrice
        print("当标记价格等于或小于: %f时" % (explMarkPrice))
        print("未实现盈亏为：%fUSDT(%fBTC)" % (lastUpl, lastUpl/explMarkPrice))
        # 平仓手续费 = 面值 * 张数 * 最新标记价格 * 平仓手续费率
        closeFeeResult = onePrice * buyCount * explMarkPrice * clossFee / 100
        print("平仓手续费为：%fUSDT(%fBTC)" %
              (closeFeeResult, closeFeeResult/explMarkPrice))
        # 档位最低维持保证金 = 面值 * 张数 * 最新标记价格 * 档位维持保证金率
        levelMgnResult = (onePrice * buyCount *
                          explMarkPrice) * (levelMgnRate / 100)
        print("档位最低维持保证金为：%fUSDT(%fBTC)" %
              (levelMgnResult, levelMgnResult/explMarkPrice))
        print("原先固定保证金为: %fUSDT(%fBTC)" % (fixMgn, fixMgn/explMarkPrice))
        tempResult = fixMgn + lastUpl - closeFeeResult
        print("当前保证金(加上未实现盈亏和减去平仓手续费)为：%fUSDT(%fBTC)" %
              (tempResult, tempResult/explMarkPrice))
        # 爆仓保证金率 = (固定保证金 + 未实现盈亏) / (面值 * 张数 * 最新标记价格)
        expisolatedMgn = (fixMgn + lastUpl) / \
            (onePrice * buyCount * explMarkPrice)
        print("保证金率为: %f%%, 等于或小于当前档位维持保证金率+平仓手续费率%f%%触发爆仓" %
              (expisolatedMgn*100, keyRate*100))
    # 计算开空的未实现盈亏
    if posSide == "short":
        # (当前所需维持保证金率 + 平仓手续费率)a = (固定保证金b + 面值c * 张数d * 开仓均价e - 面值c * 张数d * 最新标记价格f) / (面值c * 张数d * 最新标记价格f)
        # a = (b + c * d * e - c * d * f) / (c * d * f)
        # 求爆仓的变量f：最新标记价格
        # f = (b + c * d * e) / (a * c * d + c * d)
        # 最新标记价格(爆仓) = (固定保证金 + 面值 * 张数 * 开仓均价) / ((当前所需维持保证金率 + 平仓手续费率) * 面值 * 张数 + 面值 * 张数)
        explMarkPrice = (fixMgn + onePrice * buyCount * buyPrice) / \
            (keyRate * onePrice * buyCount + onePrice * buyCount)
        # 未实现盈亏 (买入开多) = 面值 * 张数 * 开仓均价 - 面值 * 张数 * 最新标记价格
        lastUpl = onePrice * buyCount * buyPrice - onePrice * buyCount * explMarkPrice
        print("当标记价格等于或大于: %f时" % (explMarkPrice))
        print("未实现盈亏为：%fUSDT(%fBTC)" % (lastUpl, lastUpl/explMarkPrice))
        # 平仓手续费 = 面值 * 张数 * 最新标记价格 * 平仓手续费率
        closeFeeResult = onePrice * buyCount * explMarkPrice * clossFee / 100
        print("平仓手续费为：%fUSDT(%fBTC)" %
              (closeFeeResult, closeFeeResult/explMarkPrice))
        # 档位最低维持保证金 = 面值 * 张数 * 最新标记价格 * 档位维持保证金率
        levelMgnResult = (onePrice * buyCount *
                          explMarkPrice) * (levelMgnRate / 100)
        print("档位最低维持保证金为：%fUSDT(%fBTC)" %
              (levelMgnResult, levelMgnResult/explMarkPrice))
        print("原先固定保证金为: %fUSDT(%fBTC)" % (fixMgn, fixMgn/explMarkPrice))
        tempResult = fixMgn + lastUpl - closeFeeResult
        print("当前保证金(加上未实现盈亏和减去平仓手续费)为：%fUSDT(%fBTC)" %
              (tempResult, tempResult/explMarkPrice))
        # 爆仓保证金率 = (固定保证金 + 未实现盈亏) / (面值 * 张数 * 最新标记价格)
        expisolatedMgn = (fixMgn + lastUpl) / \
            (onePrice * buyCount * explMarkPrice)
        print("保证金率为: %f%%, 等于或大于当前档位维持保证金率+平仓手续费率%f%%触发爆仓" %
              (expisolatedMgn*100, keyRate*100))
    print("-----------------------------------------")

def main():
    # 手续费 https://www.okex.com/fees.html
    # 合约爆仓手续费按照用户当前所处等级的taker费率收取。
    # 挂单手续费 (这里要按自己的用户等级调整)
    makerFee = 0.02
    # 吃单手续费 (这里要按自己的用户等级调整)
    takerFee = 0.05
    # 购入价
    buyPrice = 100
    # 购入张数
    buyCount = 1
    # 杠杆
    lever = 1
    # 持仓方向
    posSide = 'long'
    # 最新标记价格
    lastMarkPrice = 100

    parser = argparse.ArgumentParser()
    parser.add_argument("--mgnType", type=int, help="保证金类型:0(币本位)/1(USDT本位)")
    parser.add_argument("--buyPrice", type=float, help="购入价格")
    parser.add_argument("--buyCount", type=float, help="购入张数")
    parser.add_argument("--lever", type=int, help="杠杆倍数")
    parser.add_argument("--posSide", type=str, help="持仓方向:'long'/'short'")
    parser.add_argument("--lastMarkPrice", type=float, help="最新标记价格")
    parser.add_argument("--makerFee", type=float, help="挂单手续费")
    parser.add_argument("--takerFee", type=float, help="吃单手续费")
    args = parser.parse_args()
    if args.buyPrice:
        buyPrice = args.buyPrice
    if args.buyCount:
        buyCount = args.buyCount
    if args.lever:
        lever = args.lever
    if args.posSide:
        posSide = args.posSide
    if args.lastMarkPrice:
        lastMarkPrice = args.lastMarkPrice
    if args.makerFee:
        makerFee = args.makerFee
    if args.takerFee:
        takerFee = args.takerFee

    if args.mgnType == 0:
        clacPAMgn(buyPrice, buyCount, lever, posSide, lastMarkPrice, takerFee)
    if args.mgnType == 1:
        clacBSMgn(buyPrice, buyCount, lever, posSide, lastMarkPrice, takerFee)

main()