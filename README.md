# SISMDI — Sistema Website Mata Dalan Institute (Django)

Implementasi Django dari website Mata Dalan Institute (MDI), disusun mengikuti struktur
project konvensi Anda (seperti project `sibtian`): app `Config`, `Custom`, `Main`,
`User`, `Website`.

## Struktur App

| App        | Peran                                                                 |
|------------|------------------------------------------------------------------------|
| `Website`  | **Frontend publik** — semua model konten (Slide, Vision/Mission, Activity, News, Article, OrgMember, Partner, Document, ContactMessage), views, urls, templates, dan static assets tema MDI. |
| `Main`     | **Backend/Dashboard** — login, logout, halaman dashboard (`Home/`), layout admin custom (`Layout/`: navbar + sidebar). Sidebar berisi link cepat ke Django Admin per model. |
| `User`     | Model `Profile` (ekstensi `auth.User` dengan role admin/editor/author/member, foto, jabatan), signal auto-create profile, dan `decorators.py` (`allowed_users`, `unauthenticated_user`, `admin_only`) untuk kontrol akses berbasis role. |
| `Config`   | Model `SiteConfig` (singleton) — pengaturan situs: nama, logo, kontak, koordinat lokasi, dll. Tersedia di semua template via context processor `{{ site_config }}`. |
| `Custom`   | Data master/lookup lintas app: `Category`, `Municipality`, `AdministrativePost`, `Year`. |

## Cara Menjalankan

`db.sqlite3` dan `media/` **tidak** termasuk di repository ini (lihat `.gitignore`) —
setiap clone/deploy jalankan migrate + seed_data untuk mengisi data demo dari awal.

```bash
# 1. Buat & aktifkan virtual environment (opsional tapi disarankan)
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Salin .env.example -> .env dan sesuaikan (lihat bagian "Konfigurasi Produksi" di bawah)
cp .env.example .env

# 4. Jalankan migrasi
python manage.py migrate

# 5. Isi data awal/demo (aman dijalankan berkali-kali - pakai update_or_create)
python manage.py seed_data

# 6. Jalankan server
python manage.py runserver
```

Buka **http://127.0.0.1:8000/** untuk website publik,
dan **http://127.0.0.1:8000/dashboard/login/** untuk login ke panel admin.

### Akun Default (dari `seed_data`)
- **Superuser/Admin dashboard:** `admin` / `admin12345`
- **Staff/Author (penulis artikel):** `aderito.ximenes`, `maria.guterres`, `joao.belo`,
  `fatima.soares`, `domingos.amaral` — semua password `mdi12345`

⚠️ **Ganti semua password ini sebelum deploy ke production.**

## Alur Login/Logout

- Login **satu pintu** via Django Auth (`django.contrib.auth`), dilayani oleh app `Main`
  (`/dashboard/login/`, `/dashboard/logout/`).
- Navbar di frontend publik (`Website`) otomatis menampilkan status login: tombol
  **Login** jika belum masuk, atau dropdown nama pengguna (dengan link ke Dashboard
  jika role-nya `admin`/`editor`/`author`) jika sudah masuk.
- Kontrol akses berbasis role tersedia di `User/decorators.py`:
  ```python
  from User.decorators import allowed_users

  @allowed_users(allowed_roles=['admin', 'editor'])
  def some_view(request):
      ...
  ```

## Mengelola Konten

Dua cara mengelola isi website:

1. **Django Admin** (`/admin/`) — cara paling cepat, semua model sudah terdaftar dengan
   `list_display`, filter, dan search yang rapi.
2. **Dashboard custom** (`/dashboard/`) — tampilan ringkasan/statistik, sidebar berisi
   pintasan langsung ke halaman admin per model (Hero Slider, Vision & Mission,
   Activities, News, Articles, Organigrama, Partners, Documents, dll).

> Dashboard `Main` saat ini adalah **shell/kerangka** (ringkasan + navigasi) — CRUD
> sesungguhnya memakai Django Admin bawaan agar cepat dipakai. Jika ke depan Anda ingin
> form CRUD custom bergaya AdminLTE penuh (seperti pada project `sibtian`), tinggal
> tambahkan views/templates baru di app `Main` yang memanggil model dari `Website.models`.

## Bahasa (Tetum/Indonesia/Portugis/Inggris)

Sistem bahasa memakai **Django i18n resmi** (`{% trans %}` / `{% blocktrans %}` +
`django.middleware.locale.LocaleMiddleware` + view `set_language`) — **bukan** lagi
localStorage/JavaScript. Pemilihan bahasa di topbar mengirim POST ke `/i18n/setlang/`,
lalu Django menyimpan preferensi di session/cookie `django_language` dan merender ulang
halaman di bahasa tsb (`<html lang="...">` ikut berubah).

Ada **dua lapis** konten yang diterjemahkan:

