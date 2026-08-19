# Kreativ kvest — tavsiya kartochkasi

Slaydga qo'yish uchun tayyor kartochka: https://krea-kvest.netlify.app/ havolasini tavsiya qiladi.

| Fayl | Nima |
| --- | --- |
| `card-uz.png` / `card-ru.png` | Slaydga qo'yiladigan tayyor rasm, 2× (1630×1655) |
| `card-uz.html` / `card-ru.html` | Kartochkaning HTML manbasi |
| `index.html` | Ikkala variantni ko'rsatuvchi sahifa |
| `build_card.py` | HTML generatori — matnlar shu yerda tahrirlanadi |
| `render.sh` | HTML → PNG (headless Chromium) |
| `qr-path.txt` | QR kod (segno, EC level M) SVG path ma'lumoti |

## Qayta yig'ish

```bash
./render.sh
```

Matnni o'zgartirish uchun `build_card.py` ichidagi `UZ` va `RU` lug'atlarini tahrirlang.
