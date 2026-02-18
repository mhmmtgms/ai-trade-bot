from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.api import router as api_router
from app.routes.panel import router as panel_router

app = FastAPI(
    title="🤖 Yapay Zeka Trade Bot Paneli",
    description="Kripto ve Polymarket işlemlerini yönettiğiniz kontrol paneli.",
    version="1.0.0",
)

# Routerları ekle
app.include_router(api_router)
app.include_router(panel_router)

# Static klasör (favicon vs için)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return {"durum": "aktif", "mesaj": "Panel çalışıyor 🚀"}
