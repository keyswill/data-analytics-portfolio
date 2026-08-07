from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OUT = "resume/Kiran_Williams_Resume.pdf"
W, H = letter
LEFT, RIGHT = 34, W - 34
NAVY = HexColor("#173a59")
TEXT = HexColor("#191919")
GRAY = HexColor("#555555")
RULE = HexColor("#8da1b3")

pdfmetrics.registerFont(TTFont("ResumeSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("ResumeSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("ResumeSans-Oblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


def width(text, font="ResumeSans", size=9.2):
    return stringWidth(text, font, size)


def wrapped(c, text, x, y, max_width, font="ResumeSans", size=9.2,
            leading=11, first_indent=0, hanging_indent=0, bullet=False):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        available = max_width - (first_indent if not lines else hanging_indent)
        if width(trial, font, size) <= available:
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
    c.setFont("ResumeSans-Bold", 11)
    c.drawString(LEFT, y, title)
    y -= 4
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(LEFT, y, RIGHT, y)
    return y - 13


def linked_parts(c, parts, x, y, size=9.1):
    for text, font, color, url in parts:
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, text)
        w = width(text, font, size)
        if url:
            c.linkURL(url, (x, y - 1, x + w, y + size), relative=0)
        x += w


def header(c, page):
    y = H - 42
    if page == 1:
        c.setFillColor(NAVY)
        c.setFont("ResumeSans-Bold", 19)
        c.drawString(LEFT, y, "KIRAN WILLIAMS")
        y -= 17
        c.setFillColor(TEXT)
        c.setFont("ResumeSans-Bold", 11.2)
        c.drawString(LEFT, y, "BUSINESS ANALYST | DATA ANALYST | BI ANALYST")
        y -= 15
        linked_parts(c, [
            ("Baltimore-Washington, D.C. Area  |  240-997-3696  |  ", "ResumeSans", TEXT, None),
            ("kiranwilliams1997@gmail.com", "ResumeSans", NAVY, "mailto:kiranwilliams1997@gmail.com"),
            ("  |  ", "ResumeSans", TEXT, None),
            ("LinkedIn", "ResumeSans", NAVY, "https://www.linkedin.com/in/kiranwilliams/"),
            ("  |  ", "ResumeSans", TEXT, None),
            ("Portfolio", "ResumeSans", NAVY, "https://github.com/keyswill/data-analytics-portfolio"),
        ], LEFT, y, 8.55)
        return y - 19
    c.setFillColor(NAVY)
    c.setFont("ResumeSans-Bold", 12)
    c.drawString(LEFT, y, "KIRAN WILLIAMS")
    c.setFont("ResumeSans", 8.6)
    c.setFillColor(GRAY)
    c.drawRightString(RIGHT, y, "Business Analyst | Data Analyst | BI Analyst")
    c.setStrokeColor(RULE)
    c.line(LEFT, y - 7, RIGHT, y - 7)
    return y - 24


def footer(c, page):
    c.setFont("ResumeSans", 7.8)
    c.setFillColor(GRAY)
    c.drawCentredString(W / 2, 20, f"Kiran Williams | Page {page} of 2")


def dated_line(c, left, right, y, size=9.1):
    c.setFont("ResumeSans-Bold", size)
    c.setFillColor(TEXT)
    c.drawString(LEFT, y, left)
    c.drawRightString(RIGHT, y, right)


def education(c, degree, school, date, y):
    dated_line(c, f"{degree} | {school}", date, y, 8.8)
    return y - 13


def job(c, title, dates, employer, bullets, y):
    dated_line(c, title, dates, y, 9.2)
    y -= 11
    c.setFont("ResumeSans-Oblique", 8.8)
    c.setFillColor(GRAY)
    c.drawString(LEFT, y, employer)
    y -= 11
    for bullet in bullets:
        y = wrapped(c, bullet, LEFT + 10, y, RIGHT - LEFT - 12, size=8.7,
                    leading=10.2, first_indent=10, hanging_indent=14, bullet=True)
    return y - 4


def project(c, name, tool, url, status, problem, work, y):
    linked_parts(c, [
        (name, "ResumeSans-Bold", TEXT, None),
        (" | ", "ResumeSans", GRAY, None),
        (tool, "ResumeSans-Oblique", GRAY, None),
        (" | ", "ResumeSans", GRAY, None),
        ("GitHub", "ResumeSans-Oblique", NAVY, url),
    ], LEFT, y, 9.5)
    c.setFont("ResumeSans-Bold", 8.8)
    c.setFillColor(GRAY)
    c.drawRightString(RIGHT, y, status)
    y -= 13
    y = wrapped(c, "Business problem: " + problem, LEFT + 10, y, RIGHT - LEFT - 12,
                size=8.8, leading=10.3, first_indent=10, hanging_indent=14, bullet=True)
    y = wrapped(c, "Analysis and business value: " + work, LEFT + 10, y, RIGHT - LEFT - 12,
                size=8.8, leading=10.3, first_indent=10, hanging_indent=14, bullet=True)
    return y - 13


def build():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Kiran Williams - Two-Page Master Resume")
    c.setAuthor("Kiran Williams")
    c.setSubject("Business, Data, and BI Analyst Resume")
    c.setKeywords("Business Analyst, Data Analyst, BI Analyst, SQL, Excel, Tableau, Cognos Analytics")

    # Page 1: qualifications and business-focused analytics projects
    y = header(c, 1)
    y = section(c, "PROFESSIONAL SUMMARY", y)
    y = wrapped(c, "Business and data analytics professional with 8+ years of experience across operations, workforce management, and education. Uses SQL, Excel, Tableau, and Cognos Analytics to turn complex data into clear reporting, dashboards, and practical recommendations. Brings strong stakeholder communication, customer service, and problem-solving skills to cross-functional teams.", LEFT, y, RIGHT - LEFT, size=9.0, leading=10.7) - 7

    y = section(c, "CORE SKILLS", y)
    y = wrapped(c, "Analytics: SQL, Excel (PivotTables, PivotCharts, slicers), Tableau, Google Sheets, Cognos Analytics, data cleaning, exploratory analysis, dashboard development, KPI reporting, data validation, data governance", LEFT, y, RIGHT - LEFT, size=8.85, leading=10.4)
    y = wrapped(c, "Business: requirements definition, stakeholder communication, business problem framing, operational reporting, workforce analytics, root-cause investigation, process improvement, cross-functional collaboration", LEFT, y, RIGHT - LEFT, size=8.85, leading=10.4) - 7

    y = section(c, "PORTFOLIO PROJECTS", y)
    y = project(c, "Citi Bike Operational Analytics", "MySQL, Tableau", "https://github.com/keyswill/citibike-operational-analytics", "In progress", "Operations teams need to know when and where completed trip patterns may signal pressure on bike or dock availability.", "Consolidated and validated 4,674,903 May 2026 rides from five source tables; defined station activity, net flow, imbalance, and time-based measures that will help prioritize stations for monitoring and rebalancing investigation without claiming confirmed shortages.", y)

    y = project(c, "Student Performance Analytics", "Tableau", "https://github.com/keyswill/student-performance-analysis", "2026", "School leaders need to combine grades, attendance, behavior, and intervention history to identify students and groups requiring earlier review.", "Integrated five synthetic datasets for 120 students into three dashboards; found a 12.37-point grade difference below versus at-or-above 85% attendance, supporting attendance as a human-review trigger rather than an automatic intervention rule.", y)

    y = project(c, "World Life Expectancy Analysis", "MySQL", "https://github.com/keyswill/world-life-expectancy-analysis", "2026", "A global health organization needs a transparent way to prioritize countries for deeper investigation when analytical resources are limited.", "Cleaned 2,941 records into 2,938 validated country-year observations and used CTEs, window functions, correlation, GDP-peer benchmarks, and a six-indicator screening score to create an auditable review list rather than an automatic funding decision.", y)

    y = project(c, "Electronics Sales Performance Analysis", "Excel", "https://github.com/keyswill/e-commerce-business-performance-analysis", "2026", "Sales leaders need to distinguish high-volume products from high-revenue products and understand how concentrated performance is across the catalog.", "Cleaned 30,394 rows into 30,206 validated transaction lines and built an interactive dashboard for $5.64M revenue, 29,018 orders, and 33,969 units; showed that laptops and phones produced 61% of revenue while batteries led unit volume, supporting separate merchandising views of demand and value.", y)

    y = project(c, "Employee Satisfaction Analysis", "Tableau", "https://github.com/keyswill/employee-satisfaction-analysis", "2026", "HR leaders need to locate satisfaction gaps and recurring concerns without allowing unequal department sizes or confounding factors to distort comparisons.", "Joined 3,711 survey responses to 1,000 employee profiles, normalized concern shares within departments, and identified Finance as the lowest-satisfaction group; the dashboard directs targeted listening and commute or compensation investigation without claiming causality.", y)

    if y < 36:
        raise RuntimeError(f"Page 1 overflow: final y={y}")
    footer(c, 1)
    c.showPage()

    # Page 2: education and professional experience
    y = header(c, 2)
    y = section(c, "EDUCATION AND CERTIFICATIONS", y)
    y = education(c, "MBA (GPA: 4.0/4.0)", "University of Maryland Global Campus", "Expected May 2028", y)
    y = education(c, "M.S., Data Analytics (GPA: 4.0/4.0)", "University of Maryland Global Campus", "Expected May 2027", y)
    y = education(c, "Graduate Certificate, Business Analytics", "University of Maryland Global Campus", "Aug 2026", y)
    y = education(c, "Google Data Analytics Certificate", "Google", "Sep 2021", y)
    y = education(c, "B.A., Chemistry", "University of Maryland Baltimore County", "Dec 2020", y) - 3

    y = section(c, "PROFESSIONAL EXPERIENCE", y)
    y = job(c, "Retail Operations Associate", "Nov 2025-Present", "Kohl's, Laurel, MD", [
        "Support inventory processing and order fulfillment across a 2,000+ unit environment while adapting to changing daily operational priorities.",
        "Provide customer service by responding to shopper questions and communicating inventory or order needs to the appropriate team members.",
        "Earned Associate of the Month within four months for operational performance and adaptability."
    ], y)
    y = job(c, "Guest Services & Operations Supervisor", "Dec 2018-Present", "Chesapeake Employers Insurance Arena, Baltimore, MD", [
        "Trained 50+ employees and supported real-time staffing and safety decisions during arena operations.",
        "Held ongoing conversations with arena leadership to communicate frontline observations, staffing needs, and operational concerns.",
        "Provided customer service to arena guests and communicated questions or concerns to the appropriate staff."
    ], y)
    y = job(c, "Middle School Science Teacher", "Aug 2023-Jun 2025", "Anne Arundel County Public Schools, Odenton, MD", [
        "Monitored performance, attendance, and behavior for 300+ students to identify patterns and students requiring closer review.",
        "Communicated findings and coordinated targeted supports with school leaders, teachers, families, and students.",
        "Responded to student and family questions, explained performance concerns, and communicated next steps with school staff."
    ], y)
    y = job(c, "Workforce Specialist", "Oct 2021-Aug 2023", "UMBC Facilities Management, Baltimore, MD", [
        "Coordinated hiring, onboarding, scheduling, and training for 20-30 student employees while providing day-to-day service and support.",
        "Analyzed work-order performance and contributed to operational changes that reduced response time by 20%.",
        "Analyzed employee satisfaction survey results and communicated workforce findings and recommendations to operational stakeholders."
    ], y)
    y = job(c, "High School Science Teacher", "Sep 2020-Jun 2021", "Prince George's County Public Schools, Hyattsville, MD", [
        "Evaluated performance and attendance patterns across 150-200 students.",
        "Built and maintained recurring Excel reports used for instructional planning and intervention decisions.",
        "Responded to student questions and explained performance, attendance, and support expectations in clear terms."
    ], y)
    if y < 36:
        raise RuntimeError(f"Page 2 overflow: final y={y}")
    footer(c, 2)
    c.save()


if __name__ == "__main__":
    build()
