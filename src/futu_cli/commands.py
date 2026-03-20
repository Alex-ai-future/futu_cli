"""Futu CLI commands implementation."""

import sys
from datetime import datetime, timedelta

from rich.console import Console
from rich.table import Table

from futu import RET_OK, TrdEnv, CashFlowDirection

from .api import init_context, unlock_trade, get_stock_type, check_connection
from .config import config

console = Console()


def cmd_positions():
    """查询持仓."""
    quote_ctx, trade_ctx = init_context()
    try:
        if not unlock_trade(trade_ctx):
            return

        ret, data = trade_ctx.position_list_query()
        if ret != RET_OK:
            console.print(f"[red]❌ 查询持仓失败：{data}[/]")
            return

        if data.empty:
            console.print("[yellow]💰 当前无持仓[/]")
            return

        # 创建表格
        table = Table(title="📊 持仓情况")
        table.add_column("代码", style="cyan", justify="left")
        table.add_column("名称", style="cyan", justify="left")
        table.add_column("方向", justify="center")
        table.add_column("类型", justify="center")
        table.add_column("币种", justify="center")
        table.add_column("成本价", justify="right")
        table.add_column("市价", justify="right")
        table.add_column("持仓", justify="right")
        table.add_column("市值", justify="right")
        table.add_column("盈亏", justify="right")
        table.add_column("盈亏率", justify="right")

        for _, row in data.iterrows():
            code = str(row.get("code", ""))
            name = str(row.get("stock_name", ""))

            # 持仓方向
            qty = row.get("qty", 0)
            side = "多" if qty > 0 else "空" if qty < 0 else "平"

            # 证券类型
            api_type = str(row.get("stock_type", ""))
            stock_type = get_stock_type(code, api_type if api_type != "未知" else None)

            # 币种
            currency = str(row.get("currency", ""))

            # 成本价和市价
            cost_price = row.get("cost_price", 0)
            cost_price_str = f"${cost_price:,.3f}" if cost_price else "-"
            nominal_price = row.get("nominal_price", 0)
            nominal_price_str = f"${nominal_price:,.3f}" if nominal_price else "-"

            qty_str = str(abs(qty))
            market_val = f"${row.get('market_val', 0):,.2f}"
            pl = row.get("pl_val", 0)
            pl_str = f"{'+' if pl > 0 else ''}${pl:,.2f}"
            pl_style = "green" if pl > 0 else "red" if pl < 0 else ""
            pl_ratio = f"{'+' if row.get('pl_ratio', 0) > 0 else ''}{row.get('pl_ratio', 0):.2f}%"

            table.add_row(
                code,
                name,
                side,
                stock_type,
                currency,
                cost_price_str,
                nominal_price_str,
                qty_str,
                market_val,
                f"[{pl_style}]{pl_str}[/{pl_style}]" if pl_style else pl_str,
                f"[{pl_style}]{pl_ratio}[/{pl_style}]" if pl_style else pl_ratio,
            )

        console.print(table)

        # 汇总信息
        total_pl = data["pl_val"].sum()
        total_val = data["market_val"].sum()
        total_style = "green" if total_pl > 0 else "red" if total_pl < 0 else ""
        console.print(
            f"\n[bold]总市值：[/] ${total_val:,.2f} | [bold]总盈亏：[/][{total_style}]{'+' if total_pl > 0 else ''}${total_pl:,.2f}[/{total_style}]"
        )

    except Exception as e:
        console.print(f"[red]❌ 查询失败：{e}[/]")
        import traceback

        traceback.print_exc()
    finally:
        quote_ctx.close()
        trade_ctx.close()


def cmd_orders():
    """查询订单."""
    quote_ctx, trade_ctx = init_context()
    try:
        if not unlock_trade(trade_ctx):
            return

        ret, data = trade_ctx.order_list_query()
        if ret != RET_OK:
            console.print(f"[red]❌ 查询订单失败：{data}[/]")
            return

        if data.empty:
            console.print("[yellow]📋 无订单记录[/]")
            return

        # 创建表格
        table = Table(title="📋 订单列表")
        table.add_column("订单 ID", style="cyan", justify="right")
        table.add_column("代码", style="cyan", justify="left")
        table.add_column("方向", justify="center")
        table.add_column("价格", justify="right")
        table.add_column("数量", justify="right")
        table.add_column("状态", justify="left")

        for _, row in data.iterrows():
            order_id = str(row.get("order_id", ""))
            code = str(row.get("code", ""))
            side = str(row.get("trd_side", ""))
            price = f"{row.get('price', 0):.2f}"
            qty = str(row.get("qty", 0))
            status = str(row.get("order_status", ""))

            table.add_row(order_id, code, side, price, qty, status)

        console.print(table)

    except Exception as e:
        console.print(f"[red]❌ 查询失败：{e}[/]")
    finally:
        quote_ctx.close()
        trade_ctx.close()


