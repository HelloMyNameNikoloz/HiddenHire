CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    original_job_url TEXT NOT NULL,
    career_page_url TEXT,
    location TEXT,
    country TEXT DEFAULT 'Germany',
    remote_type TEXT,
    employment_type TEXT,
    hours_per_week TEXT,
    salary_min REAL,
    salary_max REAL,
    salary_currency TEXT DEFAULT 'EUR',
    salary_period TEXT,
    posted_date TEXT,
    application_deadline TEXT,
    tech_stack TEXT,
    requirements TEXT,
    description_short TEXT,
    why_relevant TEXT,
    source_type TEXT,
    crosscheck_linkedin_profile_found INTEGER DEFAULT 0,
    crosscheck_indeed_profile_found INTEGER DEFAULT 0,
    crosscheck_stepstone_profile_found INTEGER DEFAULT 0,
    crosscheck_xing_profile_found INTEGER DEFAULT 0,
    same_offer_found_on_linkedin INTEGER DEFAULT 0,
    same_offer_found_on_indeed INTEGER DEFAULT 0,
    same_offer_found_on_stepstone INTEGER DEFAULT 0,
    same_offer_found_on_xing INTEGER DEFAULT 0,
    is_rejected_platform_duplicate INTEGER DEFAULT 0,
    hidden_score INTEGER DEFAULT 0,
    red_flags TEXT,
    recommendation TEXT,
    application_method TEXT,
    contact_email TEXT,
    status TEXT DEFAULT 'new',
    applied_date TEXT,
    follow_up_date TEXT,
    notes TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_hidden_score ON jobs(hidden_score);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_jobs_deadline ON jobs(application_deadline);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX IF NOT EXISTS idx_jobs_duplicate_key
    ON jobs(employer_name, job_title, original_job_url);
