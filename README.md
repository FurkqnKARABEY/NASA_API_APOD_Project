# NASA_API_APOD_Project
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# NASA API Anahtarı (Gerçek API anahtarını kullan)
API_KEY = "bZFN1Htu4LbzzQTAqFvf3Jg703Eega2bL9P6ZRmq"

# API URL'leri
APOD_URL = "https://api.nasa.gov/planetary/apod"

# Tarih aralığı (Son 7 gün)
today = datetime.date.today()
start_date = today - datetime.timedelta(days=7)

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = today.strftime('%Y-%m-%d')

# APOD verisini çekme fonksiyonu
def get_apod_data():
    params = {
        'api_key': API_KEY,
        'start_date': start_date_str,
        'end_date': end_date_str
    }
    
    response = requests.get(APOD_URL, params=params)
    apod_images = []
    
    if response.status_code == 200:
        apod_data = response.json()
        
        # API'den dönen veri bir liste mi?
        if isinstance(apod_data, list):
            entries = apod_data
        elif isinstance(apod_data, dict) and "date" in apod_data:
            entries = [apod_data]  # Tek bir giriş varsa listeye çevir
        else:
            print("Beklenmeyen JSON formatı:", apod_data)
            return []

        for entry in entries:
            # Eğer görsel içeriği varsa ekleyelim
            if "url" in entry and (entry['url'].endswith(".jpg") or entry['url'].endswith(".png")):
                apod_images.append(entry['url'])
                print(f"Tarih: {entry['date']}")
                print(f"Başlık: {entry['title']}")
                print(f"Açıklama: {entry['explanation']}")
                print(f"Görsel URL: {entry['url']}\n")
    
    else:
        print(f"APOD verisi çekilirken hata oluştu: {response.status_code}")

    return apod_images

# Grafik gösterme fonksiyonu
def plot_graphs():
    apod_images = get_apod_data()
    
    if not apod_images:
        print("Görüntü bulunamadı.")
        return

    try:
        response = requests.get(apod_images[0], stream=True)
        response.raw.decode_content = True

        # Resmin uygun formatta olup olmadığını kontrol et
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type:
            print(f"Hata: İçerik görsel değil ({content_type})")
            return

        img = Image.open(io.BytesIO(response.content))
        image_np = np.array(img)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(image_np, aspect='auto')
        ax.axis('off')
        ax.set_title("Astronomy Picture of the Day (APOD) - İlk Görsel", fontsize=14)
        plt.show()

    except Exception as e:
        print(f"Görsel yüklenirken bir hata oluştu: {e}")

# Fonksiyonu çalıştır
plot_graphs()
