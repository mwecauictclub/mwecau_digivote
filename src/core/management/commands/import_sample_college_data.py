"""
Management command to import sample college data from CSV file.
Imports student enrollment data for testing purposes.

Usage:
    python manage.py import_sample_college_data --file data/csc_students_sample.csv
    python manage.py import_sample_college_data --dry-run  # Preview without saving
"""

import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import User, Course


class Command(BaseCommand):
    help = 'Import sample college student data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/csc_students_sample.csv',
            help='Path to CSV file containing student data (default: data/csc_students_sample.csv)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview import without saving to database',
        )
        parser.add_argument(
            '--course',
            type=str,
            default='MW009',
            help='Course code to associate with students (default: MW009 - Computer Science)',
        )

    def handle(self, *args, **options):
        csv_file = options['file']
        dry_run = options['dry_run']
        course_code = options['course']

        # Validate file exists
        if not os.path.exists(csv_file):
            raise CommandError(f'CSV file not found: {csv_file}')

        # Get course
        try:
            course = Course.objects.get(code=course_code)
        except Course.DoesNotExist:
            raise CommandError(f'Course not found: {course_code}')

        self.stdout.write(
            self.style.SUCCESS(f'\n📚 Starting import from: {csv_file}')
        )
        self.stdout.write(f'📖 Target course: {course.code} - {course.name}')
        self.stdout.write(f'🔄 Dry run mode: {"ON" if dry_run else "OFF"}\n')

        created_count = 0
        updated_count = 0
        error_count = 0
        errors = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                if not reader.fieldnames:
                    raise CommandError('CSV file is empty or has no headers')

                # Validate required columns
                required_fields = ['registration_number', 'name']
                missing_fields = [
                    field for field in required_fields 
                    if field not in reader.fieldnames
                ]
                if missing_fields:
                    raise CommandError(
                        f'CSV missing required columns: {", ".join(missing_fields)}'
                    )

                rows = list(reader)
                self.stdout.write(
                    f'📋 Found {len(rows)} rows in CSV\n'
                )

                with transaction.atomic():
                    for idx, row in enumerate(rows, 1):
                        try:
                            registration_number = row['registration_number'].strip()
                            name = row['name'].strip()

                            if not registration_number or not name:
                                error_count += 1
                                errors.append(
                                    f'Row {idx}: Missing registration_number or name'
                                )
                                continue

                            # Check if user exists
                            user, created = User.objects.get_or_create(
                                registration_number=registration_number,
                                defaults={
                                    'username': registration_number,
                                    'first_name': name.split()[0] if name.split() else 'Student',
                                    'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                                    'email': f'{registration_number}@mwecau.ac.tz',
                                    'is_active': True,
                                }
                            )

                            # Add course to user's courses
                            user.courses.add(course)

                            if created:
                                created_count += 1
                                status = '✓ Created'
                            else:
                                updated_count += 1
                                status = '↻ Updated'

                            # Print progress every 10 rows
                            if idx % 10 == 0:
                                self.stdout.write(
                                    f'{status}: {registration_number} - {name}'
                                )

                        except Exception as e:
                            error_count += 1
                            errors.append(f'Row {idx}: {str(e)}')

                # Only commit if not dry-run
                if dry_run:
                    transaction.set_rollback(True)
                    self.stdout.write(
                        self.style.WARNING('\n⚠️  DRY RUN MODE - Changes not saved to database')
                    )

        except IOError as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')

        # Print summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(
            self.style.SUCCESS(f'✓ Created: {created_count} new students')
        )
        self.stdout.write(
            self.style.SUCCESS(f'↻ Updated: {updated_count} existing students')
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'✗ Errors: {error_count}')
            )
        self.stdout.write('=' * 70)

        if errors and error_count <= 10:
            self.stdout.write('\nError details:')
            for error in errors[:10]:
                self.stdout.write(self.style.ERROR(f'  • {error}'))
            if len(errors) > 10:
                self.stdout.write(self.style.ERROR(f'  ... and {len(errors) - 10} more'))

        if not dry_run and (created_count > 0 or updated_count > 0):
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Successfully imported {created_count + updated_count} students '
                    f'for course {course.code}\n'
                )
            )
        elif dry_run:
            self.stdout.write(
                f'\n✓ Would import {created_count + updated_count} students '
                f'for course {course.code}\n'
            )
