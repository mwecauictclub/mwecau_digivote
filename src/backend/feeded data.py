from core.models import User, CollegeData, Course, State
from election.models import Election

# Create superuser (commissioner)
commissioner = User.objects.create_superuser(
    registration_number='T/ADMIN/2020/0002',
    email='admin@mail.com',
    password='adminpass'
)

# Create State and Course
state = State.objects.create(name='Kifumbu')
course = Course.objects.create(name='Computer Science', code='CS100')

# Create CollegeData
CollegeData.objects.create(
    registration_number='T/DEG/2020/0003',
    first_name='Neema',
    last_name='John',
    email='neema@mail.com',
    course=course,
    uploaded_by=commissioner
)

# Create an active election (for voter tokens)
Election.objects.create(
    title='Student Election 2025',
    start_date='2025-08-01',
    end_date='2025-08-30',
    is_active=True,
    has_ended=False
)