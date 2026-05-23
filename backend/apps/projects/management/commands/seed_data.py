from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.projects.models import Project, Finding, FindingLibrary
from apps.reports.models import ReportTemplate, Section

User = get_user_model()

FINDINGS_DATA = [
    {
        "title": "SQL Injection in Login Endpoint",
        "severity": "critical",
        "cvss_score": "9.8",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "description": "<p>The login endpoint <code>/api/auth/token/</code> is vulnerable to SQL injection via the <code>email</code> parameter.</p>",
        "impact": "<p>An attacker can bypass authentication, extract the entire user database, and potentially execute OS commands.</p>",
        "steps_to_reproduce": "<p>Send: <code>POST /api/auth/token/ email=' OR 1=1--&password=x</code></p>",
        "remediation": "<p>Use parameterized queries or ORM abstractions. Validate and sanitize all user input.</p>",
        "affected_components": "/api/auth/token/",
    },
    {
        "title": "Reflected XSS in Search Parameter",
        "severity": "high",
        "cvss_score": "7.2",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "description": "<p>The <code>q</code> query parameter on the search page is reflected into the HTML response without encoding.</p>",
        "impact": "<p>Allows attackers to execute arbitrary JavaScript in the context of victim users' browsers.</p>",
        "steps_to_reproduce": "<p>Navigate to: <code>/search?q=&lt;script&gt;alert(1)&lt;/script&gt;</code></p>",
        "remediation": "<p>HTML-encode all user-supplied data before rendering. Implement a strict Content Security Policy.</p>",
        "affected_components": "/search",
    },
    {
        "title": "Missing Rate Limiting on Authentication",
        "severity": "high",
        "cvss_score": "7.5",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "description": "<p>No rate limiting is applied to the login endpoint, allowing unlimited brute-force attempts.</p>",
        "impact": "<p>Attackers can perform credential stuffing and brute-force attacks at scale.</p>",
        "steps_to_reproduce": "<p>Send 1000+ POST requests to <code>/api/auth/token/</code> with varying passwords—no lockout occurs.</p>",
        "remediation": "<p>Implement rate limiting (e.g., django-ratelimit). Lock accounts after 5 failed attempts. Add CAPTCHA.</p>",
        "affected_components": "/api/auth/token/",
    },
    {
        "title": "Sensitive Data in HTTP Response Headers",
        "severity": "medium",
        "cvss_score": "5.3",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "description": "<p>The <code>X-Powered-By</code> and <code>Server</code> headers expose backend technology versions.</p>",
        "impact": "<p>Facilitates targeted attacks by revealing the technology stack and versions in use.</p>",
        "steps_to_reproduce": "<p>Inspect any HTTP response headers.</p>",
        "remediation": "<p>Remove or mask <code>Server</code> and <code>X-Powered-By</code> headers in nginx and Django configuration.</p>",
        "affected_components": "All endpoints",
    },
    {
        "title": "CORS Misconfiguration",
        "severity": "medium",
        "cvss_score": "6.1",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "description": "<p>The API accepts requests from any origin (<code>Access-Control-Allow-Origin: *</code>) including credentialed requests.</p>",
        "impact": "<p>Allows malicious websites to make authenticated API calls on behalf of logged-in users.</p>",
        "steps_to_reproduce": "<p>Send a cross-origin request with credentials from any domain—the server responds with the requested data.</p>",
        "remediation": "<p>Restrict CORS to explicit allowed origins. Never combine <code>Allow-Origin: *</code> with <code>Allow-Credentials: true</code>.</p>",
        "affected_components": "/api/",
    },
    {
        "title": "Insecure Direct Object Reference (IDOR)",
        "severity": "high",
        "cvss_score": "8.1",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N",
        "description": "<p>Project resources can be accessed by any authenticated user by guessing or enumerating IDs.</p>",
        "impact": "<p>Authenticated users can read and modify other users' project data.</p>",
        "steps_to_reproduce": "<p>Log in as User A, then access <code>/api/projects/{User_B_project_id}/</code>—data is returned.</p>",
        "remediation": "<p>Enforce ownership checks in all ViewSet <code>get_queryset()</code> methods. Use <code>IsOwnerOrTeamMember</code> permission.</p>",
        "affected_components": "/api/projects/",
    },
    {
        "title": "Weak Password Policy",
        "severity": "medium",
        "cvss_score": "4.3",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N",
        "description": "<p>The application allows passwords as short as 1 character with no complexity requirements.</p>",
        "impact": "<p>Accounts can be compromised through simple dictionary or brute-force attacks.</p>",
        "steps_to_reproduce": "<p>Register a user with password <code>1</code>—registration succeeds.</p>",
        "remediation": "<p>Enforce minimum 12-character passwords with mixed case, digits, and symbols. Use Django's built-in password validators.</p>",
        "affected_components": "/api/accounts/register/",
    },
    {
        "title": "Missing Security Headers",
        "severity": "low",
        "cvss_score": "3.1",
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N",
        "description": "<p>Security headers including <code>Content-Security-Policy</code>, <code>X-Frame-Options</code>, and <code>Strict-Transport-Security</code> are absent.</p>",
        "impact": "<p>Increases the attack surface for XSS, clickjacking, and protocol downgrade attacks.</p>",
        "steps_to_reproduce": "<p>Inspect response headers—required security headers are missing.</p>",
        "remediation": "<p>Add security headers via nginx or Django's <code>SecurityMiddleware</code>. Use django-csp for Content Security Policy.</p>",
        "affected_components": "All pages",
    },
    {
        "title": "JWT Secret Key Exposure in Debug Mode",
        "severity": "critical",
        "cvss_score": "9.1",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
        "description": "<p>Django debug mode is enabled in production, which exposes the <code>SECRET_KEY</code> in error pages.</p>",
        "impact": "<p>With the SECRET_KEY an attacker can forge arbitrary JWT tokens and gain full administrative access.</p>",
        "steps_to_reproduce": "<p>Trigger a 500 error—Django debug traceback reveals <code>SECRET_KEY</code> value in settings dump.</p>",
        "remediation": "<p>Set <code>DEBUG=False</code> in production. Store secrets in environment variables. Rotate the SECRET_KEY immediately.</p>",
        "affected_components": "Django settings, all endpoints",
    },
    {
        "title": "Verbose Error Messages",
        "severity": "low",
        "cvss_score": "2.7",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N",
        "description": "<p>API error responses include full stack traces and internal file paths.</p>",
        "impact": "<p>Reveals internal application structure useful for targeted exploitation.</p>",
        "steps_to_reproduce": "<p>Send a malformed request to any API endpoint—full Python traceback is returned in the response body.</p>",
        "remediation": "<p>Return generic error messages to clients. Log detailed errors server-side only.</p>",
        "affected_components": "/api/",
    },
    {
        "title": "Unvalidated File Upload",
        "severity": "high",
        "cvss_score": "7.8",
        "cvss_vector": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H",
        "description": "<p>The file upload endpoint accepts any file type without validation of MIME type or file contents.</p>",
        "impact": "<p>Allows upload and potential execution of malicious files including web shells.</p>",
        "steps_to_reproduce": "<p>Upload a file named <code>shell.php</code> with PHP code—the file is stored and accessible via URL.</p>",
        "remediation": "<p>Validate file type by inspecting magic bytes, not just extension. Serve uploads from isolated storage. Disable execution in upload directories.</p>",
        "affected_components": "/api/projects/{id}/upload/",
    },
    {
        "title": "Cleartext Credentials in Application Logs",
        "severity": "medium",
        "cvss_score": "5.5",
        "cvss_vector": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N",
        "description": "<p>Authentication requests are logged verbatim, including plaintext passwords in the request body.</p>",
        "impact": "<p>Any user with log access can harvest credentials, enabling lateral movement.</p>",
        "steps_to_reproduce": "<p>Authenticate via the API, then check <code>/var/log/app/access.log</code>—plaintext password is present.</p>",
        "remediation": "<p>Sanitize sensitive fields before logging. Use structured logging with a sensitive-field redaction list.</p>",
        "affected_components": "Application logging subsystem",
    },
    {
        "title": "SSL/TLS Version Downgrade Possible",
        "severity": "medium",
        "cvss_score": "5.9",
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "description": "<p>The server supports TLS 1.0 and TLS 1.1 which contain known vulnerabilities (POODLE, BEAST).</p>",
        "impact": "<p>Allows man-in-the-middle attacks to downgrade TLS sessions and decrypt traffic.</p>",
        "steps_to_reproduce": "<p>Connect using <code>openssl s_client -tls1 -connect host:443</code>—connection succeeds.</p>",
        "remediation": "<p>Disable TLS 1.0 and 1.1 in nginx. Enforce TLS 1.2 minimum with strong cipher suites.</p>",
        "affected_components": "nginx TLS configuration",
    },
    {
        "title": "Outdated Third-Party Libraries",
        "severity": "info",
        "cvss_score": None,
        "cvss_vector": "",
        "description": "<p>Several npm and Python packages are significantly out of date and contain known CVEs.</p>",
        "impact": "<p>Known vulnerabilities in dependencies may be exploitable depending on application usage patterns.</p>",
        "steps_to_reproduce": "<p>Run <code>npm audit</code> and <code>pip-audit</code>—multiple high-severity findings reported.</p>",
        "remediation": "<p>Establish a dependency update policy. Enable Dependabot or Renovate for automated PRs. Update all dependencies to latest stable versions.</p>",
        "affected_components": "package.json, requirements.txt",
    },
    {
        "title": "Missing Anti-CSRF Tokens",
        "severity": "medium",
        "cvss_score": "6.5",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N",
        "description": "<p>State-changing API endpoints do not validate CSRF tokens, relying solely on JWT Bearer tokens.</p>",
        "impact": "<p>Allows CSRF attacks from third-party sites when SameSite cookie protection is not enforced.</p>",
        "steps_to_reproduce": "<p>Create a cross-origin form that submits to a state-changing endpoint—the request succeeds.</p>",
        "remediation": "<p>Set JWT tokens in <code>SameSite=Strict</code> cookies rather than localStorage. Alternatively, validate the <code>Origin</code> header server-side.</p>",
        "affected_components": "/api/ (all state-changing endpoints)",
    },
]


