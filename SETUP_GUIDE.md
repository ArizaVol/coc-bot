# Detaylı Kurulum Kılavuzu

Clash of Clans Bot'unu adım adım kurmanız için bu rehberi takip edin.

## Bölüm 1: Python Kurulumu

### Windows
1. https://www.python.org/downloads/ adresine git
2. Python 3.9+ sürümünü indir
3. **ÖNEMLİ**: Kurulum sırasında "Add Python to PATH" işaretlemeyi kontrol et
4. Kurulumu tamamla

```bash
python --version
pip --version
```

### macOS
```bash
brew install python3
python3 --version
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
python3 --version
```

## Bölüm 2: Android SDK (ADB) Kurulumu

### Windows - Seçenek 1: Android Studio (Tavsiye Edilen)
1. https://developer.android.com/studio adresinden Android Studio'yu indir
2. Kur ve başlat
3. Tools → Device Manager → Yeni emulator oluştur

### Windows - Seçenek 2: Command Line Tools
1. https://developer.android.com/studio#command-tools adresinden indir
2. C:\Android\cmdline-tools\ dizinine çıkar
3. Ortam değişkeni ekle:
   - ANDROID_HOME = C:\Android
   - PATH'e C:\Android\platform-tools ekle

### macOS
```bash
brew install android-platform-tools
```

### Linux
```bash
sudo apt-get install android-sdk android-sdk-platform-tools
```

**ADB'yi kontrol edin:**
```bash
adb --version
```

## Bölüm 3: BlueStacks Kurulumu

1. https://www.bluestacks.com/ adresinden indir
2. Kur ve başlat
3. Google Play Store'dan Clash of Clans indir ve yükle

### BlueStacks'te ADB'yi Etkinleştirme

1. Ayarlar (sağ üst köşe)
2. Gelişmiş → "Android Debug Bridge (ADB)"
3. "Enable ADB" butonuna tıkla
4. Emulator'u yeniden başlat

## Bölüm 4: Bağlantı Testi

```bash
adb start-server
adb connect 127.0.0.1:5555
adb devices

# Beklenen çıktı:
# List of attached devices
# 127.0.0.1:5555        device
```

**Problem olursa:**
```bash
adb kill-server
adb start-server
```

## Bölüm 5: Python Projesini Kurma

### 1. Repository'yi klonla

```bash
git clone https://github.com/ArizaVol/coc-bot.git
cd coc-bot
```

### 2. Virtual Environment oluştur

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 4. Konfigürasyon dosyasını kontrol et

`config.yaml` dosyasında BlueStacks ayarlarınız doğru mu kontrol edin.

## Bölüm 6: Test Etme

### Adım 1: BlueStacks Aç
1. BlueStacks'i başlat
2. Clash of Clans'ı aç
3. Ana ekran görünür olana kadar bekle

### Adım 2: Botu Çalıştır

```bash
python bot.py
```

**Beklenen çıktı:**
```
2026-05-22 10:15:30 - __main__ - INFO - ==================================================
2026-05-22 10:15:30 - __main__ - INFO - Clash of Clans Bot Initialized
2026-05-22 10:15:31 - adb_manager - INFO - Connecting to device: 127.0.0.1:5555
2026-05-22 10:15:32 - adb_manager - INFO - ✓ Successfully connected to device
```

## 🐛 Hata Giderme

### "adb: command not found"
```bash
# ADB PATH'e eklenmiş mi kontrol et
echo %PATH%  # Windows
echo $PATH   # macOS/Linux
```

### "Failed to connect to device"
```bash
adb kill-server
adb start-server
adb connect 127.0.0.1:5555
```

### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install --upgrade opencv-python
```

---

**Kurulum sırasında sorun yaşarsan, bot.log dosyasını kontrol et!**
