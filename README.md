# CodeAlpha_SecureCodingReview

**CodeAlpha Cybersecurity Internship — Task 3: Secure Coding Review**

## 📌 What this project is

A secure coding review of a small Python **Flask** web app ("Student Portal") that
simulates login, password hashing, a ping/diagnostics endpoint, and a profile page.
The app was **intentionally written with realistic vulnerabilities**, then reviewed
both manually and with an automated static analyzer, and finally remediated.

## 📂 Folder contents

| Path | Description |
|---|---|
| `vulnerable_app/app.py` | The original, insecure application selected for review (8 intentional vulnerabilities). |
| `fixed_app/app.py` | The remediated version, with every finding fixed and labeled `FIX 1`–`FIX 8`. |
| `SECURITY_REVIEW_REPORT.pdf` | Full report: methodology, findings table, detailed CWE-referenced write-ups, remediation, and before/after verification. |
| `bandit_scan_results/bandit_report_vulnerable_app.txt` | Raw output of the Bandit static analyzer run against the vulnerable app. |
| `bandit_scan_results/bandit_report_fixed_app.txt` | Raw output of Bandit run against the fixed app, confirming the issues are resolved. |
| `generate_report.py` | Script used to generate the PDF report (ReportLab). |
| `requirements.txt` | Dependencies needed to run the sample app / re-run the scan. |

## 🔍 Methodology

1. **Manual code review** — traced every user-input path (form fields, query params)
   through the app to see where it reached a database query, shell command, hash
   function, template, or deserialization call.
2. **Automated static analysis** — ran [Bandit](https://bandit.readthedocs.io/),
   a Python-specific SAST tool, to independently confirm findings.
3. **Remediation** — rewrote each vulnerable code path following secure coding
   best practices.
4. **Re-verification** — re-ran Bandit against the fixed app to confirm all
   High/Medium severity issues were eliminated.

## 🐞 Vulnerabilities found & fixed

| # | Vulnerability | Severity | CWE |
|---|---|---|---|
| 1 | Hardcoded secret key | Low | CWE-798 |
| 2 | SQL Injection | High | CWE-89 |
| 3 | Reflected XSS | Medium | CWE-79 |
| 4 | Weak password hashing (MD5) | High | CWE-327 |
| 5 | OS Command Injection | High | CWE-78 |
| 6 | Server-Side Template Injection | High | CWE-1336 |
| 7 | Insecure deserialization (pickle) | High | CWE-502 |
| 8 | Debug mode / bind to all interfaces | Medium | CWE-489, 605 |

Full descriptions, evidence, and fixes for each are in `SECURITY_REVIEW_REPORT.pdf`.

## ▶️ How to reproduce the scan

```bash
pip install -r requirements.txt
bandit -r vulnerable_app/app.py    # shows all 8 issues
bandit -r fixed_app/app.py         # shows 0 High/Medium issues
```

## ⚠️ Disclaimer

`vulnerable_app/app.py` contains **intentional** security flaws for training/demo
purposes only. It must never be deployed or exposed on a real network.

## 🎓 Submitted as part of

CodeAlpha Cybersecurity Internship — Task 3 (Secure Coding Review)
GitHub repo naming convention: `CodeAlpha_SecureCodingReview`