class Command(BaseCommand):
    help = "Seed database with sample projects, findings, and report templates"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Admin user
        admin, created = User.objects.get_or_create(
            email="admin@preport.local",
            defaults={"username": "admin", "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write("  Created admin@preport.local (password: admin123)")

        # Analyst user
        analyst, created = User.objects.get_or_create(
            email="analyst@preport.local",
            defaults={"username": "analyst"},
        )
        if created:
            analyst.set_password("analyst123")
            analyst.save()
            self.stdout.write("  Created analyst@preport.local (password: analyst123)")

        # Report templates
        tpl_default, _ = ReportTemplate.objects.get_or_create(
            name="Standard Pentest Report",
            defaults={
                "description": "Full penetration test report with executive summary and technical findings.",
                "is_default": True,
                "css_styles": "body { font-family: DejaVu Sans, sans-serif; }",
            },
        )
        Section.objects.get_or_create(report_template=tpl_default, title="Executive Summary", defaults={"order": 1, "content": "<p>This section provides a high-level overview for management.</p>"})
        Section.objects.get_or_create(report_template=tpl_default, title="Methodology", defaults={"order": 2, "content": "<p>Testing was conducted according to PTES and OWASP guidelines.</p>"})
        Section.objects.get_or_create(report_template=tpl_default, title="Findings", defaults={"order": 3, "content": ""})
        Section.objects.get_or_create(report_template=tpl_default, title="Recommendations", defaults={"order": 4, "content": "<p>Address all critical and high findings within 30 days.</p>"})

        tpl_web, _ = ReportTemplate.objects.get_or_create(
            name="Web Application Assessment",
            defaults={
                "description": "Focused report template for web application penetration tests.",
                "is_default": False,
            },
        )
        Section.objects.get_or_create(report_template=tpl_web, title="Scope & Objectives", defaults={"order": 1})
        Section.objects.get_or_create(report_template=tpl_web, title="OWASP Top 10 Coverage", defaults={"order": 2})
        Section.objects.get_or_create(report_template=tpl_web, title="Technical Findings", defaults={"order": 3})

        self.stdout.write("  Created 2 report templates")

        # Projects
        projects_data = [
            {
                "project_name": "AcmeCorp External Pentest",
                "client_name": "Acme Corporation",
                "project_type": "external",
                "status": "completed",
                "scope": "External perimeter: web app, VPN endpoints, public-facing APIs",
                "findings": FINDINGS_DATA[:5],
            },
            {
                "project_name": "FinTech Web App Assessment",
                "client_name": "FinTech Solutions Ltd",
                "project_type": "web",
                "status": "in_progress",
                "scope": "Main web application at app.fintech.example.com, REST API",
                "findings": FINDINGS_DATA[5:10],
            },
            {
                "project_name": "RetailCo Internal Network",
                "client_name": "RetailCo Inc",
                "project_type": "internal",
                "status": "review",
                "scope": "Internal network 10.0.0.0/8, Active Directory, file servers",
                "findings": FINDINGS_DATA[10:15],
            },
        ]

        total_findings = 0
        for idx, pd in enumerate(projects_data):
            project, created = Project.objects.get_or_create(
                project_name=pd["project_name"],
                defaults={
                    "client_name": pd["client_name"],
                    "project_type": pd["project_type"],
                    "status": pd["status"],
                    "scope": pd["scope"],
                    "owner": admin,
                },
            )
            if not created:
                continue

            project.team_members.add(analyst)

            for order, fd in enumerate(pd["findings"], 1):
                Finding.objects.create(
                    project=project,
                    order=order,
                    created_by=admin,
                    cvss_score=fd["cvss_score"],
                    **{k: v for k, v in fd.items() if k not in ("cvss_score",)},
                )
                total_findings += 1

        self.stdout.write(f"  Created {len(projects_data)} projects, {total_findings} findings")

        # Finding library
        library_count = 0
        for fd in FINDINGS_DATA[:5]:
            _, created = FindingLibrary.objects.get_or_create(
                title=fd["title"],
                defaults={
                    "severity": fd["severity"],
                    "cvss_score": fd["cvss_score"],
                    "cvss_vector": fd["cvss_vector"],
                    "description": fd["description"],
                    "impact": fd["impact"],
                    "remediation": fd["remediation"],
                    "created_by": admin,
                },
            )
            if created:
                library_count += 1

        self.stdout.write(f"  Created {library_count} library items")
        self.stdout.write(self.style.SUCCESS("Done! Seed data loaded successfully."))
