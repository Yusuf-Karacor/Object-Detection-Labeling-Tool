

import webbrowser
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QTimer,Qt
import os
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QCheckBox, QProgressBar, QWidget, QPushButton, QLineEdit, QLabel , QMessageBox,QSlider,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import uic
from ultralytics import YOLO

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi('main_ara.ui', self)

        self.main_horizontal_layout = QHBoxLayout(self.siniflar_widget)
        
        self.siniflar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.siniflar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.kutuphane_cekme.clicked.connect(self.kutuphane_cekme_def)
        self.listeye_aktar.clicked.connect(self.aktar)
        self.arama_button.clicked.connect(self.ara_sinif)
        self.resim_cek.clicked.connect(self.resim_cek_def)
        self.tespit_yap.clicked.connect(self.resimlerde_tespit_yap)
        self.iptal_et.clicked.connect(self.iptal_et_fonksiyon)
        self.iptal_et.setEnabled(False)
        self.github.clicked.connect(self.gitlink)
        self.linkedin.clicked.connect(self.linkedinlink)


        self.loaded_class_names = None
        self.yukleme_miktari = self.findChild(QProgressBar, 'yukleme_miktari')
        self.yukleme_miktari.hide()
        self.model_yol = None
        self.model = None
        self.loaded_class_names = None
        self.resimler= None
        self.secilen_siniflar=None


    def kutuphane_cekme_def(self):
        self.model = None
        self.loaded_class_names = None


        self.kutuphane_cekme.setStyleSheet("")
        self.model_yol  , _ = QFileDialog.getOpenFileName(self, "PT UZANTILI DOSYAYI SEÇ", "", "PT Dosyalar� (*.pt)")
        
        if self.model_yol :
            self.model = YOLO(self.model_yol) 
            print("YOLO modeli başarıyla yüklendi.")
        else:
            self.aktar()
            return
        if not self.model:
            self.aktar()
            return

        while self.main_horizontal_layout.count():
            item = self.main_horizontal_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                item.layout().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
        
        self.loaded_class_names = self.model.names
        print(f"Modelde {len(self.loaded_class_names)} adet sınıf bulundu.")
        
        current_vertical_layout = None
        checkbox_count_in_column = 0
        
        for i, class_name in self.loaded_class_names.items():
            if checkbox_count_in_column % 4 == 0:
                current_vertical_layout = QVBoxLayout()
                self.main_horizontal_layout.addLayout(current_vertical_layout)
                checkbox_count_in_column = 0

            checkbox = QCheckBox(f"ID: {i} - Sınıf Adı: {class_name}")
            current_vertical_layout.addWidget(checkbox)
            checkbox_count_in_column += 1
        
        if current_vertical_layout:
            while checkbox_count_in_column < 4:
                current_vertical_layout.addStretch(1)
                checkbox_count_in_column += 1

        self.main_horizontal_layout.addStretch(1)
        
        self.siniflar_widget.update()
        self.kutuphane_cekme.setStyleSheet("background-color: #388E3C; color: white;")
  
  
  
  
    def ara_sinif(self):
        def turkce_kucult(text):
            mapping = str.maketrans("Iİ", "ıi")
            return text.translate(mapping).casefold()
        

                # Önce tüm checkbox'ların arka planını temizle
        for i in range(self.main_horizontal_layout.count()):
            column_layout = self.main_horizontal_layout.itemAt(i).layout()
            if column_layout is None:
                continue
            for j in range(column_layout.count()):
                widget = column_layout.itemAt(j).widget()
                if isinstance(widget, QCheckBox):
                    widget.setStyleSheet("")  # eski rengini temizle

        search_text = turkce_kucult(self.search_input.text().strip())
        print(search_text)
        if not search_text:
            self.result_label.setText("Lütfen bir sınıf adı girin.")
            return

        if self.loaded_class_names is None:
            self.result_label.setText("Sınıflar henüz yüklenmedi. Lütfen önce 'Sınıfları Ekle' butonuna tıklayın.")
            return

        found_checkbox = None

        # Önce tüm checkbox'ların arka planını temizle
        for i in range(self.main_horizontal_layout.count()):
            column_layout = self.main_horizontal_layout.itemAt(i).layout()
            if column_layout is None:
                continue
            for j in range(column_layout.count()):
                widget = column_layout.itemAt(j).widget()
                if isinstance(widget, QCheckBox):
                    widget.setStyleSheet("")  # eski rengini temizle

        # Aranan sınıfı bul
        for class_id, class_name in self.loaded_class_names.items():
            if class_name.casefold().strip() == search_text:
                # Checkbox’ı bul
                for i in range(self.main_horizontal_layout.count()):
                    column_layout = self.main_horizontal_layout.itemAt(i).layout()
                    if column_layout is None:
                        continue
                    for j in range(column_layout.count()):
                        widget = column_layout.itemAt(j).widget()
                        if isinstance(widget, QCheckBox):
                            # Checkbox text'inde sınıf adını ara
                            if class_name in widget.text():
                                found_checkbox = widget
                                break
                    if found_checkbox:
                        break
                break

        if found_checkbox:
            found_checkbox.setStyleSheet("background-color: red")
            self.result_label.setText(f"'{search_text}' sınıfının ID'si: {class_id}")
        else:
            self.result_label.setText(f"'{search_text}' sınıf bulunamadı.")




    def resim_cek_def(self):
        self.resimler =None
        self.resim_cek.setStyleSheet("")
        self.resim_klasoru = QFileDialog.getExistingDirectory(self, "Klasör Seç", "")
        if not self.resim_klasoru:  
            self.resim_cek.setStyleSheet("")
            return

        resim_uzantilari = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
        self.resimler = [
            os.path.join(self.resim_klasoru, f)
            for f in os.listdir(self.resim_klasoru)
            if f.casefold().endswith(resim_uzantilari)
        ]
        self.resimler.sort()
        self.toplam_resim_sayisi = len(self.resimler)
        self.yukleme_miktari.show()

        if self.yukleme_miktari:
            self.yukleme_miktari.setMaximum(self.toplam_resim_sayisi)
            
            self.yukleme_miktari.setValue(0)
            
            self.yukleme_miktari.setFormat(f"Hazır: {self.toplam_resim_sayisi} Resim Yüklendi")
            self.yukleme_miktari.setTextVisible(True)
            

            
            QMessageBox.information(self, "Bilgi", f"Toplam {self.toplam_resim_sayisi} adet resim yüklendi. Etiketlemeye hazır.")
            self.resim_cek.setStyleSheet("background-color: #388E3C; color: white;")
        else:
            QMessageBox.warning(self, "Uyarı", "Hata: 'yukleme_miktari' bileşeni bulunamadı.")   
   
    def aktar(self):
        self.listeye_aktar.setStyleSheet("")

        target_layout = self.siniflar_widget_2.layout()
        if target_layout is None:
            target_layout = QHBoxLayout(self.siniflar_widget_2)
            self.siniflar_widget_2.setLayout(target_layout)

        while target_layout.count():
            item = target_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                item.layout().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
        QApplication.processEvents() 
        if not hasattr(self, 'model') or self.model is None:
                    QMessageBox.warning(self, "Uyarı", "Lütfen önce bir **YOLO modeli (.pt)** yükleyin.")
                    self.listeye_aktar.setStyleSheet("")
                    return

        self.secilen_siniflar = []
        for i in range(self.main_horizontal_layout.count()):
            column_layout = self.main_horizontal_layout.itemAt(i).layout()
            if column_layout is None:
                continue
            for j in range(column_layout.count()):
                widget = column_layout.itemAt(j).widget()
                if isinstance(widget, QCheckBox) and widget.isChecked():
                    class_name = widget.text().split(" - Sınıf Adı: ")[-1]
                    self.secilen_siniflar.append(class_name)

        for idx in range(0, len(self.secilen_siniflar), 4):
            current_v_layout = QVBoxLayout()
            target_layout.addLayout(current_v_layout)
            group = self.secilen_siniflar[idx:idx+4]
            for class_name in group:
                label = QLabel(f"• {class_name}")
                current_v_layout.addWidget(label)
            for _ in range(4 - len(group)):
                current_v_layout.addWidget(QLabel(""))

        target_layout.addStretch(1)
        self.siniflar_widget_2.update()
        print( self.secilen_siniflar)
        self.listeye_aktar.setStyleSheet("background-color: #388E3C; color: white;")


    def resimlerde_tespit_yap(self):
            
            self.iptal_kontrol = False
            self.tespit_yap.setStyleSheet("")



            if not self.model:
                QMessageBox.warning(self, "Uyarı", "Lütfen önce bir **YOLO modeli (.pt)** yükleyin.")
                return

            if not self.resimler:
                QMessageBox.warning(self, "Uyarı", "Lütfen önce **resim klasörünü** seçin.")
                return

           
            if not self.secilen_siniflar:
                QMessageBox.warning(self, "Uyarı", "Lütfen önce tespit etmek istediğiniz **sınıfları** seçin ve listeye aktarın.")
                return
            
            self.kayit_klasoru = QFileDialog.getExistingDirectory(self, "YOLO Etiketlerinin Kayıt Klasörünü Seç", os.getcwd())
            if not self.kayit_klasoru:
                QMessageBox.information(self, "Bilgi", "Kaydetme işlemi iptal edildi.")
                return
            
            self.tracking_klasoru = os.path.join(self.kayit_klasoru, 'tracking')

            self.labels_klasoru = os.path.join(self.tracking_klasoru, 'labels')
            self.images_klasoru = os.path.join(self.tracking_klasoru, 'images') # 💡 YENİ: Images klasörünü tanımla
            os.makedirs(self.labels_klasoru, exist_ok=True)
            os.makedirs(self.images_klasoru, exist_ok=True) # 💡 YENİ: Images klasörünü oluştur
            self.islenmis_klasoru = os.path.join(self.kayit_klasoru, 'islenmis') # 💡 YENİ: Images klasörünü tanımla
            os.makedirs(self.islenmis_klasoru, exist_ok=True)
            
            
            # Güven Eşiği (Varsayılan 0.55)
            conf_threshold = self.esik_deger.value()                
            
            self.esik_deger.setEnabled(False)
            self.kutuphane_cekme.setEnabled(False)
            self.listeye_aktar.setEnabled(False)
            self.arama_button.setEnabled(False)
            self.resim_cek.setEnabled(False)
            self.tespit_yap.setEnabled(False)
            self.iptal_et.setEnabled(True)





            
            islem_basarili = True
            sinif_esleme = {
    class_name: new_id 
    for new_id, class_name in enumerate(self.secilen_siniflar)
}



            try:
               self.tespit_yap.setStyleSheet("background-color: #388E3C; color: white;")

               for index, resim_yolu in enumerate(self.resimler): 

                    if(self.iptal_kontrol):
                        break 
                    frame = cv2.imread(resim_yolu)
                    resim_adi_uzantisiz = os.path.splitext(os.path.basename(resim_yolu))[0] 
                    
                    resim_uzantisi = os.path.splitext(resim_yolu)[1]
                    if frame is None:
                        print(f"HATA: Resim dosyası okunamadı: {resim_yolu}. Atlanıyor.")
                        continue
                    frame = cv2.resize(frame, (1920, 1080))
                    Yukseklik, Genislik, _ = frame.shape 
                    frame_2=frame.copy()
                    yolo_etiket_satirlari = []

                    results = self.model.predict(source=frame)
                    for result in results:
                        boxes = result.boxes.xyxy.cpu().numpy()
                        scores = result.boxes.conf.cpu().numpy()
                        labels = result.boxes.cls.cpu().numpy()
                    
                    for box, score, label in zip(boxes, scores, labels):
                        if score >= conf_threshold:
                            
                            label_id = int(label)
                            
                            label_text = self.model.names[label_id]
                            
                            if label_text in self.secilen_siniflar:
                                

                                yeni_id = sinif_esleme[label_text]
                                x1, y1, x2, y2 = box.astype(int)
                                SABIT_KIRMIZI = (0, 0, 255) 
                                
                                score_text = f'{score:.2f}'
                                color = SABIT_KIRMIZI # Rengi kırmızıya sabitle
                                
                                cv2.rectangle(frame_2, (x1, y1), (x2, y2), color, 2)
                                
                                etiket_metni = f'{label_text}: {score_text}' 
                                
                                cv2.putText(frame_2, etiket_metni, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                                center_x = (x1 + x2) / 2
                                center_y = (y1 + y2) / 2
                                width = x2 - x1
                                height = y2 - y1
                                
                                norm_center_x = center_x / Genislik
                                norm_center_y = center_y / Yukseklik
                                norm_width = width / Genislik
                                norm_height = height / Yukseklik
                                
                                yolo_satir = f"{yeni_id} {norm_center_x:.6f} {norm_center_y:.6f} {norm_width:.6f} {norm_height:.6f}"
                                yolo_etiket_satirlari.append(yolo_satir)
                                
                                print(f'Resim: {os.path.basename(resim_yolu)} - Tespit edilen etiket: {label_text} ({score:.2f})')

                    if yolo_etiket_satirlari:
                        etiket_dosya_yolu = os.path.join(self.labels_klasoru, f"{resim_adi_uzantisiz}.txt")
                        with open(etiket_dosya_yolu, 'w') as f:
                            f.write('\n'.join(yolo_etiket_satirlari))
                        print(f"-> {os.path.basename(etiket_dosya_yolu)} dosyasına {len(yolo_etiket_satirlari)} adet etiket yazıldı.")


                        islenmis_kayit_yolu = os.path.join(self.islenmis_klasoru, f"{resim_adi_uzantisiz}_islenmis{resim_uzantisi}")
                        cv2.imwrite(islenmis_kayit_yolu, frame_2)
                        print(f"-> İşlenmiş resim kaydedildi: {os.path.basename(islenmis_kayit_yolu)}")
                        
                        kayit_resim_yolu = os.path.join(self.images_klasoru, f"{resim_adi_uzantisiz}{resim_uzantisi}")
                        cv2.imwrite(kayit_resim_yolu, frame) 
                        print(f"-> Yeniden boyutlandırılmış (ham) resim kaydedildi: {os.path.basename(kayit_resim_yolu)}")

                    current_value = index + 1
                    self.yukleme_miktari.setValue(current_value) 
                    
                    progress_text = f"{current_value} / {self.toplam_resim_sayisi}"
                    self.yukleme_miktari.setFormat(progress_text)
                    QApplication.processEvents() 

            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Tespit sırasında bir hata oluştu: {e}")
                islem_basarili = False
                

                

            if islem_basarili:
                
                data_yaml_yolu = os.path.join(self.tracking_klasoru, 'data.yaml')

                yaml_icerigi = [
                    "path: ../", # path: '../' tracking klasöründen çıkıp ana kayit_klasoru'na gitmek için
                    "train: tracking/images",

                    "",
                    f"nc: {len(self.secilen_siniflar)}",
                    f"names: {self.secilen_siniflar}"
                ]
                
                try:
                    with open(data_yaml_yolu, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(yaml_icerigi))
                    print(f"✅ data.yaml başarıyla oluşturuldu: {data_yaml_yolu}")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"data.yaml dosyası yazılırken bir hata oluştu: {e}")
                    islem_basarili = False # YAML yazımında hata olursa işlemi başarısız olarak işaretle


            if islem_basarili:
                QMessageBox.information(
                    self, 
                    "Başarılı", 
                    f"Tüm resimler için YOLO formatında etiketler oluşturuldu, **data.yaml** dosyası hazırlandı ve sonuçlar: \n\n**'{self.tracking_klasoru}'** klasörüne kaydedildi.\n\nToplam: **{index}** resim işlendi."
                )

            self.tespit_yap.setStyleSheet("")
            self.esik_deger.setEnabled(True)
            self.kutuphane_cekme.setEnabled(True)
            self.listeye_aktar.setEnabled(True)
            self.arama_button.setEnabled(True)
            self.resim_cek.setEnabled(True)
            self.tespit_yap.setEnabled(True)
            self.iptal_et.setEnabled(False)

    def iptal_et_fonksiyon(self):
        self.iptal_kontrol = True
        self.tespit_yap.setStyleSheet("")

        # 2. Arayüzü güncelle ve butonları serbest bırak
        self.yukleme_miktari.setFormat("İPTAL İSTEĞİ ALINDI...")
        QApplication.processEvents() 


    def linkedinlink(self):
        url = "www.linkedin.com/in/yusuf-karaçor" 
        webbrowser.open(url)  
    
    def gitlink(self):
        url = "https://github.com/Yusuf-Karacor" 
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
