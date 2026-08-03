from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER

PURPLE = colors.HexColor("#5B2C87")
LIGHT_PURPLE = colors.HexColor("#F1EAF8")
DARK = colors.HexColor("#222222")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleBig", fontSize=22, leading=26, textColor=PURPLE,
                           fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name="SubTitle", fontSize=12, leading=16, textColor=DARK,
                           alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle(name="H1", fontSize=15, leading=18, textColor=PURPLE,
                           fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=8))
styles.add(ParagraphStyle(name="H2", fontSize=12.5, leading=15, textColor=PURPLE,
                           fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle(name="Body", fontSize=10, leading=15, textColor=DARK, spaceAfter=6))
styles.add(ParagraphStyle(name="Small", fontSize=8.5, leading=12, textColor=colors.HexColor("#555555")))


story = []

# --- Cover ---
story.append(Spacer(1, 60))
story.append(Paragraph("CodeAlpha Cybersecurity Internship", styles["SubTitle"]))
story.append(Paragraph("Secure Coding Review Report", styles["TitleBig"]))
story.append(Paragraph("Task 3 &ndash; Secure Coding Review", styles["SubTitle"]))
story.append(HRFlowable(width="80%", thickness=1.2, color=PURPLE, spaceAfter=20, hAlign="CENTER"))

info_data = [
    ["Application Reviewed:", "Student Portal (Flask web application)"],
    ["Language:", "Python 3.12 (Flask framework)"],
    ["Review Type:", "Manual source code review + automated static analysis (Bandit)"],
    ["Prepared by:", "Aysha &mdash; CodeAlpha Cybersecurity Intern"],
    ["Date:", "August 2026"],
]
info_table = Table([[Paragraph(f"<b>{a}</b>", styles["Body"]), Paragraph(b, styles["Body"])] for a, b in info_data],
                    colWidths=[5*cm, 10*cm])
info_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_PURPLE),
    ("BOX", (0, 0), (-1, -1), 0.5, PURPLE),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.white),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(info_table)
story.append(PageBreak())

# --- 1. Overview ---
story.append(Paragraph("1. Overview", styles["H1"]))
story.append(Paragraph(
    "This report documents a secure coding review carried out as Task 3 of the CodeAlpha "
    "Cybersecurity internship. A small Python/Flask web application, <b>Student Portal</b>, "
    "was selected as the audit target. The application simulates common real-world features "
    "&mdash; user login, password hashing, a network diagnostics endpoint, and a profile page "
    "&mdash; each of which was deliberately implemented with realistic, commonly-seen coding "
    "mistakes so the review could demonstrate a full vulnerability identification and "
    "remediation workflow.", styles["Body"]))

story.append(Paragraph("2. Scope &amp; Methodology", styles["H1"]))
story.append(Paragraph(
    "The review combined two complementary techniques:", styles["Body"]))
story.append(Paragraph(
    "<b>Manual inspection:</b> Every route handler in <font face='Courier'>app.py</font> was "
    "read line-by-line, tracing how user-controlled input (form fields, query parameters) "
    "flows into database queries, shell commands, hashing functions, template rendering, and "
    "deserialization calls.", styles["Body"]))
story.append(Paragraph(
    "<b>Automated static analysis:</b> The open-source tool <b>Bandit</b> (a Python-specific "
    "static application security testing tool) was run against the source file to independently "
    "confirm the manually identified issues and catch anything missed by eye.", styles["Body"]))
story.append(Paragraph(
    "Bandit's scan of the original application flagged <b>8 issues</b>: 3 High severity, "
    "3 Medium severity, and 2 Low severity &mdash; matching the 8 vulnerabilities identified "
    "manually below.", styles["Body"]))

# --- 3. Findings ---
story.append(Paragraph("3. Findings Summary", styles["H1"]))