def cmd_accinfo():
    """查询账户信息."""
    quote_ctx, trade_ctx = init_context()
    try:
        if not unlock_trade(trade_ctx):
            return

        ret, data = trade_ctx.accinfo_query()
        if ret != RET_OK:
            console.print(f"[red]❌ 查询账户信息失败：{data}[/]")
            return

        if data.empty:
            console.print("[red]❌ 未找到账户信息[/]")
            return

        for _, row in data.iterrows():
            cash = row.get("cash", 0)
            max_power_short = row.get("max_power_short", 0)
            market_val = row.get("market_val", 0)
            total_assets = row.get("total_assets", 0)

            console.print(f"\n[bold]💰 账户信息[/]")
            console.print(f"  [bold]现金：[/]${cash:,.2f}")
            console.print(f"  [bold]购买力：[/]${max_power_short:,.2f}")
            console.print(f"  [bold]持仓市值：[/]${market_val:,.2f}")
            console.print(f"  [bold]总资产：[/]${total_assets:,.2f}")

    except Exception as e:
        console.print(f"[red]❌ 查询失败：{e}[/]")
    finally:
        quote_ctx.close()
        trade_ctx.close()


def cmd_cashflow(date: str = None):
    """查询账户现金流水."""
    # 如果没有指定日期，默认为今天
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # 验证日期格式
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        console.print("[red]❌ 日期格式错误，请使用 yyyy-MM-dd 格式（如：2025-03-19）[/]")
        return

    quote_ctx, trade_ctx = init_context()
    try:
        if not unlock_trade(trade_ctx):
            return

        ret, data = trade_ctx.get_acc_cash_flow(
            clearing_date=date,
            trd_env=TrdEnv.REAL
        )
        if ret != RET_OK:
            console.print(f"[red]❌ 查询现金流水失败：{data}[/]")
            return

        if data.empty:
            console.print(f"[yellow]📋 {date} 无现金流水记录[/]")
            return

        # 创建表格
        table = Table(title=f"📋 现金流水 - {date}")
        table.add_column("流水 ID", style="cyan", justify="right")
        table.add_column("清算日期", justify="center")
        table.add_column("交收日期", justify="center")
        table.add_column("币种", justify="center")
        table.add_column("类型", justify="left")
        table.add_column("方向", justify="center")
        table.add_column("金额", justify="right")
        table.add_column("备注", justify="left")

        for _, row in data.iterrows():
            cashflow_id = str(row.get("cashflow_id", ""))
            clearing_date = str(row.get("clearing_date", ""))
            settlement_date = str(row.get("settlement_date", ""))
            currency = str(row.get("currency", ""))
            cashflow_type = str(row.get("cashflow_type", ""))
            cashflow_direction = str(row.get("cashflow_direction", ""))
            cashflow_amount = row.get("cashflow_amount", 0)
            cashflow_remark = str(row.get("cashflow_remark", ""))

            # 金额颜色（正数流入=绿色，负数流出=红色）
            amount_style = "green" if cashflow_amount > 0 else "red" if cashflow_amount < 0 else ""
            amount_str = f"{'+' if cashflow_amount > 0 else ''}${cashflow_amount:,.2f}"

            # 方向符号
            direction_symbol = "↓" if cashflow_direction == "IN" else "↑" if cashflow_direction == "OUT" else "-"

            table.add_row(
                cashflow_id,
                clearing_date,
                settlement_date,
                currency,
                cashflow_type,
                direction_symbol,
                f"[{amount_style}]{amount_str}[/{amount_style}]" if amount_style else amount_str,
                cashflow_remark[:30] + "..." if len(cashflow_remark) > 30 else cashflow_remark,
            )

        console.print(table)

        # 汇总信息
        total_inflow = data[data["cashflow_amount"] > 0]["cashflow_amount"].sum()
        total_outflow = abs(data[data["cashflow_amount"] < 0]["cashflow_amount"].sum())
        net_flow = data["cashflow_amount"].sum()
        net_style = "green" if net_flow > 0 else "red" if net_flow < 0 else ""

        console.print(
            f"\n[bold]流入：[/][green]${total_inflow:,.2f}[/] | "
            f"[bold]流出：[/][red]${total_outflow:,.2f}[/] | "
            f"[bold]净流入：[/][{net_style}]{'+' if net_flow > 0 else ''}${net_flow:,.2f}[/{net_style}]"
        )

    except Exception as e:
        console.print(f"[red]❌ 查询失败：{e}[/]")
        import traceback
        traceback.print_exc()
    finally:
        quote_ctx.close()
        trade_ctx.close()


