from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
from app.core.state import STATE
from app.core.engine import ENGINE

router = APIRouter()


class AyarGuncelle(BaseModel):
    bot_aktif: bool | None = Field(None)
    maksimum_acik_pozisyon: int | None = Field(None)
    gunluk_maks_islem: int | None = Field(None)
    islem_basi_risk_usd: float | None = Field(None)
    kar_al_yuzde: float | None = Field(None)
    zarar_durdur_yuzde: float | None = Field(None)
    zaman_dilimleri_dakika: List[int] | None = Field(None)
    piyasalar: List[str] | None = Field(None)


@router.get("/ayarlar")
def ayarlari_getir():
    return STATE.snapshot()


@router.post("/ayarlar")
def ayarlari_guncelle(payload: AyarGuncelle):
    data = payload.model_dump(exclude_none=True)

    # Bot aç/kapa
    if "bot_aktif" in data:
        active = bool(data.pop("bot_aktif"))
        if active:
            ENGINE.start()
        else:
            ENGINE.stop()
        STATE.set_bot_active(active)

    # Diğer ayarları güncelle
    if data:
        return {"guncellendi": True, "yeni_ayarlar": STATE.update_settings(data)}

    return {"guncellendi": True, "yeni_ayarlar": STATE.snapshot()}


@router.get("/bot/status")
def bot_status():
    return {"running": ENGINE.is_running(), "state": STATE.snapshot()}


# ✅ Yeni: Logları al
@router.get("/bot/logs")
def bot_logs():
    snap = STATE.snapshot()
    return {"logs": snap.get("logs", [])}


# ✅ Yeni: Panel için kolay özet (opsiyonel ama çok pratik)
@router.get("/bot/summary")
def bot_summary():
    snap = STATE.snapshot()
    return {
        "running": ENGINE.is_running(),
        "bot_aktif": snap.get("bot_aktif"),
        "last_status": snap.get("last_status"),
        "last_heartbeat_at": snap.get("last_heartbeat_at"),
        "last_price": snap.get("last_price"),
        "position": snap.get("position"),
        "balance": snap.get("balance"),
        "entry_price": snap.get("entry_price"),
        "last_trade": snap.get("last_trade"),
    }
