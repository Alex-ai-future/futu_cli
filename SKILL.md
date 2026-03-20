---
name: futu-cli
description: Use futu-cli for ALL Futu NiuNiu (富途牛牛) portfolio operations — checking positions, orders, account info, cash flow, and trading history. Invoke whenever the user requests any Futu portfolio interaction.
author: Alex-ai-future
version: "0.1.0"
tags:
  - futu
  - portfolio
  - stock
  - trading
  - finance
  - cli
  - 富途
---

# futu-cli — Futu Portfolio CLI Tool

**Binary:** `futu`
**Credentials:** `.env` file with trading password (stored locally)

## Setup

```bash
# Install (requires Python 3.9+)
uv tool install git+https://github.com/Alex-ai-future/futu_cli.git

# Upgrade to latest (recommended)
uv tool upgrade futu-cli
```

## For OpenClaw Agent

### Installation

```bash
npx skills add Alex-ai-future/futu_cli -g -a openclaw
```

| Flag | Description |
|------|-------------|
| `-g` | Global install (user-level, shared across projects) |
| `-a openclaw` | Target specific agent |
| `-y` | Non-interactive mode |

### Important: Path Configuration

**After installation:**
- Skill location: `~/.openclaw/workspace/skills/futu_cli/`
- Config file: `<skill-directory>/.env`

**Ensure agent has permissions to:**
- Read/write `.env` file (for trading password)
- Execute Python scripts

### Verify Installation

In OpenClaw conversation:
> "查看我的富途持仓"

## Authentication

**IMPORTANT FOR AGENTS**: Before executing ANY futu command, check if credentials exist first. Do NOT assume password is configured.

### Step 0: Check if already configured

```bash
futu setup  # Shows config file path and status
```

If password is set and Futu NiuNiu is running, skip to [Command Reference](#command-reference).
If password is missing, proceed to Step 1.

### Step 1: Guide user to configure

```bash
futu setup --reset  # Creates/updates .env file
```

Then edit the `.env` file to set the trading password:
```bash
vi ~/.openclaw/workspace/skills/futu_cli/.env
```

Add:
```bash
FUTU_PASSWORD=你的交易密码
FUTU_HOST=127.0.0.1
FUTU_PORT=11112
```

### Step 2: Verify Futu NiuNiu is running

Ensure:
1. ✅ Futu NiuNiu client is open
2. ✅ API listening is enabled (Settings → API Settings)
3. ✅ Listen port is 11112 (default)

### Step 3: Test connection

```bash
futu positions  # Should display positions if everything is configured correctly
```

### Handle common auth issues

| Symptom | Agent action |
|---------|-------------|
| `❌ 无法连接到富途牛牛` | Ask user to open Futu NiuNiu client and enable API listening |
| `❌ 解锁交易失败` | Check trading password in `.env` file |
| `❌ 未设置交易密码` | Run `futu setup --reset` and guide user to set password |

## Command Reference

### Portfolio Queries

| Command | Description | Example |
|---------|-------------|---------|
| `futu positions` | Query all positions | `futu positions` |
| `futu accinfo` | Query account info | `futu accinfo` |
| `futu cashflow [date]` | Query cash flow for date | `futu cashflow --date 2025-03-19` |

### Order History

| Command | Description | Example |
|---------|-------------|---------|
| `futu orders` | Query pending orders | `futu orders` |
| `futu history-orders` | Query order history | `futu history-orders --start "2025-01-01"` |
| `futu history-fills` | Query trade history | `futu history-fills --code US.AAPL` |

### Account Management

| Command | Description |
|---------|-------------|
| `futu setup` | Show config status |
| `futu setup --reset` | Create/update config file |
| `futu help` | Show help message |

## Agent Workflow Examples

### Check portfolio overview

```bash
# Get positions with P/L
futu positions

# Get account balance
futu accinfo
```

### Analyze today's cash flow

```bash
# Today's cash flow
futu cashflow

# Specific date
futu cashflow --date 2025-03-19
```

### Review trading history

```bash
# Last 90 days orders
futu history-orders

# Filter by stock
futu history-orders --code US.AAPL

# Trade fills
futu history-fills --start "2025-01-01 00:00:00"
```

### Daily portfolio check workflow

```bash
# Morning check
futu positions          # Current holdings
futu accinfo           # Account balance
futu cashflow          # Yesterday's cash flow
futu history-orders    # Recent orders
```

## Output Format

All commands output Rich-formatted tables with:
- **Colors**: Green for profit, red for loss
- **Summary**: Total values at bottom
- **Currency**: USD, HKD, etc. shown in 币种 column

### Example: positions output

```
📊 持仓情况
┏━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ 代码 ┃ 名称 ┃ 方向 ┃ 类型 ┃ 币种 ┃ 成本价   ┃ 市价   ┃ 持仓 ┃ 市值     ┃ 盈亏   ┃ 盈亏率 ┃
┡━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ US.… │ AAPL │ 多   │ 正股 │ USD  │ $150.000 │ $155.… │ 100  │ $15,500 │ +$500  │ +3.33% │
│ HK.… │ 腾讯 │ 多   │ 港股 │ HKD  │ $350.000 │ $370.… │ 200  │ $74,000 │ +$4,000│ +5.71% │
└──────┴──────┴──────┴──────┴──────┴─────────┴────────┴──────┴─────────┴────────┴────────┘

总市值：$89,500 | 总盈亏：+$4,500
```

## Error Codes

| Error | Code | Agent action |
|-------|------|-------------|
| Connection failed | `❌ 无法连接到富途牛牛` | Ask user to start Futu NiuNiu and enable API |
| Password error | `❌ 解锁交易失败` | Check password in `.env`, remind about remaining attempts |
| Missing password | `❌ 未设置交易密码` | Run `futu setup --reset` |
| Invalid date format | `❌ 日期格式错误` | Use `YYYY-MM-DD` format (e.g., `2025-03-19`) |
| Query failed | `❌ 查询失败` | Check specific error message |

## Limitations

- **Query only** — no trading operations (buy/sell not supported)
- **Futu NiuNiu required** — client must be running with API enabled
- **Real trading only** — simulated accounts not supported for some queries
- **Rate limited** — some APIs have rate limits (e.g., 10 requests per 30s)
- **Single account** — one Futu account at a time

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FUTU_PASSWORD` | — | Trading password (required) |
| `FUTU_HOST` | `127.0.0.1` | API listen address |
| `FUTU_PORT` | `11112` | API listen port |

## Safety Notes for Agents

- **Do NOT ask for password in chat** — guide user to edit `.env` file locally
- **Treat password as secret** — do not echo `.env` content to stdout
- **Verify before executing** — check `futu setup` before running queries
- **Handle errors gracefully** — provide actionable guidance based on error type
- **Respect rate limits** — do not parallelize multiple futu commands

## Troubleshooting

**Q: Commands fail with connection error?**

A: Check:
1. Futu NiuNiu client is running
2. API listening is enabled (Settings → API Settings)
3. Port is correct (default 11112)

**Q: Password error?**

A: 
1. Check `.env` file has correct password
2. Password has limited attempts (usually 10)
3. Edit `.env` to update password

**Q: How to find config file?**

A: Run `futu setup` — it shows the exact path to the `.env` file.

**Q: Agent can't execute commands?**

A: Verify:
1. Skill is installed: `npx skills list`
2. `.env` file exists and is configured
3. Agent has execute permissions
