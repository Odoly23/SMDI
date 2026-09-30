import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.utils.text import slugify

from config.models import SiteConfig
from custom.models import Category, Municipality, Year
from users.models import Profile, GROUP_ADMIN, GROUP_STAFF, GROUP_MEMBER
from website.models import (
    Slide, VisionMission, WhoWeAre, Program, Activity,
    NewsPost, NewsImage, Article, OrgMember, Founder, Partner
)


class Command(BaseCommand):
    help = "Isi data awal (seed) untuk website Mata Dalan Institute (MDI)."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding data MDI...")

        # ---------- Grupu (kontrolu asesu dashboard - haree config.decorators.allowed_users) ----------
        for group_name in [GROUP_ADMIN, GROUP_STAFF, GROUP_MEMBER]:
            Group.objects.get_or_create(name=group_name)

        # ---------- SiteConfig ----------
        SiteConfig.load()

        # ---------- Custom lookups ----------
        for name in ["Dili", "Viqueque", "Manatuto", "Aileu", "Ermera", "Covalima", "Liquiçá", "RAEOA"]:
            Municipality.objects.get_or_create(name=name)
        for y in [2020, 2021, 2022, 2023, 2024, 2025]:
            Year.objects.get_or_create(value=y)

        doc_categories = [
            ("doc-pnds", "Doc PNDS"),
            ("doc-oge", "Doc OJE"),
            ("doc-petroleum", "Doc Fundu Petroleum"),
            ("doc-statistika", "Statistika"),
            ("doc-outros", "Dok Seluk"),
        ]
        for slug, name in doc_categories:
            Category.objects.get_or_create(slug=slug, defaults={"name": name, "context": "document"})

        # =====================================================================
        # VISION / MISSION  (fonte: dokumentu "MDI Profile", versaun EN + Tetun)
        # =====================================================================
        vm = VisionMission.load()
        vm.vision_text = (
            "MDI prevee sosiedade timorense ida ne'e demokrátiku, autónomu, ho análitiku, "
            "no partisipativu, ne'ebe serve nu'udar fatuk-inan ba dezenvolvimentu nasionál "
            "ne'ebe sustentável. Organizasaun ne'e haka'as-an atu kuda kultura ida "
            "responsabilizasaun no transparénsia nian, hodi estabelese fundasaun ba "
            "governasaun ne'ebe efikás no étika."
        )
        vm.vision_text_i18n = {
            "id": "MDI membayangkan masyarakat Timor-Leste yang demokratis, otonom, analitis, "
                  "dan partisipatif, yang menjadi landasan bagi pembangunan nasional yang "
                  "berkelanjutan. Organisasi ini berupaya menumbuhkan budaya akuntabilitas dan "
                  "transparansi, guna membangun fondasi bagi tata kelola yang efektif dan etis.",
            "pt": "O MDI antevê uma sociedade timorense democrática, autónoma, analiticamente "
                  "envolvida e participativa, que sirva de pedra angular para o desenvolvimento "
                  "nacional sustentável. A organização esforça-se por cultivar uma cultura de "
                  "responsabilização e transparência, estabelecendo as bases para uma "
                  "governação eficaz e ética.",
            "en": "MDI envisions a democratic, autonomous, analytically engaged, and "
                  "participatory Timorese society, serving as the cornerstone for sustainable "
                  "national development. The organization strives to cultivate a culture of "
                  "accountability and transparency, establishing the foundation for effective, "
                  "ethical governance.",
        }
        vm.mission_text = "MDI nia misaun mak atu haforsa transparénsia, servisu públiku no partisipasaun komunidade."
        vm.mission_text_i18n = {
            "id": "Misi MDI adalah memperkuat transparansi, layanan publik, dan partisipasi masyarakat.",
            "pt": "A missão do MDI é reforçar a transparência, os serviços públicos e a participação comunitária.",
            "en": "MDI's mission is to strengthen transparency, public services and community participation.",
        }
        vm.mission_points = {
            "tet": [
                "Hasa'e transparénsia no mekanizmu responsabilizasaun iha ámbitu Orsamentu Jerál "
                "Estadu (OGE) no polítika dezenvolvimentu iha Timor-Leste, hodi garante utilizasaun "
                "ótimu fundu públiku.",
                "Hadi'a programa asisténsia públika no rasionaliza fasilitasaun nesesidade báziku "
                "komunidade nian hodi haburas dezenvolvimentu sósiu-ekonómiku.",
                "Promove envolvimentu ativu komunidade nian iha prosesu dezenvolvimentu hodi "
                "garante inkluzividade no responde ba nesesidade lokál sira.",
                "Hakbi'it organizasaun sosiedade sivíl sira atu sai nu'udar ajente kontrolu sosiál, "
                "hodi responsabiliza governu ba ninia asaun no desizaun sira.",
            ],
            "id": [
                "Meningkatkan transparansi dan mekanisme akuntabilitas dalam kerangka Anggaran "
                "Umum Negara (OGE) dan kebijakan pembangunan di Timor-Leste, guna memastikan "
                "pemanfaatan optimal dana publik.",
                "Meningkatkan program bantuan publik dan menyederhanakan fasilitasi kebutuhan "
                "dasar masyarakat guna mendorong pembangunan sosial-ekonomi.",
                "Mendorong keterlibatan aktif masyarakat dalam proses pembangunan guna memastikan "
                "inklusivitas dan daya tanggap terhadap kebutuhan lokal.",
                "Memberdayakan organisasi masyarakat sipil untuk menjadi agen kontrol sosial, yang "
                "meminta pertanggungjawaban pemerintah atas tindakan dan keputusannya.",
            ],
            "pt": [
                "Reforçar a transparência e os mecanismos de responsabilização no âmbito do "
                "Orçamento Geral do Estado (OGE) e da política de desenvolvimento em "
                "Timor-Leste, garantindo a utilização ótima dos fundos públicos.",
                "Melhorar os programas de assistência pública e simplificar a facilitação das "
                "necessidades básicas das comunidades para promover o desenvolvimento "
                "socioeconómico.",
                "Promover o envolvimento ativo da comunidade no processo de desenvolvimento, "
                "garantindo a inclusão e a capacidade de resposta às necessidades locais.",
                "Capacitar as organizações da sociedade civil para atuarem como agentes de "
                "controlo social, responsabilizando o governo pelas suas ações e decisões.",
            ],
            "en": [
                "Enhance transparency and accountability mechanisms within the framework of the "
                "General State Budget (OGE) and development policy in Timor-Leste, ensuring the "
                "optimal utilization of public funds.",
                "Improve public assistance programs and streamline the facilitation of basic "
                "community needs to foster socio-economic development.",
                "Promote active community engagement in the development process to ensure "
                "inclusivity and responsiveness to local needs.",
                "Empower civil society organizations to act as social control agents, holding the "
                "government accountable for its actions and decisions.",
            ],
        }
        vm.save()

        # =====================================================================
        # WHO WE ARE / PROFILE  (fonte: dokumentu "MDI Profile")
        # =====================================================================
        wwa = WhoWeAre.load()
        wwa.profile_text = (
            "Mata Dalan Institute (MDI) maka organizasaun naun-governamentál (ONG) ida ne'ebe "
            "harii iha tinan 2005. Nia iha kompromisu atu haburas transparénsia no "
            "responsabilizasaun sosiál iha nia área sira operasaun nian."
        )
        wwa.profile_text_i18n = {
            "id": "Mata Dalan Institute (MDI) adalah organisasi non-pemerintah (LSM) yang "
                  "didirikan pada tahun 2005. MDI berkomitmen untuk mendorong transparansi dan "
                  "akuntabilitas sosial di wilayah operasinya.",
            "pt": "O Mata Dalan Institute (MDI) é uma organização não-governamental (ONG) "
                  "fundada em 2005. Está empenhado em promover a transparência e a "
                  "responsabilização social nas suas áreas de atuação.",
            "en": "The Mata Dalan Institute (MDI) is a non-governmental organization (NGO) "
                  "established in 2005. It is committed to fostering transparency and social "
                  "accountability within its areas of operation.",
        }
        wwa.who_we_are_text = (
            "MDI nia misaun bazeia ba fiar katak aprosimasaun partisipativu no advokasia bazeia "
            "ba evidénsia importante tebes ba dezenvolvimentu sustentável no governasaun ida "
            "ne'ebe di'ak liu."
        )
        wwa.who_we_are_text_i18n = {
            "id": "Misi MDI didasarkan pada keyakinan bahwa pendekatan partisipatif dan advokasi "
                  "berbasis bukti sangat penting bagi pembangunan berkelanjutan dan tata kelola "
                  "yang lebih baik.",
            "pt": "A missão do MDI assenta na convicção de que as abordagens participativas e a "
                  "advocacia baseada em evidências são essenciais para o desenvolvimento "
                  "sustentável e uma melhor governação.",
            "en": "MDI's mission is grounded in the belief that participatory approaches and "
                  "evidence-based advocacy are critical to sustainable development and good "
                  "governance.",
        }
        wwa.established_year = "2005"
        wwa.based_in = "Bebonuk, Comoro, Dili, Timor-Leste"
        wwa.focus_area = "Monitoring, Advocacy & Community Strengthening"

        wwa.org_structure_title = "Estrutura Organizasionál"
        wwa.org_structure_intro = "MDI hetan apoiu hosi ekipa ida ho membru pesoál dedikadu na'in 18, inklui:"
        wwa.org_structure_intro_i18n = {
            "id": "MDI didukung oleh tim yang terdiri dari 18 staf yang berdedikasi, termasuk:",
            "pt": "O MDI conta com o apoio de uma equipa de 18 membros de pessoal dedicado, incluindo:",
            "en": "MDI is supported by a team of 18 dedicated staff members, including:",
        }
        wwa.org_structure_items = {
            "tet": [
                "Pesoál jestaun superiór na'in 4,",
                "Membru funsionáriu na'in 3 ne'ebe responsavél ba administrasaun, finansas, no lojístika,",
                "Pesoál programa na'in 12, no",
                "Enumeradór 20, balansu hanesan tuir jéneru.",
            ],
            "id": [
                "4 personel manajemen senior,",
                "3 staf yang menangani administrasi, keuangan, dan logistik,",
                "12 staf program, dan",
                "20 enumerator, seimbang berdasarkan gender.",
            ],
            "pt": [
                "4 elementos de gestão sénior,",
                "3 membros do pessoal responsáveis pela administração, finanças e logística,",
                "12 elementos do pessoal de programa, e",
                "20 enumeradores, equilibrados em termos de género.",
            ],
            "en": [
                "4 senior management personnel,",
                "3 staff members handling administration, finance, and logistics,",
                "12 program staff, and",
                "20 enumerators, balanced equally by gender.",
            ],
        }
        wwa.org_structure_outro = (
            "Estrutura ida-ne'e garante kapasidade ida ne'ebe sufostikadu atu implementa "
            "programa sira enkuantu mantein efisiénsia operasionál no ekuidade jéneru iha "
            "organizasaun nia laran."
        )
        wwa.org_structure_outro_i18n = {
            "id": "Struktur ini memastikan kapasitas yang kuat untuk melaksanakan program sambil "
                  "menjaga efisiensi operasional dan kesetaraan gender dalam organisasi.",
            "pt": "Esta estrutura garante uma capacidade robusta para implementar os programas, "
                  "mantendo a eficiência operacional e a equidade de género dentro da organização.",
            "en": "This structure ensures a robust capacity to implement programs while "
                  "maintaining operational efficiency and gender equity within the organization.",
        }

        wwa.strategy_title = "Abordajen Estratéjiku"
        wwa.strategy_text = (
            "MDI nia estratéjia operasionál sentra iha metodolojia peskiza partisipativu no "
            "advokasia bazeia ba evidénsia. Hodi fó prioridade ba envolvimentu parte interesada "
            "sira no aproveita dadus empíriku, MDI haburas propriedade komunidade, "
            "sustentabilidade, no foti desizaun informadu iha ninia intervensaun sira. "
            "Aprosimasaun ida-ne'e permite MDI atu rezolve nesesidade lokál sira ho efetivu "
            "enkuantu promove inkluzividade no empoderamentu."
        )
        wwa.strategy_text_i18n = {
            "id": "Strategi operasional MDI berpusat pada metodologi penelitian partisipatif dan "
                  "advokasi berbasis bukti. Dengan mengutamakan keterlibatan pemangku "
                  "kepentingan dan memanfaatkan data empiris, MDI mendorong rasa kepemilikan "
                  "komunitas, keberlanjutan, dan pengambilan keputusan yang berdasarkan "
                  "informasi dalam setiap intervensinya. Pendekatan ini memungkinkan MDI untuk "
                  "menjawab kebutuhan lokal secara efektif sekaligus mendorong inklusivitas dan "
                  "pemberdayaan.",
            "pt": "A estratégia operacional do MDI centra-se em metodologias de investigação "
                  "participativa e advocacia baseada em evidências. Ao dar prioridade ao "
                  "envolvimento das partes interessadas e ao tirar partido de dados empíricos, "
                  "o MDI promove a apropriação comunitária, a sustentabilidade e a tomada de "
                  "decisões informadas nas suas intervenções. Esta abordagem permite ao MDI "
                  "responder eficazmente às necessidades locais, promovendo simultaneamente a "
                  "inclusão e o empoderamento.",
            "en": "MDI's operational strategy centers on participatory research methodologies "
                  "and evidence-based advocacy. By prioritizing stakeholder involvement and "
                  "leveraging empirical data, MDI fosters community ownership, sustainability, "
                  "and informed decision-making in its interventions. This approach enables MDI "
                  "to address local needs effectively while promoting inclusivity and "
                  "empowerment.",
        }

        wwa.geo_focus_title = "Foku Jeográfiku"
        wwa.geo_focus_intro = "MDI halo operasaun iha área jeográfika ne'ebe luan iha Timor-Leste, ho rejiaun alvu sira inklui:"
        wwa.geo_focus_intro_i18n = {
            "id": "MDI beroperasi di wilayah geografis yang luas di Timor-Leste, dengan wilayah "
                  "sasaran meliputi:",
            "pt": "O MDI opera numa vasta área geográfica em Timor-Leste, com regiões-alvo que "
                  "incluem:",
            "en": "MDI operates across a wide geographical area in Timor-Leste, with target "
                  "regions including:",
        }
        wwa.geo_focus_regions = {
            "tet": ["Dili", "Viqueque", "Manatuto", "Aileu", "Ermera", "Covalima", "Liquiçá", "RAEOA"],
            "id": ["Dili", "Viqueque", "Manatuto", "Aileu", "Ermera", "Covalima", "Liquiçá", "RAEOA"],
            "pt": ["Dili", "Viqueque", "Manatuto", "Aileu", "Ermera", "Covalima", "Liquiçá", "RAEOA"],
            "en": ["Dili", "Viqueque", "Manatuto", "Aileu", "Ermera", "Covalima", "Liquiçá", "RAEOA"],
        }
        wwa.geo_focus_outro = (
            "Liuhusi ninia serbisu, MDI hakarak rezolve dezafiu sosio-ekonómiku sira ne'ebe "
            "maka prevalente iha rejiaun sira-ne'e, hodi garante dezenvolvimentu ne'ebe "
            "ekuitativu no iha impaktu."
        )
        wwa.geo_focus_outro_i18n = {
            "id": "Melalui kerjanya, MDI bertujuan mengatasi tantangan sosial-ekonomi yang lazim "
                  "terjadi di wilayah-wilayah ini, guna memastikan pembangunan yang adil dan "
                  "berdampak.",
            "pt": "Através do seu trabalho, o MDI procura enfrentar os desafios socioeconómicos "
                  "prevalecentes nestas regiões, garantindo um desenvolvimento equitativo e com "
                  "impacto.",
            "en": "Through its work, MDI aims to address the socio-economic challenges "
                  "prevalent in these regions, ensuring equitable and impactful development.",
        }
        wwa.save()

        # =====================================================================
        # PROGRAMS: Pilar 1 / Pilar 2 (+ 2.1-2.4) / Pilar 3
        # (fonte: dokumentu "Strategic Plan" 2026-2030)
        # =====================================================================
        Program.objects.all().delete()

        def make_program(slug, title, title_i18n, heading, heading_i18n, desc, desc_i18n,
                          indicators_tet, indicators_en, icon, order, parent=None):
            obj = Program.objects.create(
                slug=slug, parent=parent, title=title, title_i18n=title_i18n,
                heading=heading, heading_i18n=heading_i18n,
                description=desc, description_i18n=desc_i18n,
                indicators={"tet": indicators_tet, "en": indicators_en},
                icon=icon, order=order,
            )
            return obj

        pilar1 = make_program(
            "pilar-1", "Pilar 1",
            {"id": "Pilar 1", "pt": "Pilar 1", "en": "Pillar 1"},
            "Outcome 1 – Pilar 1: Jestaun Institusionál Forte no Sustentabilidade Finanseira",
            {"id": "Outcome 1 – Pilar 1: Manajemen Kelembagaan Kuat dan Keberlanjutan Finansial",
             "pt": "Outcome 1 – Pilar 1: Gestão Institucional Forte e Sustentabilidade Financeira",
             "en": "Outcome 1 – Pillar 1: Strong Institutional Management and Financial Sustainability"},
            "MDI iha sistema governansa, jestaun institusionál no kapasidade organizasionál "
            "ne'ebé forte, transparente no sustentável, ho sistema finanseiru ne'ebé "
            "diversifikadu atu suporta implementasaun efetiva ba Planu Estratéjiku 2026–2030.",
            {"id": "MDI memiliki sistem tata kelola, manajemen kelembagaan, dan kapasitas "
                   "organisasi yang kuat, transparan, dan berkelanjutan, dengan sistem keuangan "
                   "yang terdiversifikasi untuk mendukung pelaksanaan Rencana Strategis "
                   "2026–2030 secara efektif.",
             "pt": "O MDI possui um sistema de governação, gestão institucional e capacidade "
                   "organizacional fortes, transparentes e sustentáveis, com um sistema "
                   "financeiro diversificado para apoiar a implementação eficaz do Plano "
                   "Estratégico 2026–2030.",
             "en": "MDI has a strong, transparent and sustainable governance system, "
                   "institutional management and organizational capacity, with a diversified "
                   "financial system to support the effective implementation of the "
                   "2026–2030 Strategic Plan."},
            [
                "Sistema polítika interna, SOP, manual operasional no mekanizmu kontrolu institusionál implementa ho efetivu.",
                "Sistema Monitorizasaun, Avaliasaun no Aprendizajen (MEL) funsiona hanesan instrumentu melhoria contínua.",
                "MDI iha sistema dijitál ba jestaun programa, finansas, rekursu umanu no informasaun institusionál.",
                "MDI aumenta kapasidade mobilizasaun rekursu liuhusi grant, parseria estratéjika, konsultoria no fonte sustentabilidade seluk.",
                "Prezensa no identidade institusionál MDI aumenta iha nivel nasional, rejionál no internasionál.",
            ],
            [
                "Internal policy systems, SOPs, operational manuals and institutional control mechanisms are effectively implemented.",
                "The Monitoring, Evaluation and Learning (MEL) system functions as a continuous improvement tool.",
                "MDI has digital systems for program, finance, human resource and institutional information management.",
                "MDI increases its resource mobilization capacity through grants, strategic partnerships, consultancy and other sustainability sources.",
                "MDI's institutional presence and identity grows at national, regional and international level.",
            ],
            "bi-diagram-3", 0,
        )

        pilar2 = make_program(
            "pilar-2", "Pilar 2",
            {"id": "Pilar 2", "pt": "Pilar 2", "en": "Pillar 2"},
            "Outcome 2 – Pilar 2: Think Tank ASEAN (SIS) – Influénsia Estratéjika no Parseria",
            {"id": "Outcome 2 – Pilar 2: Think Tank ASEAN (SIS) – Pengaruh Strategis dan Kemitraan",
             "pt": "Outcome 2 – Pilar 2: Think Tank ASEAN (SIS) – Influência Estratégica e Parcerias",
             "en": "Outcome 2 – Pillar 2: ASEAN Think Tank (SIS) – Strategic Influence and Partnership"},
            "MDI sai nu'udar think tank nasionál kredível no influente iha peskiza, análiza "
            "polítika no diálogu estratéjiku kona-ba ASEAN, relasaun internasionál no asuntu "
            "emerjente ne'ebé relevante ba Timor-Leste.",
            {"id": "MDI menjadi lembaga think tank nasional yang kredibel dan berpengaruh dalam "
                   "penelitian, analisis kebijakan, dan dialog strategis mengenai ASEAN, "
                   "hubungan internasional, dan isu-isu baru yang relevan bagi Timor-Leste.",
             "pt": "O MDI torna-se um think tank nacional credível e influente na investigação, "
                   "análise de políticas e diálogo estratégico sobre a ASEAN, relações "
                   "internacionais e questões emergentes relevantes para Timor-Leste.",
             "en": "MDI becomes a credible and influential national think tank in research, "
                   "policy analysis and strategic dialogue on ASEAN, international relations "
                   "and emerging issues relevant to Timor-Leste."},
            [
                "Governu, Parlamentu, universidade no partes interesadu uza rezultadu peskiza no rekomendasaun MDI-SIS iha prosesu advokasia no tomada desizaun.",
                "MDI-SIS produz policy brief, relatóriu estratéjiku no publikasaun kona-ba ASEAN no asuntu internasionál.",
                "MDI-SIS hametin parseria ho think tank, universidade no instituisaun rejionál/internasionál.",
                "Fórum polítika, semináriu no diálogu estratéjiku organiza regularmente.",
                "Sosiedade Timor-Leste aumenta koñesimentu kona-ba ASEAN, integrasaun rejionál no oportunidade estratéjika.",
            ],
            [
                "Government, Parliament, universities and stakeholders use MDI-SIS research results and recommendations in advocacy and decision-making.",
                "MDI-SIS produces policy briefs, strategic reports and publications on ASEAN and international affairs.",
                "MDI-SIS strengthens partnerships with regional/international think tanks, universities and institutions.",
                "Policy forums, seminars and strategic dialogues are regularly organized.",
                "Timorese society increases its knowledge of ASEAN, regional integration and strategic opportunities.",
            ],
            "bi-globe-asia-australia", 1,
        )

        make_program(
            "pilar-2-1", "2.1 Influénsia Estratéjika",
            {"id": "2.1 Pengaruh Strategis", "pt": "2.1 Influência Estratégica", "en": "2.1 Strategic Influence"},
            "Outcome 2.1 – Influénsia Estratéjika no Parseria",
            {"id": "Outcome 2.1 – Pengaruh Strategis dan Kemitraan",
             "pt": "Outcome 2.1 – Influência Estratégica e Parcerias",
             "en": "Outcome 2.1 – Strategic Influence and Partnership"},
            "MDI sai nu'udar think tank nasionál kredível no influente iha peskiza, análiza "
            "polítika no diálogu estratéjiku kona-ba ASEAN, relasaun internasionál no asuntu "
            "emerjente ne'ebé relevante ba Timor-Leste.",
            {"id": "MDI menjadi lembaga think tank nasional yang kredibel dan berpengaruh dalam "
                   "penelitian, analisis kebijakan, dan dialog strategis mengenai ASEAN.",
             "pt": "O MDI torna-se um think tank nacional credível e influente na investigação "
                   "e diálogo estratégico sobre a ASEAN.",
             "en": "MDI becomes a credible and influential national think tank in research and "
                   "strategic dialogue on ASEAN."},
            [
                "Governu, Parlamentu, universidade no partes interesadu uza rezultadu peskiza no rekomendasaun MDI-SIS iha prosesu advokasia no tomada desizaun.",
                "MDI-SIS produz policy brief, relatóriu estratéjiku no publikasaun kona-ba ASEAN no asuntu internasionál.",
                "MDI-SIS hametin parseria ho think tank, universidade no instituisaun rejionál/internasionál.",
                "Fórum polítika, semináriu no diálogu estratéjiku organiza regularmente.",
                "Sosiedade Timor-Leste aumenta koñesimentu kona-ba ASEAN, integrasaun rejionál no oportunidade estratéjika.",
            ],
            [
                "Government, Parliament, universities and stakeholders use MDI-SIS research results and recommendations in advocacy and decision-making.",
                "MDI-SIS produces policy briefs, strategic reports and publications on ASEAN and international affairs.",
                "MDI-SIS strengthens partnerships with regional/international think tanks, universities and institutions.",
                "Policy forums, seminars and strategic dialogues are regularly organized.",
                "Timorese society increases its knowledge of ASEAN, regional integration and strategic opportunities.",
            ],
            "bi-diagram-2", 0, parent=pilar2,
        )

        make_program(
            "pilar-2-2", "2.2 Polítika Bazeia Evidénsia",
            {"id": "2.2 Kebijakan Berbasis Bukti", "pt": "2.2 Política Baseada em Evidências", "en": "2.2 Evidence-Based Policy"},
            "Outcome 2.2 – Kapasidade Institusionál no Polítika Bazeia ba Evidénsia",
            {"id": "Outcome 2.2 – Kapasitas Kelembagaan dan Kebijakan Berbasis Bukti",
             "pt": "Outcome 2.2 – Capacidade Institucional e Política Baseada em Evidências",
             "en": "Outcome 2.2 – Institutional Capacity and Evidence-Based Policy"},
            "MDI sai nu'udar sentru koñesimentu ne'ebé produz, analiza no disemina evidénsia "
            "kredível hodi suporta formulasaun polítika públika inkluziva, transparente no "
            "bazeia ba dadus.",
            {"id": "MDI menjadi pusat pengetahuan yang menghasilkan, menganalisis, dan "
                   "menyebarluaskan bukti yang kredibel untuk mendukung perumusan kebijakan "
                   "publik yang inklusif, transparan, dan berbasis data.",
             "pt": "O MDI torna-se um centro de conhecimento que produz, analisa e dissemina "
                   "evidências credíveis para apoiar a formulação de políticas públicas "
                   "inclusivas, transparentes e baseadas em dados.",
             "en": "MDI becomes a knowledge center that produces, analyzes and disseminates "
                   "credible evidence to support inclusive, transparent and data-driven public "
                   "policy formulation."},
            [
                "MDI produz peskiza, estudu no análiza polítika kona-ba asuntu dezenvolvimentu nasional.",
                "Rezultadu peskiza MDI uza husi instituisaun estadu, organizasaun sivíl no parseiru dezenvolvimentu.",
                "Polítika GEDSI integra iha programa, peskiza no operasaun institusionál MDI.",
                "MDI uza dadus nasional no dadus lokál hodi kontribui ba tomada desizaun bazeia ba evidénsia.",
                "Publikasaun, policy brief no produtu koñesimentu MDI aumenta nia kredibilidade públika.",
            ],
            [
                "MDI produces research, studies and policy analysis on national development issues.",
                "MDI research results are used by state institutions, civil society organizations and development partners.",
                "GEDSI policy is integrated into MDI's programs, research and institutional operations.",
                "MDI uses national and local data to contribute to evidence-based decision-making.",
                "MDI publications, policy briefs and knowledge products increase its public credibility.",
            ],
            "bi-clipboard-data", 1, parent=pilar2,
        )

        make_program(
            "pilar-2-3", "2.3 Aprendizajen no Excelénsia",
            {"id": "2.3 Pembelajaran dan Keunggulan", "pt": "2.3 Aprendizagem e Excelência", "en": "2.3 Learning and Excellence"},
            "Outcome 2.3 – Koñesimentu, Aprendizajen no Excelénsia Institusionál",
            {"id": "Outcome 2.3 – Pengetahuan, Pembelajaran, dan Keunggulan Kelembagaan",
             "pt": "Outcome 2.3 – Conhecimento, Aprendizagem e Excelência Institucional",
             "en": "Outcome 2.3 – Knowledge, Learning and Institutional Excellence"},
            "MDI hametin kultura aprendizajen, inovasaun no dezenvolvimentu lideransa hodi sai "
            "instituisaun koñesimentu ne'ebé adaptável, inovadora no ho excelénsia "
            "institusionál.",
            {"id": "MDI memperkuat budaya pembelajaran, inovasi, dan pengembangan kepemimpinan "
                   "untuk menjadi lembaga pengetahuan yang adaptif, inovatif, dan unggul.",
             "pt": "O MDI reforça uma cultura de aprendizagem, inovação e desenvolvimento de "
                   "liderança para se tornar uma instituição de conhecimento adaptável, "
                   "inovadora e de excelência institucional.",
             "en": "MDI strengthens a culture of learning, innovation and leadership development "
                   "to become an adaptable, innovative knowledge institution with institutional "
                   "excellence."},
            [
                "Programa fellowship, mentoria, estajiu no dezenvolvimentu kapasidade implementa ba staff no stakeholder sira.",
                "MDI iha mekanizmu aprendizajen organizasionál no partilha koñesimentu.",
                "Lideransa no kapasidade téknika staff aumenta liuhusi formasaun contínua.",
                "Teknolojia no inovasaun uza hodi aumenta efisiénsia programa no operasaun.",
                "MDI sai referénsia ba aprendizajen no inovasaun iha área governansa no dezenvolvimentu.",
            ],
            [
                "Fellowship, mentoring, internship and capacity development programs are implemented for staff and stakeholders.",
                "MDI has organizational learning and knowledge-sharing mechanisms.",
                "Staff leadership and technical capacity increase through continuous training.",
                "Technology and innovation are used to increase program and operational efficiency.",
                "MDI becomes a reference for learning and innovation in the governance and development field.",
            ],
            "bi-mortarboard", 2, parent=pilar2,
        )

        make_program(
            "pilar-2-4", "2.4 Boa Governasaun no E-Governance",
            {"id": "2.4 Tata Kelola Baik dan E-Governance", "pt": "2.4 Boa Governação e E-Governance", "en": "2.4 Good Governance and E-Governance"},
            "Outcome 2.4 – Boa Governasaun no E-Governance",
            {"id": "Outcome 2.4 – Tata Kelola Baik dan E-Governance",
             "pt": "Outcome 2.4 – Boa Governação e E-Governance",
             "en": "Outcome 2.4 – Good Governance and E-Governance"},
            "Instituisaun públika no partes interesadu sira hametin boa governasaun liuhusi "
            "transparénsia, akuntabilidade, inovasaun dijitál no asesu inkluzivu ba servisu "
            "públiku.",
            {"id": "Institusi publik dan pemangku kepentingan memperkuat tata kelola yang baik "
                   "melalui transparansi, akuntabilitas, inovasi digital, dan akses inklusif "
                   "terhadap layanan publik.",
             "pt": "As instituições públicas e as partes interessadas reforçam a boa governação "
                   "através da transparência, responsabilização, inovação digital e acesso "
                   "inclusivo aos serviços públicos.",
             "en": "Public institutions and stakeholders strengthen good governance through "
                   "transparency, accountability, digital innovation and inclusive access to "
                   "public services."},
            [
                "Peskiza no análiza kona-ba e-governance no transformasaun dijitál produz hodi informa polítika públika.",
                "Instituisaun públika aumenta kapasidade iha utilizasaun sistema dijitál no prestasaun servisu.",
                "Mekanizmu transparénsia, open data no akuntabilidade dijitál promove.",
                "Sidadaun, liuliu grupu vulnerável, aumenta asesu ba informasaun no servisu públiku.",
                "Diálogu polítika kona-ba boa governasaun no transformasaun dijitál organiza regularmente.",
            ],
            [
                "Research and analysis on e-governance and digital transformation is produced to inform public policy.",
                "Public institutions increase capacity in digital systems use and service delivery.",
                "Transparency, open data and digital accountability mechanisms are promoted.",
                "Citizens, particularly vulnerable groups, increase access to public information and services.",
                "Policy dialogue on good governance and digital transformation is regularly organized.",
            ],
            "bi-cpu", 3, parent=pilar2,
        )

        make_program(
            "pilar-3", "Pilar 3",
            {"id": "Pilar 3", "pt": "Pilar 3", "en": "Pillar 3"},
            "Outcome 3 – Pilar 3: Partisipasaun Komunitária, Reziliénsia Ekonómika no Mudansa Klimátika",
            {"id": "Outcome 3 – Pilar 3: Partisipasi Komunitas, Ketahanan Ekonomi, dan Perubahan Iklim",
             "pt": "Outcome 3 – Pilar 3: Participação Comunitária, Resiliência Económica e Alterações Climáticas",
             "en": "Outcome 3 – Pillar 3: Community Participation, Economic Resilience and Climate Change"},
            "Komunidade no grupu alvu sira aumenta kapasidade atu partisipa iha prosesu "
            "dezenvolvimentu, influensia desizaun no dezenvolve oportunidade sosial no "
            "ekonómika sustentável hodi reziliente ba mudansa klimatika.",
            {"id": "Komunitas dan kelompok sasaran meningkatkan kapasitas untuk berpartisipasi "
                   "dalam proses pembangunan, memengaruhi keputusan, dan mengembangkan peluang "
                   "sosial-ekonomi berkelanjutan yang tangguh terhadap perubahan iklim.",
             "pt": "As comunidades e os grupos-alvo aumentam a sua capacidade de participar no "
                   "processo de desenvolvimento, influenciar decisões e desenvolver "
                   "oportunidades socioeconómicas sustentáveis e resilientes às alterações "
                   "climáticas.",
             "en": "Communities and target groups increase their capacity to participate in the "
                   "development process, influence decisions and develop sustainable social and "
                   "economic opportunities that are resilient to climate change."},
            [
                "Feto, juventude, ema ho defisiénsia no grupu vulnerável sira aumenta partisipasaun iha prosesu dezenvolvimentu.",
                "Komunidade aumenta kapasidade kona-ba governasaun lokal, direitu sidadaun no partisipasaun públika.",
                "Inisiativa ekonomia komunitária, empreendedorizmu no livelihood sustentável dezenvolve.",
                "Komunidade aumenta asesu ba merkadu, oportunidade investimentu no rede ekonomia lokal.",
                "Modelu dezenvolvimentu bazeia ba komunidade promove iha nivel lokal.",
                "Komunidade aumenta koñesimentu no kapasidade kona-ba adaptasaun klimátika no konservasaun ambientál.",
                "Prátika agrikultura klimátika inteligente, agroekolojia no ekonomia verde promove.",
                "Ekosistema importante hanesan mangrove, floresta no biodiversidade hetan apoiu ba konservasaun no restaurasaun.",
                "Sistema alerta sedu no planu preparasaun emerjénsia dezenvolve iha nivel komunitáriu.",
                "Parseria ho Governu, sosiedade sivíl, setor privadu no parseiru internasionál hametin ba asaun klimátika.",
            ],
            [
                "Women, youth, persons with disabilities and vulnerable groups increase participation in the development process.",
                "Communities increase capacity in local governance, citizen rights and public participation.",
                "Community economic initiatives, entrepreneurship and sustainable livelihoods are developed.",
                "Communities increase access to markets, investment opportunities and local economic networks.",
                "Community-based development models are promoted at local level.",
                "Communities increase knowledge and capacity on climate adaptation and environmental conservation.",
                "Climate-smart agriculture, agroecology and green economy practices are promoted.",
                "Important ecosystems such as mangroves, forests and biodiversity receive support for conservation and restoration.",
                "Early warning systems and emergency preparedness plans are developed at community level.",
                "Partnerships with Government, civil society, the private sector and international partners are strengthened for climate action.",
            ],
            "bi-tree", 2,
        )

        # =====================================================================
        # ORGANIGRAMA (Hierárkiku) — dadus placeholder, user sei troka fali
        # =====================================================================
        OrgMember.objects.all().delete()
        top = OrgMember.objects.create(name="[Naran Diretor Ezekutivu]", position="Diretor Ezekutivu", level=0, order=0)
        directors = [
            ("[Naran Diretor Programa]", "Diretor Programa"),
            ("[Naran Diretor Administrasaun no Finansas]", "Diretor Administrasaun no Finansas"),
            ("[Naran Diretor Peskiza no Advokasia]", "Diretor Peskiza no Advokasia"),
        ]
        director_objs = []
        for i, (name, pos) in enumerate(directors):
            d = OrgMember.objects.create(name=name, position=pos, parent=top, level=1, order=i)
            director_objs.append(d)

        coordinators = [
            ("[Naran Koordenador Pilar 1]", "Koordenador Pilar 1 - Jestaun Institusionál"),
            ("[Naran Koordenador Pilar 2]", "Koordenador Pilar 2 - Think Tank ASEAN (SIS)"),
            ("[Naran Koordenador Pilar 3]", "Koordenador Pilar 3 - Komunidade no Klima"),
            ("[Naran Ofisial Monitorizasaun]", "Ofisial Monitorizasaun, Avaliasaun & Aprendizajen"),
        ]
        for i, (name, pos) in enumerate(coordinators):
            OrgMember.objects.create(name=name, position=pos, parent=director_objs[0], level=2, order=i)

        # ---------- Slides ----------
        slides_data = [
            ("Institute For Monitoring, Advocacy and Community Strengthening",
             "Advancing Good Governance", "MDI works with communities in Timor-Leste.", "website/slides/slide1.svg", 0,
             {"id": "Lembaga Pemantauan, Advokasi dan Penguatan Komunitas",
              "pt": "Instituto de Monitorização, Advocacia e Fortalecimento Comunitário",
              "en": "Institute for Monitoring, Advocacy and Community Strengthening"},
             {"id": "Mendorong Tata Kelola yang Baik", "pt": "Promovendo a Boa Governação",
              "en": "Advancing Good Governance"},
             {"id": "MDI bekerja bersama masyarakat di Timor-Leste.",
              "pt": "O MDI trabalha com as comunidades em Timor-Leste.",
              "en": "MDI works with communities in Timor-Leste."}),
            ("Since the year 2005", "Strengthening Community Voice",
             "From participatory research to social audits.", "website/slides/slide2.svg", 1,
             {"id": "Sejak tahun 2005", "pt": "Desde o ano 2005", "en": "Since the year 2005"},
             {"id": "Menguatkan Suara Komunitas", "pt": "Fortalecendo a Voz da Comunidade",
              "en": "Strengthening Community Voice"},
             {"id": "Dari riset partisipatif hingga audit sosial.",
              "pt": "Da pesquisa participativa à auditoria social.",
              "en": "From participatory research to social audits."}),
            ("Social Audit & Mapping", "Reliable Data for Government Decisions",
             "We collect, analyse and share information.", "website/slides/slide3.svg", 2,
             {"id": "Audit Sosial & Pemetaan", "pt": "Auditoria Social e Mapeamento",
              "en": "Social Audit & Mapping"},
             {"id": "Data Andal untuk Keputusan Pemerintah", "pt": "Dados Fiáveis para Decisões Governamentais",
              "en": "Reliable Data for Government Decisions"},
             {"id": "Kami mengumpulkan, menganalisis, dan membagikan informasi.",
              "pt": "Recolhemos, analisamos e partilhamos informação.",
              "en": "We collect, analyse and share information."}),
        ]
        Slide.objects.all().delete()
        for kicker, title, text, img, order, kicker_i18n, title_i18n, text_i18n in slides_data:
            s = Slide(kicker=kicker, title=title, text=text, order=order, is_active=True,
                      kicker_i18n=kicker_i18n, title_i18n=title_i18n, text_i18n=text_i18n)
            s.image.name = img
            s.save()

        # ---------- Activities ----------
        activities_data = [
            ("Auditoria Sosial", "Auditoria Sosial Programa PNDS",
             "Monitorizasaun independente ba implementasaun projetu PNDS - Uma Kbi'it Laek "
             "iha suku sira.", "website/activities/activity1.svg"),
            ("Mapamentu", "Mapamentu Partisipativu Rai",
             "Peskiza jestaun uzu rai hamutuk ho lideransa komunitaria atu identifika "
             "informasaun espasial suku.", "website/activities/activity2.svg"),
            ("Advokasia", "Advokasia Programa TAPSA",
             "Suporta komunidade Lissadila no Guico atu hametin soberania ai-han no "
             "reziliensia klimatika.", "website/activities/activity3.svg"),
            ("Auditoria Finansa", "Auditoria Eksterna Finansa MDI",
             "Prosesu auditoria finansa anual atu garante transparensia no kontabilidade "
             "internu organizasaun.", "website/activities/activity4.svg"),
            ("Dialogu Politika", "Audiensia ho Entidade Estadu",
             "Fasilita dialogu entre lideransa komunitaria no autoridade governu konaba "
             "problema infrastrutura lokal.", "website/activities/activity5.svg"),
        ]
        Activity.objects.all().delete()
        for i, (tag, title, desc, img) in enumerate(activities_data):
            a = Activity(tag=tag, title=title, description=desc, order=i, is_published=True)
            a.image.name = img
            a.save()

        # ---------- News ----------
        news_data = [
            ("Relatoriu Auditoria Sosial PNDS - UKL Publika Ona",
             "MDI publika relatoriu final auditoria sosial konaba implementasaun projetu "
             "PNDS Uma Kbi'it Laek, hosi dezenu metodolojia to'o validasaun iha suku.",
             datetime.date(2022, 2, 22), "Dili", "pilar-2-2", "Suku Bebonuk, Postu Dom Aleixo"),
            ("Istoria Advokasia TAPSA iha Lissadila no Guico",
             "Dezde 2018, MDI hamutuk ho lideransa komunitaria halo advokasia konaba "
             "impaktu inundasaun no errozaun mota Loes.", datetime.date(2021, 10, 14),
             "Covalima", "pilar-3", "Suku Lissadila no Guiço"),
            ("Relatoriu Auditoria Finansa Eksterna 2015",
             "Dokumentu auditoria finansa eksterna ba situasaun finansa MDI ba tinan "
             "fiskal 2015 agora asesivel ba publiku.", datetime.date(2021, 7, 7), None, "pilar-1", ""),
            ("Sorumutu ho DGDR no DN-ST.PNDS",
             "Ekipa MDI no Gabineti UAS halo audiensia hodi konfirma rezultadu preliminar "
             "auditoria sosial mekanismu UKL.", datetime.date(2021, 6, 1), "Dili", "pilar-2-2", ""),
            ("Aprezentasaun Rezultadu PDIM ba ADN",
             "MDI hamutuk ho UAS aprezenta rezultadu akompañamentu implementasaun "
             "infrastrutura liu husi programa PDIM.", datetime.date(2020, 11, 5), "Dili", "pilar-2-4", ""),
        ]
        for title, excerpt, pub_date, muni_name, prog_slug, loc_detail in news_data:
            slug = slugify(title)[:60]
            muni_obj = Municipality.objects.filter(name=muni_name).first() if muni_name else None
            prog_obj = Program.objects.filter(slug=prog_slug).first() if prog_slug else None
            NewsPost.objects.update_or_create(
                slug=slug,
                defaults={"title": title, "excerpt": excerpt, "body": excerpt,
                          "published_date": pub_date, "is_published": True,
                          "municipality": muni_obj, "related_program": prog_obj,
                          "location_detail": loc_detail}
            )

        # ---------- Demo galeri foto (multi-foto) untuk berita pertama ----------
        first_news = NewsPost.objects.filter(slug=slugify(news_data[0][0])[:60]).first()
        if first_news:
            NewsImage.objects.filter(news=first_news).delete()
            gallery_photos = [
                ("website/activities/activity1.svg", "Fiskalizasaun iha fatin projetu"),
                ("website/activities/activity2.svg", "Diskusaun ho lideransa suku"),
                ("website/activities/activity3.svg", "Validasaun dadus hamutuk komunidade"),
                ("website/activities/activity4.svg", "Sesaun aprezentasaun rezultadu"),
            ]
            for i, (img_path, caption) in enumerate(gallery_photos):
                gi = NewsImage(news=first_news, caption=caption, order=i)
                gi.image.name = img_path
                gi.save()

        # ---------- Staff / Authors + Articles ----------
        staff_data = [
            ("aderito.ximenes", "Aderito Ximenes", "Peskizador Senior", "staff1.svg",
             "Governasaun Lokal no Dezafiu Implementasaun UKL",
             "Analize kona-ba desafiu tekniku no politiku ne'ebe infrenta durante "
             "implementasaun mekanismu UKL iha suku.", datetime.date(2022, 3, 1), "article_cover1.svg"),
            ("maria.guterres", "Maria Guterres", "Ofisial Advokasia", "staff2.svg",
             "Importansia Mapa Partisipativa ba Planeamentu Suku",
             "Oinsa mapa partisipativu bele ajuda lideransa suku atu halo planu asaun "
             "mitigasaun risku klimatika.", datetime.date(2022, 1, 15), "article_cover2.svg"),
            ("joao.belo", "João Belo", "Koordenador Programa", "staff3.svg",
             "Litaun Auditoria Sosial nian ba Kualidade Infrastrutura",
             "Reflesaun konaba resultadu auditoria sosial no ninia kontribuisaun ba "
             "kualidade konstrusaun publiku.", datetime.date(2021, 12, 10), "article_cover3.svg"),
            ("fatima.soares", "Fatima Soares", "Ofisial Komunikasaun", "staff4.svg",
             "Fahe Informasaun ba Komunidade liu husi Radiu Komunidade",
             "Estrategia komunikasaun MDI atu hato'o rezultadu peskiza ba komunidade "
             "rural iha forma simples.", datetime.date(2021, 9, 20), "article_cover4.svg"),
            ("domingos.amaral", "Domingos Amaral", "Peskizador Junior", "staff5.svg",
             "Notas Kampu: Peskiza Jestaun Rai iha Lisadila",
             "Seriu notas kampu kona-ba metodolojia koleta dadus espasial durante "
             "peskiza jestaun uzu rai.", datetime.date(2021, 8, 5), "article_cover5.svg"),
        ]
        for username, fullname, position, photo, art_title, art_excerpt, art_date, cover in staff_data:
            first, *rest = fullname.split(" ")
            last = " ".join(rest)
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first, "last_name": last, "email": f"{username}@mditl.org"}
            )
            if created:
                user.set_password("mdi12345")
                user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.position = position
            profile.photo.name = f"website/team/{photo}"
            profile.save()
            staff_group = Group.objects.get(name=GROUP_STAFF)
            user.groups.add(staff_group)

            slug = slugify(art_title)[:60]
            article_obj, _ = Article.objects.update_or_create(
                slug=slug,
                defaults={"title": art_title, "excerpt": art_excerpt, "body": art_excerpt,
                          "author": user, "published_date": art_date, "is_published": True}
            )
            article_obj.cover_image.name = f"website/articles/{cover}"
            article_obj.save()

        # ---------- Founders (fundador asli MDI) — agora hatudu iha pájina Profile ----------
        Founder.objects.all().delete()
        founders_data = [
            ("Sr. Justino Soares", "Actual Country Director WaterAid", "justino_soares.png"),
            ("Sr. Estevanus Coli", "Actual Director MDI", "estevanus_coli.png"),
            ("Sr. Valente Lelo Bau", "Prezidente Koperativa FUNAMOR", "valente_lelo_bau.png"),
            ("Sr. Helio Dias da Silva", "Actual Prezidente MOKATIL", "helio_dias_da_silva.png"),
            ("Sr. Jorzinha Bainco", "Actual Coord. Finance & Administration MDI", "jorzinha_bainco.png"),
        ]
        for i, (name, position, photo) in enumerate(founders_data):
            f = Founder(name=name, position=position, order=i)
            f.photo.name = f"website/founders/{photo}"
            f.save()

        # ---------- Partners / Donors ----------
        Partner.objects.all().delete()
        partners = [
            ("Oxfam Timor-Leste", "partner"), ("CARE International", "partner"),
            ("Rede Ba Rai", "partner"), ("TRAIN Network", "partner"),
        ]
        donors = [
            ("European Union", "donor"), ("CCFD - Terre Solidaire", "donor"),
            ("Agence Française de Développement", "donor"), ("Office of the Prime Minister - UAS", "donor"),
        ]
        for i, (name, ptype) in enumerate(partners + donors):
            Partner.objects.create(name=name, type=ptype, order=i)

        # ---------- Superuser dashboard ----------
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser("admin", "admin@mditl.org", "admin12345")
            Profile.objects.filter(user=admin_user).update(position="Administrador Sistema")
            admin_group = Group.objects.get(name=GROUP_ADMIN)
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.WARNING(
                "Superuser 'admin' kriadu ho password 'admin12345' - troka lalais bainhira produsaun!"
            ))

        self.stdout.write(self.style.SUCCESS("Seed data MDI kompletu!"))
