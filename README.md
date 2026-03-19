# Futu CLI

> **Make Futu portfolio your CLI.** Query positions, quotes, orders and more from Futu NiuNiu.

## Install

```bash
# Install via uv (one-time)
uv tool install git+https://github.com/yourusername/futu_cli.git

# Or from source
git clone https://github.com/yourusername/futu_cli.git
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

# Query stock quote
futu quote US.AAPL
futu quote HK.00700

# Query account info
futu accinfo

# Query orders
futu orders
```

## Commands

| Command | Description |
|---------|-------------|
| `futu positions` | Query all positions (stocks, options, etc.) |
| `futu quote <code>` | Query real-time stock quote |
| `futu orders` | Query pending and history orders |
| `futu accinfo` | Query account information (cash, buying power) |
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

After running `futu setup --reset`, the configuration file is created at:
- `~/.futu-cli/.env` (when installed via `uv tool install`)
- `./.env` (when running from source)

**Security:** The file permission is set to `600` (only owner can read/write).

## Development

### Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/futu_cli.git
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

## License

Apache-2.0
