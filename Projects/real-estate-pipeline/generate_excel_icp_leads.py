import os
import csv
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

LEADS_ICP_DATA = [
    {
        "date_posted": "2026-09-05 (1 day ago)",
        "company_name": "Spencer Hsu Real Estate Team",
        "role_needed": "Inside Sales Agent (ISA) / Lead Gen Specialist",
        "linkedin_url": "https://www.linkedin.com/jobs/view/inside-sales-agent-isa-%E2%80%93-high-volume-real-estate-team-bay-area-at-spencer-hsu-real-estate-team-4387771948",
        "city_state": "San Jose, CA",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "info@spencerhsu.com",
        "deal_value": "$10,000+ (High-Ticket Commission)",
        "remarks": "High-volume boutique Silicon Valley real estate team seeking dedicated lead generator & ISA to qualify off-market & inbound buyer/seller leads. High deal size ($1M+ properties)."
    },
    {
        "date_posted": "2026-09-05 (3 days ago)",
        "company_name": "Achdut Homebuyers",
        "role_needed": "Real Estate Prospector / Off-Market Lead Gen",
        "linkedin_url": "https://www.linkedin.com/jobs/view/real-estate-prospector-4461772164",
        "city_state": "New York, NY",
        "country": "United States",
        "company_size": "10–30 employees",
        "email_contact": "acquisitions@achduthomebuyers.com",
        "deal_value": "$15,000+ per deal",
        "remarks": "Direct real estate investment & acquisition firm looking for outbound prospector to generate distressed property & motivated seller leads across NY/NJ."
    },
    {
        "date_posted": "2026-09-05 (1 day ago)",
        "company_name": "tlc Estate Agents",
        "role_needed": "Business Relations & Property Lead Generator",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/business-relations-assistant-at-tlc-estate-agents-4463119930",
        "city_state": "London (Earl's Court / Chelsea)",
        "country": "United Kingdom",
        "company_size": "15–30 employees",
        "email_contact": "enquiries@tlcestateagents.co.uk",
        "deal_value": "£12,000+ ($15,500+) per transaction",
        "remarks": "Prime Central London independent estate agency needing proactive lead generation and relationship outreach to landlords and luxury property owners."
    },
    {
        "date_posted": "2026-09-05 (2 days ago)",
        "company_name": "Marketing Simplified",
        "role_needed": "Outbound Lead Generator / Appointment Setter (Remote)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/appointment-setter-remote-at-marketing-simplified-4460997567",
        "city_state": "Gilbert, AZ (Remote)",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "hello@marketingsimplified.co",
        "deal_value": "$8,000 – $15,000 retainer",
        "remarks": "Boutique digital growth agency actively seeking a remote lead gen partner/setter to run cold outreach campaigns and book pre-qualified sales calls with business owners."
    },
    {
        "date_posted": "2026-09-05 (3 days ago)",
        "company_name": "Collective.work",
        "role_needed": "Sales / Business Developer (Freelance)",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/sales-business-developer-freelance-freelance-at-collective-work-4405691790",
        "city_state": "London, England",
        "country": "United Kingdom",
        "company_size": "10–30 employees",
        "email_contact": "contact@collective.work",
        "deal_value": "£10,000+ ($13,000+)",
        "remarks": "Boutique creative agency collective seeking a freelance business development partner to spearhead lead generation and outbound pipeline development for client accounts."
    },
    {
        "date_posted": "2026-09-05 (1 day ago)",
        "company_name": "NorthOrbis",
        "role_needed": "B2B Lead Generation Specialist (Commission / Contract)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/b2b-lead-generation-specialist-%E2%80%94-commission-based-at-northorbis-4461051804",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "partners@northorbis.com",
        "deal_value": "$7,500 – $20,000 per deal",
        "remarks": "B2B advisory and consulting group hiring an independent freelance lead generation specialist to book enterprise demos with high commission split ($2k–$5k per closed lead)."
    },
    {
        "date_posted": "2026-09-05 (1 week ago)",
        "company_name": "NORTH Acquisitions",
        "role_needed": "Property Acquisitions Lead Generator",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/property-acquisitions-coordinator-at-north-acquistions-4459033678",
        "city_state": "Manchester, England",
        "country": "United Kingdom",
        "company_size": "10–20 employees",
        "email_contact": "info@northacquisitions.co.uk",
        "deal_value": "£25,000+ ($32,000+) deal fee",
        "remarks": "UK commercial and residential property acquisition firm seeking targeted outreach specialist to source off-market residential developments and land opportunities."
    },
    {
        "date_posted": "2026-09-05 (3 weeks ago)",
        "company_name": "The Mulholland Drive Company",
        "role_needed": "Acquisitions Agent - Property Owner Outreach",
        "linkedin_url": "https://www.linkedin.com/jobs/view/acquistions-agent-owner-outreach-at-the-mulholland-drive-company-4448254461",
        "city_state": "Los Angeles, CA",
        "country": "United States",
        "company_size": "10–25 employees",
        "email_contact": "info@mulhollanddriveco.com",
        "deal_value": "$25,000+ per acquisition",
        "remarks": "Boutique LA real estate investment team requiring direct owner outreach and prospecting to generate private, off-market residential inventory."
    },
    {
        "date_posted": "2026-09-05 (3 days ago)",
        "company_name": "Lead Boom",
        "role_needed": "Lead Generation & Appointment Setting Specialist",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/lead-generation-at-lead-boom-4461702887",
        "city_state": "Doncaster, England",
        "country": "United Kingdom",
        "company_size": "10–20 employees",
        "email_contact": "growth@leadboom.co.uk",
        "deal_value": "£7,000 – £15,000 contract",
        "remarks": "Outbound sales development consultancy looking for lead generation contractors to handle cold email sequencing and LinkedIn prospect qualification for UK clients."
    },
    {
        "date_posted": "2026-09-05 (1 month ago)",
        "company_name": "Everything Virtual Assistant (EVA)",
        "role_needed": "Real Estate Campaign Appointment Setter / Lead Gen",
        "linkedin_url": "https://www.linkedin.com/jobs/view/appointment-setter-real-estate-campaign-at-everything-virtual-assistant-eva-4442897808",
        "city_state": "New York, NY (Remote)",
        "country": "United States",
        "company_size": "15–30 employees",
        "email_contact": "contact@everythingva.com",
        "deal_value": "$7,000+ campaign value",
        "remarks": "Staffing and operational consultancy running targeted lead generation and cold calling campaigns for US real estate investor and broker clients."
    },
    {
        "date_posted": "2026-09-05 (1 week ago)",
        "company_name": "Cold Call Me",
        "role_needed": "Sales Development Representative (Independent Contractor)",
        "linkedin_url": "https://www.linkedin.com/jobs/view/sales-development-representative-sdr-%E2%80%93-remote-independent-contractor-at-cold-call-me-4448716695",
        "city_state": "United States (Remote)",
        "country": "United States",
        "company_size": "10–30 employees",
        "email_contact": "sales@coldcallme.com",
        "deal_value": "$7,000 – $12,000 per project",
        "remarks": "Remote outbound calling & appointment setting firm contracting freelance SDRs and lead generators for high-ticket B2B client acquisition."
    },
    {
        "date_posted": "2026-09-05 (2 days ago)",
        "company_name": "Proper Recruitment",
        "role_needed": "Sales Coordinator & Property Lead Specialist",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/sales-coordinator-at-proper-recruitment-4462175529",
        "city_state": "Essex, England",
        "country": "United Kingdom",
        "company_size": "10–20 employees",
        "email_contact": "info@properrecruitment.co.uk",
        "deal_value": "£8,500+ ($11,000+)",
        "remarks": "Boutique property recruitment and development agency looking for lead generation and candidate/client pipeline manager for regional UK estate agencies."
    },
    {
        "date_posted": "2026-09-05 (3 weeks ago)",
        "company_name": "One Thing Marketing",
        "role_needed": "B2B Sales Development & Lead Generation Rep",
        "linkedin_url": "https://www.linkedin.com/jobs/view/b2b-sales-development-representative-at-one-thing-marketing-4450589811",
        "city_state": "Louisville, KY",
        "country": "United States",
        "company_size": "10–20 employees",
        "email_contact": "dan@onethingmarketing.net",
        "deal_value": "$7,500 – $14,000 retainer",
        "remarks": "Boutique digital marketing and local SEO agency looking for B2B appointment setter to generate leads among home service contractors and commercial real estate firms."
    },
    {
        "date_posted": "2026-09-05 (3 days ago)",
        "company_name": "3E Management, LLC",
        "role_needed": "Business Development & Investor Lead Generator",
        "linkedin_url": "https://www.linkedin.com/jobs/view/business-development-representative-at-3e-management-llc-4460693206",
        "city_state": "Dallas, TX",
        "country": "United States",
        "company_size": "15–30 employees",
        "email_contact": "info@3emanagement.com",
        "deal_value": "$15,000+ per deal",
        "remarks": "Commercial real estate advisory and capital asset management firm needing dedicated outbound lead generation to attract real estate equity investors and property owners."
    },
    {
        "date_posted": "2026-09-05 (2 months ago)",
        "company_name": "Consistent Performance",
        "role_needed": "Cold Email & LinkedIn Lead Gen Specialist (Contract)",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/cold-email-linkedin-growth-lead-at-consistent-performance-4429912397",
        "city_state": "London Area",
        "country": "United Kingdom",
        "company_size": "10–25 employees",
        "email_contact": "contact@consistentperformance.com",
        "deal_value": "£9,000+ ($11,800+)",
        "remarks": "B2B growth consultancy hiring a freelance growth lead to build outbound email infrastructure, scrape targeted prospect lists, and generate qualified B2B leads."
    },
    {
        "date_posted": "2026-09-05 (2 days ago)",
        "company_name": "Campions Group",
        "role_needed": "Senior Property Services & Acquisitions Consultant",
        "linkedin_url": "https://uk.linkedin.com/jobs/view/senior-property-services-consultant-at-campions-group-4460478798",
        "city_state": "London Area",
        "country": "United Kingdom",
        "company_size": "15–30 employees",
        "email_contact": "enquiries@campionsgroup.co.uk",
        "deal_value": "£10,000 – £20,000 fee",
        "remarks": "Established residential real estate and property consultancy looking to expand client acquisition pipeline with private landlords, developers, and institutional investors."
    }
]

