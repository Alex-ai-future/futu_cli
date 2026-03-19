#!/usr/bin/env python3
"""
Futu CLI - Make Futu portfolio your CLI.

Query positions, orders, account info and more from Futu NiuNiu.
"""

import sys
import click
from rich.console import Console

from .commands import (
    cmd_positions,
    cmd_orders,
    cmd_accinfo,
    cmd_cashflow,
    cmd_history_orders,
    cmd_history_fills,
    cmd_setup,
    cmd_help,
)
from . import __version__

console = Console()


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit.")
@click.pass_context
def main(ctx, version):
    """🦞 Futu CLI - 富途投资组合查询工具

    Query positions, orders, account info and more from Futu NiuNiu.

    \b
    Examples:
      futu positions
      futu orders
      futu accinfo
      futu setup

    \b
    Environment Variables:
      FUTU_PASSWORD      Trading password (required)
      FUTU_HOST          API host (default: 127.0.0.1)
      FUTU_PORT          API port (default: 11112)
    """
    if version:
        console.print(f"Futu CLI version {__version__}")
        sys.exit(0)

    # If no command is given, show help
    if ctx.invoked_subcommand is None:
        cmd_help()


@main.command()
def positions():
    """📊 Query positions (stocks, options, etc.)"""
    cmd_positions()


@main.command()
def orders():
    """📋 Query orders (pending and history)"""
    cmd_orders()


@main.command()
def accinfo():
    """💰 Query account information (cash, buying power, etc.)"""
    cmd_accinfo()


@main.command()
@click.option("--date", "-d", default=None, help="Clearing date (yyyy-MM-dd format, default: today)")
def cashflow(date):
    """📋 Query account cash flow"""
    cmd_cashflow(date)


@main.command()
@click.option("--start", "-s", default=None, help="Start time (YYYY-MM-DD HH:MM:SS)")
@click.option("--end", "-e", default=None, help="End time (YYYY-MM-DD HH:MM:SS)")
@click.option("--code", "-c", default=None, help="Stock code filter")
def history_orders(start, end, code):
    """📋 Query history orders"""
    cmd_history_orders(start=start, end=end, code=code)


@main.command()
@click.option("--start", "-s", default=None, help="Start time (YYYY-MM-DD HH:MM:SS)")
@click.option("--end", "-e", default=None, help="End time (YYYY-MM-DD HH:MM:SS)")
@click.option("--code", "-c", default=None, help="Stock code filter")
def history_fills(start, end, code):
    """📋 Query history deals/fills"""
    cmd_history_fills(start=start, end=end, code=code)


@main.command()
@click.option("--reset", is_flag=True, help="Reset configuration file")
def setup(reset):
    """🔧 Configuration wizard"""
    if reset:
        from .config import config

        config.create_env_file()
        console.print(f"[green]✅[/] Configuration file created: {config.env_file}")
        console.print("")
        console.print("Please edit the file to set your trading password:")
        console.print(f"   vi {config.env_file}")
        console.print("")
    else:
        cmd_setup()


@main.command()
def help():
    """Show this help message and exit."""
    cmd_help()


if __name__ == "__main__":
    main()