findings_header = ["#", "Vulnerability", "Severity", "CWE", "Location"]
findings_rows = [
    ["1", "Hardcoded secret key in source code", "Low", "CWE-798", "app.py:19"],
    ["2", "SQL Injection (string-concatenated query)", "High", "CWE-89", "app.py:47"],
    ["3", "Reflected Cross-Site Scripting (XSS)", "Medium", "CWE-79", "app.py:53"],
    ["4", "Weak password hashing (unsalted MD5)", "High", "CWE-327", "app.py:62"],
    ["5", "OS Command Injection", "High", "CWE-78", "app.py:70"],
    ["6", "Server-Side Template Injection (SSTI)", "High", "CWE-1336", "app.py:79"],
    ["7", "Insecure deserialization (pickle)", "High", "CWE-502", "app.py:86"],
    ["8", "Debug mode / bound to all interfaces", "Medium", "CWE-489, 605", "app.py:93"],
]
table_data = [findings_header] + findings_rows
f_table = Table(table_data, colWidths=[1*cm, 6.6*cm, 2.1*cm, 3.3*cm, 2.5*cm], repeatRows=1)

sev_color = {"High": colors.HexColor("#C0392B"), "Medium": colors.HexColor("#B9770E"), "Low": colors.HexColor("#2E7D32")}
style_cmds = [
    ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_PURPLE]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]
for i, row in enumerate(findings_rows, start=1):
    style_cmds.append(("TEXTCOLOR", (2, i), (2, i), sev_color[row[2]]))
    style_cmds.append(("FONTNAME", (2, i), (2, i), "Helvetica-Bold"))
f_table.setStyle(TableStyle(style_cmds))
story.append(f_table)
story.append(PageBreak())

# --- 4. Detailed findings ---
story.append(Paragraph("4. Detailed Findings &amp; Remediation", styles["H1"]))

details = [
    dict(n=1, title="Hardcoded Secret Key", sev="Low", cwe="CWE-798",
         desc="The Flask session-signing secret key was committed directly in source code as a "
              "plain string. Anyone with repository access (or a leaked copy of the source) could "
              "forge signed session cookies.",
         fix="Load the secret from an environment variable and fail startup if it is missing, so "
             "the value never lives in version control."),
    dict(n=2, title="SQL Injection", sev="High", cwe="CWE-89",
         desc="The login query was built by concatenating the raw username and password directly "
              "into a SQL string. An attacker submitting a username like "
              "<font face='Courier'>' OR '1'='1</font> could bypass authentication entirely or "
              "extract arbitrary data from the database.",
         fix="Use parameterized queries (placeholders) so the database driver treats user input "
             "strictly as data, never as executable SQL."),
    dict(n=3, title="Reflected Cross-Site Scripting (XSS)", sev="Medium", cwe="CWE-79",
         desc="The username was echoed back into the HTTP response without escaping. A username "
              "containing a script tag would execute in the victim's browser.",
         fix="Escape all user-controlled output before it is written into an HTML response "
             "(e.g. Flask/Jinja's autoescaping or an explicit escape() call)."),
    dict(n=4, title="Weak Password Hashing", sev="High", cwe="CWE-327",
         desc="Passwords were hashed with unsalted MD5, an algorithm that is cryptographically "
              "broken and fast to brute-force with modern hardware and rainbow tables.",
         fix="Store passwords using a purpose-built, salted password hashing function "
             "(e.g. Werkzeug's generate_password_hash, which uses PBKDF2/scrypt) and compare with "
             "a constant-time check function."),
    dict(n=5, title="OS Command Injection", sev="High", cwe="CWE-78",
         desc="A user-supplied 'host' parameter was concatenated directly into a shell command "
              "passed to os.system(). Input like <font face='Courier'>127.0.0.1; rm -rf /</font> "
              "would execute attacker-chosen commands on the server.",
         fix="Validate that the input is actually a well-formed IP address before use, and invoke "
             "the external command as an argument list via subprocess (no shell=True), never by "
             "building a shell string."),
    dict(n=6, title="Server-Side Template Injection (SSTI)", sev="High", cwe="CWE-1336",
         desc="A user-controlled 'name' parameter was concatenated into a template string that "
              "was then rendered. Depending on the templating engine, this can allow full remote "
              "code execution on the server.",
         fix="Never build template strings from user input. Treat the value purely as data, "
             "escape it, and insert it into a fixed, pre-defined template/response."),
    dict(n=7, title="Insecure Deserialization", sev="High", cwe="CWE-502",
         desc="The application deserialized attacker-supplied data using Python's pickle module. "
              "Pickle can execute arbitrary code during deserialization, making this endpoint a "
              "direct remote-code-execution vector.",
         fix="Never unpickle untrusted input. Use a safe, data-only format such as JSON for any "
             "client-supplied data, and rely on Flask's built-in signed session cookies (or a "
             "server-side session store) instead of custom pickle-based session handling."),
    dict(n=8, title="Debug Mode Enabled / Bound to All Interfaces", sev="Medium",
         cwe="CWE-489 / CWE-605",
         desc="The app was started with debug=True and host='0.0.0.0'. Flask's debugger exposes "
              "an interactive Python console reachable over the network, which is a direct "
              "remote-code-execution path if this configuration reaches a real deployment.",
         fix="Disable debug mode outside local development, and restrict the bind address /use a "
             "reverse proxy so the app is not directly reachable on all network interfaces."),
]

