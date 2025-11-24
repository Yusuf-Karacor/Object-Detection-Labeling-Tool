
## 🇬🇧 English README

# Object Detection Labeling Tool

## 🚀 Project Overview
The Object Detection Labeling Tool is a desktop application built to automate YOLO-based dataset preparation.  
Using a PyQt5 interface and the Ultralytics YOLO library, it performs batch object detection across image folders and generates standard YOLO-format (.txt) label files.

This tool significantly accelerates dataset annotation and prepares outputs for tracking or training pipelines.

---

## ✨ Key Features
- **YOLO Model Integration:** Load any `.pt` YOLO model  
- **Batch Processing:** Automatically detects objects in an entire image folder  
- **Class Filtering:** Select only the classes you want to label  
- **Automatic Annotation:** Generates normalized YOLO `.txt` files  
- **Visual Output:** Saves images with bounding boxes and confidence scores  
- **Pipeline Ready:** Creates `images/`, `labels/`, and `data.yaml` for training  
- **Progress Tracking:** Displays processed/total image count in real time  

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### Steps
**1. Clone the repository:**
```bash
git clone https://github.com/Yusuf-Karacor/Object-Detection-Labeling-Tool.git
cd Object-Detection-Labeling-Tool
```

**2. Install dependencies:**
```bash
pip install ultralytics opencv-python pyqt5
```
**3. Run the application:**
```bash
python main.py
```
# 📝 Usage Guide (English)

### 1. Load a YOLO model  
Use **Sınıfları Ekle** to select your `.pt` YOLO model.

### 2. Select Classes  
Choose the classes you want to detect and label.

### 3. Select the Image Folder  
Pick the directory containing the images to be processed.

### 4. Run Detection & Labeling  
Click **Tespit Yap** and select your output directory.

---

## 📁 Output Directory Structure
```
Output_Folder/
├── tracking/
│   ├── images/       # Resized images
│   ├── labels/       # YOLO-format .txt labels
│   └── data.yaml     # YOLO training configuration
└── islenmis/         # Images with bounding boxes
```

---

# 🇹🇷 Türkçe README  
# Object Detection Labeling Tool (Nesne Tespiti Etiketleme Aracı)

## 🚀 Projeye Genel Bakış
**Object Detection Labeling Tool**, YOLO tabanlı nesne tespiti iş akışınızı otomatik hale getirmek için geliştirilmiş bir masaüstü uygulamasıdır.  
PyQt5 arayüzü ve Ultralytics YOLO kütüphanesi sayesinde, bir klasördeki tüm resimlerdeki nesneleri tespit eder ve sonuçları **YOLO formatında (.txt)** kaydeder.

Bu araç, büyük veri setlerini etiketleme sürecini hızlandırmak ve çıktıların doğrudan eğitim / takip pipeline’larında kullanılmasını sağlamak için idealdir.

---

## ✨ Temel Özellikler
- **YOLO Model Entegrasyonu:** .pt uzantılı tüm YOLO modelleri yüklenebilir.  
- **Toplu İşleme:** Bir klasördeki tüm resimleri tek seferde işler.  
- **Sınıf Filtreleme:** Sadece istediğiniz sınıfları seçip etiketletebilirsiniz.  
- **Otomatik Etiketleme:** Normalize YOLO formatında .txt etiketleri üretir.  
- **Görsel Çıktı:** Bounding box çizimli görüntüleri ayrı klasöre kaydeder.  
- **Pipeline Hazırlığı:** YOLO eğitimine hazır `images/`, `labels/`, `data.yaml` yapısı oluşturur.  
- **İlerleme Takibi:** Anlık ilerleme çubuğu ile toplam/işlenen resim sayısı gösterilir.

---

## ⚙️ Kurulum ve Çalıştırma

### 🧩 Ön Koşullar
- Python 3.8+
- pip

### 🔧 Adımlar
**1. Depoyu klonlayın:**
```bash
git clone https://github.com/Yusuf-Karacor/Object-Detection-Labeling-Tool.git
cd Object-Detection-Labeling-Tool
```

**2. Bağımlılıkları yükleyin:**
```bash
pip install ultralytics opencv-python pyqt5
```
**3. Uygulamayı başlatın:**
```bash
python main.py
```

# 📝 Nasıl Kullanılır? / How to Use

## 🇹🇷 Türkçe

### YOLO Modelini Yükleyin:
“Sınıfları Ekle” butonu ile `.pt` modelinizi seçin.

### Sınıfları Seçin:
Listeden istediğiniz sınıfları işaretleyin ve kaydırın.

### Resim Klasörünü Seçin:
İşlenecek fotoğrafların bulunduğu dizini seçin.

### Tespit ve Etiketlemeyi Başlatın:
“Tespit Yap ” butonu ile işlemi başlatın ve çıktı klasörünü seçin.

---

## 📁 Çıktı Klasör Yapısı
```
Cikti_Klasoru/
├── tracking/
│   ├── images/       # Yeniden boyutlandırılmış ham resimler
│   ├── labels/       # YOLO formatındaki etiket dosyaları (.txt)
│   └── data.yaml     # YOLO eğitim konfigürasyonu
└── islenmis/         # Bounding box çizilmiş işlenmiş görüntüler
```

---
