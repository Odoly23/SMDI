# SISMDI — Sistema Website Mata Dalan Institute (Django)

Implementasi Django dari website Mata Dalan Institute (MDI), disusun mengikuti struktur
project konvensi Anda: app `config`, `custom`, `main`, `users`, `website` (huruf kecil
semua), `views.py`/`forms.py`/`decorators.py` mengikuti gaya kode Anda sendiri.

## Struktur App

| App        | Peran                                                                 |
|------------|------------------------------------------------------------------------|
| `website`  | **Frontend publik** — semua model konten (Slide, Vision/Mission, Activity, News, Article, OrgMember, Partner, Document, ContactMessage), views, urls, templates, dan static assets tema MDI. |
| `main`     | **Backend/Dashboard** — login, logout, halaman dashboard (`home/`), layout admin custom (`layout/`: topbar + navbar + sidebar mobile), dan CRUD custom bergaya crispy-forms untuk **semua** model konten (`views_website.py`, `views_org.py`, `views_inbox.py`, `views_singleton.py`, `views_lookup.py`, `views_users.py`). Django Admin (`/admin/`) hanya dipakai untuk `Group`/permisaun. |
| `users`    | Model `Profile` (ekstensi `auth.User` — foto, jabatan/posisi, bio, telepon) dan signal auto-create profile. Kontrol akses **bukan** lewat field role lagi, tapi lewat `django.contrib.auth.models.Group` (lihat bagian "Grupu Utilizador" di bawah). |
| `config`   | Model `SiteConfig` (singleton) — pengaturan situs: nama, logo, kontak, koordinat lokasi, dll. Tersedia di semua template via context processor `{{ site_config }}`. `config/decorators.py` berisi `allowed_users`/`unauthenticated_user` untuk kontrol akses berbasis grupu. |
| `custom`   | Data master/lookup lintas app: `Category`, `Municipality`, `AdministrativePost`, `Year`. |

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
- **Superuser/Admin dashboard:** `admin` / `admin12345` (grupu `admin`)
- **Staff (penulis artikel):** `aderito.ximenes`, `maria.guterres`, `joao.belo`,
  `fatima.soares`, `domingos.amaral` — semua password `mdi12345` (grupu `staff`)

⚠️ **Ganti semua password ini sebelum deploy ke production.**

## Grupu Utilizador (Kontrolu Asesu)

Kontrolu asesu ba dashboard uza **Django Groups** (`django.contrib.auth.models.Group`),
laos field `role` iha model — hanesan konvensaun iha projetu Anda nian. Iha grupu tolu
deit:

| Grupu   | Asesu                                                                 |
|---------|-------------------------------------------------------------------------|
| `admin` | Asesu total — dashboard + menu "Sistema" (Konfigurasaun, Kategoria, Utilizador, Grupu). |
| `staff` | Asesu dashboard (kria/edita konteúdu website) — la haree menu "Sistema". |
| `member`| Grupu baze/públiku — **la iha** asesu ba dashboard (haree deit website públiku). |

`config/decorators.py` (copiadu tuir kódigu Anda, tanpa ubah):

```python
from config.decorators import allowed_users, unauthenticated_user

@allowed_users(allowed_roles=['admin', 'staff'])
def some_view(request):
    ...
```

`allowed_users` lee `request.user.groups.all()[0].name` (utilizador hanesan ida ho
grupu ida deit) no redireciona ba `home/404.html` se grupu la permitidu. Grupu sira-ne'e
automatikamente kriadu no atribuidu iha `seed_data` (haree `users/models.py` — konstante
`GROUP_ADMIN`, `GROUP_STAFF`, `GROUP_MEMBER`).

## Alur Login/Logout

- Login **satu pintu** via Django Auth (`django.contrib.auth`), dilayani oleh app `main`
  (`/dashboard/login/`, `/dashboard/logout/`).
- View `main/views.py` mengikuti pola: `@login_required` + `@allowed_users(allowed_roles=[...])`
  ditumpuk, dengan context `group`/`page`/`title`/`legend` di setiap view dashboard.

## Panel Admin (Dashboard)

Tampilan dashboard (`main/templates/layout/`) memakai tema navy institusional:

- **Topbar** — bar tipis di atas berisi kontak (email/telepon/alamat).
- **Navbar utama** — logo + menu dropdown (Konteúdu, Publikasaun, Sistema) untuk desktop.
- **Sidebar mobile** — menu ikon+label off-canvas (slide dari kiri, push content),
  otomatis aktif di lebar layar < 992px, disembunyikan di desktop (menu dropdown navbar
  dipakai sebagai gantinya).
- Menu "Sistema" (Konfigurasi Situs, Kategori, Munisípiu, Postu Administrativu, Tinan,
  Konta Staff, Grupu) hanya tampil untuk grupu `admin`.

CSS-nya ada di `main/static/main/css/dashboard.css`.

## Mengelola Konten

