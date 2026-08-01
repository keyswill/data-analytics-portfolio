from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OUT = "resume/Kiran_Williams_Resume.pdf"
W, H = letter
LEFT, RIGHT = 26, W - 26
NAVY = HexColor("#173a59")
TEXT = HexColor("#191919")
GRAY = HexColor("#555555")
RULE = HexColor("#8da1b3")

pdfmetrics.registerFont(TTFont("ResumeSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("ResumeSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("ResumeSans-Oblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


def width(text, font="ResumeSans", size=9.2):
    return stringWidth(text, font, size)


def wrapped(c, text, x, y, max_width, font="ResumeSans", size=9.2, leading=10.5,
            first_indent=0, hanging_indent=0, bullet=False):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        current_max = max_width - (first_indent if not lines else hanging_indent)
        if width(trial, font, size) <= current_max:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for i, value in enumerate(lines):
        indent = first_indent if i == 0 else hanging_indent
        c.setFont(font, size)
        c.setFillColor(TEXT)
        if bullet and i == 0:
            c.setFillColor(NAVY)
            c.drawString(x, y, u"\u2022")
            c.setFillColor(TEXT)
        c.drawString(x + indent, y, value)
        y -= leading
    return y


def section(c, title, y):
    c.setFillColor(NAVY)
    c.setFont("ResumeSans-Bold", 10.7)
    c.drawString(LEFT, y, title)
    y -= 4
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(LEFT, y, RIGHT, y)
    return y - 11


def linked_parts(c, parts, x, y, size=9.1):
    for text, font, color, url in parts:
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, text)
        w = width(text, font, size)
        if url:
            c.linkURL(url, (x, y - 1, x + w, y + size), relative=0)
        x += w
    return x


def dated_line(c, left, right, y, size=9.0):
    c.setFont("ResumeSans-Bold", size)
    c.setFillColor(TEXT)
    c.drawString(LEFT, y, left)
    c.drawRightString(RIGHT, y, right)
    return y


def project(c, name, tool, url, date, bullet, y):
    linked_parts(c, [
        (name, "ResumeSans-Bold", TEXT, None),
        (" | ", "ResumeSans", GRAY, None),
        (tool, "ResumeSans-Oblique", GRAY, None),
        (" | ", "ResumeSans", GRAY, None),
        ("GitHub Project", "ResumeSans-Oblique", NAVY, url),
    ], LEFT, y, 9.0)
    c.setFont("ResumeSans-Bold", 8.8)
    c.setFillColor(TEXT)
    c.drawRightString(RIGHT, y, date)
    return wrapped(c, bullet, LEFT + 10, y - 11, RIGHT - LEFT - 13,
                   size=8.9, leading=10.0, first_indent=10, hanging_indent=14, bullet=True) - 2


def education(c, degree, school, date, y):
    dated_line(c, f"{degree} | {school}", date, y, 8.7)
    return y - 12


def job(c, title, dates, employer, bullet_lines, y):
    dated_line(c, title, dates, y, 9.0)
    y -= 10.5
    c.setFont("ResumeSans-Oblique", 8.7)
    c.setFillColor(GRAY)
    c.drawString(LEFT, y, employer)
    y -= 10.5
    for bullet in bullet_lines:
        y = wrapped(c, bullet, LEFT + 10, y, RIGHT - LEFT - 12, size=8.55,
                    leading=9.5, first_indent=10, hanging_indent=14, bullet=True)
    return y - 2


def build():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Kiran Williams - Business, Data, and BI Analyst Resume")
    c.setAuthor("Kiran Williams")
    c.setSubject("Resume")
    c.setKeywords("Business Analyst, Data Analyst, BI Analyst, SQL, Tableau, Excel, Cognos, Analytics")

    y = H - 37
    c.setFillColor(NAVY)
    c.setFont("ResumeSans-Bold", 18)
    c.drawString(LEFT, y, "KIRAN WILLIAMS")
    y -= 15
    c.setFillColor(TEXT)
    c.setFont("ResumeSans-Bold", 10.8)
    c.drawString(LEFT, y, "BUSINESS ANALYST | DATA ANALYST | BI ANALYST")
    y -= 13
    linked_parts(c, [
        ("Baltimore-Washington, D.C. Area  |  240-997-3696  |  ", "ResumeSans", TEXT, None),
        ("kiranwilliams1997@gmail.com", "ResumeSans", NAVY, "mailto:kiranwilliams1997@gmail.com"),
        ("  |  ", "ResumeSans", TEXT, None),
        ("LinkedIn", "ResumeSans", NAVY, "https://www.linkedin.com/in/kiranwilliams/"),
        ("  |  ", "ResumeSans", TEXT, None),
        ("Portfolio", "ResumeSans", NAVY, "https://github.com/keyswill/data-analytics-portfolio"),
    ], LEFT, y, 8.75)
    y -= 16

    y = section(c, "PROFESSIONAL SUMMARY", y)
    y = wrapped(c, "Business and data analytics professional with 8+ years of cross-functional experience translating operational, workforce, and education data into dashboards, reporting, and actionable recommendations. Skilled in SQL, Excel, Tableau, Cognos Analytics, data cleaning, exploratory data analysis, KPI reporting, and business analysis.", LEFT, y, RIGHT - LEFT, size=8.9, leading=10.2) - 5

    y = section(c, "CORE SKILLS", y)
    linked_parts(c, [("Analytics: ", "ResumeSans-Bold", NAVY, None)], LEFT, y, 8.8)
    y = wrapped(c, "SQL, Excel (PivotTables, PivotCharts, slicers), Tableau, Google Sheets, Cognos Analytics, data cleaning, exploratory data analysis, dashboard development, KPI reporting, business analysis, data governance", LEFT + 44, y, RIGHT - LEFT - 44, size=8.8, leading=10.0, hanging_indent=-44)
    linked_parts(c, [("Business: ", "ResumeSans-Bold", NAVY, None)], LEFT, y, 8.8)
    y = wrapped(c, "requirements definition, stakeholder communication, workforce analytics, operational reporting, root-cause investigation, cross-functional collaboration", LEFT + 44, y, RIGHT - LEFT - 44, size=8.8, leading=10.0, hanging_indent=-44) - 5

    y = section(c, "SELECTED ANALYTICS PROJECTS", y)
    y = project(c, "Employee Satisfaction Analysis", "Tableau", "https://github.com/keyswill/employee-satisfaction-analysis", "2026", "Joined 1,000 employee profiles to 3,711 survey responses and built an interactive Tableau dashboard; normalized department comparisons and identified Finance as the lowest-satisfaction department (35.8).", y)
    y = project(c, "Electronics Sales Performance Analysis", "Excel", "https://github.com/keyswill/e-commerce-business-performance-analysis", "2026", "Cleaned 30,394 raw rows into 30,206 validated transaction lines and built an interactive Excel dashboard summarizing $5.64M in revenue, 29,018 unique orders, and 33,969 units sold.", y)
    y = project(c, "Mansfield Residential Listing Analysis", "Tableau", "https://github.com/keyswill/mansfield-residential-listing-analysis", "2026", "Analyzed 336 archived Mansfield, Texas listings; identified square footage as the strongest available price relationship (r = 0.656) and a 22% lower median price per square foot for foreclosures.", y)

    y = section(c, "EDUCATION AND CERTIFICATIONS", y)
    y = education(c, "MBA", "University of Maryland Global Campus", "Expected May 2028", y)
    y = education(c, "M.S., Data Analytics (GPA: 4.0/4.0)", "University of Maryland Global Campus", "Expected May 2027", y)
    y = education(c, "Graduate Certificate, Business Analytics", "University of Maryland Global Campus", "Aug 2026", y)
    y = education(c, "Google Data Analytics Certificate", "Google", "Sep 2021", y)
    y = education(c, "B.A., Chemistry", "University of Maryland Baltimore County", "Dec 2020", y) - 2

    y = section(c, "PROFESSIONAL EXPERIENCE", y)
    y = job(c, "Retail Operations Associate", "Nov 2025-Present", "Kohl's, Laurel, MD", ["Support inventory and fulfillment for a 2,000+ unit environment; earned Associate of the Month within four months for operational performance and adaptability."], y)
    y = job(c, "Guest Services & Operations Supervisor", "Dec 2018-Present", "Chesapeake Employers Insurance Arena, Baltimore, MD", ["Trained 50+ employees, supported real-time staffing and safety decisions, and presented 50+ operational recommendations to senior arena leadership."], y)
    y = job(c, "Middle School Science Teacher", "Aug 2023-Jun 2025", "Anne Arundel County Public Schools, Odenton, MD", ["Monitored performance, attendance, and behavior for 300+ students; communicated findings and coordinated targeted supports with leaders, teachers, families, and students."], y)
    y = job(c, "Workforce Specialist", "Oct 2021-Aug 2023", "UMBC Facilities Management, Baltimore, MD", ["Coordinated hiring, onboarding, scheduling, and training for 20-30 student employees; analyzed work-order performance and contributed to a 20% response-time reduction.", "Analyzed employee satisfaction survey results and communicated workforce findings and recommendations to operational stakeholders."], y)
    y = job(c, "High School Science Teacher", "Sep 2020-Jun 2021", "Prince George's County Public Schools, Hyattsville, MD", ["Evaluated performance and attendance for 150-200 students and maintained recurring Excel reports for instructional decisions."], y)

    if y < 22:
        raise RuntimeError(f"Resume overflowed page: final y={y}")
    c.save()


if __name__ == "__main__":
    build()
