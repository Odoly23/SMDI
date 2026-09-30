#!/usr/bin/env python3
"""Build & compile locale/*/LC_MESSAGES/django.po -> django.mo without needing
gettext CLI tools (xgettext/msgfmt), using polib only.

Usage: python3 compile_locale.py
"""
import polib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / "locale"

# msgid (English, as written in templates) -> {"tet": .., "id": .., "pt": .., "en": ..}
STRINGS = {
    "Home": {"tet": "Uma Pájina", "id": "Beranda", "pt": "Início", "en": "Home"},
    "Who We Are": {"tet": "Ita Sé", "id": "Tentang Kami", "pt": "Quem Somos", "en": "Who We Are"},
    "Program": {"tet": "Programa", "id": "Program", "pt": "Programa", "en": "Program"},
    "Documents": {"tet": "Dokumentus", "id": "Dokumen", "pt": "Documentos", "en": "Documents"},
    "Doc PNDS": {"tet": "Doc PNDS", "id": "Dok PNDS", "pt": "Doc PNDS", "en": "PNDS Doc"},
    "Doc OGE": {"tet": "Doc OJE", "id": "Dok OGE", "pt": "Doc OGE", "en": "OGE Doc"},
    "Petroleum Fund Doc": {"tet": "Doc Fundu Petroleum", "id": "Dok Dana Minyak", "pt": "Doc Fundo Petrolífero", "en": "Petroleum Fund Doc"},
    "Statistics": {"tet": "Estatístika", "id": "Statistik", "pt": "Estatísticas", "en": "Statistics"},
    "Other Documents": {"tet": "Dokumentu Seluk", "id": "Dokumen Lainnya", "pt": "Outros Documentos", "en": "Other Documents"},
    "Vision and Mission": {"tet": "Vizaun no Misaun", "id": "Visi dan Misi", "pt": "Visão e Missão", "en": "Vision and Mission"},
    "What We Do": {"tet": "Saida ne'ebé Ami Halo", "id": "Apa yang Kami Lakukan", "pt": "O Que Fazemos", "en": "What We Do"},
    "Partners": {"tet": "Parseiru", "id": "Mitra", "pt": "Parceiros", "en": "Partners"},
    "Donors": {"tet": "Doadór", "id": "Donor", "pt": "Doadores", "en": "Donors"},
    "Contact": {"tet": "Kontaktu", "id": "Kontak", "pt": "Contacto", "en": "Contact"},
    "Dashboard": {"tet": "Painel", "id": "Dasbor", "pt": "Painel", "en": "Dashboard"},
    "Logout": {"tet": "Sai", "id": "Keluar", "pt": "Sair", "en": "Logout"},
    "Login": {"tet": "Tama", "id": "Masuk", "pt": "Entrar", "en": "Login"},
    "Quick Links": {"tet": "Ligasaun Lalais", "id": "Tautan Cepat", "pt": "Ligações Rápidas", "en": "Quick Links"},
    "Partners and Networks": {"tet": "Parseiru no Rede", "id": "Mitra dan Jaringan", "pt": "Parceiros e Redes", "en": "Partners and Networks"},
    "Current Donors": {"tet": "Doadór Atuál", "id": "Donor Saat Ini", "pt": "Doadores Atuais", "en": "Current Donors"},
    "All rights reserved.": {"tet": "Hotu-hotu rezervadu.", "id": "Hak cipta dilindungi.", "pt": "Todos os direitos reservados.", "en": "All rights reserved."},
    "Vision": {"tet": "Vizaun", "id": "Visi", "pt": "Visão", "en": "Vision"},
    "Mission": {"tet": "Misaun", "id": "Misi", "pt": "Missão", "en": "Mission"},
    "Profile": {"tet": "Profile", "id": "Profil", "pt": "Perfil", "en": "Profile"},
    "Read more": {"tet": "Lee tan", "id": "Baca selengkapnya", "pt": "Ler mais", "en": "Read more"},
    "What We Do (heading small)": {"tet": "Saida ne'ebé Ami Halo", "id": "Apa yang Kami Lakukan", "pt": "O Que Fazemos", "en": "What We Do"},
    "MDI's Core Activities": {"tet": "Atividade Xave MDI", "id": "Kegiatan Inti MDI", "pt": "Atividades Principais do MDI", "en": "MDI's Core Activities"},
    "Regular activities.": {"tet": "Atividade regulár.", "id": "Kegiatan rutin.", "pt": "Atividades regulares.", "en": "Regular activities."},
    "View All Activities": {"tet": "Haree Atividade Hotu", "id": "Lihat Semua Kegiatan", "pt": "Ver Todas as Atividades", "en": "View All Activities"},
    "Updates": {"tet": "Atualizasaun", "id": "Pembaruan", "pt": "Atualizações", "en": "Updates"},
    "Latest News": {"tet": "Notísia Foun", "id": "Berita Terbaru", "pt": "Últimas Notícias", "en": "Latest News"},
    "Follow our news.": {"tet": "Akompaña ami nia notísia.", "id": "Ikuti berita kami.", "pt": "Acompanhe as nossas notícias.", "en": "Follow our news."},
    "Read more »": {"tet": "Lee tan »", "id": "Baca selengkapnya »", "pt": "Ler mais »", "en": "Read more »"},
    "Blog & Analysis": {"tet": "Blog & Análize", "id": "Blog & Analisis", "pt": "Blog e Análise", "en": "Blog & Analysis"},
    "Articles from the MDI Team": {"tet": "Artigu husi Ekipa MDI", "id": "Artikel dari Tim MDI", "pt": "Artigos da Equipa do MDI", "en": "Articles from the MDI Team"},
    "Reflections from our team.": {"tet": "Refleksaun husi ami nia ekipa.", "id": "Refleksi dari tim kami.", "pt": "Reflexões da nossa equipa.", "en": "Reflections from our team."},
    "Structure": {"tet": "Estrutura", "id": "Struktur", "pt": "Estrutura", "en": "Structure"},
    "Mata Dalan Institute (MDI) Organizational Chart": {"tet": "Organigrama Mata Dalan Institute (MDI)", "id": "Struktur Organisasi Mata Dalan Institute (MDI)", "pt": "Organograma do Mata Dalan Institute (MDI)", "en": "Mata Dalan Institute (MDI) Organizational Chart"},
    "MDI's internal management and coordination structure.": {"tet": "Estrutura jestaun no koordenasaun internu MDI nian.", "id": "Struktur manajemen dan koordinasi internal MDI.", "pt": "Estrutura de gestão e coordenação interna do MDI.", "en": "MDI's internal management and coordination structure."},
    "No org chart data yet. Add it via Django Admin → Website → Org Chart Member.": {
        "tet": "Seidauk iha dadus organigrama. Aumenta liu husi Django Admin → Website → Membru Organigrama.",
        "id": "Belum ada data struktur organisasi. Tambahkan melalui Django Admin → Website → Org Chart Member.",
        "pt": "Ainda não há dados do organograma. Adicione através do Django Admin → Website → Org Chart Member.",
        "en": "No org chart data yet. Add it via Django Admin → Website → Org Chart Member."},
    "Visit Us": {"tet": "Vizita Ami", "id": "Kunjungi Kami", "pt": "Visite-nos", "en": "Visit Us"},
    "Our Location": {"tet": "Ami nia Lokalizasaun", "id": "Lokasi Kami", "pt": "A Nossa Localização", "en": "Our Location"},
    "Coordinates": {"tet": "Koordenada", "id": "Koordinat", "pt": "Coordenadas", "en": "Coordinates"},
    "Get Route From My Location": {"tet": "Buka Rota husi Ami nia Lokalizasaun", "id": "Dapatkan Rute dari Lokasi Saya", "pt": "Obter Rota a partir da Minha Localização", "en": "Get Route From My Location"},
    "Open in Google Maps": {"tet": "Loke iha Google Maps", "id": "Buka di Google Maps", "pt": "Abrir no Google Maps", "en": "Open in Google Maps"},
    'Click "Get Route" to draw driving directions from your current location.': {
        "tet": "Klik \"Buka Rota\" atu dezeña dalan kondusaun husi ita nia lokalizasaun atuál.",
        "id": "Klik \"Dapatkan Rute\" untuk menampilkan petunjuk arah dari lokasi Anda saat ini.",
        "pt": "Clique em \"Obter Rota\" para traçar o trajeto a partir da sua localização atual.",
        "en": 'Click "Get Route" to draw driving directions from your current location.'},
    "Collaboration": {"tet": "Kolaborasaun", "id": "Kolaborasi", "pt": "Colaboração", "en": "Collaboration"},
    "Partners and Donors": {"tet": "Parseiru no Doadór", "id": "Mitra dan Donor", "pt": "Parceiros e Doadores", "en": "Partners and Donors"},
    "Thanks to our partners.": {"tet": "Obrigadu ba ami nia parseiru sira.", "id": "Terima kasih kepada para mitra kami.", "pt": "Obrigado aos nossos parceiros.", "en": "Thanks to our partners."},
    "By": {"tet": "Husi", "id": "Oleh", "pt": "Por", "en": "By"},
    "min read": {"tet": "minutu lee", "id": "menit baca", "pt": "min de leitura", "en": "min read"},
    "Back to Articles": {"tet": "Fila ba Artigu", "id": "Kembali ke Artikel", "pt": "Voltar aos Artigos", "en": "Back to Articles"},
    "Articles": {"tet": "Artigu", "id": "Artikel", "pt": "Artigos", "en": "Articles"},
    "No articles yet.": {"tet": "Seidauk iha artigu.", "id": "Belum ada artikel.", "pt": "Ainda não há artigos.", "en": "No articles yet."},
    "Name": {"tet": "Naran", "id": "Nama", "pt": "Nome", "en": "Name"},
    "Message": {"tet": "Mensajen", "id": "Pesan", "pt": "Mensagem", "en": "Message"},
    "Send Message": {"tet": "Haruka Mensajen", "id": "Kirim Pesan", "pt": "Enviar Mensagem", "en": "Send Message"},
    "Contact Us": {"tet": "Kontaktu Ami", "id": "Hubungi Kami", "pt": "Contacte-nos", "en": "Contact Us"},
    "Have a question or want to collaborate with MDI? Send us a message using the form below or reach us via the details listed here.": {
        "tet": "Iha pergunta ka hakarak kolabora ho MDI? Haruka mensajen ba ami liu husi formuláriu iha kraik ka liu husi detalhe ne'ebé lista iha ne'e.",
        "id": "Ada pertanyaan atau ingin berkolaborasi dengan MDI? Kirimkan pesan melalui formulir di bawah ini atau hubungi kami melalui detail yang tercantum di sini.",
        "pt": "Tem alguma questão ou deseja colaborar com o MDI? Envie-nos uma mensagem através do formulário abaixo ou contacte-nos através dos detalhes aqui indicados.",
        "en": "Have a question or want to collaborate with MDI? Send us a message using the form below or reach us via the details listed here."},
    "No donor data yet. Add it via Django Admin.": {"tet": "Seidauk iha dadus doadór. Aumenta liu husi Django Admin.", "id": "Belum ada data donor. Tambahkan melalui Django Admin.", "pt": "Ainda não há dados de doadores. Adicione através do Django Admin.", "en": "No donor data yet. Add it via Django Admin."},
    "Download": {"tet": "Download", "id": "Unduh", "pt": "Transferir", "en": "Download"},
    "No documents yet in this category.": {"tet": "Seidauk iha dokumentu ba kategoria ne'e.", "id": "Belum ada dokumen di kategori ini.", "pt": "Ainda não há documentos nesta categoria.", "en": "No documents yet in this category."},
    "Photo Gallery": {"tet": "Galeria Foto", "id": "Galeri Foto", "pt": "Galeria de Fotos", "en": "Photo Gallery"},
    "Back to News": {"tet": "Fila ba Notísia", "id": "Kembali ke Berita", "pt": "Voltar às Notícias", "en": "Back to News"},
    "Detail Data": {"tet": "Detalha Dadus", "id": "Detail Data", "pt": "Detalhes dos Dados", "en": "Detail Data"},
    "Published Date": {"tet": "Data Publikadu", "id": "Tanggal Terbit", "pt": "Data de Publicação", "en": "Published Date"},
    "Category": {"tet": "Kategoria", "id": "Kategori", "pt": "Categoria", "en": "Category"},
    "Location": {"tet": "Lokalizasaun", "id": "Lokasi", "pt": "Localização", "en": "Location"},
    "Location Detail": {"tet": "Detalha Lokalizasaun", "id": "Detail Lokasi", "pt": "Detalhe da Localização", "en": "Location Detail"},
    "Related Program": {"tet": "Programa Relasionadu", "id": "Program Terkait", "pt": "Programa Relacionado", "en": "Related Program"},
    "Source": {"tet": "Fonte", "id": "Sumber", "pt": "Fonte", "en": "Source"},
    "photos in this story": {"tet": "foto iha istória ida-ne'e", "id": "foto dalam berita ini", "pt": "fotos nesta notícia", "en": "photos in this story"},
    "No news yet.": {"tet": "Seidauk iha notísia.", "id": "Belum ada berita.", "pt": "Ainda não há notícias.", "en": "No news yet."},
    "MDI collaborates with civil society networks, international agencies, and government institutions:": {
        "tet": "MDI kolabora hamutuk ho rede sosiedade sivíl, ajénsia internasionál no instituisaun governu:",
        "id": "MDI berkolaborasi dengan jaringan masyarakat sipil, lembaga internasional, dan institusi pemerintah:",
        "pt": "O MDI colabora com redes da sociedade civil, agências internacionais e instituições governamentais:",
        "en": "MDI collaborates with civil society networks, international agencies, and government institutions:"},
    "No partner data yet. Add it via Django Admin.": {"tet": "Seidauk iha dadus parseiru. Aumenta liu husi Django Admin.", "id": "Belum ada data mitra. Tambahkan melalui Django Admin.", "pt": "Ainda não há dados de parceiros. Adicione através do Django Admin.", "en": "No partner data yet. Add it via Django Admin."},
    "Program Areas": {"tet": "Área Programa", "id": "Bidang Program", "pt": "Áreas de Programa", "en": "Program Areas"},
    "Expected Indicators": {"tet": "Indikadór Esperadu", "id": "Indikator yang Diharapkan", "pt": "Indicadores Esperados", "en": "Expected Indicators"},
    "Sub-Outcomes": {"tet": "Sub-Rezultadu", "id": "Sub-Hasil", "pt": "Sub-Resultados", "en": "Sub-Outcomes"},
    "Program Structure": {"tet": "Estrutura Programa", "id": "Struktur Program", "pt": "Estrutura do Programa", "en": "Program Structure"},
    "section.": {"tet": "seksaun.", "id": "bagian.", "pt": "secção.", "en": "section."},
    "Our Foundation": {"tet": "Ami nia Fundasaun", "id": "Fondasi Kami", "pt": "A Nossa Fundação", "en": "Our Foundation"},
    "Quick Facts": {"tet": "Dadus Rápidu", "id": "Fakta Singkat", "pt": "Factos Rápidos", "en": "Quick Facts"},
    "Full Name:": {"tet": "Naran Kompletu:", "id": "Nama Lengkap:", "pt": "Nome Completo:", "en": "Full Name:"},
    "Established:": {"tet": "Estabelesidu:", "id": "Didirikan:", "pt": "Fundado em:", "en": "Established:"},
    "Location:": {"tet": "Fatin:", "id": "Lokasi:", "pt": "Localização:", "en": "Location:"},
    "Focus:": {"tet": "Fokus:", "id": "Fokus:", "pt": "Foco:", "en": "Focus:"},
    "Email:": {"tet": "Email:", "id": "Email:", "pt": "Email:", "en": "Email:"},
    "Phone:": {"tet": "Telefone:", "id": "Telepon:", "pt": "Telefone:", "en": "Phone:"},
    "Approach": {"tet": "Abordajen", "id": "Pendekatan", "pt": "Abordagem", "en": "Approach"},
    "Coverage": {"tet": "Kobertura", "id": "Cakupan", "pt": "Cobertura", "en": "Coverage"},
    "Founders": {"tet": "Fundadór", "id": "Pendiri", "pt": "Fundadores", "en": "Founders"},
    "Founders of Mata Dalan Institute (MDI)": {"tet": "Fundadór Mata Dalan Institute (MDI)", "id": "Pendiri Mata Dalan Institute (MDI)", "pt": "Fundadores do Mata Dalan Institute (MDI)", "en": "Founders of Mata Dalan Institute (MDI)"},
    "The founding members of MDI.": {"tet": "Membru fundadór MDI nian.", "id": "Anggota pendiri MDI.", "pt": "Os membros fundadores do MDI.", "en": "The founding members of MDI."},
    "No founder data yet. Add it via Django Admin → Website → Founder.": {
        "tet": "Seidauk iha dadus fundadór. Aumenta liu husi Django Admin → Website → Fundadór.",
        "id": "Belum ada data pendiri. Tambahkan melalui Django Admin → Website → Founder.",
        "pt": "Ainda não há dados de fundadores. Adicione através do Django Admin → Website → Founder.",
        "en": "No founder data yet. Add it via Django Admin → Website → Founder."},
    "Get to Know Us": {"tet": "Koñese Ami", "id": "Kenali Kami", "pt": "Conheça-nos", "en": "Get to Know Us"},
}

