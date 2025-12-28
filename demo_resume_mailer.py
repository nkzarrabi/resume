#!/usr/bin/env python3
"""
Demo script showing the resume_mailer in action with realistic examples.
"""

from resume_mailer import ResumeParser, CompanyAssessment, CoverLetterGenerator


def demo_scenario(name, company_info):
    """Run a demo scenario and display results."""
    print("\n" + "=" * 70)
    print(f"SCENARIO: {name}")
    print("=" * 70)
    
    # Parse resume
    parser = ResumeParser()
    
    # Display company info
    print(f"\nCompany: {company_info['company_name']}")
    print(f"Position: {company_info['position']}")
    print(f"Industry: {company_info['industry']}")
    print(f"Company Size: {company_info['company_size']}")
    print(f"Required Skills: {', '.join(company_info['required_skills'][:5])}")
    
    # Calculate assessment
    assessment = CompanyAssessment(parser.data)
    result = assessment.calculate_success_score(company_info)
    
    # Display results
    print(f"\n{'-' * 70}")
    print("ASSESSMENT RESULTS")
    print(f"{'-' * 70}")
    print(f"Overall Success Score: {result['total_score']}/100")
    print(f"Recommendation: {result['recommendation']}")
    
    print(f"\nScore Breakdown:")
    print(f"  • Skills Match:        {result['breakdown']['skills_match']}/40")
    print(f"  • Experience:          {result['breakdown']['experience']}/30")
    print(f"  • Culture Fit:         {result['breakdown']['culture_fit']}/15")
    print(f"  • Growth Potential:    {result['breakdown']['growth_potential']}/15")
    
    if result['strengths']:
        print(f"\nKey Strengths:")
        for strength in result['strengths']:
            print(f"  ✓ {strength}")
    
    if result['areas_to_emphasize']:
        print(f"\nAreas to Emphasize:")
        for i, area in enumerate(result['areas_to_emphasize'][:3], 1):
            print(f"  {i}. {area}")
    
    # Generate cover letter preview
    generator = CoverLetterGenerator(parser.data)
    cover_letter = generator.generate(company_info, result)
    
    print(f"\n{'-' * 70}")
    print("COVER LETTER PREVIEW (First 400 characters)")
    print(f"{'-' * 70}")
    print(cover_letter[:400] + "...")
    
    return result


def main():
    """Run demo scenarios."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "RESUME MAILER - DEMONSTRATION" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Scenario 1: Perfect iOS Match
    scenario1 = {
        'company_name': 'AppVentures',
        'position': 'Senior iOS Developer',
        'required_skills': ['Swift', 'SwiftUI', 'Firebase', 'iOS SDK', 'Apple Maps'],
        'industry': 'tech',
        'company_size': 'startup',
        'work_culture': 'fast-paced',
        'remote_policy': 'remote'
    }
    result1 = demo_scenario("iOS Startup - Perfect Match", scenario1)
    
    # Scenario 2: E-commerce DevOps
    scenario2 = {
        'company_name': 'ShopFlow Technologies',
        'position': 'DevOps Engineer',
        'required_skills': ['Python', 'AWS', 'CI/CD', 'Docker', 'Shopify API', 'Django'],
        'industry': 'ecommerce',
        'company_size': 'medium',
        'work_culture': 'balanced',
        'remote_policy': 'hybrid'
    }
    result2 = demo_scenario("E-commerce DevOps - Strong Match", scenario2)
    
    # Scenario 3: Full Stack Web
    scenario3 = {
        'company_name': 'WebScale Inc',
        'position': 'Full Stack Developer',
        'required_skills': ['Python', 'JavaScript', 'React', 'Django', 'PostgreSQL'],
        'industry': 'tech',
        'company_size': 'medium',
        'work_culture': 'balanced',
        'remote_policy': 'remote'
    }
    result3 = demo_scenario("Full Stack Web - Good Match", scenario3)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF SCENARIOS")
    print("=" * 70)
    
    scenarios = [
        ("iOS Startup", result1['total_score'], result1['recommendation']),
        ("E-commerce DevOps", result2['total_score'], result2['recommendation']),
        ("Full Stack Web", result3['total_score'], result3['recommendation'])
    ]
    
    for name, score, rec in scenarios:
        print(f"\n{name:.<40} {score:>3}/100")
        print(f"  → {rec}")
    
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. The highest scoring positions align with recent iOS development experience
   and demonstrated expertise in Swift/SwiftUI.

2. E-commerce and DevOps roles score well due to extensive automation
   experience and platform integration work at Keivan Woven Arts.

3. The assessment correctly identifies transferable skills for full-stack
   positions while recognizing the strongest matches.

4. Cover letters are automatically customized to emphasize the most relevant
   experience and skills for each position.
    """)
    
    print("=" * 70)
    print("Next Steps:")
    print("  • Run 'python resume_mailer.py' for interactive mode")
    print("  • See RESUME_MAILER_README.md for full documentation")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