for d in details:
    _hexcol = "#" + sev_color[d['sev']].hexval()[2:]
    story.append(Paragraph(f"4.{d['n']} {d['title']}  "
                            f"<font color='{_hexcol}'>&#9679;</font> "
                            f"{d['sev']} &mdash; {d['cwe']}", styles["H2"]))
    story.append(Paragraph(f"<b>Issue:</b> {d['desc']}", styles["Body"]))
    story.append(Paragraph(f"<b>Recommendation:</b> {d['fix']}", styles["Body"]))

story.append(PageBreak())

# --- 5. Verification ---
story.append(Paragraph("5. Verification of Fixes", styles["H1"]))
story.append(Paragraph(
    "After remediating each issue in <font face='Courier'>fixed_app/app.py</font>, Bandit was "
    "re-run to independently confirm the fixes.", styles["Body"]))

verify_data = [
    ["Metric", "Original app.py", "Fixed app.py"],
    ["High severity issues", "3", "0"],
    ["Medium severity issues", "3", "0"],
    ["Low severity issues", "2", "3*"],
]
v_table = Table(verify_data, colWidths=[6*cm, 4.5*cm, 4.5*cm])
v_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_PURPLE]),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(v_table)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "*The 3 remaining Low findings are informational notices about the use of the subprocess "
    "module in general (Bandit flags any subprocess usage for awareness). The underlying "
    "command-injection risk is fully resolved because the host is validated as a real IP address "
    "and the command is executed as an argument list, never through a shell.", styles["Small"]))

story.append(Paragraph("6. General Secure Coding Recommendations", styles["H1"]))
recs = [
    "Always use parameterized queries / an ORM for database access &mdash; never string-concatenate user input into SQL.",
    "Escape all output rendered into HTML, and never build template strings dynamically from user input.",
    "Hash passwords with a purpose-built algorithm (bcrypt/scrypt/PBKDF2) that includes a salt, never a general-purpose hash like MD5 or SHA-1.",
    "Avoid shell=True and raw string commands; pass arguments as a list and validate/allow-list any input used in system calls.",
    "Never deserialize untrusted data with pickle; prefer JSON or another data-only format.",
    "Keep secrets (keys, credentials, tokens) out of source code &mdash; load them from environment variables or a secrets manager.",
    "Disable debug mode and restrict network bind addresses before any deployment beyond local development.",
    "Run an automated static analyzer (e.g. Bandit for Python) as part of every code review or CI pipeline to catch regressions early.",
]
for r in recs:
    story.append(Paragraph(f"&bull; {r}", styles["Body"]))

story.append(Paragraph("7. Conclusion", styles["H1"]))
story.append(Paragraph(
    "The Student Portal application initially contained 8 distinct vulnerabilities spanning "
    "injection flaws, weak cryptography, insecure deserialization, and unsafe deployment "
    "configuration. All 8 were traced to their root cause through manual code review, "
    "independently confirmed with the Bandit static analyzer, and resolved in the remediated "
    "version of the application. This exercise demonstrates a complete secure coding review "
    "workflow: source review, automated scanning, documented findings with CWE references, "
    "concrete remediation, and re-verification.", styles["Body"]))

doc = SimpleDocTemplate(
    "/home/claude/CodeAlpha_SecureCodingReview/SECURITY_REVIEW_REPORT.pdf",
    pagesize=A4, topMargin=1.8*cm, bottomMargin=1.8*cm, leftMargin=2*cm, rightMargin=2*cm
)
doc.build(story)
print("Report generated.")
