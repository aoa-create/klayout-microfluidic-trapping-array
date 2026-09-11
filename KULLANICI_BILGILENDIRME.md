# Kullanıcı Bilgilendirme — klayout-microfluidic-trapping-array

> **Bu dosya bu projenin ana kullanıcı bilgi sayfasıdır.** Repository kökünde tutulur ve her görevde güncellenir. Yazılım geliştirmeyi öğrenme aşamasındaki bir kullanıcı düşünülerek sade Türkçe kullanılır.

## 1. Bu proje nedir?

Bu proje, deterministik mikroakışkan trapping-array tasarımlarını KLayout üzerinde PCell/makro yaklaşımıyla geliştirmek için kullanılır. Koordinat, birim, parametre, seed ve fabrikasyon onayı sınırlarının izlenebilir kalması hedeflenir.

## 2. Projedeki her dosya ve klasör ne işe yarıyor?

Aşağıdaki tree, Git tarafından takip edilen proje yapısını gösterir. Her yolun yanında ne işe yaradığı açıklanmıştır.

```text
klayout-microfluidic-trapping-array/
├── .cline/ ← Cline/agent çalışma kurallarını içerir. [Yol: .cline]
│   └── rules/ ← “rules” alanıyla ilgili dosyaları gruplar. [Yol: .cline/rules]
│       └── documentation.md ← “documentation” konusunu açıklayan Markdown belgesidir. [Yol: .cline/rules/documentation.md]
├── .github/ ← GitHub otomasyon ve CI/CD dosyalarını içerir. [Yol: .github]
│   └── workflows/ ← “workflows” alanıyla ilgili dosyaları gruplar. [Yol: .github/workflows]
│       ├── ci.yml ← GitHub Actions otomatik test/doğrulama iş akışıdır. [Yol: .github/workflows/ci.yml]
│       └── user-documentation-gate.yml ← GitHub Actions otomatik test/doğrulama iş akışıdır. [Yol: .github/workflows/user-documentation-gate.yml]
├── .gitignore ← Git'e eklenmemesi gereken yerel/geçici dosyaları tanımlar. [Yol: .gitignore]
├── AGENTS.md ← Kod ajanlarının uyması gereken proje kurallarını tanımlar. [Yol: AGENTS.md]
├── KULLANICI_BILGILENDIRME.md ← “KULLANICI BILGILENDIRME” konusunu açıklayan Markdown belgesidir. [Yol: KULLANICI_BILGILENDIRME.md]
├── README.md ← Projenin ana tanıtım, kurulum ve kullanım belgesidir. [Yol: README.md]
├── SECURITY.md ← “SECURITY” konusunu açıklayan Markdown belgesidir. [Yol: SECURITY.md]
├── docs/ ← Proje dokümantasyonunu içerir. [Yol: docs]
│   └── kullanici-bilgilendirme/ ← “kullanici-bilgilendirme” alanıyla ilgili dosyaları gruplar. [Yol: docs/kullanici-bilgilendirme]
│       └── PATH_MANIFEST.txt ← “PATH_MANIFEST.txt” adlı proje dosyasıdır; bulunduğu klasörün işlevinin bir parçasıdır. [Yol: docs/kullanici-bilgilendirme/PATH_MANIFEST.txt]
├── pyproject.toml ← Uygulama veya geliştirme araçları için yapılandırma dosyasıdır. [Yol: pyproject.toml]
├── tests/ ← Otomatik testleri içerir. [Yol: tests]
│   └── test_macro_structure.py ← “macro structure” davranışını doğrulayan Python test dosyasıdır. [Yol: tests/test_macro_structure.py]
└── trapping_array_pcell.lym ← “trapping_array_pcell.lym” adlı proje dosyasıdır; bulunduğu klasörün işlevinin bir parçasıdır. [Yol: trapping_array_pcell.lym]
```

> Git boş klasörleri takip etmediği için yalnızca repository içinde gerçekten izlenen yollar gösterilir.

## 3. Sistem nasıl çalışıyor?

```mermaid
flowchart LR
    A[Görev] --> B[Kod / belge değişikliği]
    B --> C[Test]
    C --> D[KULLANICI_BILGILENDIRME güncelle]
    D --> E[Documentation Gate]
    E --> F[Checkpoint / Proje Gate]
    F --> G[Commit / Push / Merge]
```

## 4. Son Yapılan İşler

| Tarih | İş | Sonuç |
|---|---|---|
| 2026-09-12 | Kullanıcı bilgilendirme ve documentation gate sistemi projeye eklendi. | Tamamlandı |

> Bundan sonra **her görev** bu tabloya veya bu bölümün altına anlaşılır bir özet olarak işlenir.

## 5. Zorunlu kural

Yeni bir dosya/klasör eklenir, taşınır veya silinirse tree aynı görev içinde güncellenir. Dosya yapısı değişmese bile yapılan iş “Son Yapılan İşler” bölümüne eklenir. `PATH_MANIFEST.txt` ve bu sayfa güncel değilse CI başarısız olur ve görev tamamlanmış sayılmaz.

## 6. Terimler

- **Repository:** GitHub'daki proje klasörünün tamamı.
- **Tree:** Projenin klasör/dosya ağacı.
- **Agent:** Belirli geliştirme görevlerini yapan yapay zekâ çalışanı.
- **Checkpoint:** Görevin tamamlandığını kanıtlayan doğrulama noktası.
- **Gate:** Sonraki aşamaya geçmeden önce zorunlu kontrol.
- **CI:** GitHub'ın otomatik test/doğrulama sistemi.
