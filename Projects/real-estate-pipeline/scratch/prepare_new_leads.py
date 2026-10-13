import json
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

NEW_15_LEADS = [
    {
        "date_posted": "2026-09-05 (Just now / 4m ago)",
        "company_name": "Mr.Boost Agency Limited",
        "role_needed": "Lead Generation Specialist",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/lead-generation-specialist-at-mr-boost-agency-limited-4461805258",
        "city_state": "London (Remote)",
        "country": "United Kingdom",
        "company_size": "10–25 employees",
        "email_contact": "hello@mrboostagency.co.uk",
        "deal_value": "£7,500 – £15,000 retainer",
        "remarks": "Posted 4m ago. Boutique digital growth agency seeking dedicated lead generation specialist to run targeted B2B outbound prospecting."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "Spencer Hsu Real Estate Team",
        "role_needed": "Inside Sales Agent (ISA) – High-Volume Real Estate Team",
        "linkedin_url": "https://www.linkedin.com/jobs/view/inside-sales-agent-isa-%E2%80%93-high-volume-real-estate-team-bay-area-at-spencer-hsu-real-estate-team-4387771948",
        "city_state": "San Jose, CA",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "spencer@spencerhsu.com",
        "deal_value": "$15,000 – $45,000+ commission/deal",
        "remarks": "Posted 1d ago. High-volume Bay Area Silicon Valley real estate team hiring ISA & appointment setter to prospect and qualify high-ticket property buyers & sellers."
    },
    {
        "date_posted": "2026-09-05 (18 hours ago)",
        "company_name": "LaunchTec",
        "role_needed": "Business Development Representative / Lead Generation",
        "linkedin_url": "https://www.linkedin.com/jobs/view/business-development-representative-at-launchtec-4461402567",
        "city_state": "Denver, CO",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "careers@launchtec.io",
        "deal_value": "$7,500 – $18,000 client retainer",
        "remarks": "Posted 18h ago. Boutique advertising & growth firm hiring 1099 contractor for targeted outbound lead generation and booking qualified meetings."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "BizDevMastermind",
        "role_needed": "Business Development Representative (1099 / Commission)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/business-development-representative-at-bizdevmastermind-4461181592",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "contact@bizdevmastermind.com",
        "deal_value": "$10,000 – $30,000 contract value",
        "remarks": "Posted 1d ago. Advisory firm hiring 1099 sales contractor to prospect and book discovery calls with property management and commercial real estate clients."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "Lumian",
        "role_needed": "Business Development Representative (1099 Contractor)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/business-development-representative-at-lumian-4461922089",
        "city_state": "Indiana (Remote)",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "growth@lumian.io",
        "deal_value": "$8,000 – $25,000 consulting contracts",
        "remarks": "Posted 1d ago. Tech consulting group hiring 1099 outbound contractor to identify, prospect, and book sales calls with qualified businesses."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "Golden Horisont Ltd",
        "role_needed": "Lead Generation Specialist (Remote, Commission-Based)",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/lead-generation-specialist-at-golden-horisont-ltd-4461148639",
        "city_state": "London (Remote)",
        "country": "United Kingdom",
        "company_size": "10–30 employees",
        "email_contact": "info@goldenhorisont.com",
        "deal_value": "£8,000 – £22,000 corporate retainers",
        "remarks": "Posted 1d ago. Turnkey corporate consulting firm hiring lead gen specialist to source, qualify, and engage B2B corporate clients across 25+ jurisdictions."
    },
    {
        "date_posted": "2026-09-05 (8 hours ago)",
        "company_name": "Milsec",
        "role_needed": "Business Representative / Commercial Lead Gen",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/business-representative-at-milsec-4463714943",
        "city_state": "Doncaster, England",
        "country": "United Kingdom",
        "company_size": "10–25 employees",
        "email_contact": "enquiries@milsec.co.uk",
        "deal_value": "£8,000 – £16,000 per project",
        "remarks": "Posted 8h ago. Commercial property & security services firm hiring outbound sales representative to prospect commercial clients and secure contracts."
    },
    {
        "date_posted": "2026-09-05 (12 hours ago)",
        "company_name": "Park Hill Portraits",
        "role_needed": "Remote Appointment Setter (Full-Time)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/remote-appointment-setter-full-time-portrait-studio-at-park-hill-portraits-4461447163",
        "city_state": "Dallas, TX (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "studio@parkhillportraits.com",
        "deal_value": "$7,000 – $15,000 luxury packages",
        "remarks": "Posted 12h ago. Luxury portraiture and art studio hiring remote appointment setter to manage outbound prospect lists and schedule high-ticket bookings."
    },
    {
        "date_posted": "2026-09-05 (16 hours ago)",
        "company_name": "DualEntry",
        "role_needed": "Business Development Representative / Outbound SDR",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/business-development-representative-at-dualentry-4463650043",
        "city_state": "London (Remote)",
        "country": "United Kingdom",
        "company_size": "10–25 employees",
        "email_contact": "founders@dualentry.com",
        "deal_value": "£12,000+ ACV",
        "remarks": "Posted 16h ago. Growing fintech platform seeking outbound SDR to prospect financial directors and schedule qualified demo appointments."
    },
    {
        "date_posted": "2026-09-05 (17 hours ago)",
        "company_name": "#twiceasnice Recruiting",
        "role_needed": "Business Development Rep, B2B Sales & Marketing Services",
        "linkedin_url": "https://www.linkedin.com/jobs/view/business-development-rep-b2b-sales-marketing-services-at-%23twiceasnice-recruiting-4462338368",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "15–30 employees",
        "email_contact": "sales@twiceasnicerecruiting.com",
        "deal_value": "$10,000 – $35,000 search placements",
        "remarks": "Posted 17h ago. Boutique specialized search consultancy seeking outbound BDR to prospect corporate hiring executives and book discovery calls."
    },
    {
        "date_posted": "2026-09-05 (12 hours ago)",
        "company_name": "Hawk 3 Talent Solutions",
        "role_needed": "Business Development Advisor / Lead Generator",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/business-development-advisor-at-hawk-3-talent-solutions-4461436852",
        "city_state": "North Frodingham, England",
        "country": "United Kingdom",
        "company_size": "15–30 employees",
        "email_contact": "info@hawk3talent.co.uk",
        "deal_value": "£7,500 – £18,000 retainers",
        "remarks": "Posted 12h ago. Specialist talent consulting firm seeking business development advisor to identify new client opportunities and book corporate meetings."
    },
    {
        "date_posted": "2026-09-05 (21 hours ago)",
        "company_name": "Radius",
        "role_needed": "Appointment Setter / Outbound Sales Specialist",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/appointment-setter-at-radius-4463627171",
        "city_state": "Belfast (Remote)",
        "country": "United Kingdom",
        "company_size": "15–30 employees",
        "email_contact": "contact@radiusglobal.co.uk",
        "deal_value": "£7,000 – £14,000 contract value",
        "remarks": "Posted 21h ago. Solutions provider looking for dedicated appointment setter to conduct targeted cold outbound and schedule discovery calls."
    },
    {
        "date_posted": "2026-09-05 (21 hours ago)",
        "company_name": "RingByName",
        "role_needed": "Sales Development Representative / Outbound Lead Gen",
        "linkedin_url": "https://www.linkedin.com/jobs/view/sales-development-representative-at-ringbyname-4463619657",
        "city_state": "Miami, FL (Remote)",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "sales@ringbyname.com",
        "deal_value": "$8,000 – $20,000 client packages",
        "remarks": "Posted 21h ago. Business communications firm seeking SDR to generate qualified leads and set demo meetings with mid-sized business owners."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "CV-BRIDGE LTD",
        "role_needed": "Sales Development Representative (SDR) – Remote",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/sales-development-representative-sdr-%E2%80%93-remote-at-cv-bridge-ltd-4461120654",
        "city_state": "London (Remote)",
        "country": "United Kingdom",
        "company_size": "10–20 employees",
        "email_contact": "partnerships@cv-bridge.com",
        "deal_value": "£8,000 – £15,000 contracts",
        "remarks": "Posted 1d ago. Boutique advisory firm seeking remote SDR for cold outreach, prospective account identification, and booking discovery meetings."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "A Quality Facility Services",
        "role_needed": "Commercial Lead Generation Specialist / Telemarketer",
        "linkedin_url": "https://www.linkedin.com/jobs/view/telemarketer-at-a-quality-facility-services-4463311396",
        "city_state": "Cleveland, OH",
        "country": "United States",
        "company_size": "15–30 employees",
        "email_contact": "info@aqualityfacility.com",
        "deal_value": "$10,000 – $50,000 commercial contracts",
        "remarks": "Posted 1d ago. Commercial facility services provider seeking B2B outbound lead generator to prospect facility directors & commercial property managers."
    }
]

# Generate TSV for clipboard / subagent pasting
tsv_rows = []
for lead in NEW_15_LEADS:
    row = [
        lead["date_posted"],
        lead["company_name"],
        lead["role_needed"],
        lead["linkedin_url"],
        lead["city_state"],
        lead["country"],
        lead["company_size"],
        lead["email_contact"],
        lead["deal_value"],
        lead["remarks"]
    ]
    tsv_rows.append("\t".join(row))

tsv_content = "\n".join(tsv_rows)
with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\new_15_leads.tsv', 'w', encoding='utf-8') as f:
    f.write(tsv_content)

print(f"Generated TSV for {len(NEW_15_LEADS)} new leads.")
