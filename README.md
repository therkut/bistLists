# BIST Stock Data Fetcher & Processor

Bu proje, Borsa İstanbul (BIST) endeks verilerini (XU030, XU050, XU100, XKTUM vb.) ve Katılım Endeksi verilerini otomatik olarak çekmek, fark analizlerini işlemek ve `all_data.csv` gibi ana veri dosyalarını özel sıralama kurallarına göre güncel tutmak için geliştirilmiştir.

---

## 🚀 Özellikler

- **Endeks Veri Çekme**: BIST endekslerine ait güncel hisse senedi verilerini çeker.
- **Akıllı CSV Güncelleme**: Sadece veri değiştiğinde dosya yazarak gereksiz I/O işlemlerini engeller.
- **Katılım Endeksi & Fark Analizi**: Yeni eklenen hisseleri ve Katılım Endeksi onay durumlarını tespit eder.
- **Özel `all_data.csv` Sıralama Mantığı**:
  - `id` bilgisi mevcut olan hisseler en üstte alfabetik (A-Z) olarak sıralanır.
  - `id` bilgisi henüz olmayan (boş) hisseler en sonda alfabetik (A-Z) olarak konumlandırılır.
- **Detaylı Loglama & Hata Yönetimi**: Ağ bağlantısı ve dosya yazma süreçleri loglanır.

---

## 📁 Proje Yapısı

```
bistLists/
├── data/                             # Çıktı ve veri CSV dosyaları
│   ├── all_data.csv                  # Tüm hisseler, ID ve halka arz tarihleri (Sıralı)
│   ├── stock_xu030_data.csv          # XU030 Endeksi hisse verileri
│   ├── stock_xu050_data.csv          # XU050 Endeksi hisse verileri
│   ├── stock_xu100_data.csv          # XU100 Endeksi hisse verileri
│   └── Katilim_Endeksi_Onay_Tablosu.csv
├── src/                              # Kaynak kodlar
│   ├── fetch_stock_data.py           # Endeks verilerini çekme modülü
│   ├── fetch_difference_data.py      # Fark analizi ve all_data.csv sıralama modülü
│   ├── update_csv.py                 # CSV dosya güncelleme ve kontrol işlemleri
│   └── utils.py                      # Yardımcı fonksiyonlar
└── run.py                            # Ana çalıştırma betiği
```

---

## ⚙️ Kurulum

1. **Python 3.7+** sürümünün yüklü olduğundan emin olun.
2. Sanal ortam (virtual environment) oluşturun ve aktif edin:

```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
```

3. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

---

## 💻 Kullanım

### 1. Tüm Süreci Çalıştırma (Veri Çekme + Fark Analizi + Sıralama)

Tüm endeks verilerini çekip `all_data.csv` dosyasını otomatik sıralayarak güncellemek için:

```bash
python run.py
```

### 2. Sadece Fark Analizi ve `all_data.csv` Sıralamasını Çalıştırma

Endeks verilerini yeniden çekmeden doğrudan `all_data.csv` üzerindeki güncellemeleri ve sıralamayı çalıştırmak için:

```bash
python src/fetch_difference_data.py
```

### 3. Terminalden Tek Satır Kod İle Doğrudan `all_data.csv` Sıralama

Herhangi bir script çalıştırmadan terminal üzerinden `all_data.csv` dosyasını projedeki kurallara göre sıralamak için:

```bash
python -c "import pandas as pd; df = pd.read_csv('data/all_data.csv', dtype=str).fillna(''); non_empty = df[df['id'].str.strip() != ''].sort_values('stock', key=lambda s: s.str.upper()); empty = df[df['id'].str.strip() == ''].sort_values('stock', key=lambda s: s.str.upper()); pd.concat([non_empty, empty], ignore_index=True).to_csv('data/all_data.csv', index=False)"
```

---

## 📊 `all_data.csv` Sıralama Kuralı Detayı

`all_data.csv` dosyası işlenirken aşağıdaki kurallar uygulanır:

1. `id` sütunu dolu olan satırlar filtrelenir ve `stock` adlarına göre büyük/küçük harf duyarsız (case-insensitive) alfabetik `A-Z` sıralanır.
2. `id` sütunu boş olan satırlar filtrelenir ve `stock` adlarına göre alfabetik `A-Z` sıralanır.
3. İki grup birleştirilerek ID'li hisseler üstte, ID'siz hisseler altta kalacak şekilde [data/all_data.csv](file:///e:/TRT/Dropbox/ibrahim/PROJE/python/bistLists/data/all_data.csv) dosyasına yazılır.