def cmd_history_orders(start: str = None, end: str = None, code: str = None):
    """查询历史订单."""
    quote_ctx, trade_ctx = init_context()
    try:
        if not unlock_trade(trade_ctx):
            return

        ret, data = trade_ctx.history_order_list_query(
            start=start,
            end=end,
            code=code,
            trd_env=TrdEnv.REAL
        )
        if ret != RET_OK:
            console.print(f"[red]❌ 查询历史订单失败：{data}[/]")
            return

        if data.empty:
            console.print("[yellow]📋 无历史订单记录[/]")
            return

        # 创建表格
        table = Table(title="📋 历史订单")
        table.add_column("订单 ID", style="cyan", justify="right")
        table.add_column("代码", style="cyan", justify="left")
        table.add_column("名称", justify="left")
        table.add_column("方向", justify="center")
        table.add_column("类型", justify="center")
        table.add_column("状态", justify="center")
        table.add_column("币种", justify="center")
        table.add_column("订单价", justify="right")
        table.add_column("成交均价", justify="right")
        table.add_column("数量", justify="right")
        table.add_column("已成交", justify="right")
        table.add_column("创建时间", justify="center")

        for _, row in data.iterrows():
            order_id = str(row.get("order_id", ""))
            stock_code = str(row.get("code", ""))
            stock_name = str(row.get("stock_name", ""))
            trd_side = str(row.get("trd_side", ""))
            order_type = str(row.get("order_type", ""))
            order_status = str(row.get("order_status", ""))
            currency = str(row.get("currency", ""))
            price = row.get("price", 0)
            price_str = f"${price:,.3f}" if price else "-"
            dealt_avg_price = row.get("dealt_avg_price", 0)
            dealt_avg_price_str = f"${dealt_avg_price:,.3f}" if dealt_avg_price else "-"
            qty = f"{row.get('qty', 0):,.0f}"
            dealt_qty = f"{row.get('dealt_qty', 0):,.0f}"
            create_time = str(row.get("create_time", ""))

            table.add_row(
                order_id,
                stock_code,
                stock_name[:15] if len(stock_name) > 15 else stock_name,
                trd_side,
                order_type,
                order_status,
                currency,
                price_str,
                dealt_avg_price_str,
                qty,
                dealt_qty,
                create_time,
            )

        console.print(table)
        console.print(f"\n[bold]共 {len(data)} 条记录[/]")

    except Exception as e:
        console.print(f"[red]❌ 查询失败：{e}[/]")
        import traceback
        traceback.print_exc()
    finally:
        quote_ctx.close()
        trade_ctx.close()


