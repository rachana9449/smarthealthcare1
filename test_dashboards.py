#!/usr/bin/env python3
"""
Dashboard Testing Script for MediConnect
Tests all dashboard functionality and consistency
"""

import os
import sys
import sqlite3
from datetime import datetime
import re

def test_template_syntax():
    """Test HTML template syntax for errors"""
    print("🔍 Testing Template Syntax...")
    
    dashboard_files = [
        'templates/patient_dashboard.html',
        'templates/doctor_dashboard.html', 
        'templates/admin_dashboard.html',
        'templates/patient_dashboard_enhanced.html',
        'templates/doctor_dashboard_modern.html'
    ]
    
    errors = []
    
    for file_path in dashboard_files:
        if os.path.exists(file_path):
            print(f"  ✓ Checking {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for template syntax issues
            if_count = content.count('{% if')
            endif_count = content.count('{% endif')
            for_count = content.count('{% for')
            endfor_count = content.count('{% endfor')
            block_count = content.count('{% block')
            endblock_count = content.count('{% endblock')
            
            if if_count != endif_count:
                errors.append(f"{file_path}: Mismatched if/endif tags ({if_count} if, {endif_count} endif)")
            
            if for_count != endfor_count:
                errors.append(f"{file_path}: Mismatched for/endfor tags ({for_count} for, {endfor_count} endfor)")
                
            if block_count != endblock_count:
                errors.append(f"{file_path}: Mismatched block/endblock tags ({block_count} block, {endblock_count} endblock)")
                
            # Check for common template errors
            if '{{' in content and '}}' not in content:
                errors.append(f"{file_path}: Unclosed template variable")
                
            if '{%' in content and '%}' not in content:
                errors.append(f"{file_path}: Unclosed template tag")
        else:
            errors.append(f"Missing file: {file_path}")
    
    if errors:
        print("❌ Template Syntax Errors Found:")
        for error in errors:
            print(f"    {error}")
        return False
    else:
        print("✅ All templates have valid syntax")
        return True

def test_css_classes():
    """Test that all CSS classes used in templates are defined"""
    print("\n🎨 Testing CSS Classes...")
    
    # Key classes that should be defined
    required_classes = [
        'dashboard-grid', 'card-modern', 'stat-card', 'stat-icon', 
        'stat-number', 'stat-label', 'timeline', 'timeline-item',
        'appointment-card', 'fab', 'btn-modern', 'gradient-text'
    ]
    
    css_files = [
        'static/css/mediconnect-professional.css',
        'static/css/mediconnect-enhanced-viz.css'
    ]
    
    defined_classes = set()
    
    for css_file in css_files:
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract class definitions
            class_matches = re.findall(r'\.([a-zA-Z0-9_-]+)\s*{', content)
            defined_classes.update(class_matches)
    
    missing_classes = []
    for cls in required_classes:
        if cls not in defined_classes:
            missing_classes.append(cls)
    
    if missing_classes:
        print("❌ Missing CSS Classes:")
        for cls in missing_classes:
            print(f"    .{cls}")
        return False
    else:
        print("✅ All required CSS classes are defined")
        return True

def test_css_variables():
    """Test that all CSS variables used in templates are defined"""
    print("\n🔧 Testing CSS Variables...")
    
    required_variables = [
        '--gradient-primary', '--gradient-info', '--gradient-success',
        '--gradient-warning', '--gradient-danger', '--gray-50', '--gray-100'
    ]
    
    css_files = [
        'static/css/mediconnect-professional.css',
        'static/css/mediconnect-enhanced-viz.css'
    ]
    
    defined_variables = set()
    
    for css_file in css_files:
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract CSS variable definitions
            var_matches = re.findall(r'(--[a-zA-Z0-9_-]+):', content)
            defined_variables.update(var_matches)
    
    missing_variables = []
    for var in required_variables:
        if var not in defined_variables:
            missing_variables.append(var)
    
    if missing_variables:
        print("❌ Missing CSS Variables:")
        for var in missing_variables:
            print(f"    {var}")
        return False
    else:
        print("✅ All required CSS variables are defined")
        return True

def test_route_functions():
    """Test that all route functions referenced in templates exist"""
    print("\n🛣️  Testing Route Functions...")
    
    # Check if app.py exists and contains required routes
    if not os.path.exists('app.py'):
        print("❌ app.py not found")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    required_routes = [
        'patient_dashboard', 'doctor_dashboard', 'admin_dashboard',
        'possible_conditions', 'consult_doctor', 'patient_appointments',
        'consultation_history', 'patient_medical_records', 'patient_profile',
        'doctor_consultations', 'doctor_appointments', 'doctor_availability',
        'doctor_feedback', 'admin_verify_doctors', 'admin_users',
        'admin_consultations', 'admin_reports', 'admin_settings'
    ]
    
    missing_routes = []
    for route in required_routes:
        if f'def {route}(' not in app_content:
            missing_routes.append(route)
    
    if missing_routes:
        print("❌ Missing Route Functions:")
        for route in missing_routes:
            print(f"    {route}()")
        return False
    else:
        print("✅ All required route functions are defined")
        return True

def test_dashboard_consistency():
    """Test that all dashboards follow the same structure"""
    print("\n📊 Testing Dashboard Consistency...")
    
    dashboard_files = [
        'templates/patient_dashboard.html',
        'templates/doctor_dashboard.html', 
        'templates/admin_dashboard.html'
    ]
    
    consistency_checks = []
    
    for file_path in dashboard_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checks = {
                'extends_base_modern': 'base_modern.html' in content,
                'has_hero_section': 'Welcome Hero' in content or 'py-5' in content,
                'has_quick_stats': 'Quick Stats' in content,
                'has_dashboard_grid': 'dashboard-grid' in content,
                'has_fab': 'fab' in content,
                'uses_gradient_primary': 'var(--gradient-primary)' in content
            }
            
            consistency_checks.append((file_path, checks))
    
    # Check consistency across all dashboards
    all_consistent = True
    for check_name in ['extends_base_modern', 'has_hero_section', 'has_quick_stats', 'has_dashboard_grid', 'has_fab']:
        values = [checks[check_name] for _, checks in consistency_checks]
        if not all(values):
            print(f"❌ Inconsistent {check_name}:")
            for file_path, checks in consistency_checks:
                status = "✓" if checks[check_name] else "✗"
                print(f"    {status} {file_path}")
            all_consistent = False
    
    if all_consistent:
        print("✅ All dashboards follow consistent structure")
        return True
    else:
        return False

def test_database_schema():
    """Test that database schema supports dashboard functionality"""
    print("\n🗄️  Testing Database Schema...")
    
    if not os.path.exists('medical.db'):
        print("❌ Database file not found")
        return False
    
    try:
        conn = sqlite3.connect('medical.db')
        cursor = conn.cursor()
        
        # Check required tables
        required_tables = ['users', 'patients', 'doctors', 'consultations', 'appointments']
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        for table in required_tables:
            if table not in existing_tables:
                missing_tables.append(table)
        
        if missing_tables:
            print("❌ Missing Database Tables:")
            for table in missing_tables:
                print(f"    {table}")
            return False
        else:
            print("✅ All required database tables exist")
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def run_all_tests():
    """Run all dashboard tests"""
    print("🚀 Starting MediConnect Dashboard Tests\n")
    
    tests = [
        test_template_syntax,
        test_css_classes,
        test_css_variables,
        test_route_functions,
        test_dashboard_consistency,
        test_database_schema
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print(f"\n📋 Test Summary:")
    print(f"   Passed: {sum(results)}/{len(results)}")
    print(f"   Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! Dashboards are ready for use.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = run_all_tests()
    sys.exit(0 if success else 1)