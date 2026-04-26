from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import date

class TatilDurumu(BaseModel):
    resmi_tatil_mi: bool
    tatil_adi: Optional[str] = None

class GunlukVeri(BaseModel):
    tarih: date
    toplam_kesinti: int
    durum: str
    tatil_durumu: TatilDurumu

class KesintilerResponse(BaseModel):
    ilce_adi: str
    secilen_esik_deger: int
    toplam_kritik_gun_sayisi: int
    veriler: list[GunlukVeri]

app = FastAPI(title="Elektrik Kesintisi Gözlem Paneli")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_DB = {
    "manisa-ahmetli": [
        {"tarih": date(2023, 11, 24), "bildirimsiz_sum": 0, "bildirimli_sum": 1, "tatil_adi": None},
        {"tarih": date(2023, 11, 25), "bildirimsiz_sum": 3, "bildirimli_sum": 4, "tatil_adi": None},
        {"tarih": date(2023, 11, 26), "bildirimsiz_sum": 1, "bildirimli_sum": 2, "tatil_adi": "Cumhuriyet Bayramı"},
        {"tarih": date(2023, 11, 27), "bildirimsiz_sum": 0, "bildirimli_sum": 0, "tatil_adi": None},
    ],
    "izmir-bornova": [
        {"tarih": date(2023, 11, 24), "bildirimsiz_sum": 5, "bildirimli_sum": 5, "tatil_adi": None},
        {"tarih": date(2023, 11, 25), "bildirimsiz_sum": 0, "bildirimli_sum": 2, "tatil_adi": None},
    ],
}

def fetch_from_mock_db(ilce_adi: str):
    return MOCK_DB.get(ilce_adi, None)

@app.get("/api/kesintiler/{ilce_adi}", response_model=KesintilerResponse)
def get_kesintiler(
    ilce_adi: str,
    esik: int = Query(default=5, ge=0, description="Kritik eşik değeri (varsayılan: 5)"),
):
    rows = fetch_from_mock_db(ilce_adi)
    if rows is None:
        raise HTTPException(status_code=404, detail=f"'{ilce_adi}' için kayıt bulunamadı.")
    veriler: list[GunlukVeri] = []
    kritik_gun_sayisi = 0
    for row in rows:
        toplam_kesinti = (row["bildirimsiz_sum"] or 0) + (row["bildirimli_sum"] or 0)
        durum = "KRITIK" if toplam_kesinti >= esik else "NORMAL"
        if durum == "KRITIK":
            kritik_gun_sayisi += 1
        veriler.append(
            GunlukVeri(
                tarih=row["tarih"],
                toplam_kesinti=toplam_kesinti,
                durum=durum,
                tatil_durumu=TatilDurumu(
                    resmi_tatil_mi=row["tatil_adi"] is not None,
                    tatil_adi=row["tatil_adi"],
                ),
            )
        )
    return KesintilerResponse(
        ilce_adi=ilce_adi,
        secilen_esik_deger=esik,
        toplam_kritik_gun_sayisi=kritik_gun_sayisi,
        veriler=veriler,
    )
