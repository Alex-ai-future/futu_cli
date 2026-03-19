#!/usr/bin/env python3
"""
Futu CLI - Make Futu portfolio your CLI.

Query positions, orders, account info and more from Futu NiuNiu.
"""

import sys
import os
import click
from click.shell_completion import CompletionItem
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


def complete_stock_code(ctx, param, incomplete):
    """Complete stock codes."""
    # Common stock codes for completion
    choices = [
        "US.AAPL", "US.TSLA", "US.NVDA", "US.MSFT", "US.GOOGL", "US.AMZN",
        "HK.00700", "HK.09988", "HK.09618", "HK.01024", "HK.01810",
    ]
    return [
        CompletionItem(code)
        for code in choices
        if code.lower().startswith(incomplete.lower())
    ]


def complete_date(ctx, param, incomplete):
    """Complete date format hint."""
    return [CompletionItem("2025-03-19", help="YYYY-MM-DD format")]


def complete_datetime(ctx, param, incomplete):
    """Complete datetime format hint."""
    return [CompletionItem("2025-03-19 00:00:00", help="YYYY-MM-DD HH:MM:SS format")]


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
@click.option("--date", "-d", default=None, help="Clearing date (yyyy-MM-dd format, default: today)", shell_complete=complete_date)
def cashflow(date):
    """📋 Query account cash flow"""
    cmd_cashflow(date)


@main.command()
@click.option("--start", "-s", default=None, help="Start time (YYYY-MM-DD HH:MM:SS)", shell_complete=complete_datetime)
@click.option("--end", "-e", default=None, help="End time (YYYY-MM-DD HH:MM:SS)", shell_complete=complete_datetime)
@click.option("--code", "-c", default=None, help="Stock code filter", shell_complete=complete_stock_code)
def history_orders(start, end, code):
    """📋 Query history orders"""
    cmd_history_orders(start=start, end=end, code=code)


@main.command()
@click.option("--start", "-s", default=None, help="Start time (YYYY-MM-DD HH:MM:SS)", shell_complete=complete_datetime)
@click.option("--end", "-e", default=None, help="End time (YYYY-MM-DD HH:MM:SS)", shell_complete=complete_datetime)
@click.option("--code", "-c", default=None, help="Stock code filter", shell_complete=complete_stock_code)
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


@main.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell):
    """Generate tab completion script.
    
    Usage:
        # Bash
        futu completion bash >> ~/.bash_completion
        
        # Zsh
        futu completion zsh >> ~/.zshrc
        
        # Fish
        futu completion fish >> ~/.config/fish/completions/futu.fish
    """
    from click.shell_completion import add_completion_class, BashComplete, ZshComplete, FishComplete
    
    if shell == "bash":
        complete = BashComplete(main, {}, "futu", "_FUTU_COMPLETE")
        click.echo(complete.source())
    elif shell == "zsh":
        complete = ZshComplete(main, {}, "futu", "_FUTU_COMPLETE")
        click.echo(complete.source())
    elif shell == "fish":
        complete = FishComplete(main, {}, "futu", "_FUTU_COMPLETE")
        click.echo(complete.source())


if __name__ == "__main__":
    main()