Semua input data (kecuali `Group`/permisaun) dikelola lewat **halaman dashboard custom**
(`/dashboard/...`), bukan Django Admin — mengikuti pola referensi Anda: breadcrumb +
card `.border-success.shadow-lg` yang membungkus `{% crispy form %}` di dalam `<form>`
manual (`enctype="multipart/form-data"`), supaya tampilannya konsisten dan staff
non-teknis tidak perlu masuk ke `/admin/`.

Scaffolding yang dipakai ulang di semua ~17 model:

- `main/templates/layout/form_base.html` — halaman create/edit generik.
- `main/templates/layout/list_base.html` — halaman list generik (toolbar, tabel,
  pagination), tiap model cukup override block `table_head`/`table_body`.
- `main/templates/layout/_delete_btn.html` — tombol hapus (POST + konfirmasi JS),
  dipakai inline di tiap baris tabel.
- `main/crispy.py` — `dashboard_helper()` (set `FormHelper.form_tag = False` supaya
  `{% crispy form %}` tidak membuat `<form>` sendiri, karena template sudah punya
  `<form>` manual) dan `unique_slug()` (generate slug otomatis di view, field `slug`
  tidak pernah ditampilkan ke staff).

Pembagian view per app:

| File                        | Model                                                    |
|------------------------------|-----------------------------------------------------------|
| `main/views_website.py`      | NewsPost (+ galeri foto), Article, Activity, Document     |
| `main/views_org.py`          | Program (Pilar/Sub-Outcome), OrgMember, Founder            |
| `main/views_inbox.py`        | Partner, ContactMessage (inbox read-only)                  |
| `main/views_singleton.py`    | Slide (list biasa), VisionMission, WhoWeAre, SiteConfig (singleton — edit saja, tanpa list/hapus) |
| `main/views_lookup.py`       | Category, Municipality, AdministrativePost, Year           |
| `main/views_users.py`        | Konta staff (`User`+`Profile`+`Group`) — **admin-only**     |

`Group`/permisaun (3 grup tetap: admin/staff/member) tetap dikelola lewat Django Admin
(`/admin/auth/group/`) karena strukturnya jarang berubah.

## Forms (django-crispy-forms)

Form (mis. `website/forms.py` — `ContactMessageForm`) memakai `django-crispy-forms` +
`crispy-bootstrap5`, dengan `FormHelper`/`Layout` di `__init__`, sesuai gaya kode Anda.
Template merender dengan `{% load crispy_forms_tags %}` + `{% crispy form %}`.

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
   untuk daftar, dirender ulang oleh `website/static/website/js/main.js` saat halaman
   dimuat (membaca `<html lang="...">` yang sudah diset Django). Template filter-nya ada
   di `website/templatetags/i18n_extras.py` (`i18n_json`, `i18n_json_words`, `to_json`).
   Setiap model terkait punya field tambahan `..._i18n` (JSONField) — field teks utama
   (Tetum) diisi lewat halaman dashboard custom, sedangkan field `..._i18n` sendiri
   (opsional, untuk 3 bahasa lain) belum ada di form dashboard dan untuk saat ini masih
   diisi lewat Django Admin di bagian **"Tradusaun (opsional)"** — formatnya:
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
dibangun otomatis dari data ini lewat context processor `website.context_processors.nav_programs`
— tambah/ubah Pilar & sub-outcome cukup lewat halaman dashboard **Programa**
(`/dashboard/program/`), tidak perlu ubah template. Field `indicators` (JSONField per
bahasa) belum ada di form dashboard dan untuk saat ini masih diisi lewat Django Admin.

## Peta Lokasi (Leaflet + Routing)

Peta di homepage pakai **Leaflet.js** (offline, vendor di
`website/static/website/vendor/leaflet/`), bukan iframe OpenStreetMap. Fitur:

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

- **Galeri foto**: satu `NewsPost` bisa punya banyak foto lewat model `NewsImage` — dari
  halaman edit Notísia (`/dashboard/news/<id>/edit/`) klik tombol **"Photo gallery"**
  untuk upload & hapus foto (`/dashboard/news/<id>/gallery/`), atur `order` & `caption`.
- **Detail data** (mirip halaman Program): tiap berita bisa dilengkapi `municipality`
  (munisípiu terkait), `related_program` (link ke Program terkait, mis. PNDS),
  `location_detail` (lokasi spesifik bebas teks), dan `source_reference`. Kalau diisi,
  otomatis muncul sebagai kotak "Detail Data" di sidebar halaman detail berita.

## Artikel

Kartu & halaman detail artikel sudah dilengkapi: foto sampul (`cover_image`), badge
kategori, foto+jabatan penulis, tanggal terbit, dan **estimasi waktu baca** otomatis
(dihitung dari jumlah kata, filter `reading_time` di `i18n_extras.py`).

## Estatístika Vizitante (FlagCounter)

Website bele hatudu widget **FlagCounter** (kontador vizitante tuir nasaun) iha rua
fatin: iha topbar (besik bandeira lingua) versaun mini, no iha parte leten-wán footer
versaun kompletu ho lista bandeira.

