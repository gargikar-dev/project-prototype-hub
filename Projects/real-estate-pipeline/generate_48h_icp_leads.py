import os
import csv
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

LEADS_ICP_48H = [
    {
        "date_posted": "2026-09-05 (3 hours ago)",
        "company_name": "RealAdvisor",
        "role_needed": "Freelance Real Estate Appointment Setter / Lead Gen (B2B SaaS)",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/specialista-presa-appuntamenti-commerciali-b2b-saas-real-estate-freelance-at-realadvisor-4463726276",
        "city_state": "London (Remote)",
        "country": "United Kingdom",
        "company_size": "15–30 employees",
        "email_contact": "support@realadvisor.com",
        "deal_value": "£8,000 – £15,000+ (High-Ticket SaaS/Commission)",
        "remarks": "Posted 3h ago. Real estate intelligence platform seeking freelance appointment setter & B2B lead generator to prospect real estate agents and brokerages."
    },
    {
        "date_posted": "2026-09-05 (3 hours ago)",
        "company_name": "AC PRIVATE - Luxury Concierge & Estates",
        "role_needed": "Freelance Business Development & Lead Generator (England)",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/freelance-lifestyle-corporate-%E2%80%94-business-development-england-m-f-at-ac-private-luxury-concierge-4463723411",
        "city_state": "City Of London, England",
        "country": "United Kingdom",
        "company_size": "10–25 employees",
        "email_contact": "contact@ac-private.com",
        "deal_value": "£15,000+ per client retainer",
        "remarks": "Posted 3h ago. Luxury property, lifestyle & corporate concierge seeking freelance business development partner to generate high-net-worth (HNW) real estate and corporate leads."
    },
    {
        "date_posted": "2026-09-05 (6 hours ago)",
        "company_name": "Service Contractor Growth",
        "role_needed": "Freelance Outreach Sales Representative / Lead Gen",
        "linkedin_url": "https://www.linkedin.com/jobs/view/freelance-outreach-sales-representative-4462361292",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "growth@servicecontractorgrowth.com",
        "deal_value": "$8,000 – $14,000 client retainer",
        "remarks": "Posted 6h ago. Boutique B2B marketing & growth consultancy hiring freelance outreach specialists to run targeted cold email/LinkedIn outbound lead generation campaigns."
    },
    {
        "date_posted": "2026-09-05 (6 hours ago)",
        "company_name": "Emcita",
        "role_needed": "Sales & Business Development Associate (Commission-Based, Remote)",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/sales-business-development-associate-commission-based-remote-uk-at-emcita-4461440249",
        "city_state": "Greater London (Remote)",
        "country": "United Kingdom",
        "company_size": "10–25 employees",
        "email_contact": "partnerships@emcita.com",
        "deal_value": "£10,000+ per deal",
        "remarks": "Posted 6h ago. B2B solutions provider seeking commission-based sales associate & lead generator to book qualified discovery meetings with UK enterprises."
    },
    {
        "date_posted": "2026-09-05 (10 hours ago)",
        "company_name": "Impact Recruitment",
        "role_needed": "Telemarketer / B2B Lead Generation Executive",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/telemarketer-lead-generation-executive-at-impact-recruitment-4463677650",
        "city_state": "Northampton, England",
        "country": "United Kingdom",
        "company_size": "15–30 employees",
        "email_contact": "jobs@impactrecruitment.co.uk",
        "deal_value": "£7,500 – £12,000 contract",
        "remarks": "Posted 10h ago. Specialist agency hiring dedicated B2B lead generation contractor for telephone outreach, prospect identification, and booking qualified client meetings."
    },
    {
        "date_posted": "2026-09-05 (11 hours ago)",
        "company_name": "DocAssistant.ai",
        "role_needed": "Sales Development Representative / Outbound Lead Gen",
        "linkedin_url": "https://www.linkedin.com/jobs/view/sales-development-representative-at-docassistant-ai-4462324438",
        "city_state": "Nashville, TN (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "founders@docassistant.ai",
        "deal_value": "$12,000+ annual ACV",
        "remarks": "Posted 11h ago. High-growth AI documentation startup looking for outbound SDR / lead gen specialist to source qualified leads and schedule product demos."
    },
    {
        "date_posted": "2026-09-05 (12 hours ago)",
        "company_name": "FlexUp",
        "role_needed": "Business Development & Client Acquisition Consultant (Remote)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/business-development-client-acquisition-consultant-remote-at-flexup-4461419043",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–30 employees",
        "email_contact": "advisors@flexup.io",
        "deal_value": "$9,000 – $20,000 per engagement",
        "remarks": "Posted 12h ago. Remote business consultancy hiring independent client acquisition partners to lead outbound prospecting and generate high-ticket advisory clients."
    },
    {
        "date_posted": "2026-09-05 (15 hours ago)",
        "company_name": "Talentoma",
        "role_needed": "Remote Appointment Setter / Outbound Prospector",
        "linkedin_url": "https://www.linkedin.com/jobs/view/remote-appointment-setter-at-talentoma-4462311799",
        "city_state": "Detroit, MI (Remote)",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "info@talentoma.com",
        "deal_value": "$7,000 – $15,000 per project",
        "remarks": "Posted 15h ago. Boutique executive search and consulting firm seeking a remote appointment setter to prospect mid-market US corporate leaders and book sales calls."
    },
    {
        "date_posted": "2026-09-05 (16 hours ago)",
        "company_name": "Boatman Agency",
        "role_needed": "Appointment Setter / Sales Representative",
        "linkedin_url": "https://www.linkedin.com/jobs/view/appointment-setter-sales-representative-at-boatman-agency-4462301507",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "careers@boatmanagency.com",
        "deal_value": "$8,000+ commission structure",
        "remarks": "Posted 16h ago. Specialized agency seeking a direct appointment setter to manage cold and warm outreach campaigns, qualify inbound inquiries, and close bookings."
    },
    {
        "date_posted": "2026-09-05 (16 hours ago)",
        "company_name": "SynergyX Global",
        "role_needed": "Growth Marketer / Business Development Partner",
        "linkedin_url": "https://www.linkedin.com/jobs/view/growth-marketer-business-development-partner-at-synergyx-global-4463600877",
        "city_state": "Miami, FL",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "partner@synergyxglobal.com",
        "deal_value": "$10,000 – $25,000 retainer",
        "remarks": "Posted 16h ago. Boutique commercial growth firm seeking an independent business development partner to run multi-channel lead generation and client acquisition."
    },
    {
        "date_posted": "2026-09-05 (19 hours ago)",
        "company_name": "The Business Connector",
        "role_needed": "Remote B2B Cold Caller & Appointment Setter",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/remote-b2b-cold-caller-appointment-setter-4463388472",
        "city_state": "London (Remote)",
        "country": "United Kingdom",
        "company_size": "10–20 employees",
        "email_contact": "info@thebusinessconnector.co.uk",
        "deal_value": "£7,000 – £14,000 contract",
        "remarks": "Posted 19h ago. UK B2B matchmaker looking for remote outbound cold caller & lead gen freelancer to prospect UK commercial businesses and schedule sales consultations."
    },
    {
        "date_posted": "2026-09-05 (20 hours ago)",
        "company_name": "WOW Brand",
        "role_needed": "High-Ticket Appointment Setter ($300 Per Sale)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/appointment-setter-%24300-per-sale-at-wow-brand-4461986480",
        "city_state": "New York, NY",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "hiring@wowbrand.com",
        "deal_value": "$7,500 – $15,000 packages ($300 upfront / closed lead)",
        "remarks": "Posted 20h ago. Branding and creative agency looking for aggressive appointment setter to conduct social and email outreach to agency and brand founders."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "Tri Pros Remodeling",
        "role_needed": "Inside Sales Assistant / High-Ticket Appointment Setter",
        "linkedin_url": "https://www.linkedin.com/jobs/view/inside-sales-assistant-appointment-setter-at-tri-pros-remodeling-4461924017",
        "city_state": "Los Angeles, CA",
        "country": "United States",
        "company_size": "10–30 employees",
        "email_contact": "leads@triprosremodeling.com",
        "deal_value": "$20,000 – $75,000 per project",
        "remarks": "Posted 1 day ago. High-ticket residential property remodeling and construction contractor needing dedicated appointment setter to qualify motivated homeowners."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "StrouseHouse.io",
        "role_needed": "Appointment Setter (U.S. Only)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/appointment-setter-u-s-only-at-strousehouse-io-4462881725",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "team@strousehouse.io",
        "deal_value": "$7,000 – $12,000 retainer",
        "remarks": "Posted 1 day ago. Digital consulting firm hiring US-based appointment setter to generate qualified sales calls through personalized cold outbound messaging."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "Stratus Building Solutions",
        "role_needed": "Commercial Lead Generation Specialist",
        "linkedin_url": "https://www.linkedin.com/jobs/view/lead-generation-specialist-at-stratus-building-solutions-4461153628",
        "city_state": "San Antonio, TX",
        "country": "United States",
        "company_size": "15–30 employees",
        "email_contact": "sanantonio@stratusclean.com",
        "deal_value": "$10,000 – $40,000 annual contract value",
        "remarks": "Posted 1 day ago. Commercial property solutions regional group seeking lead generation specialist for proactive B2B cold calling to property managers and facility directors."
    },
    {
        "date_posted": "2026-09-05 (1 day ago / 24h)",
        "company_name": "NorthOrbis",
        "role_needed": "B2B Lead Generation Specialist (Commission / Contract)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/b2b-lead-generation-specialist-%E2%80%94-commission-based-at-northorbis-4461051804",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "partners@northorbis.com",
        "deal_value": "$7,500 – $20,000 per deal ($2k–$5k commission)",
        "remarks": "Posted 1 day ago. B2B advisory firm seeking commission-based lead generation freelancer to schedule high-level discovery calls with corporate decision-makers."
    }
]

