"""Configuration management for Futu CLI."""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Futu API configuration."""

    def __init__(self):
        # 获取脚本所在目录
        self.script_dir = Path(__file__).parent.parent.parent
        self.env_file = self.script_dir / ".env"

        # 先加载 .env 文件
        if self.env_file.exists():
            load_dotenv(self.env_file)
        else:
            # 尝试加载当前工作目录的 .env
            load_dotenv()

        # 配置项
        self.password = os.getenv("FUTU_PASSWORD", "")
        self.host = os.getenv("FUTU_HOST", "127.0.0.1")
        self.port = int(os.getenv("FUTU_PORT", "11112"))

    def check_config(self) -> bool:
        """检查配置是否完整."""
        if not self.password:
            return False
        return True

    def ensure_env_file(self):
        """确保 .env 文件存在."""
        if not self.env_file.exists():
            self.create_env_file()

    def create_env_file(self):
        """创建 .env 配置文件."""
        self.env_file.write_text(
            "# 富途牛牛配置\n"
            "FUTU_PASSWORD=你的交易密码\n"
            "FUTU_HOST=127.0.0.1\n"
            "FUTU_PORT=11112\n"
        )
        # 设置文件权限为 600（仅所有者可读写）
        self.env_file.chmod(0o600)

    def update_env_file(self, password: str = None, host: str = None, port: int = None):
        """更新 .env 文件."""
        content = "# 富途牛牛配置\n"

        if password:
            content += f"FUTU_PASSWORD={password}\n"
        elif self.password:
            content += f"FUTU_PASSWORD={self.password}\n"
        else:
            content += "FUTU_PASSWORD=你的交易密码\n"

        if host:
            content += f"FUTU_HOST={host}\n"
        else:
            content += f"FUTU_HOST={self.host or '127.0.0.1'}\n"

        if port:
            content += f"FUTU_PORT={port}\n"
        else:
            content += f"FUTU_PORT={self.port or 11112}\n"

        self.env_file.write_text(content)
        self.env_file.chmod(0o600)


# 全局配置实例
config = Config()
