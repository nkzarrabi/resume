# Resume Mailer - Quick Start Guide

Get started with Resume Mailer in 5 minutes!

## What is Resume Mailer?

Resume Mailer is a smart tool that helps you:
1. **Assess** your fit with potential employers (0-100 score)
2. **Generate** personalized cover letters automatically
3. **Send** your resume and cover letter via email

## Installation

```bash
# No installation needed! Just Python 3.6+
cd /path/to/resume
python3 resume_mailer.py
```

## Quick Example

```bash
$ python3 resume_mailer.py

============================================================
Resume Mailer - Company Fit Assessment & Email Tool
============================================================

Loading resume data...
✓ Loaded resume for: Nikou Zarrabi

Please provide information about the company and position:

Company Name: TechCorp
Position Title: Software Engineer
Required Skills (comma-separated): Python, Django, AWS
Industry: tech
Company Size: medium
Work Culture: balanced
Remote Policy: hybrid

============================================================
Calculating Success Score...
============================================================

Overall Success Score: 88/100
Recommendation: Excellent Fit - Highly Recommended

Score Breakdown:
  • Skills Match: 40/40
  • Experience Relevance: 20/30
  • Culture Fit: 13/15
  • Growth Potential: 15/15

Your Strengths for This Role:
  ✓ Strong technical skills alignment
  ✓ Highly relevant industry experience
  ✓ Excellent cultural fit

Would you like to generate a cover letter? (y/n): y
```

## Understanding Your Score

| Score Range | Meaning | Action |
|------------|---------|--------|
| 85-100 | Excellent Fit | Apply confidently! |
| 70-84  | Strong Fit | Great opportunity |
| 55-69  | Good Fit | Worth pursuing |
| 40-54  | Moderate Fit | Consider carefully |
| 0-39   | Low Fit | May not be ideal |

## Email Setup (Optional)

To send emails, set environment variables:

```bash
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
```

**Gmail Users**: Use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

## Demo Mode

See it in action with realistic examples:

```bash
python3 demo_resume_mailer.py
```

This runs three scenarios:
- iOS Startup position
- E-commerce DevOps role  
- Full-stack web developer

## Test the Tool

Verify everything works:

```bash
python3 test_resume_mailer.py
```

Should output:
```
============================================================
All tests passed! ✓
============================================================
```

## Common Use Cases

### 1. Quickly Assess Multiple Jobs

Run the tool for each position you're considering. Compare scores to prioritize applications.

### 2. Tailor Your Application

Use the "Areas to Emphasize" section to customize your actual cover letter and interview prep.

### 3. Track Your Applications

Save generated cover letters with company names:
```
cover_letter_techcorp.txt
cover_letter_startup_inc.txt
```

### 4. Email Campaigns

Set up email configuration once, then easily send your resume to multiple companies.

## Pro Tips

1. **Be Specific**: List exact skills from the job posting
2. **Update resume.md**: Keep your resume current for accurate assessments
3. **Customize Generated Letters**: Use them as a strong starting point
4. **Compare Scores**: Apply to positions scoring 70+ first
5. **Save Your Work**: Keep cover letters for interview prep

## What's Next?

- **Full Documentation**: See [RESUME_MAILER_README.md](./RESUME_MAILER_README.md)
- **Main Project**: See [README.md](./README.md) for resume generation
- **Get Help**: Open an issue if you encounter problems

## File Structure

```
resume/
├── resume.md                      # Your resume (source)
├── resume.pdf                     # Generated PDF resume
├── resume_mailer.py              # Main tool
├── test_resume_mailer.py         # Test suite
├── demo_resume_mailer.py         # Demo scenarios
├── email_config.example.json     # Email config template
├── QUICKSTART.md                 # This file
└── RESUME_MAILER_README.md       # Full documentation
```

## Troubleshooting

**"ModuleNotFoundError"**
- You only need Python 3.6+ standard library (no pip install needed!)

**"File not found: resume.md"**
- Make sure you're in the resume directory
- Your resume must be named `resume.md`

**"Email not sending"**
- Verify email credentials
- Use App Password for Gmail
- Check internet connection

## Example Session

```bash
# Assess a startup position
python3 resume_mailer.py
# Enter: AppCo, iOS Developer, Swift/SwiftUI, tech, startup, fast-paced, remote
# Score: 84/100 - Strong Fit

# Generate cover letter
# Answer: y

# Save to file
# Answer: y

# Send email (if configured)
# Answer: y if credentials are set
```

## Success! 🎉

You're now ready to use Resume Mailer to:
- Assess job opportunities quickly
- Generate professional cover letters
- Send targeted applications efficiently

Happy job hunting! 🚀
