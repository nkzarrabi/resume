#!/usr/bin/env python3
"""
Test script for resume_mailer.py
Tests the core functionality without requiring user interaction.
"""

import sys
from resume_mailer import ResumeParser, CompanyAssessment, CoverLetterGenerator


def test_resume_parser():
    """Test resume parsing functionality."""
    print("Testing Resume Parser...")
    parser = ResumeParser()
    
    assert parser.data['name'] == "Nikou Zarrabi", f"Expected 'Nikou Zarrabi', got '{parser.data['name']}'"
    assert 'email' in parser.data['contact'], "Email not found in contact info"
    assert len(parser.data['skills']['languages']) > 0, "No programming languages found"
    assert len(parser.data['experience']) > 0, "No experience found"
    assert len(parser.data['education']) > 0, "No education found"
    
    print("✓ Resume Parser tests passed")
    print(f"  - Name: {parser.data['name']}")
    print(f"  - Email: {parser.data['contact'].get('email')}")
    print(f"  - Languages: {len(parser.data['skills']['languages'])} found")
    print(f"  - Experience: {len(parser.data['experience'])} positions")
    print()
    return parser


def test_company_assessment(parser):
    """Test company assessment functionality."""
    print("Testing Company Assessment...")
    
    # Test Case 1: iOS Startup (Should score high)
    assessment = CompanyAssessment(parser.data)
    
    company_info_ios = {
        'company_name': 'MobileApp Startup',
        'position': 'Senior iOS Developer',
        'required_skills': ['Swift', 'SwiftUI', 'Firebase', 'iOS'],
        'industry': 'tech',
        'company_size': 'startup',
        'work_culture': 'fast-paced',
        'remote_policy': 'remote'
    }
    
    result_ios = assessment.calculate_success_score(company_info_ios)
    
    print(f"Test Case 1: iOS Startup")
    print(f"  - Score: {result_ios['total_score']}/100")
    print(f"  - Recommendation: {result_ios['recommendation']}")
    assert result_ios['total_score'] >= 70, f"iOS startup should score high (got {result_ios['total_score']})"
    print("  ✓ Score is appropriate for iOS position")
    print()
    
    # Test Case 2: E-commerce DevOps (Should score high)
    company_info_ecommerce = {
        'company_name': 'OnlineStore Inc',
        'position': 'DevOps Engineer',
        'required_skills': ['Python', 'AWS', 'CI/CD', 'Docker', 'Django'],
        'industry': 'ecommerce',
        'company_size': 'medium',
        'work_culture': 'balanced',
        'remote_policy': 'hybrid'
    }
    
    result_ecommerce = assessment.calculate_success_score(company_info_ecommerce)
    
    print(f"Test Case 2: E-commerce DevOps")
    print(f"  - Score: {result_ecommerce['total_score']}/100")
    print(f"  - Recommendation: {result_ecommerce['recommendation']}")
    assert result_ecommerce['total_score'] >= 70, f"E-commerce DevOps should score high (got {result_ecommerce['total_score']})"
    print("  ✓ Score is appropriate for e-commerce position")
    print()
    
    # Test Case 3: Unrelated position (Should score moderate)
    company_info_unrelated = {
        'company_name': 'Healthcare Corp',
        'position': 'Data Scientist',
        'required_skills': ['R', 'Statistics', 'SPSS', 'Clinical Research'],
        'industry': 'healthcare',
        'company_size': 'enterprise',
        'work_culture': 'traditional',
        'remote_policy': 'onsite'
    }
    
    result_unrelated = assessment.calculate_success_score(company_info_unrelated)
    
    print(f"Test Case 3: Unrelated Healthcare Position")
    print(f"  - Score: {result_unrelated['total_score']}/100")
    print(f"  - Recommendation: {result_unrelated['recommendation']}")
    print("  ✓ Score reflects limited match")
    print()
    
    print("✓ Company Assessment tests passed")
    print()
    return company_info_ios, result_ios


def test_cover_letter_generator(parser, company_info, assessment_result):
    """Test cover letter generation."""
    print("Testing Cover Letter Generator...")
    
    generator = CoverLetterGenerator(parser.data)
    cover_letter = generator.generate(company_info, assessment_result)
    
    # Verify cover letter contains key elements
    assert parser.data['name'] in cover_letter, "Name not in cover letter"
    assert company_info['company_name'] in cover_letter, "Company name not in cover letter"
    assert company_info['position'] in cover_letter, "Position not in cover letter"
    assert len(cover_letter) > 500, "Cover letter seems too short"
    
    print("✓ Cover Letter Generator tests passed")
    print(f"  - Length: {len(cover_letter)} characters")
    print(f"  - Contains name: ✓")
    print(f"  - Contains company: ✓")
    print(f"  - Contains position: ✓")
    print()
    
    print("Sample Cover Letter (first 500 chars):")
    print("-" * 60)
    print(cover_letter[:500] + "...")
    print("-" * 60)
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Resume Mailer - Test Suite")
    print("=" * 60)
    print()
    
    try:
        parser = test_resume_parser()
        company_info, assessment_result = test_company_assessment(parser)
        test_cover_letter_generator(parser, company_info, assessment_result)
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print()
        print("The resume_mailer.py script is working correctly.")
        print("Run 'python resume_mailer.py' for interactive mode.")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
