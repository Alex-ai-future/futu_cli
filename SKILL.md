---
name: futu-cli
description: Use futu-cli for ALL Futu NiuNiu (富途牛牛) portfolio operations — positions, orders, account info, cash flow, and trading history.
author: Alex-ai-future
version: "0.1.0"
tags: [futu, portfolio, stock, trading, finance, cli, 富途]
---

# futu-cli

**Binary:** `futu`  
**Install:** `uv tool install git+https://github.com/Alex-ai-future/futu_cli.git`

## For OpenClaw Agent

### Prerequisites

```bash
futu --help  # Check if tool is installed
uv tool install git+https://github.com/Alex-ai-future/futu_cli.git  # If not
futu setup --reset  # Configure password
```

### Install Skill

```bash
npx skills add Alex-ai-future/futu_cli -g -a openclaw
```

**Note:** `.env` is in **tool directory** (`~/.local/share/uv/tools/futu-cli/`), NOT skill directory.

## Authentication

### Step 0: Check

```bash
futu setup  # Shows config status
```

### Step 1: Configure

```bash
futu setup --reset
vi ~/.local/share/uv/tools/futu-cli/.env
```

Add:
```bash
FUTU_PASSWORD=你的交易密码
FUTU_HOST=127.0.0.1
FUTU_PORT=11112
```

### Step 2: Verify Futu NiuNiu

- ✅ Client is open
- ✅ **Settings** → **API Settings** → Enable **Listen Port**
- ✅ Port is `11112`

### Step 3: Test

```bash
futu positions
```

### Common Issues

| Symptom | Action |
|---------|--------|
| `❌ 无法连接到富途牛牛` | Open Futu NiuNiu, enable API |
| `❌ 解锁交易失败` | Check password in `.env` |
| `❌ 未设置交易密码` | Run `futu setup --reset` |

## Command Reference

### Portfolio

| Command | Description | Example |
|---------|-------------|---------|
| `futu positions` | Query positions | `futu positions` |
| `futu accinfo` | Account info | `futu accinfo` |
| `futu cashflow [date]` | Cash flow | `futu cashflow --date 2025-03-19` |

### Orders

| Command | Description | Example |
|---------|-------------|---------|
| `futu orders` | Pending orders | `futu orders` |
| `futu history-orders` | Order history | `futu history-orders --start "2025-01-01"` |
| `futu history-fills` | Trade history | `futu history-fills --code US.AAPL` |

### Account

| Command | Description |
|---------|-------------|
| `futu setup` | Config status |
| `futu setup --reset` | Create/update config |
| `futu help` | Help message |

## Agent Workflows

### Portfolio Overview

```bash
futu positions   # Holdings with P/L
futu accinfo     # Account balance
```

### Cash Flow Analysis

```bash
futu cashflow                 # Today
futu cashflow --date 2025-03-19  # Specific date
```

### Trading History

```bash
futu history-orders                    # Last 90 days
futu history-orders --code US.AAPL     # Filter by stock
futu history-fills --start "2025-01-01"  # Trade fills
```

### Daily Check

```bash
futu positions       # Holdings
futu accinfo         # Balance
futu cashflow        # Yesterday's flow
futu history-orders  # Recent orders
```

## Output Format

- **Colors**: Green = profit, Red = loss
- **Summary**: Total values at bottom
- **Currency**: Shown in 币种 column (USD, HKD, etc.)

## Error Codes

| Error | Action |
|-------|--------|
| `❌ 无法连接到富途牛牛` | Start Futu NiuNiu, enable API |
| `❌ 解锁交易失败` | Check password in `.env` (tool directory) |
| `❌ 未设置交易密码` | Run `futu setup --reset` |
| `❌ 日期格式错误` | Use `YYYY-MM-DD` format |

## Limitations

- **Query only** — no trading (buy/sell)
- **Futu NiuNiu required** — must be running with API enabled
- **Rate limited** — some APIs: 10 requests per 30s

## Safety Notes

- ⚠️ **Do NOT ask for password in chat** — guide user to edit `.env` locally
- ⚠️ **Verify before executing** — check `futu setup` first
- ⚠️ **Respect rate limits** — do not parallelize commands

## Troubleshooting

**Q: Agent can't execute commands?**

A: Verify:
1. Tool installed: `futu --help`
2. Skill installed: `npx skills list`
3. Config exists: `futu setup`

**Q: How to find config file?**

A: `futu setup` shows the exact path.
