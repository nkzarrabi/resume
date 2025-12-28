#!/usr/bin/env python3
"""
Resume Mailer - A system to assess company fit and send customized resumes with cover letters.
"""

import argparse
import json
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path


class ResumeParser:
    """Parse resume.md to extract key information."""
    
    def __init__(self, resume_path="resume.md"):
        self.resume_path = resume_path
        self.data = self._parse_resume()
    
    def _parse_resume(self):
        """Extract structured data from resume markdown."""
        with open(self.resume_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        data = {
            'name': self._extract_name(content),
            'contact': self._extract_contact(content),
            'skills': self._extract_skills(content),
            'experience': self._extract_experience(content),
            'education': self._extract_education(content),
            'projects': self._extract_projects(content),
            'summary': self._extract_summary(content)
        }
        return data
    
    def _extract_name(self, content):
        """Extract name from the first heading."""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else "Candidate"
    
    def _extract_contact(self, content):
        """Extract contact information."""
        contact = {}
        email_match = re.search(r'\[([^\]]+@[^\]]+)\]', content)
        if email_match:
            contact['email'] = email_match.group(1)
        
        phone_match = re.search(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', content)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        linkedin_match = re.search(r'linkedin\.com/in/([^\s)]+)', content, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(1)
        
        github_match = re.search(r'github\.com/([^\s)]+)', content, re.IGNORECASE)
        if github_match:
            contact['github'] = github_match.group(1)
        
        return contact
    
    def _extract_skills(self, content):
        """Extract technical skills."""
        skills = {
            'languages': [],
            'frameworks': [],
            'cloud': [],
            'specializations': []
        }
        
        skills_section = re.search(r'## Technical Skills\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if skills_section:
            section_text = skills_section.group(1)
            
            if 'Languages:' in section_text:
                lang_match = re.search(r'Languages:\*\*\s+([^\n]+)', section_text)
                if lang_match:
                    skills['languages'] = [s.strip() for s in lang_match.group(1).split(',')]
            
            if 'Frameworks' in section_text:
                fw_match = re.search(r'Frameworks[^:]*:\*\*\s+([^\n]+)', section_text)
                if fw_match:
                    skills['frameworks'] = [s.strip() for s in fw_match.group(1).split(',')]
            
            if 'Cloud' in section_text:
                cloud_match = re.search(r'Cloud[^:]*:\*\*\s+([^\n]+)', section_text)
                if cloud_match:
                    skills['cloud'] = [s.strip() for s in cloud_match.group(1).split(',')]
            
            if 'Specializations:' in section_text:
                spec_match = re.search(r'Specializations:\*\*\s+([^\n]+)', section_text)
                if spec_match:
                    skills['specializations'] = [s.strip() for s in spec_match.group(1).split(',')]
        
        return skills
    
    def _extract_experience(self, content):
        """Extract work experience."""
        experience = []
        exp_section = re.search(r'## Experience\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if exp_section:
            section_text = exp_section.group(1)
            # Extract job titles and companies
            jobs = re.findall(r'\*\*([^\*]+)\*\*\s*\n\s*\*([^\*]+)\*\s*\|\s*([^\n]+)', section_text)
            for title, company, dates in jobs:
                experience.append({
                    'title': title.strip(),
                    'company': company.strip(),
                    'dates': dates.strip()
                })
        return experience
    
    def _extract_education(self, content):
        """Extract education information."""
        education = []
        edu_section = re.search(r'## Education\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if edu_section:
            section_text = edu_section.group(1)
            degrees = re.findall(r'\*\*([^\*]+)\*\*\s*\n\s*([^\n]+)', section_text)
            for degree, details in degrees:
                education.append({
                    'degree': degree.strip(),
                    'details': details.strip()
                })
        return education
    
    def _extract_projects(self, content):
        """Extract projects."""
        projects = []
        proj_section = re.search(r'## Projects\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if proj_section:
            section_text = proj_section.group(1)
            proj_list = re.findall(r'\*\*([^\*]+)\*\*', section_text)
            projects = [p.strip() for p in proj_list]
        return projects
    
    def _extract_summary(self, content):
        """Extract professional summary."""
        summary_section = re.search(r'## Professional Summary\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if summary_section:
            return summary_section.group(1).strip()
        return ""


class CompanyAssessment:
    """Assess fit between candidate and company."""
    
    def __init__(self, resume_data):
        self.resume_data = resume_data
    
    def calculate_success_score(self, company_info):
        """
        Calculate a success score based on multiple criteria.
        
        Args:
            company_info: Dict containing:
                - company_name: str
                - position: str
                - required_skills: list of str
                - industry: str (e.g., 'tech', 'finance', 'ecommerce')
                - company_size: str ('startup', 'medium', 'enterprise')
                - work_culture: str ('fast-paced', 'balanced', 'traditional')
                - remote_policy: str ('remote', 'hybrid', 'onsite')
        
        Returns:
            Dict with score (0-100) and detailed breakdown
        """
        scores = {}
        
        # 1. Skills Match (40 points)
        scores['skills_match'] = self._assess_skills_match(company_info.get('required_skills', []))
        
        # 2. Experience Relevance (30 points)
        scores['experience'] = self._assess_experience_relevance(
            company_info.get('industry', ''),
            company_info.get('position', '')
        )
        
        # 3. Culture Fit (15 points)
        scores['culture_fit'] = self._assess_culture_fit(
            company_info.get('company_size', ''),
            company_info.get('work_culture', '')
        )
        
        # 4. Career Growth Potential (15 points)
        scores['growth_potential'] = self._assess_growth_potential(
            company_info.get('position', ''),
            company_info.get('company_size', '')
        )
        
        total_score = sum(scores.values())
        
        return {
            'total_score': total_score,
            'breakdown': scores,
            'recommendation': self._get_recommendation(total_score),
            'strengths': self._identify_strengths(scores),
            'areas_to_emphasize': self._identify_emphasis_areas(company_info, scores)
        }
    
    def _assess_skills_match(self, required_skills):
        """Calculate skills match score (0-40)."""
        if not required_skills:
            return 35  # Default good score if no specific requirements
        
        all_candidate_skills = []
        for skill_category in self.resume_data['skills'].values():
            all_candidate_skills.extend([s.lower() for s in skill_category])
        
        matched_skills = 0
        for req_skill in required_skills:
            req_skill_lower = req_skill.lower()
            if any(req_skill_lower in candidate_skill or candidate_skill in req_skill_lower 
                   for candidate_skill in all_candidate_skills):
                matched_skills += 1
        
        if len(required_skills) > 0:
            match_percentage = matched_skills / len(required_skills)
            return int(match_percentage * 40)
        return 35
    
    def _assess_experience_relevance(self, industry, position):
        """Calculate experience relevance score (0-30)."""
        score = 0
        experience = self.resume_data['experience']
        
        # Check for relevant industry experience
        industry_keywords = {
            'tech': ['software', 'developer', 'engineer', 'devops'],
            'ecommerce': ['ecommerce', 'e-commerce', 'shopify', 'retail', 'online'],
            'finance': ['financial', 'banking', 'fintech'],
            'automotive': ['automotive', 'cars', 'vehicle']
        }
        
        relevant_jobs = 0
        for job in experience:
            job_text = (job['title'] + ' ' + job['company']).lower()
            
            # Check industry match
            if industry.lower() in industry_keywords:
                if any(keyword in job_text for keyword in industry_keywords[industry.lower()]):
                    relevant_jobs += 1
            
            # Check position level match
            position_lower = position.lower()
            if any(term in position_lower for term in ['senior', 'lead', 'principal']):
                if any(term in job_text for term in ['lead', 'senior', 'engineer']):
                    score += 5
            elif 'junior' in position_lower or 'entry' in position_lower:
                score += 8  # Good fit regardless
        
        # Base score on relevant experience
        if relevant_jobs > 0:
            score += min(relevant_jobs * 8, 20)
        else:
            score += 10  # Still some credit for general experience
        
        return min(score, 30)
    
    def _assess_culture_fit(self, company_size, work_culture):
        """Calculate culture fit score (0-15)."""
        score = 0
        experience = self.resume_data['experience']
        
        # Analyze past company sizes
        has_startup_exp = any('swimming cars' in job['company'].lower() for job in experience)
        has_enterprise_exp = any('porsche' in job['company'].lower() for job in experience)
        has_small_business_exp = any('keivan' in job['company'].lower() for job in experience)
        
        if company_size.lower() == 'startup' and has_startup_exp:
            score += 8
        elif company_size.lower() == 'enterprise' and has_enterprise_exp:
            score += 8
        elif company_size.lower() == 'medium':
            score += 7  # Good fit for any background
        else:
            score += 5  # Some experience is transferable
        
        # Work culture assessment based on skills and experience
        if work_culture.lower() == 'fast-paced':
            # Check for startup experience and automation skills
            if has_startup_exp or 'CI/CD' in str(self.resume_data['skills']):
                score += 7
            else:
                score += 5
        else:
            score += 6  # Neutral fit
        
        return min(score, 15)
    
    def _assess_growth_potential(self, position, company_size):
        """Calculate growth potential score (0-15)."""
        score = 10  # Base score
        
        # Higher growth potential in smaller companies
        if company_size.lower() in ['startup', 'medium']:
            score += 5
        else:
            score += 3
        
        return min(score, 15)
    
    def _get_recommendation(self, score):
        """Generate recommendation based on score."""
        if score >= 85:
            return "Excellent Fit - Highly Recommended"
        elif score >= 70:
            return "Strong Fit - Recommended"
        elif score >= 55:
            return "Good Fit - Worth Pursuing"
        elif score >= 40:
            return "Moderate Fit - Consider Carefully"
        else:
            return "Low Fit - May Not Be Ideal"
    
    def _identify_strengths(self, scores):
        """Identify top strengths based on scores."""
        strengths = []
        
        if scores['skills_match'] >= 30:
            strengths.append("Strong technical skills alignment")
        if scores['experience'] >= 20:
            strengths.append("Highly relevant industry experience")
        if scores['culture_fit'] >= 12:
            strengths.append("Excellent cultural fit")
        if scores['growth_potential'] >= 12:
            strengths.append("Great growth opportunities")
        
        return strengths if strengths else ["Transferable skills and adaptability"]
    
    def _identify_emphasis_areas(self, company_info, scores):
        """Identify what to emphasize in cover letter."""
        areas = []
        
        if scores['skills_match'] >= 30:
            areas.append(f"Technical expertise in {', '.join(company_info.get('required_skills', [])[:3])}")
        
        if 'ecommerce' in company_info.get('industry', '').lower():
            areas.append("E-commerce platform experience and automation skills")
        
        if scores['experience'] >= 20:
            areas.append("Proven track record in similar roles")
        
        if 'startup' in company_info.get('company_size', '').lower():
            areas.append("Ability to work independently and wear multiple hats")
        
        return areas if areas else ["Strong problem-solving skills and adaptability"]


class CoverLetterGenerator:
    """Generate personalized cover letters."""
    
    def __init__(self, resume_data):
        self.resume_data = resume_data
    
    def generate(self, company_info, assessment_result):
        """
        Generate a personalized cover letter.
        
        Args:
            company_info: Dict with company details
            assessment_result: Result from CompanyAssessment
        
        Returns:
            String containing the cover letter
        """
        name = self.resume_data['name']
        email = self.resume_data['contact'].get('email', '')
        phone = self.resume_data['contact'].get('phone', '')
        
        date = datetime.now().strftime("%B %d, %Y")
        
        # Build the cover letter
        letter = f"{name}\n"
        if email:
            letter += f"{email}"
        if phone:
            letter += f" | {phone}"
        letter += f"\n\n{date}\n\n"
        
        letter += f"Hiring Manager\n"
        letter += f"{company_info.get('company_name', '[Company Name]')}\n\n"
        
        letter += f"Dear Hiring Manager,\n\n"
        
        # Opening paragraph
        letter += f"I am writing to express my strong interest in the {company_info.get('position', '[Position]')} "
        letter += f"position at {company_info.get('company_name', '[Company Name]')}. "
        
        # Add relevant experience hook
        most_recent = self.resume_data['experience'][0] if self.resume_data['experience'] else None
        if most_recent:
            letter += f"As a {most_recent['title']} with a proven track record in {company_info.get('industry', 'technology')}, "
        else:
            letter += f"With my background in software engineering and "
        
        letter += "I am excited about the opportunity to contribute to your team.\n\n"
        
        # Skills paragraph
        letter += "My technical expertise aligns well with your requirements. "
        
        if company_info.get('required_skills'):
            skills_mentioned = company_info['required_skills'][:3]
            letter += f"I bring extensive experience in {', '.join(skills_mentioned[:-1])}"
            if len(skills_mentioned) > 1:
                letter += f", and {skills_mentioned[-1]}"
            letter += ". "
        
        # Add specific accomplishments based on experience
        if self.resume_data['experience']:
            letter += self._add_relevant_accomplishments(company_info)
        
        letter += "\n\n"
        
        # Emphasis areas paragraph
        emphasis_areas = assessment_result['areas_to_emphasize']
        if emphasis_areas:
            letter += "I am particularly drawn to this opportunity because of my "
            letter += emphasis_areas[0].lower()
            if len(emphasis_areas) > 1:
                letter += f", as well as my {emphasis_areas[1].lower()}"
            letter += ". "
        
        letter += f"I am confident that my background and skills make me a strong candidate for this role"
        
        if company_info.get('company_size') == 'startup':
            letter += ", and I thrive in dynamic, fast-paced environments where I can make an immediate impact"
        elif company_info.get('company_size') == 'enterprise':
            letter += ", and I excel in collaborative environments with established processes"
        
        letter += ".\n\n"
        
        # Closing
        letter += f"I would welcome the opportunity to discuss how my experience and skills can contribute to "
        letter += f"{company_info.get('company_name', 'your organization')}'s success. "
        letter += "Thank you for considering my application.\n\n"
        
        letter += "Sincerely,\n"
        letter += f"{name}\n"
        
        return letter
    
    def _add_relevant_accomplishments(self, company_info):
        """Add relevant accomplishments based on company info."""
        text = ""
        
        industry = company_info.get('industry', '').lower()
        
        if 'ecommerce' in industry or 'retail' in industry:
            text += ("At Keivan Woven Arts, I built automated infrastructure for product listings across 3 major platforms, "
                    "reducing manual listing time by 80% and improving operational efficiency. ")
        elif 'tech' in industry or 'software' in industry:
            text += ("In my recent role, I architected and developed a production-ready SwiftUI iOS app, "
                    "implementing secure authentication and achieving zero crashes with 50+ users. ")
        elif 'devops' in company_info.get('position', '').lower():
            text += ("I have extensive experience implementing CI/CD pipelines using GitHub Actions, "
                    "decreasing deployment time from hours to minutes and reducing errors by 95%. ")
        else:
            text += ("Throughout my career, I have consistently delivered high-quality solutions, "
                    "combining technical expertise with strong problem-solving skills. ")
        
        return text


class EmailSender:
    """Handle email sending functionality."""
    
    def __init__(self, config_path='email_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load email configuration from file or environment."""
        config = {
            'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.environ.get('SMTP_PORT', '587')),
            'sender_email': os.environ.get('SENDER_EMAIL', ''),
            'sender_password': os.environ.get('SENDER_PASSWORD', ''),
        }
        
        # Try to load from config file if it exists
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        
        return config
    
    def send_resume(self, recipient_email, subject, cover_letter, resume_path='resume.pdf'):
        """
        Send resume with cover letter via email.
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject line
            cover_letter: Cover letter text
            resume_path: Path to resume PDF file
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.config['sender_email'] or not self.config['sender_password']:
            return (False, "Email configuration incomplete. Please set SENDER_EMAIL and SENDER_PASSWORD environment variables or create email_config.json")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add cover letter as body
            body = cover_letter
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach resume PDF
            if os.path.exists(resume_path):
                with open(resume_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(resume_path)}'
                    )
                    msg.attach(part)
            else:
                return (False, f"Resume file not found: {resume_path}")
            
            # Send email
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            return (True, f"Email sent successfully to {recipient_email}")
        
        except Exception as e:
            return (False, f"Failed to send email: {str(e)}")


def interactive_mode():
    """Run the tool in interactive mode."""
    print("=" * 60)
    print("Resume Mailer - Company Fit Assessment & Email Tool")
    print("=" * 60)
    print()
    
    # Parse resume
    print("Loading resume data...")
    resume_parser = ResumeParser()
    print(f"✓ Loaded resume for: {resume_parser.data['name']}\n")
    
    # Get company information
    print("Please provide information about the company and position:\n")
    
    company_info = {}
    company_info['company_name'] = input("Company Name: ").strip()
    company_info['position'] = input("Position Title: ").strip()
    
    skills_input = input("Required Skills (comma-separated): ").strip()
    company_info['required_skills'] = [s.strip() for s in skills_input.split(',')] if skills_input else []
    
    print("\nIndustry Options: tech, ecommerce, finance, automotive, other")
    company_info['industry'] = input("Industry: ").strip() or 'tech'
    
    print("\nCompany Size Options: startup, medium, enterprise")
    company_info['company_size'] = input("Company Size: ").strip() or 'medium'
    
    print("\nWork Culture Options: fast-paced, balanced, traditional")
    company_info['work_culture'] = input("Work Culture: ").strip() or 'balanced'
    
    print("\nRemote Policy Options: remote, hybrid, onsite")
    company_info['remote_policy'] = input("Remote Policy: ").strip() or 'hybrid'
    
    # Calculate assessment
    print("\n" + "=" * 60)
    print("Calculating Success Score...")
    print("=" * 60 + "\n")
    
    assessment = CompanyAssessment(resume_parser.data)
    result = assessment.calculate_success_score(company_info)
    
    # Display results
    print(f"Overall Success Score: {result['total_score']}/100")
    print(f"Recommendation: {result['recommendation']}\n")
    
    print("Score Breakdown:")
    print(f"  • Skills Match: {result['breakdown']['skills_match']}/40")
    print(f"  • Experience Relevance: {result['breakdown']['experience']}/30")
    print(f"  • Culture Fit: {result['breakdown']['culture_fit']}/15")
    print(f"  • Growth Potential: {result['breakdown']['growth_potential']}/15\n")
    
    if result['strengths']:
        print("Your Strengths for This Role:")
        for strength in result['strengths']:
            print(f"  ✓ {strength}")
        print()
    
    if result['areas_to_emphasize']:
        print("Areas to Emphasize in Cover Letter:")
        for area in result['areas_to_emphasize']:
            print(f"  → {area}")
        print()
    
    # Generate cover letter
    generate = input("Would you like to generate a cover letter? (y/n): ").strip().lower()
    
    if generate == 'y':
        print("\nGenerating cover letter...\n")
        generator = CoverLetterGenerator(resume_parser.data)
        cover_letter = generator.generate(company_info, result)
        
        print("=" * 60)
        print("COVER LETTER")
        print("=" * 60)
        print(cover_letter)
        print("=" * 60 + "\n")
        
        # Save cover letter
        save_file = input("Save cover letter to file? (y/n): ").strip().lower()
        if save_file == 'y':
            filename = f"cover_letter_{company_info['company_name'].replace(' ', '_').lower()}.txt"
            with open(filename, 'w') as f:
                f.write(cover_letter)
            print(f"✓ Cover letter saved to: {filename}\n")
        
        # Send email
        send_email = input("Would you like to send the resume via email? (y/n): ").strip().lower()
        
        if send_email == 'y':
            recipient = input("Recipient email address: ").strip()
            subject = f"Application for {company_info['position']} - {resume_parser.data['name']}"
            
            print("\nNote: Email requires SMTP configuration.")
            print("Set SENDER_EMAIL and SENDER_PASSWORD environment variables,")
            print("or create email_config.json with your email settings.\n")
            
            proceed = input("Proceed with sending? (y/n): ").strip().lower()
            
            if proceed == 'y':
                sender = EmailSender()
                success, message = sender.send_resume(recipient, subject, cover_letter)
                
                if success:
                    print(f"\n✓ {message}")
                else:
                    print(f"\n✗ {message}")
    
    print("\n" + "=" * 60)
    print("Thank you for using Resume Mailer!")
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Resume Mailer - Assess company fit and send customized resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python resume_mailer.py
  
  # Set up email configuration via environment variables
  export SENDER_EMAIL="your-email@gmail.com"
  export SENDER_PASSWORD="your-app-password"
  python resume_mailer.py
        """
    )
    
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Run in non-interactive mode (for testing)'
    )
    
    args = parser.parse_args()
    
    if args.non_interactive:
        print("Non-interactive mode selected. Use without this flag for full functionality.")
        return
    
    interactive_mode()


if __name__ == '__main__':
    main()
