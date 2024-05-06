import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import sqlite3

# Seyahat sınıfı, bir seyahatin rotasını ve konaklama bilgilerini temsil eder
class Seyahat:
    def __init__(self, rota, konaklama_bilgileri):
        self.rota = rota  # Seyahatin rotası
        self.konaklama_bilgileri = konaklama_bilgileri  # Seyahatin konaklama bilgileri

# Konaklama sınıfı, bir konaklama tesisi adını ve fiyatını temsil eder
class Konaklama:
    def __init__(self, tesis_adi, fiyat):
        self.tesis_adi = tesis_adi  # Konaklama tesisi adı
        self.fiyat = fiyat  # Konaklama fiyatı

    def __str__(self):
        return f"{self.tesis_adi}, {self.fiyat}"

# Rota sınıfı, bir seyahatin rota detaylarını ve konaklama seçeneklerini temsil eder
class Rota:
    def __init__(self, rota_detaylari, konaklama_secenekleri):
        self.rota_detaylari = rota_detaylari  # Rota detayları
        self.konaklama_secenekleri = konaklama_secenekleri  # Konaklama seçenekleri

# Veritabanı sınıfı, SQLite3 bağlantısını yönetir
class Veritabani:
    def __init__(self):
        self.conn = sqlite3.connect('seyahat.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Seyahat (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                rota TEXT,
                                konaklama_bilgileri TEXT)''')
        self.conn.commit()

    def insert_seyahat(self, rota, konaklama_bilgileri):
        self.cursor.execute("INSERT INTO Seyahat (rota, konaklama_bilgileri) VALUES (?, ?)", (rota, konaklama_bilgileri))
        self.conn.commit()

# Arayüz sınıfı, PyQt5 kullanarak bir grafik arayüz oluşturur
class Arayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyahat Planlama Uygulaması")  # Arayüz başlığı
        self.veritabani = Veritabani()  # Veritabanı bağlantısını oluştur
        self.seyahat = None  # Başlangıçta None olarak tanımlanıyor
        self.initUI()

    # Arayüzün ana bileşenlerini oluşturur
    def initUI(self):
        self.result_label = QLabel()  # Sonuç etiketi
        self.result_label.setStyleSheet("color: green; font-weight: bold;")

        # Arka plan resmi
        self.background_image = QLabel(self)
        pixmap = self.load_image_from_url("https://asistanakademi.com/images/seyahat-organizasyonu-egitimi.jpg")  # URL'yi değiştirin
        if pixmap:
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)  # Resmi küçültüyoruz
            self.background_image.setPixmap(pixmap)
            self.background_image.setAlignment(Qt.AlignCenter)  # Resmi merkeze hizalar

        # Grup kutuları oluşturuldu
        seyahat_groupbox = self.create_seyahat_groupbox()
        konaklama_ekle_groupbox = self.create_konaklama_ekle_groupbox()
        rota_ekle_groupbox = self.create_rota_ekle_groupbox()
        rapor_olustur_groupbox = self.create_rapor_olustur_groupbox()

        main_layout = QVBoxLayout()  # Ana dikey düzen
        main_layout.addWidget(self.background_image)  # Arka plan resmi eklendi
        main_layout.addWidget(seyahat_groupbox)  # Seyahat grubu eklendi
        main_layout.addWidget(konaklama_ekle_groupbox)  # Konaklama ekleme grubu eklendi
        main_layout.addWidget(rota_ekle_groupbox)  # Rota ekleme grubu eklendi
        main_layout.addWidget(rapor_olustur_groupbox)  # Rapor oluşturma grubu eklendi
        main_layout.addWidget(self.result_label)  # Sonuç etiketi eklendi

        self.setLayout(main_layout)  # Ana düzene yerleştirildi

    # Arka plan resmini web URL'sinden yükleyen metot
    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap
        except Exception as e:
            print("Arka plan resmi yüklenirken bir hata oluştu:", e)
            return None

    # Seyahat ekleme grubu oluşturur
    def create_seyahat_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturuldu
        layout = QHBoxLayout()  # Yatay düzen oluşturuldu
        groupbox.setLayout(layout)  # Grup kutusuna düzen eklendi

        # Etiketler ve combo kutuları oluşturuldu
        rota_label = QLabel("Rota:")
        self.rota_entry = QComboBox()
        self.rota_entry.addItems(["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"])
        konaklama_label = QLabel("Konaklama Bilgileri:")
        self.konaklama_combobox = QComboBox()
        self.konaklama_combobox.addItems(["Kiralık", "Eşyalı Ev veya Odalar", "Öğrenci Yurtları", "Aile Yanı"])

        # Buton oluşturuldu ve tıklama olayı bağlandı
        seyahat_ekle_button = QPushButton("Seyahat Ekle")
        seyahat_ekle_button.clicked.connect(self.seyahat_ekle)

        # Widget'a düzen eklendi
        layout.addWidget(rota_label)
        layout.addWidget(self.rota_entry)
        layout.addWidget(konaklama_label)
        layout.addWidget(self.konaklama_combobox)
        layout.addWidget(seyahat_ekle_button)

        return groupbox

    # Konaklama ekleme grubu oluşturur
    def create_konaklama_ekle_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturuldu
        layout = QHBoxLayout()  # Yatay düzen oluşturuldu
        groupbox.setLayout(layout)  # Grup kutusuna düzen eklendi

        # Etiketler ve giriş kutuları oluşturuldu
        tesis_adi_label = QLabel("Tesis Adı:")
        self.tesis_adi_entry = QLineEdit()
        fiyat_label = QLabel("Fiyat:")
        self.fiyat_entry = QLineEdit()

        # Buton oluşturuldu ve tıklama olayı bağlandı
        konaklama_ekle_button = QPushButton("Konaklama Ekle")
        konaklama_ekle_button.clicked.connect(self.konaklama_ekle)

        # Widget'a düzen eklendi
        layout.addWidget(tesis_adi_label)
        layout.addWidget(self.tesis_adi_entry)
        layout.addWidget(fiyat_label)
        layout.addWidget(self.fiyat_entry)
        layout.addWidget(konaklama_ekle_button)

        return groupbox

    # Rota ekleme grubu oluşturur
    def create_rota_ekle_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturuldu
        layout = QHBoxLayout()  # Yatay düzen oluşturuldu
        groupbox.setLayout(layout)  # Grup kutusuna düzen eklendi

        # Etiketler ve giriş kutuları oluşturuldu
        rota_detaylari_label = QLabel("Rota Detayları:")
        self.rota_detaylari_entry = QLineEdit()
        konaklama_secenekleri_label = QLabel("Konaklama Seçenekleri:")
        self.konaklama_secenekleri_combobox = QComboBox()
        self.konaklama_secenekleri_combobox.addItems(["Rezervasyon", "Rezervasyonsuz"])

        # Buton oluşturuldu ve tıklama olayı bağlandı
        rota_ekle_button = QPushButton("Rota Ekle")
        rota_ekle_button.clicked.connect(self.rota_ekle)

        # Widget'a düzen eklendi
        layout.addWidget(rota_detaylari_label)
        layout.addWidget(self.rota_detaylari_entry)
        layout.addWidget(konaklama_secenekleri_label)
        layout.addWidget(self.konaklama_secenekleri_combobox)
        layout.addWidget(rota_ekle_button)

        return groupbox

    # Rapor oluşturma grubu oluşturur
    def create_rapor_olustur_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturuldu
        layout = QHBoxLayout()  # Yatay düzen oluşturuldu
        groupbox.setLayout(layout)  # Grup kutusuna düzen eklendi

        # Buton oluşturuldu ve tıklama olayı bağlandı
        rapor_olustur_button = QPushButton("Rapor Oluştur")
        rapor_olustur_button.clicked.connect(self.rapor_olustur)

        # Widget'a düzen eklendi
        layout.addWidget(rapor_olustur_button)

        return groupbox

    # Seyahat eklemeyi işler
    def seyahat_ekle(self):
        rota = self.rota_entry.currentText()
        konaklama_bilgileri = self.konaklama_combobox.currentText()

        if rota.strip() == "" or konaklama_bilgileri.strip() == "":
            self.result_label.setText("Lütfen rota ve konaklama bilgilerini girin.")
            return

        self.veritabani.insert_seyahat(rota, konaklama_bilgileri)
        self.result_label.setText("Seyahat başarıyla eklendi.")

    # Konaklama eklemeyi işler
    def konaklama_ekle(self):
        tesis_adi = self.tesis_adi_entry.text()
        fiyat = self.fiyat_entry.text()

        if tesis_adi.strip() == "" or fiyat.strip() == "":
            self.result_label.setText("Lütfen tesis adı ve fiyat bilgilerini girin.")
            return

        self.veritabani.insert_konaklama(tesis_adi, fiyat)
        self.result_label.setText("Konaklama bilgileri başarıyla eklendi.")

    # Rota eklemeyi işler
    def rota_ekle(self):
        rota_detaylari = self.rota_detaylari_entry.text()
        konaklama_secenekleri = self.konaklama_secenekleri_combobox.currentText()

        if rota_detaylari.strip() == "" or konaklama_secenekleri.strip() == "":
            self.result_label.setText("Lütfen rota detayları ve konaklama seçeneklerini girin.")
            return

        self.veritabani.insert_rota(rota_detaylari, konaklama_secenekleri)
        self.result_label.setText(f"Rota başarıyla eklendi: {rota_detaylari}, {konaklama_secenekleri}")

    # Rapor oluşturmayı işler
    def rapor_olustur(self):
        self.result_label.clear()  # Önceki raporu temizle

        seyahatler = self.veritabani.get_seyahatler()
        if seyahatler:
            for seyahat in seyahatler:
                rota = seyahat[1]
                konaklama_bilgileri = seyahat[2]
                rapor = f"Rota: {rota}, Konaklama: {konaklama_bilgileri}"
                self.result_label.setText(rapor)
        else:
            self.result_label.setText("Kayıtlı seyahat bulunamadı.")

if __name__ == '__main__':
    app = QApplication([])  # Uygulama oluşturuldu
    ex = Arayuz()  # Arayüz örneği oluşturuldu
    ex.show()  # Arayüz gösterildi
    sys.exit(app.exec_())  # Uygulama başlatıldı
