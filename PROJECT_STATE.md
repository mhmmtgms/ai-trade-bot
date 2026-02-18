\# AI Trade Bot — PROJECT STATE (B0)



\## Ortam

\- OS: Windows

\- Python: 3.12

\- Framework: FastAPI + Uvicorn

\- Çalışma: Local (http://127.0.0.1:8000)

\- Editör: Not Defteri (VS Code kullanılmıyor)



\## Proje Yapısı

ai\_trade\_bot/

\- app/

&nbsp; - core/

&nbsp;   - state.py

&nbsp;   - engine.py

&nbsp; - routes/

&nbsp;   - api.py

&nbsp;   - panel.py

&nbsp; - templates/

&nbsp;   - dashboard.html

&nbsp; - static/

&nbsp; - main.py

\- venv/ (GitHub'a eklenmez)

\- requirements.txt



\## State (app/core/state.py)

\- BotSettings ayarları memory’de tutulur

\- Thread-safe lock var

\- snapshot(), update\_settings(), set\_bot\_active()

\- Runtime alanları eklendi:

&nbsp; - last\_price, position (0/1), balance, entry\_price, last\_trade, logs

\- add\_log() log tutar (limit: 50)

\- update\_runtime() runtime alanlarını günceller



\## Engine (app/core/engine.py)

\- BotEngine thread ile çalışır

\- start(), stop(), is\_running()

\- Loop içinde:

&nbsp; - Fake fiyat üretir (95-105)

&nbsp; - heartbeat günceller

&nbsp; - log yazar

&nbsp; - basit BUY/SELL simülasyonu yapar

\- CPU/RAM sorunu yaşandı (Chrome/Panel donması)

\- Çözüm: loop süresi ve panel polling artırılacak (ör: 10 sn)



\## API (app/routes/api.py)

\- GET /ayarlar

\- POST /ayarlar

\- GET /bot/status

\- B0 için ayrıca planlanan endpointler:

&nbsp; - GET /bot/summary

&nbsp; - GET /bot/logs



\## Panel (app/templates/dashboard.html)

\- /panel sayfası var

\- Ayarlar formu + Toggle çalışıyor

\- Sağ panel canlı özet var

\- B0 için runtime/log kutuları eklendi

\- Polling ile /bot/summary ve /bot/logs çekilecek

\- Performans için:

&nbsp; - polling süresi 10 sn veya daha fazla

&nbsp; - log ekranda sadece son 20 satır gösterilecek



\## Çalıştırma

PowerShell/CMD:

1\) cd C:\\Users\\user\\Desktop\\ai\_trade\_bot

2\) venv\\Scripts\\activate

3\) uvicorn app.main:app

(Not: --reload kullanılmıyor)



\## Son Hedef (B0)

1\) Engine stabil: donma yok, düşük CPU

2\) Runtime: heartbeat/price/position/balance panelde görünsün

3\) Logs: panelde akış düzgün görünsün