1. **Teks antarmuka statis** (menu, judul section, label tombol, breadcrumb) — via tag
   `{% trans "..." %}` / `{% blocktrans %}` di template. Katalog terjemahannya ada di
   `locale/<tet|id|pt|en>/LC_MESSAGES/django.po` (+ `.mo` terkompilasi).
   - Untuk **menambah/mengedit** terjemahan: edit `locale/<lang>/LC_MESSAGES/django.po`
     (field `msgstr`), lalu kompilasi ulang. Karena sandbox pengembangan ini tidak
     memiliki `gettext`/`msgfmt`, dipakai script `compile_locale.py` (butuh `pip install
     polib`) sebagai pengganti `django-admin compilemessages`:
     ```bash
     python3 compile_locale.py
     ```
     Kalau di server produksi Anda ada `gettext` terpasang, cara standar Django
     (`django-admin makemessages -l id` lalu `django-admin compilemessages`) juga tetap
     berfungsi normal terhadap file `.po` yang sama.
2. **Konten dari database** (Vision & Mission — termasuk `mission_points` 4 poin misi,
   Who We Are/Profile — termasuk struktur organisasi, pendekatan strategis, fokus
   geografis, teks Slide hero, heading/deskripsi/indikator Program) — via atribut
   `data-i18n-multi='{"tet":"..","id":"..",...}'` atau `data-i18n-list='{"tet":[...],...}'`
   untuk daftar, dirender ulang oleh `Website/static/Website/js/main.js` saat halaman
   dimuat (membaca `<html lang="...">` yang sudah diset Django). Template filter-nya ada
   di `Website/templatetags/i18n_extras.py` (`i18n_json`, `i18n_json_words`, `to_json`).
   Setiap model terkait punya field tambahan `..._i18n` (JSONField) yang bisa diisi lewat
   Django Admin di bagian **"Tradusaun (opsional)"** — formatnya:
   ```json
   {"id": "Teks Bahasa Indonesia", "pt": "Texto em Português", "en": "English text"}
   ```
   Kalau field ini dikosongkan, situs otomatis pakai teks Tetum (field utama) sebagai
   fallback — jadi situs tidak pernah "kosong", tapi kualitas 4-bahasa akan lebih baik
   kalau field ini diisi.

   **Konten yang BELUM ikut sistem ini** (masih satu bahasa/Tetum saja): isi lengkap
   berita (`NewsPost.body`), artikel (`Article.body`), dan deskripsi Activity — karena
   jumlahnya banyak & sering berubah, menerjemahkan tiap satu butuh effort admin. Kalau
   nanti dibutuhkan, pola field `..._i18n` yang sama tinggal ditambahkan ke model-model itu.

## Struktur Program (Pilar 1 / Pilar 2 / Pilar 3)

Menu **Program** mengikuti struktur Rencana Strategis MDI 2026–2030: model `Program`
sekarang punya field `parent` (self-FK) sehingga bisa membentuk hierarki:

- **Pilar 1** — Jestaun Institusionál Forte no Sustentabilidade Finanseira (berdiri sendiri)
- **Pilar 2** — Think Tank ASEAN (SIS), dengan 4 sub-outcome sebagai anak (`parent=Pilar 2`):
  - 2.1 Influénsia Estratéjika no Parseria
  - 2.2 Kapasidade Institusionál no Polítika Bazeia ba Evidénsia
  - 2.3 Koñesimentu, Aprendizajen no Excelénsia Institusionál
  - 2.4 Boa Governasaun no E-Governance
- **Pilar 3** — Partisipasaun Komunitária, Reziliénsia Ekonómika no Mudansa Klimátika (berdiri sendiri)

Setiap Program (Pilar maupun sub-outcome) punya field `indicators` (JSONField per bahasa)
untuk daftar "Indikadór Esperadu" yang tampil di halaman detail. Menu navbar & footer
dibangun otomatis dari data ini lewat context processor `Website.context_processors.nav_programs`
— tambah/ubah Pilar & sub-outcome cukup lewat Django Admin, tidak perlu ubah template.

## Peta Lokasi (Leaflet + Routing)

Peta di homepage sekarang pakai **Leaflet.js** (offline, vendor di
`Website/static/Website/vendor/leaflet/`), bukan lagi iframe OpenStreetMap. Fitur:

- Marker + popup nama & alamat kantor MDI.
- Tombol **"Get Route From My Location"** — minta izin GPS browser pengunjung
  (`navigator.geolocation`), lalu menggambar rute mengemudi dari lokasi pengunjung ke
  kantor MDI memakai **Leaflet Routing Machine** (server rute publik OSRM, butuh
  internet saat dibuka — normal untuk semua peta interaktif).
- Tombol alternatif **"Open in Google Maps"** untuk yang tidak mau kasih izin lokasi.
- Peta tile (gambar dasar) diambil dari `tile.openstreetmap.org` — butuh koneksi
  internet pengunjung saat halaman dibuka (standar untuk semua web map interaktif,
  termasuk Google Maps).

