import pyaudio
import wave
import threading
import queue

# Parametreler:
FORMAT = pyaudio.paInt16  # Ses formatı.
CHANNELS = 1  # Tek kanal ses kaydı
RATE = 44100  # Örnekleme hızı
CHUNK = 1024  # Ses örneklerinin gruplanması
OUTPUT_FILENAME = "output.wav"  # Kaydedilecek dosyanın adı

# PyAudio nesnesinin oluşması
p = pyaudio.PyAudio()

# Stream nesnesi mikrofondan gelen ses verilerini alır.
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Kayıt başladı. Kaydı durdurmak için 'enter' tuşuna basınız... ")

# Boş bir liste oluşturuyoruz ve bu liste kaydedilen seslerileri tutacak.
frames = []

# Aşağıdaki değişken durdurulup durdurulmadığını belirlemek için.
stop_recording = False

# Bir fonksiyon tanımlıyoruz ve bu fonksiyon sürekli olarak ses örneklerini kaydedecek.
def record_audio():
    global stop_recording
    while not stop_recording:
        data = stream.read
        (CHUNK)
        frames.append(data)


# "threading.Thread" sınıfını kullanarak bir thread oluşturuyoruz ve "record_audio" fonksiyonunu hedef olarak belirliyoruz.
record_thread = threading.Thread(target=record_audio)

# Thread'i başlatıyoruz ve buda "record_audio" fonksiyonunun çalışmasını başlatır.
record_thread.start()

# Burada ana thread kullanıcadan bir girdi bekliyor.
# Kullanıcının "enter" tuşuna basmasını beklemek için kullanılır.
input("Kaydı durdurmak için 'enter' tuşuna basın...\n")

# Kullanıcı "enter" tuşuna bastığında, "stop_recording" değişkenini "True" olarak ayarlayarak kaydın durmasını sağlanır.
stop_recording = True
# Kayıt işlemi tamamlanana kadar bekleniyor. Burası tüm ses örneklerinin kayıt edilmesini sağlar
record_thread.join()

print("Kayıt tamamlandı")

# Kayıt işlemini sonlandırma
stream.stop_stream()
stream.close()
p.terminate()

# Ses örneklerini bir WAV dosyasına yazma
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print("Dosya kaydedildi", OUTPUT_FILENAME)