Atu ativa:

1. Baa iha https://flagcounter.com/ → klik **"Get your free counter!"**.
2. Hili estilu/bandeira ne'ebe ita hakarak (cores, kolunas, dll) — la presiza kria konta.
3. Depois submete, site sei fó kódigu HTML ho URL hanesan
   `https://s01.flagcounter.com/count2/`**`abcd1`**`/...` — kopia deit parte **`abcd1`**
   (ID kontador ne'e).
4. Baa iha dashboard → **Konfigurasaun Situs** (`/dashboard/site-config/`) → kola ID
   ne'e iha kampu **FlagCounter ID** → Save.

Widget sei aparese automatikamente iha website públiku (topbar + footer). Se kampu
ne'e mamuk, widget la hatudu iha-ne'e (labele iha imajen kebrada).

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
├── config/                      ← SiteConfig, forms.py (SiteConfigForm), decorators.py (allowed_users, unauthenticated_user)
├── custom/                      ← Category, Municipality, AdministrativePost, Year, forms.py
├── users/                       ← Profile, signals, forms.py (StaffUserCreateForm/UpdateForm) — kontrolu asesu → django.contrib.auth.models.Group
├── website/                     ← APP UTAMA FRONTEND
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py                 ← django-crispy-forms: ContactMessageForm (publik) + ModelForm dashboard per model
│   ├── context_processors.py    ← nav_programs (menu Pilar/sub-outcome)
│   ├── templatetags/i18n_extras.py
│   ├── management/commands/seed_data.py
│   ├── templates/website/       ← base.html + semua halaman
│   └── static/website/          ← Bootstrap, ikon, font, gambar, CSS/JS tema
└── main/                        ← APP UTAMA BACKEND/DASHBOARD
    ├── views.py                 ← login, logout, home
    ├── views_website.py         ← CRUD News/Article/Activity/Document
    ├── views_org.py             ← CRUD Program/OrgMember/Founder
    ├── views_inbox.py           ← CRUD Partner + inbox ContactMessage
    ├── views_singleton.py       ← CRUD Slide + edit VisionMission/WhoWeAre/SiteConfig
    ├── views_lookup.py          ← CRUD Category/Municipality/AdministrativePost/Year
    ├── views_users.py           ← CRUD Konta Staff (admin-only)
    ├── crispy.py                ← dashboard_helper(), unique_slug()
    ├── urls.py
    ├── context_processors.py    ← dashboard_badges (kontador mensajen seidauk lidu)
    ├── templates/home/          ← home.html, login.html, logout.html, 404.html
    ├── templates/layout/        ← layout.html, topbar.html, navbar.html, sidebar.html,
    │                              form_base.html, list_base.html, _delete_btn.html (scaffolding CRUD)
    ├── templates/dashboard/     ← list/form/detail per model (news, article, activity,
    │                              document, program, orgmember, founder, partner,
    │                              message, slide, category, municipality, adminpost,
    │                              year, staff)
    └── static/main/css/dashboard.css
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
bukan `manage.py runserver`. Jika `createsuperuser` dipakai, tambahkan user itu ke grupu
`admin` secara manual (Django Admin → Utilizador → grupu, atau lewat dashboard
**Konta Staff** `/dashboard/staff/` kalau sudah ada akun `admin` lain yang bisa login).

## Yang Perlu Dilengkapi Selanjutnya

1. **Konten asli**: seed_data mengisi konten contoh (termasuk struktur organigrama
   placeholder `[Naran Diretor Ezekutivu]` dst) — edit/tambah lewat dashboard
   **Organigrama** (`/dashboard/orgmember/`) dengan data & foto asli MDI (khususnya
   nama & posisi staf sesungguhnya).
2. **File dokumen PDF**: model `Document` sudah siap, tinggal upload file lewat
   dashboard **Dokumentu** (`/dashboard/document/`) di kategori yang sesuai (Doc PNDS,
   Doc OJE, dst — kategori sudah dibuat oleh seed_data, atau tambah baru lewat
   **Kategoria** `/dashboard/category/`).
3. **Ganti password default** akun `admin` dan semua akun staff sebelum production —
   atau lebih baik, jangan jalankan `seed_data` di produksi dan buat akun sendiri lewat
   `createsuperuser` + assign grupu manual. Password staff selanjutnya bisa diganti
   lewat dashboard **Konta Staff** (`/dashboard/staff/<id>/edit/`).
4. **SECRET_KEY & DEBUG**: WAJIB diisi lewat `.env` sebelum online (lihat bagian
   "Konfigurasi Produksi" di atas) — jangan pernah pakai `DEBUG=True` di produksi.
5. **Email**: form kontak saat ini hanya menyimpan ke database (`ContactMessage`,
   dibaca lewat kotak masuk dashboard `/dashboard/message/`). Untuk kirim notifikasi
   email sungguhan, isi `EMAIL_*` di `.env` dengan kredensial SMTP.
