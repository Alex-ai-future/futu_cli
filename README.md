# Futu CLI

> **Make Futu portfolio your CLI.** Query positions, orders, account info and more from Futu NiuNiu.

## Install

```bash
# Install via uv (one-time)
uv tool install git+https://github.com/Alex-ai-future/futu_cli.git

# Or from source
git clone https://github.com/Alex-ai-future/futu_cli.git
cd futu_cli
uv tool install .
```

> **Note:** Requires [uv](https://docs.astral.sh/uv/) to be installed. If not installed:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

## Quick Start

### 1. Configure (first time only)

```bash
# Create configuration file
futu setup --reset

# Edit the configuration file to set your trading password
# The file location will be shown after running setup --reset
```

### 2. Setup Futu NiuNiu

1. Open Futu NiuNiu client
2. Go to **Settings** → **API Settings**
3. Enable **Listen Port**
4. Ensure listen address is `127.0.0.1` (default port 11112)

### 3. Run Commands

```bash
# Query positions
futu positions

# Query account info
futu accinfo

# Query orders
futu orders

# Query cash flow (default: today)
futu cashflow

# Query cash flow for specific date
futu cashflow --date 2025-03-19

# Query history orders (default: last 90 days)
futu history-orders

# Query history orders with filters
futu history-orders --start "2025-01-01 00:00:00" --code US.AAPL

# Query history deals/fills
futu history-fills
futu history-fills --code HK.00700
```

## Commands

| Command | Description |
|---------|-------------|
| `futu positions` | Query all positions (stocks, options, etc.) |
| `futu orders` | Query pending and history orders |
| `futu accinfo` | Query account information (cash, buying power) |
| `futu cashflow [date]` | Query account cash flow for specified date (yyyy-MM-dd) |
| `futu history-orders` | Query history orders (default: last 90 days) |
| `futu history-fills` | Query history deals/fills (default: last 90 days) |
| `futu setup` | Configuration wizard |
| `futu help` | Show help message |

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FUTU_PASSWORD` | - | Trading password (required) |
| `FUTU_HOST` | `127.0.0.1` | API listen address |
| `FUTU_PORT` | `11112` | API listen port |

### Config File Location

The `.env` file is located in the **project root directory**:

| Installation | Config Path |
|--------------|-------------|
| Source run | `futu_cli/.env` |
| `uv tool install` | `~/.local/share/uv/tools/futu-cli/.env` |
| AI Agent skill | `<skill-directory>/.env` |

**To find your config path:**
```bash
futu setup  # Shows the current config file path
```

**Security:** The file permission is set to `600` (only owner can read/write).

## Development

### Setup Environment

```bash
# Clone the repository
git clone https://github.com/Alex-ai-future/futu_cli.git
cd futu_cli

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Run Commands

```bash
# Run directly
python -m futu_cli.main positions

# Or use the installed command (after uv tool install)
futu positions
```

## Troubleshooting

### Connection Failed

- Check if Futu NiuNiu client is running
- Verify API listen is enabled (Settings → API Settings)
- Ensure port number is correct (default 11112)

### Unlock Trade Failed

- Check if trading password is correct
- Verify remaining attempt count

### Module Import Error

```bash
# Install futu-api package
pip install futu-api python-dotenv
```

## Security

- ⚠️ Trading password is stored in local `.env` file
- ⚠️ File permission is `600` (only owner can read/write)
- ⚠️ Do NOT upload `.env` to code repository or share with others
- ⚠️ This tool is for **query only**, no trading operations

## Uninstall

```bash
uv tool uninstall futu-cli
```

## For AI Agent (OpenClaw)

futu_cli 自带 [`SKILL.md`](./SKILL.md)，让 AI Agent 能自动学习并使用本工具。

### Skills CLI（推荐）

```bash
npx skills add Alex-ai-future/futu_cli -g -a openclaw
```

| 参数 | 说明 |
|------|------|
| `-g` | 全局安装（用户级别，跨项目共享） |
| `-a openclaw` | 指定目标 Agent |
| `-y` | 非交互模式 |

### 重要：Agent 路径配置

Agent 需要访问 futu_cli 的外部路径才能正确执行命令。

**安装后的路径：**
- 技能位置：`~/.openclaw/workspace/skills/futu_cli/`
- 配置文件：技能目录下的 `.env` 文件

**确保 Agent 有以下权限：**
- 读取/写入 `.env` 文件（配置交易密码）
- 执行 Python 脚本

### 验证安装

在 OpenClaw 中对话：
> "查看我的富途持仓"

### 常见问题

**Q: Agent 无法执行命令？**

A: 检查以下几点：
1. 技能是否正确安装（运行 `npx skills list` 查看）
2. `.env` 文件是否存在且配置正确
3. 富途牛牛客户端是否已启动并开启 API 监听

**Q: 如何修改配置？**

A: 编辑技能目录下的 `.env` 文件：
```bash
vi ~/.openclaw/workspace/skills/futu_cli/.env
```

## Tab Completion

Enable tab completion for faster command input:

```bash
# Bash
futu completion bash >> ~/.bash_completion
source ~/.bash_completion

# Zsh
futu completion zsh >> ~/.zshrc
source ~/.zshrc

# Fish
futu completion fish >> ~/.config/fish/completions/futu.fish
```

**What gets completed:**
- Command names: `futu posi[Tab]` → `futu positions`
- Options: `futu cashflow --[Tab]` → `--date`, `--help`
- Stock codes: `futu quote US.[Tab]` → `US.AAPL`, `US.TSLA`, etc.
- Date formats: `futu cashflow --date [Tab]` → `2025-03-19`

## License

Apache-2.0
