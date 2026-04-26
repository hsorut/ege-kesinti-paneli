const ilceler = {
    izmir: ["Aliağa", "Balçova", "Bayraklı", "Bornova", "Buca", "Çiğli", "Gaziemir", "Güzelbahçe", "Karabağlar", "Karşıyaka", "Konak", "Narlıdere", "Urla"], // Örnek olarak birkaçını yazdım
    manisa: ["Ahmetli", "Akhisar", "Alaşehir", "Demirci", "Gölmarmara", "Gördes", "Kırkağaç", "Köprübaşı", "Kula", "Salihli", "Sarıgöl", "Saruhanlı", "Selendi", "Soma", "Şehzadeler", "Turgutlu", "Yunusemre"]
};

function ilceleriGuncelle() {
    const sehirSecimi = document.getElementById("sehir-secimi");
    const ilceSecimi = document.getElementById("ilce-secimi");
    const secilenSehir = sehirSecimi.value;

    // İlçe kutusunu temizle
    ilceSecimi.innerHTML = '<option value="">İlçe Seçiniz...</option>';

    if (secilenSehir !== "") {
        // Seçilen şehre göre ilçeleri ekle
        ilceler[secilenSehir].forEach(ilce => {
            let option = document.createElement("option");
            option.value = ilce.toLowerCase();
            option.text = ilce;
            ilceSecimi.appendChild(option);
        });
        // İlçe kutusunu aktif et
        ilceSecimi.disabled = false;
    } else {
        // Şehir seçilmemişse ilçe kutusunu kapat
        ilceSecimi.disabled = true;
    }
}