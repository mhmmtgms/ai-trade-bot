from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import threading
from datetime import datetime


@dataclass
class BotSettings:
    bot_aktif: bool = False
    maksimum_acik_pozisyon: int = 10
    gunluk_maks_islem: int = 100
    islem_basi_risk_usd: float = 2.0
    kar_al_yuzde: float = 3.0
    zarar_durdur_yuzde: float = 1.0
    zaman_dilimleri_dakika: List[int] = field(default_factory=lambda: [5, 10, 15, 30])
    piyasalar: List[str] = field(default_factory=lambda: ["BTC", "ETH"])


class AppState:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.settings = BotSettings()
        self.last_saved_at: str | None = None
        self.last_status: str = "KAPALI"
        self.last_heartbeat_at: str | None = None
        # --- Runtime (engine) state ---
        self.last_price: float | None = None
        self.position: int = 0              # 0 = pozisyon yok, 1 = long (B0 basit)
        self.balance: float = 10000.0
        self.entry_price: float | None = None
        self.last_trade: str | None = None
        self.logs: List[str] = []


    def snapshot(self) -> dict:
        with self.lock:
            s = self.settings
            return {
                "bot_aktif": s.bot_aktif,
                "maksimum_acik_pozisyon": s.maksimum_acik_pozisyon,
                "gunluk_maks_islem": s.gunluk_maks_islem,
                "islem_basi_risk_usd": s.islem_basi_risk_usd,
                "kar_al_yuzde": s.kar_al_yuzde,
                "zarar_durdur_yuzde": s.zarar_durdur_yuzde,
                "zaman_dilimleri_dakika": list(s.zaman_dilimleri_dakika),
                "piyasalar": list(s.piyasalar),
                "last_saved_at": self.last_saved_at,
                "last_status": self.last_status,
                "last_heartbeat_at": self.last_heartbeat_at,
                # --- Runtime (engine) ---
                "last_price": self.last_price,
                "position": self.position,
                "balance": self.balance,
                "entry_price": self.entry_price,
                "last_trade": self.last_trade,
                "logs": list(self.logs),

            }

    def update_settings(self, data: dict) -> dict:
        with self.lock:
            for k, v in data.items():
                if hasattr(self.settings, k):
                    setattr(self.settings, k, v)
            self.last_saved_at = datetime.now().strftime("%H:%M:%S kaydedildi")
            return self.snapshot()

    def set_bot_active(self, active: bool) -> dict:
        with self.lock:
            self.settings.bot_aktif = active
            self.last_status = "ACIK" if active else "KAPALI"
            self.last_heartbeat_at = datetime.now().strftime("%H:%M:%S")
            return self.snapshot()

    def add_log(self, message: str) -> None:
        with self.lock:
            self.logs.append(message)
            if len(self.logs) > 50:
                self.logs.pop(0)

    def update_runtime(self, data: dict) -> dict:
        with self.lock:
            for k, v in data.items():
                if hasattr(self, k):
                    setattr(self, k, v)
            return self.snapshot()

STATE = AppState()