def cmd_history_fills(start: str = None, end: str = None, code: str = None):
    """查询历史成交."""
    quote_ctx, trade_ctx = init_context()
    try:
        if not unlock_trade(trade_ctx):
            return

        ret, data = trade_ctx.history_deal_list_query(
            start=start,
            end=end,
            code=code,
            trd_env=TrdEnv.REAL
        )
        if ret != RET_OK:
            console.print(f"[red]❌ 查询历史成交失败：{data}[/]")
            return

        if data.empty:
            console.print("[yellow]📋 无历史成交记录[/]")
            return

        # 创建表格
        table = Table(title="📋 历史成交")
        table.add_column("成交 ID", style="cyan", justify="right")
        table.add_column("订单 ID", style="cyan", justify="right")
        table.add_column("代码", style="cyan", justify="left")
        table.add_column("名称", justify="left")
        table.add_column("方向", justify="center")
        table.add_column("市场", justify="center")
        table.add_column("状态", justify="center")
        table.add_column("数量", justify="right")
        table.add_column("价格", justify="right")
        table.add_column("时间", justify="center")
        table.add_column("对手经纪", justify="left")

        for _, row in data.iterrows():
            deal_id = str(row.get("deal_id", ""))
            order_id = str(row.get("order_id", ""))
            stock_code = str(row.get("code", ""))
            stock_name = str(row.get("stock_name", ""))
            trd_side = str(row.get("trd_side", ""))
            deal_market = str(row.get("deal_market", ""))
            status = str(row.get("status", ""))
            qty = f"{row.get('qty', 0):,.0f}"
            price = f"{row.get('price', 0):.3f}"
            create_time = str(row.get("create_time", ""))
            counter_broker = str(row.get("counter_broker_name", ""))

            table.add_row(
                deal_id,
                order_id,
                stock_code,
                stock_name[:15] if len(stock_name) > 15 else stock_name,
                trd_side,
                deal_market,
                status,
                qty,
                price,
                create_time,
                counter_broker if counter_broker != "N/A" else "-",
            )

        console.print(table)
        console.print(f"\n[bold]共 {len(data)} 条记录[/]")

    except Exception as e:
        console.print(f"[red]❌ 查询失败：{e}[/]")
        import traceback
        traceback.print_exc()
    finally:
        quote_ctx.close()
        trade_ctx.close()


def cmd_setup():
    """配置向导."""
    from .config import config

    console.print("[bold]🔧 Futu CLI 配置向导[/]\n")

    # 检查现有配置
    if config.env_file.exists():
        console.print(f"📁 配置文件已存在：{config.env_file}")
        console.print("")
        if config.password:
            console.print("  ✅ 交易密码：已配置")
        else:
            console.print("  ⚠️  交易密码：未配置")

        console.print(f"  ✅ 监听地址：{config.host}")
        console.print(f"  ✅ 监听端口：{config.port}")
        console.print("")

        # 检查连接
        if check_connection():
            console.print("  ✅ 富途牛牛连接：正常")
        else:
            console.print("  ❌ 富途牛牛连接：失败")
        console.print("")
    else:
        console.print(f"📁 配置文件不存在：{config.env_file}")
        console.print("")

    # 提示用户是否要修改配置
    console.print("💡 如需修改配置，请编辑 .env 文件：")
    console.print(f"   vi {config.env_file}")
    console.print("")
    console.print("或运行以下命令重新创建：")
    console.print(f"   futu setup --reset")
    console.print("")


def cmd_help():
    """显示帮助信息."""
    console.print("""
[bold]🦞 Futu CLI[/] - 富途投资组合查询工具

[bold]用法：[/] futu <命令> [参数]

[bold]可用命令：[/]
  [cyan]positions[/]              查询持仓
  [cyan]orders[/]                 查询订单
  [cyan]accinfo[/]                查询账户信息
  [cyan]cashflow[/] [日期]        查询现金流水
  [cyan]history-orders[/]         查询历史订单
  [cyan]history-fills[/]          查询历史成交
  [cyan]setup[/]                  配置向导
  [cyan]help[/]                   显示帮助

[bold]示例：[/]
  [green]futu positions[/]
  [green]futu orders[/]
  [green]futu accinfo[/]
  [green]futu cashflow[/]
  [green]futu cashflow --date 2025-03-19[/]
  [green]futu history-orders[/]
  [green]futu history-orders --start "2025-01-01" --code US.AAPL[/]
  [green]futu history-fills --code HK.00700[/]

[bold]环境变量：[/]
  FUTU_PASSWORD      交易密码（必填）
  FUTU_HOST          监听地址（默认 127.0.0.1）
  FUTU_PORT          监听端口（默认 11112）

[bold]配置方法：[/]
  1. 运行 [cyan]futu setup[/] 查看配置
  2. 编辑 .env 文件配置交易密码
  3. 打开富途牛牛客户端并开启 API 监听

[bold]安全提示：[/]
  ⚠️  交易密码保存在本地 .env 文件中
  ⚠️  文件权限为 600（仅所有者可读写）
  ⚠️  请勿将 .env 文件上传到代码仓库或分享给他人
""")
