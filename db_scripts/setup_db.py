import psycopg2
from psycopg2 import sql
from datetime import datetime

# -----------------------------
# اتصال بالـ PostgreSQL في Docker
# -----------------------------
conn = psycopg2.connect(
    dbname="my_database",
    user="admin",
    password="password123",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# -----------------------------
# إنشاء الجداول الأساسية
# -----------------------------
queries = [
"""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('student','graduate','recruiter')),
    university VARCHAR(100),
    graduation_year INT,
    profile_picture TEXT,
    bio TEXT,
    resume_link TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
""",
"""
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    industry VARCHAR(100),
    description TEXT,
    website TEXT,
    contact_email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
""",
"""
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    requirements TEXT,
    location VARCHAR(100),
    salary_range VARCHAR(50),
    status VARCHAR(20) DEFAULT 'open',
    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    deadline TIMESTAMP
);
""",
"""
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    job_id INT REFERENCES jobs(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT NOW()
);
""",
"""
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
""",
"""
CREATE TABLE IF NOT EXISTS user_skills (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, skill_id)
);
"""
]

for q in queries:
    cur.execute(q)

# -----------------------------
# إنشاء Indexes لتحسين الأداء
# -----------------------------
indexes = [
    "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
    "CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_applications_job ON applications(job_id);"
]

for idx in indexes:
    cur.execute(idx)

# -----------------------------
# إضافة بعض البيانات التجريبية
# -----------------------------
cur.execute("""
INSERT INTO companies (name, industry, description, website, contact_email)
VALUES
('TechCorp', 'Software', 'Leading software company', 'https://techcorp.com', 'hr@techcorp.com'),
('EduSolutions', 'Education', 'Innovative educational solutions', 'https://edusolutions.com', 'contact@edusolutions.com')
ON CONFLICT DO NOTHING;
""")

cur.execute("""
INSERT INTO users (name, email, password_hash, role, university, graduation_year)
VALUES
('Alice Smith', 'alice@example.com', 'hashed_password1', 'student', 'MIT', 2026),
('Bob Johnson', 'bob@example.com', 'hashed_password2', 'graduate', 'Stanford', 2024),
('Charlie Lee', 'charlie@example.com', 'hashed_password3', 'recruiter', NULL, NULL)
ON CONFLICT DO NOTHING;
""")

cur.execute("""
INSERT INTO skills (name)
VALUES
('Python'), ('JavaScript'), ('Data Analysis'), ('Machine Learning')
ON CONFLICT DO NOTHING;
""")

cur.execute("""
INSERT INTO jobs (title, description, requirements, location, salary_range, company_id, deadline)
VALUES
('Software Engineer Intern', 'Work on web applications', 'Python, Django', 'Remote', '$1000-$1500', 1, %s),
('Data Analyst', 'Analyze student data', 'SQL, Excel', 'New York', '$2000-$2500', 2, %s)
ON CONFLICT DO NOTHING;
""", (datetime(2026,12,31), datetime(2026,11,30)))

# ربط المستخدمين بالمهارات
cur.execute("""
INSERT INTO user_skills (user_id, skill_id)
VALUES
(1, 1), -- Alice knows Python
(1, 3), -- Alice knows Data Analysis
(2, 4)  -- Bob knows Machine Learning
ON CONFLICT DO NOTHING;
""")

# حفظ التغييرات
conn.commit()
cur.close()
conn.close()

print("Professional PostgreSQL database setup completed successfully!")