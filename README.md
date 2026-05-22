# Clash of Clans Bot - Educational Version

🤖 Private server üzerinde çalışan, öğrenme amacıyla oluşturulmuş Clash of Clans otomasyon botu.

## ⚠️ Uyarı

Bu bot **SADECE** kendi private server'ınızda test amacıyla kullanılmalıdır. Gerçek Clash of Clans sunucularına karşı kullanılması Supercell'in Hizmet Şartları ihlalidir ve hesabınızın yasaklanmasına neden olabilir.

## 🎯 Özellikler

- ✅ ADB üzerinden Android emülatöre bağlantı
- ✅ Ekran görüntüsü alma ve analiz
- ✅ Template Matching ile UI butonlarını bulma
- ✅ Otomatik saldırı düzenleme
- ✅ Kaynak filtreleme (altın/iksir)
- ✅ Hedef kaynak seviyesine ulaşınca durma
- ✅ Detaylı logging sistemi
- ✅ YAML tabanlı konfigürasyon

## 📋 Gereksinimler

- Python 3.8+
- Android SDK (ADB)
- BlueStacks Emulator veya benzer Android emulator
- OpenCV, Pillow, NumPy

## 🚀 Kurulum

### 1. Android SDK kurulumu

**Windows:**
```bash
choco install android-sdk
```

**macOS:**
```bash
brew install android-sdk
```

**Linux:**
```bash
sudo apt-get install android-sdk
```

### 2. Python bağımlılıklarını yükleyin

```bash
pip install -r requirements.txt
```

### 3. BlueStacks'i kurup ayarlayın

1. [BlueStacks](https://www.bluestacks.com/) indir ve kur
2. Clash of Clans'ı BlueStacks'a yükle
3. Ayarlar → Gelişmiş → ADB'yi etkinleştir

### 4. ADB bağlantısını test edin

```bash
adb connect 127.0.0.1:5555
adb devices
```

## ⚙️ Konfigürasyon

`config.yaml` dosyasını düzenleyin:

```yaml
adb:
  device_ip: "127.0.0.1"
  device_port: 5555

game:
  min_gold: 50000
  min_elixir: 50000
  target_gold_threshold: 200000
  target_elixir_threshold: 200000

bot:
  attack_delay: 5
  debug_mode: true
```

## 🎮 Kullanım

```bash
python bot.py
```

## 📊 Log Dosyası

Tüm işlemler `bot.log` dosyasına kaydedilir.

## 🔧 Modüller

- `adb_manager.py` - Android cihaza bağlantı
- `vision.py` - Görüntü analizi
- `game_state.py` - Oyun durumu takibi
- `bot.py` - Ana bot mantığı

## 📚 Kaynaklar

- [ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [OpenCV Python Tutorial](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [Python YAML](https://pyyaml.org/)

---

**Versiyon:** 1.0.0-beta
**Durum:** 🚧 Aktif Geliştirme
