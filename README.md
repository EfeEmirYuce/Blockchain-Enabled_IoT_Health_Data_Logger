# Blockchain Enabled IoT Health Data Logger

Bu proje, IoT cihazlarından gelen sağlık verilerini blockchain üzerinde güvenli şekilde kaydetmek ve okumak amacıyla geliştirilmiştir. Uygulama Docker Compose kullanılarak çalıştırılmaktadır. Aşağıda projeyi çalıştırmak, durdurmak, logları izlemek ve blockchain üzerinden veri okumak için kullanılan temel komutlar yer almaktadır.

Projeyi başlatmak için:
docker-compose up -d --build

Projeyi tamamen kapatmak için:
docker-compose down

Servisleri silmeden durdurmak için:
docker-compose stop

Durdurulmuş servisleri tekrar başlatmak için:
docker-compose start

Uygulama loglarını canlı olarak izlemek için:
docker-compose logs -f app

Blockchain üzerinde kayıtlı verileri okumak için:
docker-compose exec app python reader.py 0xKONTRAT_ADRESI

Not: 0xKONTRAT_ADRESI yerine ilgili akıllı kontrat adresi girilmelidir. Proje Docker sayesinde platformdan bağımsız şekilde çalıştırılabilir ve ekip çalışmasına uygundur.