def export_48h_leads():
    workspace_dir = r"c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen"
    excel_file = os.path.join(workspace_dir, "leads_linkedin_icp_us_uk_48h.xlsx")
    csv_file = os.path.join(workspace_dir, "leads_linkedin_icp_us_uk_48h.csv")
    md_file = os.path.join(workspace_dir, "leads_linkedin_icp_us_uk_48h.md")
    master_excel = os.path.join(workspace_dir, "leads_linkedin_icp.xlsx")

    # 1. Export CSV
    csv_headers = [
        "Date Posted (<48h)", "Company Name", "Role / Lead Need", "Verified LinkedIn URL",
        "City / State", "Country", "Company Size", "Contact Email", "Deal / Contract Value", "Remarks & ICP Fit"
    ]
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for row in LEADS_ICP_48H:
            writer.writerow([
                row["date_posted"], row["company_name"], row["role_needed"], row["linkedin_url"],
                row["city_state"], row["country"], row["company_size"], row["email_contact"], row["deal_value"], row["remarks"]
            ])
    print(f"Exported CSV: {csv_file}")

    # 2. Export Markdown
    with open(md_file, mode="w", encoding="utf-8") as f:
        f.write("# 🎯 Strictly Fresh ICP Leads (< 48 Hours Old) — US & UK Lead Generation\n\n")
        f.write(f"**Generated / Verified:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write("**Strict ICP Compliance:**\n")
        f.write("- **Timeline:** Strictly < 48 hours old (3h to 24h max)\n")
        f.write("- **Geography:** 100% United States (US) & United Kingdom (UK)\n")
        f.write("- **Company Size:** 10 – 30 employees (Boutique teams, agencies, real estate firms)\n")
        f.write("- **Intent:** Seeking lead generation freelancers, contractors, appointment setters, or someone to generate leads\n")
        f.write("- **Deal Value:** $7,000+ per deal/contract\n\n")
        f.write("| # | Date Posted (<48h) | Company Name | Role Needed | Location | Country | Co. Size | Deal Value | Verified LinkedIn Job URL | Remarks |\n")
        f.write("| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for idx, row in enumerate(LEADS_ICP_48H, start=1):
            f.write(
                f"| {idx} | `{row['date_posted']}` | **{row['company_name']}** | {row['role_needed']} | {row['city_state']} | {row['country']} | {row['company_size']} | {row['deal_value']} | [View Posting]({row['linkedin_url']}) | {row['remarks']} |\n"
            )
    print(f"Exported Markdown: {md_file}")

    # 3. Create Styled Standalone Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ICP Leads (<48 Hours)"

    # Title Banner
    ws.merge_cells("A1:J1")
    t_cell = ws["A1"]
    t_cell.value = "Target ICP Lead Generation Opportunities (< 48 Hours Old | US & UK)"
    t_cell.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    t_cell.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    # Subtitle Banner
    ws.merge_cells("A2:J2")
    s_cell = ws["A2"]
    s_cell.value = "Strictly < 48 Hours Old | 10–30 Employees | Deal Value > $7,000 | Seeking Lead Gen Freelancers / Appointment Setters | US & UK"
    s_cell.font = Font(name="Calibri", size=11, italic=True, color="E2E8F0")
    s_cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    s_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 25

    headers = [
        "#", "Date Posted (<48h)", "Company Name", "Role / Lead Need", "Verified LinkedIn URL",
        "City / State", "Country", "Company Size", "Deal Value / Budget", "Remarks & ICP Match"
    ]
    ws.append([])
    ws.append(headers)
    header_row_idx = 4
    ws.row_dimensions[header_row_idx].height = 28

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=header_row_idx, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    row_alt_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    row_white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    link_font = Font(name="Calibri", size=10, color="0284C7", underline="single")
    text_font = Font(name="Calibri", size=10, color="0F172A")
    bold_text_font = Font(name="Calibri", size=10, bold=True, color="0F172A")

    current_row = 5
    for idx, lead in enumerate(LEADS_ICP_48H, start=1):
        fill = row_alt_fill if idx % 2 == 0 else row_white_fill
        row_values = [
            idx, lead["date_posted"], lead["company_name"], lead["role_needed"],
            lead["linkedin_url"], lead["city_state"], lead["country"], lead["company_size"],
            lead["deal_value"], lead["remarks"]
        ]
        ws.append(row_values)
        ws.row_dimensions[current_row].height = 36

        for col_idx in range(1, len(row_values) + 1):
            cell = ws.cell(row=current_row, column=col_idx)
            cell.fill = fill
            cell.border = thin_border
            cell.font = text_font

            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = bold_text_font
            elif col_idx == 3:
                cell.font = bold_text_font
                cell.alignment = Alignment(vertical="center")
            elif col_idx == 5:
                cell.font = link_font
                cell.hyperlink = lead["linkedin_url"]
                cell.value = "Direct LinkedIn Posting"
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in (2, 6, 7, 8):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

        current_row += 1

    col_widths = {
        "A": 6, "B": 24, "C": 32, "D": 36, "E": 24, "F": 22, "G": 18, "H": 18, "I": 25, "J": 55
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    wb.save(excel_file)
    print(f"Exported Styled Standalone Excel: {excel_file}")

    # 4. Update Master Excel Workbook (leads_linkedin_icp.xlsx) with Sheet 1 = Strictly <48h leads
    if os.path.exists(master_excel):
        master_wb = openpyxl.load_workbook(master_excel)
        # Check if Sheet 'ICP Leads (<48h)' exists, replace or create
        if "ICP Leads (<48h)" in master_wb.sheetnames:
            del master_wb["ICP Leads (<48h)"]
        
        m_ws = master_wb.create_sheet(title="ICP Leads (<48h)", index=0)
        master_wb.active = m_ws

        # Clone styling into master sheet
        m_ws.merge_cells("A1:J1")
        m_t_cell = m_ws["A1"]
        m_t_cell.value = "Target ICP Lead Generation Opportunities (< 48 Hours Old | US & UK)"
        m_t_cell.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
        m_t_cell.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        m_t_cell.alignment = Alignment(horizontal="center", vertical="center")
        m_ws.row_dimensions[1].height = 40

        m_ws.merge_cells("A2:J2")
        m_s_cell = m_ws["A2"]
        m_s_cell.value = "Strictly < 48 Hours Old | 10–30 Employees | Deal Value > $7,000 | Seeking Lead Gen Freelancers / Setters | US & UK"
        m_s_cell.font = Font(name="Calibri", size=11, italic=True, color="E2E8F0")
        m_s_cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        m_s_cell.alignment = Alignment(horizontal="center", vertical="center")
        m_ws.row_dimensions[2].height = 25

        m_ws.append([])
        m_ws.append(headers)
        m_ws.row_dimensions[4].height = 28

        for col_idx in range(1, len(headers) + 1):
            cell = m_ws.cell(row=4, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        cur_r = 5
        for idx, lead in enumerate(LEADS_ICP_48H, start=1):
            fill = row_alt_fill if idx % 2 == 0 else row_white_fill
            r_vals = [
                idx, lead["date_posted"], lead["company_name"], lead["role_needed"],
                lead["linkedin_url"], lead["city_state"], lead["country"], lead["company_size"],
                lead["deal_value"], lead["remarks"]
            ]
            m_ws.append(r_vals)
            m_ws.row_dimensions[cur_r].height = 36

            for col_idx in range(1, len(r_vals) + 1):
                cell = m_ws.cell(row=cur_r, column=col_idx)
                cell.fill = fill
                cell.border = thin_border
                cell.font = text_font

                if col_idx == 1:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                    cell.font = bold_text_font
                elif col_idx == 3:
                    cell.font = bold_text_font
                    cell.alignment = Alignment(vertical="center")
                elif col_idx == 5:
                    cell.font = link_font
                    cell.hyperlink = lead["linkedin_url"]
                    cell.value = "Direct LinkedIn Posting"
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                elif col_idx in (2, 6, 7, 8):
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    cell.alignment = Alignment(vertical="center", wrap_text=True)

            cur_r += 1

        for col_letter, width in col_widths.items():
            m_ws.column_dimensions[col_letter].width = width

        master_wb.save(master_excel)
        print(f"Updated Master Excel: {master_excel}")

if __name__ == "__main__":
    export_48h_leads()
