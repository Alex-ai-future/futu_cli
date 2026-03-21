"""Futu API connection and utilities."""

import socket
import sys
from typing import Tuple, Optional

from futu import OpenQuoteContext, OpenSecTradeContext, RET_OK

from .config import config


def get_stock_type(code: str, api_type: Optional[str] = None) -> str:
    """
    判断证券类型

    Args:
        code: 股票代码
        api_type: API 返回的 stock_type（可选）

    Returns:
        证券类型字符串
    """
    # 优先使用 API 返回的类型（如果可靠）
    if api_type and api_type not in ["未知", ""]:
        # 映射 API 返回的类型
        type_map = {
            "STOCK": "正股",
            "OPTION": "期权",
            "WARRANT": "窝轮",
            "FUTURE": "期货",
            "BOND": "债券",
        }
        return type_map.get(api_type, api_type)

    # 根据代码格式判断
    code_upper = code.upper()

    # 期权格式：US.AAPL260320P250000 或 HK.00700C230901
    if any(x in code_upper for x in ["P", "C"]) and len(code) > 12:
        # 检查是否有日期格式（6 位数字）
        import re

        if re.search(r"\d{6}", code):
            return "期权"

    # 港股格式：HK.xxxxx
    if code_upper.startswith("HK."):
        return "港股"

    # 美股格式：US.xxxxx
    if code_upper.startswith("US."):
        return "美股"

    # ETF 判断（代码中包含 ETF 或常见 ETF 名称）
    etf_keywords = ["ETF", "ARK", "QQQ", "SPY", "IWM"]
    if any(k in code_upper for k in etf_keywords):
        return "ETF"

    # 默认为正股
    return "正股"


def check_connection() -> bool:
    """检查富途牛牛连接."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((config.host, config.port))
        sock.close()

        if result != 0:
            print("❌ 无法连接到富途牛牛")
            print("")
            print("可能原因：")
            print("  1. 富途牛牛客户端未启动")
            print("  2. API 监听未开启")
            print("  3. 端口号不正确")
            print("")
            print("解决方法：")
            print("  1. 打开富途牛牛客户端")
            print("  2. 进入 设置 → API 设置")
            print("  3. 开启 监听端口")
            print(f"  4. 确认监听地址为 {config.host}，端口为 {config.port}")
            return False
        return True
    except Exception as e:
        print(f"❌ 连接检查失败：{e}")
        return False


def init_context() -> Tuple[OpenQuoteContext, OpenSecTradeContext]:
    """初始化上下文."""
    # 先检查连接
    if not check_connection():
        sys.exit(1)

    try:
        quote_ctx = OpenQuoteContext(host=config.host, port=config.port)
        trade_ctx = OpenSecTradeContext(host=config.host, port=config.port)
        return quote_ctx, trade_ctx
    except Exception as e:
        print(f"❌ 初始化连接失败：{e}")
        print("")
        print("请检查：")
        print("  1. futu-api 库是否正确安装")
        print("  2. 富途牛牛客户端是否正常运行")
        sys.exit(1)


def unlock_trade(trade_ctx: OpenSecTradeContext) -> bool:
    """
    解锁交易接口。
    
    注意：GUI 版本 OpenD 已屏蔽 API 解锁接口，必须在 OpenD GUI 界面手动解锁。
    此函数仅检查是否已解锁，不执行解锁操作。
    """
    # GUI 版本已屏蔽 unlock_trade 接口，直接返回 True
    # 用户需要在 OpenD GUI 界面手动点击「解锁交易」按钮
    return True
