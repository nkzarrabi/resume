# Resume Mailer

A Python-based tool to assess your fit with potential employers and automatically send customized resumes with personalized cover letters.

## Features

### 1. **Company Success Assessment**
The tool analyzes your resume against company requirements and calculates a success score (0-100) based on:
- **Skills Match (40 points)**: How well your technical skills align with job requirements
- **Experience Relevance (30 points)**: Industry and role-specific experience alignment
- **Culture Fit (15 points)**: Compatibility with company size and work culture
- **Growth Potential (15 points)**: Career advancement opportunities at the company

### 2. **Personalized Cover Letter Generation**
Automatically generates professional cover letters that:
- Highlight your relevant experience and accomplishments
- Emphasize key strengths based on the assessment
- Adapt tone and content to company size (startup vs. enterprise)
- Include specific skills mentioned in the job requirements

### 3. **Email Integration**
Send your resume and cover letter directly to hiring managers via email with:
- Professional email formatting
- PDF resume attachment
- Cover letter as email body
- SMTP support (Gmail, Outlook, etc.)

## Installation

### Prerequisites
- Python 3.6 or higher
- Your resume in `resume.md` format (already in this repository)
- Your resume PDF file (generated via `nix build` or available in releases)

### Setup

1. Make the script executable:
```bash
chmod +x resume_mailer.py
```

2. (Optional) Configure email settings:

**Option A: Environment Variables**
```bash
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
```

**Option B: Configuration File**
Create a file named `email_config.json`:
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password"
}
```

**Note for Gmail Users**: Use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## Usage

### Interactive Mode (Recommended)

Run the script without arguments for a guided experience:

```bash
python resume_mailer.py
```

The tool will prompt you for:
1. Company name
2. Position title
3. Required skills
4. Industry (tech, ecommerce, finance, automotive, other)
5. Company size (startup, medium, enterprise)
6. Work culture (fast-paced, balanced, traditional)
7. Remote policy (remote, hybrid, onsite)

### Example Workflow

```
$ python resume_mailer.py

============================================================
Resume Mailer - Company Fit Assessment & Email Tool
============================================================

Loading resume data...
✓ Loaded resume for: Nikou Zarrabi

Please provide information about the company and position:

Company Name: Tech Startup Inc
Position Title: Senior iOS Developer
Required Skills (comma-separated): Swift, SwiftUI, Firebase, iOS
Industry: tech
Company Size: startup
Work Culture: fast-paced
Remote Policy: remote

============================================================
Calculating Success Score...
============================================================

Overall Success Score: 88/100
Recommendation: Excellent Fit - Highly Recommended

Score Breakdown:
  • Skills Match: 38/40
  • Experience Relevance: 28/30
  • Culture Fit: 14/15
  • Growth Potential: 15/15

Your Strengths for This Role:
  ✓ Strong technical skills alignment
  ✓ Highly relevant industry experience
  ✓ Excellent cultural fit
  ✓ Great growth opportunities

Areas to Emphasize in Cover Letter:
  → Technical expertise in Swift, SwiftUI, Firebase
  → Proven track record in similar roles
  → Ability to work independently and wear multiple hats

