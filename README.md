# KidsPlay — website

Trang GitHub Pages cho App Store / Google Play (khung theo cc-chart-site).

- Trang chủ: https://thientran2910.github.io/kidsplay-site/
- Hỗ trợ: .../support.html
- Quyền riêng tư: .../privacy.html (app mở `privacy.html?lang=en` cho người dùng tiếng Anh)
- Điều khoản: .../terms.html

## Sửa trang

Các file `.html` ở gốc repo là file **sinh ra**, đừng sửa tay. Sửa trong `src/` rồi chạy `python3 src/build.py`.

| File trong `src/` | Nội dung |
|---|---|
| `shared.css`, `shared.js` | Token màu (sáng/tối), header, footer, nút VI/EN và sáng/tối |
| `page.css` | Giao diện trang chủ, hỗ trợ, 404, trang pháp lý |
| `home.body.html`, `support.body.html`, `404.body.html` | Nội dung các trang |
| `content/{privacy,terms}.{vi,en}.html` | Nội dung pháp lý chép nguyên văn từ `kids_play/firebase/hosting`; build tự chia mục và dựng mục lục |
| `toc.js` | Mục lục bám cuộn |
| `build.py` | Ghép trang, icon, header/footer; sinh bản xem trước vào `build/` (không commit) |
| `icon128.png` | Icon app, nhúng base64 |

Ngôn ngữ: mặc định tiếng Việt; `?lang=vi|en` ưu tiên và được nhớ; nút VI/EN đổi được. Email hỗ trợ: `SUPPORT_EMAIL` trong `build.py`.