BLOCKTRANS = {
    "Bem-vindu ba {{ name }}": {
        "tet": "Bem-vindu ba %(name)s",
        "id": "Selamat datang di %(name)s",
        "pt": "Bem-vindo ao %(name)s",
        "en": "Welcome to %(name)s",
    },
    "List of public documents related to the {{ name }} category.": {
        "tet": "Lista dokumentu públiku relasiona ho kategoria %(name)s.",
        "id": "Daftar dokumen publik terkait kategori %(name)s.",
        "pt": "Lista de documentos públicos relacionados com a categoria %(name)s.",
        "en": "List of public documents related to the %(name)s category.",
    },
    "Active since {{ year }}": {
        "tet": "Ativu dezde %(year)s",
        "id": "Aktif sejak %(year)s",
        "pt": "Ativo desde %(year)s",
        "en": "Active since %(year)s",
    },
    "Based in {{ place }}": {
        "tet": "Baze iha %(place)s",
        "id": "Berbasis di %(place)s",
        "pt": "Sediado em %(place)s",
        "en": "Based in %(place)s",
    },
    "Detailed content and relevant documents for this program area can be found in the": {
        "tet": "Konteúdu detalhadu no dokumentu relevante ba área programa ne'e bele haree iha seksaun",
        "id": "Konten rinci dan dokumen terkait untuk area program ini dapat ditemukan di bagian",
        "pt": "Conteúdo detalhado e documentos relevantes para esta área de programa podem ser encontrados na secção",
        "en": "Detailed content and relevant documents for this program area can be found in the",
    },
}

LANGS = ["tet", "id", "pt", "en"]

for lang in LANGS:
    po = polib.POFile()
    po.metadata = {
        "Project-Id-Version": "1.0",
        "Language": lang,
        "Content-Type": "text/plain; charset=utf-8",
        "MIME-Version": "1.0",
        "Content-Transfer-Encoding": "8bit",
    }
    for msgid, translations in STRINGS.items():
        po.append(polib.POEntry(msgid=msgid, msgstr=translations.get(lang, translations["en"])))
    for msgid, translations in BLOCKTRANS.items():
        entry_msgid = msgid.replace("{{ name }}", "%(name)s").replace("{{ year }}", "%(year)s").replace("{{ place }}", "%(place)s")
        po.append(polib.POEntry(msgid=entry_msgid, msgstr=translations.get(lang, translations["en"])))

    lang_dir = LOCALE_DIR / lang / "LC_MESSAGES"
    lang_dir.mkdir(parents=True, exist_ok=True)
    po_path = lang_dir / "django.po"
    mo_path = lang_dir / "django.mo"
    po.save(str(po_path))
    po.save_as_mofile(str(mo_path))
    print(f"{po_path}: {len(po)} entries -> {mo_path}")

print("Done.")
