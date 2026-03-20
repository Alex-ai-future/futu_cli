# Futu CLI

> **Make Futu portfolio your CLI.** Query positions, orders, account info and more from Futu NiuNiu.

## Install

```bash
uv tool install git+https://github.com/Alex-ai-future/futu_cli.git
```

> Requires [uv](https://docs.astral.sh/uv/). Not installed? `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Quick Start

### 1. Configure

```bash
futu setup --reset  # Creates .env file
```

### 2. Setup Futu NiuNiu

1. Open Futu NiuNiu client
2. **Settings** → **API Settings** → Enable **Listen Port**
3. Confirm address `127.0.0.1`, port `11112`

### 3. Run Commands

```bash
futu positions      # Query positions
futu accinfo        # Account info
futu cashflow       # Today's cash flow
futu history-orders # Order history
```

## Commands

| Command | Description |
|---------|-------------|
| `futu positions` | Query all positions (stocks, options, etc.) |
| `futu orders` | Query pending orders |
| `futu accinfo` | Query account info (cash, buying power) |
| `futu cashflow [date]` | Query cash flow (default: today) |
| `futu history-orders` | Query order history (default: last 90 days) |
| `futu history-fills` | Query trade history (default: last 90 days) |
| `futu setup` | Configuration wizard |

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FUTU_PASSWORD` | - | Trading password (required) |
| `FUTU_HOST` | `127.0.0.1` | API listen address |
| `FUTU_PORT` | `11112` | API listen port |

### Config File Location

```bash
futu setup  # Shows current config path
```

| Installation | Config Path |
|--------------|-------------|
| `uv tool install` | `~/.local/share/uv/tools/futu-cli/.env` |

**Security:** File permission `600` (only owner can read/write).

## For AI Agent (OpenClaw)

futu_cli uses a **two-layer architecture**:

| Layer | Install | Location | Purpose |
|-------|---------|----------|---------|
| **Tool** | `uv tool install ...` | `~/.local/share/uv/tools/futu-cli/` | Python code + `.env` |
| **Skill** | `npx skills add ...` | `~/.openclaw/workspace/skills/futu_cli/` | SKILL.md (teaches agent) |

**Important:** `.env` is in **tool directory**, NOT skill directory!

### Install for Agent

```bash
# 1. Install tool
uv tool install git+https://github.com/Alex-ai-future/futu_cli.git
futu setup --reset

# 2. Install skill
npx skills add Alex-ai-future/futu_cli -g -a openclaw
```

### Verify

In OpenClaw: > "查看我的富途持仓"

## Security

- ⚠️ **Query only** — no trading operations
- ⚠️ Password stored in local `.env` file (permission `600`)
- ⚠️ Do NOT upload `.env` to code repository

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `❌ 无法连接到富途牛牛` | Start Futu NiuNiu, enable API listening |
| `❌ 解锁交易失败` | Check password in `.env` |
| `❌ 未设置交易密码` | Run `futu setup --reset` |

## Uninstall

```bash
uv tool uninstall futu-cli
```

## License

Apache-2.0