## Berita: Galeri Foto & Detail Data

- **Galeri foto**: satu `NewsPost` bisa punya banyak foto lewat model `NewsImage`
  (inline form di Django Admin → News → edit berita → bagian "News images", isi
  sebanyak yang perlu, atur `order` & `caption`).
- **Detail data** (mirip halaman Program): tiap berita bisa dilengkapi `municipality`
  (munisípiu terkait), `related_program` (link ke Program terkait, mis. PNDS),
  `location_detail` (lokasi spesifik bebas teks), dan `source_reference`. Kalau diisi,
  otomatis muncul sebagai kotak "Detail Data" di sidebar halaman detail berita.

## Artikel

Kartu & halaman detail artikel sudah dilengkapi: foto sampul (`cover_image`), badge
kategori, foto+jabatan penulis, tanggal terbit, dan **estimasi waktu baca** otomatis
(dihitung dari jumlah kata, filter `reading_time` di `i18n_extras.py`).

## Struktur Folder

```
sismdi_project/
├── manage.py
├── requirements.txt
├── compile_locale.py            ← kompilasi locale/*.po -> *.mo tanpa perlu gettext CLI
├── .env.example                 ← template variabel environment produksi (copy jadi .env)
├── .gitignore                   ← db.sqlite3, media/, .env, dst TIDAK ikut git
├── locale/                      ← katalog terjemahan Django i18n (tet/id/pt/en)
├── sismdi/                      ← settings, root urls, wsgi/asgi
├── Config/                      ← SiteConfig
├── Custom/                      ← Category, Municipality, AdministrativePost, Year
├── User/                        ← Profile, decorators, signals
├── Website/                     ← APP UTAMA FRONTEND
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   ├── context_processors.py    ← nav_programs (menu Pilar/sub-outcome)
│   ├── templatetags/i18n_extras.py
│   ├── management/commands/seed_data.py
│   ├── templates/Website/       ← base.html + semua halaman
│   └── static/Website/          ← Bootstrap, ikon, font, gambar, CSS/JS tema
└── Main/                        ← APP UTAMA BACKEND/DASHBOARD
    ├── views.py (login, logout, home)
    ├── urls.py
    ├── templates/Home/          ← home.html, login.html, logout.html
    ├── templates/Layout/        ← Layout.html, navbar.html, sidebar.html
    └── static/Main/css/dashboard.css
```

## Konfigurasi Produksi

Semua pengaturan sensitif dibaca dari environment variable (lihat `.env.example`):
`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_SECURE_SSL_REDIRECT`, `DATABASE_URL` (opsional,
untuk PostgreSQL/MySQL), dan pengaturan `EMAIL_*`. Saat `DJANGO_DEBUG=False`, Django
otomatis mengaktifkan `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, dan HSTS.

Langkah deploy singkat:

```bash
cp .env.example .env        # lalu isi nilai produksi yang sebenarnya
python3 -c "import secrets; print(secrets.token_urlsafe(50))"   # generate DJANGO_SECRET_KEY
python manage.py migrate
python manage.py seed_data          # opsional: hapus/lewati jika sudah punya data produksi
python manage.py createsuperuser    # buat akun admin sendiri, JANGAN pakai admin/admin12345
python manage.py collectstatic --noinput
python manage.py check --deploy     # pastikan tidak ada warning keamanan
```

Jalankan lewat WSGI/ASGI server produksi (mis. `gunicorn sismdi.wsgi:application`),
bukan `manage.py runserver`.

## Yang Perlu Dilengkapi Selanjutnya

1. **Konten asli**: seed_data mengisi konten contoh (termasuk struktur organigrama
   placeholder `[Naran Diretor Ezekutivu]` dst) — edit/tambah lewat Django Admin dengan
   data & foto asli MDI (khususnya Organigrama → nama & posisi staf sesungguhnya).
2. **File dokumen PDF**: model `Document` sudah siap, tinggal upload file lewat admin
   di kategori yang sesuai (Doc PNDS, Doc OJE, dst — kategori sudah dibuat oleh seed_data).
3. **Ganti password default** akun `admin` dan semua akun staff sebelum production —
   atau lebih baik, jangan jalankan `seed_data` di produksi dan buat akun sendiri lewat
   `createsuperuser`.
4. **SECRET_KEY & DEBUG**: WAJIB diisi lewat `.env` sebelum online (lihat bagian
   "Konfigurasi Produksi" di atas) — jangan pernah pakai `DEBUG=True` di produksi.
5. **Email**: form kontak saat ini hanya menyimpan ke database (`ContactMessage`,
   terlihat di Django Admin & Dashboard). Untuk kirim notifikasi email sungguhan, isi
   `EMAIL_*` di `.env` dengan kredensial SMTP.