Would you like to generate a cover letter? (y/n): y
```

## Understanding Your Success Score

### Score Ranges
- **85-100**: Excellent Fit - Highly Recommended
  - Strong alignment across all criteria
  - Apply with confidence
  
- **70-84**: Strong Fit - Recommended
  - Good match with minor gaps
  - Great opportunity to pursue
  
- **55-69**: Good Fit - Worth Pursuing
  - Decent alignment with room to grow
  - Consider if other factors align
  
- **40-54**: Moderate Fit - Consider Carefully
  - Some misalignment in key areas
  - Evaluate if worth investing time
  
- **0-39**: Low Fit - May Not Be Ideal
  - Significant gaps in requirements
  - Consider if you have transferable skills

### Interpreting the Breakdown

**Skills Match (40 points max)**
- Compares your technical skills with job requirements
- Higher scores mean more of the required skills match your background

**Experience Relevance (30 points max)**
- Evaluates industry and position-level alignment
- Considers your past roles and their relevance to the target position

**Culture Fit (15 points max)**
- Analyzes compatibility with company size and work culture
- Based on your past company experiences

**Growth Potential (15 points max)**
- Estimates career advancement opportunities
- Generally higher for startups and medium-sized companies

## Email Configuration

### Gmail Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other" (name it "Resume Mailer")
   - Copy the 16-character password
3. Use this App Password (not your regular password) in the configuration

### Other Email Providers

For Outlook, Yahoo, or other providers, update the SMTP settings:

```json
{
  "smtp_server": "smtp.office365.com",  # Outlook
  "smtp_port": 587,
  "sender_email": "your-email@outlook.com",
  "sender_password": "your-password"
}
```

Common SMTP servers:
- Gmail: `smtp.gmail.com:587`
- Outlook: `smtp.office365.com:587`
- Yahoo: `smtp.mail.yahoo.com:587`

## Tips for Best Results

1. **Be Specific with Required Skills**
   - List the exact technologies mentioned in the job posting
   - Use common abbreviations (e.g., "JS" instead of "JavaScript" if that's what the posting uses)

2. **Choose the Right Industry**
   - Select the industry that best matches the company
   - This helps the tool identify relevant experience

3. **Company Size Matters**
   - Startups: Usually looking for generalists who can wear multiple hats
   - Enterprise: Often prefer specialists with deep expertise
   - Medium: Good balance of both

4. **Review and Customize the Cover Letter**
   - The generated letter is a strong starting point
   - Add specific details about why you're interested in the company
   - Mention any personal connections or specific company achievements

5. **Test Email Before Sending**
   - Send a test email to yourself first
   - Verify the formatting and attachment

## Troubleshooting

### Email Not Sending

**Problem**: "Email configuration incomplete"
- **Solution**: Set SENDER_EMAIL and SENDER_PASSWORD environment variables or create email_config.json

**Problem**: "Authentication failed"
- **Solution**: For Gmail, use an App Password, not your regular password
- **Solution**: Ensure 2FA is enabled on your account

**Problem**: "SMTP connection failed"
- **Solution**: Check your SMTP server and port settings
- **Solution**: Verify your internet connection
- **Solution**: Some networks block SMTP ports (try a different network)

### Score Seems Off

**Problem**: Score is lower than expected
- **Solution**: Ensure you've listed all relevant required skills
- **Solution**: Verify the industry selection matches the company
- **Solution**: Remember the score is just a guide - your unique experiences matter too

### Cover Letter Not Generated

**Problem**: Cover letter looks generic
- **Solution**: Provide more specific required skills
- **Solution**: The tool uses your resume data - ensure your resume.md is up to date
- **Solution**: Edit the generated letter to add personal touches

## Privacy & Security

- ⚠️ **Never commit email_config.json to version control**
- The `.gitignore` file already excludes this file
- Email credentials are only used locally to send emails
- No data is sent to external services except the email recipient
- Consider using environment variables instead of config files for better security

## Advanced Usage

### Non-Interactive Mode

For automated workflows or testing:

```bash
python resume_mailer.py --non-interactive
```

### Customization

The tool is designed to be easily customizable. You can modify:

- **Assessment Weights**: Edit the `calculate_success_score` method in the `CompanyAssessment` class
- **Cover Letter Template**: Modify the `generate` method in the `CoverLetterGenerator` class
- **Resume Parsing**: Update the `ResumeParser` class to extract additional information

## Examples

### Example 1: E-commerce Company

```
Company Name: ShopTech
Position: DevOps Engineer
Required Skills: AWS, CI/CD, Docker, Python, Shopify
Industry: ecommerce
Company Size: medium
Work Culture: balanced
Remote Policy: hybrid
```

Expected high scores due to:
- E-commerce platform experience
- DevOps and CI/CD expertise
- Automation background

### Example 2: iOS Startup

```
Company Name: AppCo
Position: iOS Developer
Required Skills: Swift, SwiftUI, Firebase, iOS SDK
Industry: tech
Company Size: startup
Work Culture: fast-paced
Remote Policy: remote
```

Expected high scores due to:
- Direct iOS development experience
- Startup experience
- Full-stack mobile skills

### Example 3: Enterprise Tech

```
Company Name: BigTech Corp
Position: Software Engineer
Required Skills: Python, Django, REST APIs, PostgreSQL
Industry: tech
Company Size: enterprise
Work Culture: traditional
Remote Policy: hybrid
```

Expected good scores due to:
- Backend development experience
- Django expertise
- API development background

## Support

If you encounter issues or have questions:
1. Check the Troubleshooting section above
2. Review your resume.md to ensure it's properly formatted
3. Verify your email configuration
4. Open an issue in the GitHub repository

## License

This tool is part of the resume-md project and follows the same license.