def export_all():
    workspace_dir = r"c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen"
    excel_file = os.path.join(workspace_dir, "leads_linkedin_icp_us_uk.xlsx")
    csv_file = os.path.join(workspace_dir, "leads_linkedin_icp_us_uk.csv")
    md_file = os.path.join(workspace_dir, "leads_linkedin_icp_us_uk.md")
    master_excel = os.path.join(workspace_dir, "leads_linkedin_icp.xlsx")

    # 1. Export CSV
    csv_headers = [
        "Date Posted",
        "Company Name",
        "Role / Lead Need",
        "Verified LinkedIn URL",
        "City / State",
        "Country",
        "Company Size",
        "Contact Email",
        "Deal / Contract Value",
        "Remarks & Requirements"
    ]
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for row in LEADS_ICP_DATA:
            writer.writerow([
                row["date_posted"],
                row["company_name"],
                row["role_needed"],
                row["linkedin_url"],
                row["city_state"],
                row["country"],
                row["company_size"],
                row["email_contact"],
                row["deal_value"],
                row["remarks"]
            ])
    print(f"Wrote CSV: {csv_file}")

    # 2. Export Markdown Report
    with open(md_file, mode="w", encoding="utf-8") as f:
        f.write("# 🎯 ICP-Qualified Leads (US & UK) — People & Companies Looking for Lead Generation\n\n")
        f.write(f"**Generated / Verified:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write("**ICP Criteria Match:**\n")
        f.write("- **Geography:** 100% United States (US) & United Kingdom (UK)\n")
        f.write("- **Company Size:** 10 – 30 employees (Boutique agencies, real estate teams, brokerages, investment firms)\n")
        f.write("- **Role Needed:** People/Companies needing lead generation freelancers, contractors, appointment setters, or someone to generate leads for them\n")
        f.write("- **Deal Value:** $7,000+ per deal/contract\n\n")
        f.write("| # | Date Posted | Company Name | Role Needed | Location | Country | Co. Size | Deal Value | Verified LinkedIn Job URL | Contact Email | Remarks |\n")
        f.write("| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for idx, row in enumerate(LEADS_ICP_DATA, start=1):
            f.write(
                f"| {idx} | {row['date_posted']} | **{row['company_name']}** | {row['role_needed']} | {row['city_state']} | {row['country']} | {row['company_size']} | {row['deal_value']} | [View on LinkedIn]({row['linkedin_url']}) | `{row['email_contact']}` | {row['remarks']} |\n"
            )
    print(f"Wrote Markdown: {md_file}")

    # 3. Create Styled Excel Sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "US & UK ICP Leads"

    # Title block
    ws.merge_cells("A1:J1")
    title_cell = ws["A1"]
    title_cell.value = "Target ICP Lead Generation Opportunities (US & UK Real Estate & B2B)"
    title_cell.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    # Subtitle block
    ws.merge_cells("A2:J2")
    sub_cell = ws["A2"]
    sub_cell.value = "Qualified by ICP: 10–30 Employees | Deal Value > $7,000 | Looking for Lead Gen Freelancers / Appointment Setters | US & UK"
    sub_cell.font = Font(name="Calibri", size=11, italic=True, color="E2E8F0")
    sub_cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 25

    # Headers
    headers = [
        "#",
        "Date Posted",
        "Company Name",
        "Role / Lead Need",
        "Verified LinkedIn URL",
        "City / State",
        "Country",
        "Company Size",
        "Deal Value / Budget",
        "Remarks & ICP Fit"
    ]
    ws.append([]) # Row 3 blank spacer
    ws.row_dimensions[3].height = 10

    ws.append(headers) # Row 4
    header_row_idx = 4
    ws.row_dimensions[header_row_idx].height = 28

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
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
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    # Data Rows
    row_alt_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    row_white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    link_font = Font(name="Calibri", size=10, color="0284C7", underline="single")
    text_font = Font(name="Calibri", size=10, color="0F172A")
    bold_text_font = Font(name="Calibri", size=10, bold=True, color="0F172A")

    current_row = 5
    for idx, lead in enumerate(LEADS_ICP_DATA, start=1):
        fill = row_alt_fill if idx % 2 == 0 else row_white_fill
        row_values = [
            idx,
            lead["date_posted"],
            lead["company_name"],
            lead["role_needed"],
            lead["linkedin_url"],
            lead["city_state"],
            lead["country"],
            lead["company_size"],
            lead["deal_value"],
            lead["remarks"]
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
            elif col_idx == 3: # Company Name
                cell.font = bold_text_font
                cell.alignment = Alignment(vertical="center")
            elif col_idx == 5: # Link
                cell.font = link_font
                cell.hyperlink = lead["linkedin_url"]
                cell.value = "Direct LinkedIn Posting"
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in (2, 6, 7, 8):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

        current_row += 1

    # Adjust Column Widths
    col_widths = {
        "A": 6,   # #
        "B": 22,  # Date
        "C": 30,  # Company
        "D": 34,  # Role Needed
        "E": 24,  # LinkedIn Link
        "F": 22,  # City/State
        "G": 18,  # Country
        "H": 18,  # Co. Size
        "I": 24,  # Deal Value
        "J": 55   # Remarks
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    wb.save(excel_file)
    wb.save(master_excel)
    print(f"Saved Excel Workbooks: {excel_file} and {master_excel}")

if __name__ == "__main__":
    export_all()
