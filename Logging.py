import os
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogContext:
    guild_id: int
    channel_id: int
    user_id: int
    command_name: str
    request_id: str
    timestamp: datetime = datetime.now()
    

class SimpleLogger:
    def __init__(self, filename: str = "bot_logs.txt"):
        self.filename = filename
        
        # Create directory if needed
        os.makedirs(os.path.dirname(filename), exist_ok=True) if "/" in filename else None
        
        # Optional: add a header on startup
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"\n--- Log started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    
    def _format_message(self, message: str, level: str = "INFO", ctx: LogContext | None = None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if ctx:
            prefix = (
                f"[{timestamp}] [{level}] "
                f"[Guild:{ctx.guild_id or 'N/A'} | Channel:{ctx.channel_id or 'N/A'} | "
                f"User:{ctx.user_id or 'N/A'} | Command:{ctx.command_name or 'N/A'} | Req:{ctx.request_id}]"
            )
        else:
            prefix = f"[{timestamp}] [{level}]"
        return f"{prefix} {message}\n"

    def log(self, message: str, level: str = "INFO", ctx: LogContext | None = None):
        formatted = self._format_message(message, level, ctx)
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(formatted)

    def info(self, message: str, ctx: LogContext | None = None):
        self.log(message, "INFO", ctx)

    def warning(self, message: str, ctx: LogContext | None = None):
        self.log(message, "WARNING", ctx)

    def error(self, message: str, ctx: LogContext | None = None):
        self.log(message, "ERROR", ctx)

    def critical(self, message: str, ctx: LogContext | None = None):
        self.log(message, "CRITICAL", ctx)