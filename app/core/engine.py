import threading
import time
import random
from datetime import datetime
from .state import STATE


class BotEngine:
    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        if self.is_running():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _simulate_trade(self, price: float, now: str) -> None:
        snap = STATE.snapshot()

        position = snap.get("position", 0)
        balance = snap.get("balance", 10000.0)
        entry_price = snap.get("entry_price", None)

        # BUY: pozisyon yoksa ve fiyat düşükse
        if position == 0 and price < 97:
            STATE.update_runtime({
                "position": 1,
                "entry_price": price,
                "last_trade": f"BUY @ {price}"
            })
            STATE.add_log(f"[{now}] ✅ BUY executed @ {price}")

        # SELL: pozisyon varsa ve fiyat yüksekse
        elif position == 1 and price > 103 and entry_price is not None:
            pnl = round(price - float(entry_price), 2)
            new_balance = round(balance + pnl, 2)

            STATE.update_runtime({
                "position": 0,
                "entry_price": None,
                "balance": new_balance,
                "last_trade": f"SELL @ {price} | PnL: {pnl} | Balance: {new_balance}"
            })
            STATE.add_log(f"[{now}] ✅ SELL executed @ {price} | PnL: {pnl} | Balance: {new_balance}")

    def _run_loop(self) -> None:
        STATE.set_bot_active(True)

        while not self._stop_event.is_set():
            now = datetime.now().strftime("%H:%M:%S")

            # 1) Fake fiyat üret (95-105 arası)
            price = round(random.uniform(95, 105), 2)

            # 2) Runtime state güncelle
            STATE.update_runtime({
                "last_heartbeat_at": now,
                "last_price": price
            })

            # 3) Log yaz
            STATE.add_log(f"[{now}] Heartbeat | Price: {price}")

            # 4) Fake trade simülasyonu
            self._simulate_trade(price, now)

            time.sleep(10)

        STATE.set_bot_active(False)


ENGINE = BotEngine()
