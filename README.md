# HiddenHire

HiddenHire is a local Flask app for importing, reviewing, filtering, and tracking hidden job offers found directly on employer websites in Germany.

## Features

- CSV file upload or direct CSV paste with schema validation and duplicate detection
- SQLite storage with rejected platform-duplicate audit trail
- Dashboard with search, filters, and CSV export
- Job detail page with status tracking and private notes
- Analytics page with smart opportunity summaries
- Light mode and premium dark mode with local theme persistence
- Local-only MVP with no login

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
flask --app app run --debug
```

On first run, HiddenHire creates its SQLite database inside the project:

`database/hiddenhire.sqlite`

If an older `instance/hiddenhire.sqlite` or prior AppData copy exists, HiddenHire copies it into this project-local location automatically.

## Upload a CSV

1. Open `http://127.0.0.1:5000/upload`
2. Upload a UTF-8 `.csv` file up to 5 MB or paste raw CSV text directly
3. Review the import summary for inserted rows, skipped duplicates, rejected platform duplicates, and row errors

## Required CSV schema

The CSV must include these columns exactly:

`id, employer_name, job_title, original_job_url, career_page_url, location, country, remote_type, employment_type, hours_per_week, salary_min, salary_max, salary_currency, salary_period, posted_date, application_deadline, tech_stack, requirements, description_short, why_relevant, source_type, crosscheck_linkedin_profile_found, crosscheck_indeed_profile_found, crosscheck_stepstone_profile_found, crosscheck_xing_profile_found, same_offer_found_on_linkedin, same_offer_found_on_indeed, same_offer_found_on_stepstone, same_offer_found_on_xing, hidden_score, red_flags, recommendation, application_method, contact_email, status, applied_date, follow_up_date, notes, created_at`

## Example CSV row

```csv
"id","employer_name","job_title","original_job_url","career_page_url","location","country","remote_type","employment_type","hours_per_week","salary_min","salary_max","salary_currency","salary_period","posted_date","application_deadline","tech_stack","requirements","description_short","why_relevant","source_type","crosscheck_linkedin_profile_found","crosscheck_indeed_profile_found","crosscheck_stepstone_profile_found","crosscheck_xing_profile_found","same_offer_found_on_linkedin","same_offer_found_on_indeed","same_offer_found_on_stepstone","same_offer_found_on_xing","hidden_score","red_flags","recommendation","application_method","contact_email","status","applied_date","follow_up_date","notes","created_at"
"","Example GmbH","Working Student Python Developer","https://example.de/jobs/python","https://example.de/careers","Halle","Germany","hybrid","working_student","20","18","22","EUR","hour","2026-04-20","2026-05-05","Python; Flask; SQLite","Flask basics; SQL","Support internal tools","Direct employer site and local fit","direct_employer_website","false","true","false","false","false","false","false","false","84","Indeed company profile found","High relevance for flexible student role","email","jobs@example.de","new","","","Follow up with tailored cover letter","2026-04-24"
```

## Notes

- Duplicate imports are skipped based on `employer_name + job_title + original_job_url`
- If the same offer is found on LinkedIn, Indeed, StepStone, or Xing, HiddenHire marks it as rejected and hides it from the dashboard by default
- Company profiles found on large platforms count as red flags but do not auto-reject the job
- Export uses the active dashboard filters
- HiddenHire is designed for local-only use
