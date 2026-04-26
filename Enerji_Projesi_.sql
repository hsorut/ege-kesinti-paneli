/* ENERJİ KESİNTİ ANALİZİ - MASTER SCRIPT 
   Bu dosya tüm tabloları temizler ve analiz hazır hale getirir.
*/

-- 1. ADIM: Eski tablolar varsa temizle (Hata almamak için)
IF OBJECT_ID('Tatiller_Final', 'U') IS NOT NULL DROP TABLE Tatiller_Final;
IF OBJECT_ID('Kesintiler', 'U') IS NOT NULL DROP TABLE Kesintiler;
IF OBJECT_ID('Tatiller_Ham', 'U') IS NOT NULL DROP TABLE Tatiller_Ham;
IF OBJECT_ID('Gelecek_Kesintiler', 'U') IS NOT NULL DROP TABLE Gelecek_Kesintiler;

-- 2. ADIM: Tablo Yapılarını Oluştur
CREATE TABLE Kesintiler (
    tarih DATE,
    ilce VARCHAR(100),
    bildirimsiz_sum INT,
    bildirimli_sum INT
);

CREATE TABLE Tatiller_Ham (
    [Yıl] INT,
    [Ay] INT,
    [Gün] INT,
    [Tatil_Adı] VARCHAR(255)
);

CREATE TABLE Gelecek_Kesintiler (
    tarih DATE,
    ilce VARCHAR(100)
);

-- 3. ADIM: Verileri Ham Tablolardan Aktar
-- (Not: Veri yükleme sihirbazını kullandığın tabloların isimlerinden emin ol)
INSERT INTO Kesintiler SELECT * FROM Kesintiler_Veri;
INSERT INTO Tatiller_Ham SELECT * FROM Tatiller_Ham_Veri;
INSERT INTO Gelecek_Kesintiler SELECT * FROM Gelecek_Kesintiler_Yukleme;

-- 4. ADIM: Tatil Tarihlerini Birleştir (Madde 2)
SELECT 
    DATEFROMPARTS([Yıl], [Ay], [Gün]) AS tarih, 
    [Tatil_Adı]
INTO Tatiller_Final
FROM Tatiller_Ham;

-- 5. ADIM: FINAL BİRLEŞTİRME VE ANALİZ (Madde 3)
SELECT 
    K.tarih, 
    K.ilce, 
    (K.bildirimsiz_sum + K.bildirimli_sum) AS toplam_kesinti,
    T.[Tatil_Adı]
FROM Kesintiler AS K
LEFT JOIN Tatiller_Final AS T ON K.tarih = T.tarih
ORDER BY K.tarih;