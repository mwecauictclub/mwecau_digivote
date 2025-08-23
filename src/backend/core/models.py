from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    """Define a model manager for User model with registration number authentication."""

    use_in_migrations = True

    def _create_user(self, registration_number, password, **extra_fields):
        """Create and save a User with the given registration number and password."""
        if not registration_number:
            raise ValueError('The given registration number must be set')
        
        # Normalize email if provided
        email = extra_fields.get('email')
        if email:
            extra_fields['email'] = self.normalize_email(email)
            
        user = self.model(registration_number=registration_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, registration_number, password=None, **extra_fields):
        """Create and save a regular User with the given registration number."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(registration_number, password, **extra_fields)

    def create_superuser(self, registration_number, password, **extra_fields):
        """Create and save a SuperUser with the given registration number."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(registration_number, password, **extra_fields)

    def create_from_college_data(self, college_data_id):
        """Create a User from CollegeData, generating a default password.
        # Added to support async user creation tasks with Celery, ensuring seamless conversion
        # from CollegeData to User with a secure default password.
        """
        from .models import CollegeData
        college_data = CollegeData.objects.get(id=college_data_id)
        if college_data.is_used:
            raise ValueError('College data already used')
        
        # Generate random password
        import secrets
        default_password = secrets.token_hex(8)
        
        user = self.create_user(
            registration_number=college_data.registration_number,
            password=default_password,
            first_name=college_data.first_name,  # Split full_name
            last_name=college_data.last_name,
            course=college_data.course,
            email=college_data.email,
            is_verified=False  # Require manual verification
        )
        
        college_data.mark_as_used()
        return user, default_password

class State(models.Model):
    """Model representing a state/region."""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'state_majimbo'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),  # Added index for faster lookups in analytics tasks
        ]

class Course(models.Model):
    """Model representing a course offered by the university."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        db_table = 'course'
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),  # Added index for faster lookups in tasks
        ]

class User(AbstractUser):
    """Custom User model with registration number authentication."""
    
    ROLE_VOTER = 'voter'
    ROLE_CANDIDATE = 'candidate'
    ROLE_CLASS_LEADER = 'class_leader'
    ROLE_COMMISSIONER = 'commissioner'
    
    ROLE_CHOICES = [
        (ROLE_VOTER, 'Voter'),
        (ROLE_CANDIDATE, 'Candidate'),
        (ROLE_CLASS_LEADER, 'Class Leader'),
        (ROLE_COMMISSIONER, 'Commissioner'),
    ]
    
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_OTHER = 'other'
    
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    ]
    
    # Remove username field and use registration_number for authentication
    username = None
    
    # Fields
    registration_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9/]+$',
            message='Registration number must contain only uppercase letters, numbers, or slashes.'
        )],  # Added validator for consistent format
        help_text="University registration number (e.g., MWU/1234/2023)"
    )
    email = models.EmailField(
        _('email address'),
        unique=True,  # Made unique to prevent duplicates and support notifications
        help_text="Required email for notifications and password resets"
    )
    voter_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="Optional voter identification number"
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text="User's gender for position eligibility"  # Added to support Position.gender_restriction
    )
    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User's state/region"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User's academic course"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_VOTER,
        help_text="User's role in the election system"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the user account is verified"
    )
    
    # Timestamps
    date_verified = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_voted = models.DateTimeField(null=True, blank=True)  # Added to track voting activity for debugging
    
    # Authentication settings
    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['email']  # Made email required
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.registration_number})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() if full_name.strip() else self.registration_number
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.registration_number
    
    # Role checking methods
    def is_voter(self):
        return self.role == self.ROLE_VOTER
    
    def is_candidate(self):
        return self.role == self.ROLE_CANDIDATE
    
    def is_class_leader(self):
        return self.role == self.ROLE_CLASS_LEADER
    
    def is_commissioner(self):
        return self.role == self.ROLE_COMMISSIONER
    
    # Permission helpers
    def can_vote(self):
        """Check if user can participate in voting."""
        return self.is_verified and (self.is_voter() or self.is_candidate())
    
    def can_manage_elections(self):
        """Check if user can manage elections."""
        return self.is_commissioner() or self.is_staff
    
    def can_upload_college_data(self):
        """Check if user can upload college data."""
        return self.is_class_leader() or self.is_commissioner() or self.is_staff
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['role', 'is_verified']),
            models.Index(fields=['state', 'course']),
            models.Index(fields=['email']),
            models.Index(fields=['gender']),  # Added for Position gender restriction queries
        ]

class CollegeData(models.Model):
    """Model for storing pre-uploaded college data by Class Leaders."""
    registration_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9/]+$',
            message='Registration number must contain only uppercase letters, numbers, or slashes.'
        )]  # Added validator for consistency with User
    )
    first_name = models.CharField(max_length=50)  # Split full_name for User compatibility
    last_name = models.CharField(max_length=50)  # Split full_name
    email = models.EmailField(
        unique=True,  # Added to ensure valid user creation
        help_text="Required email for user account creation"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': [User.ROLE_CLASS_LEADER, User.ROLE_COMMISSIONER]},
        help_text="Class leader or commissioner who uploaded this data"
    )
    is_used = models.BooleanField(
        default=False,
        help_text="Whether this data has been used to create a user account"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('failed', 'Failed'),
        ],
        default='pending',
        help_text="Processing status for async tasks"  # Added for Celery task tracking
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.registration_number})"
    
    def mark_as_used(self):
        """Mark this college data as used for user creation."""
        self.is_used = True
        self.status = 'processed'
        self.save(update_fields=['is_used', 'status'])
    
    class Meta:
        db_table = 'college_data'
        verbose_name = 'College Data'
        verbose_name_plural = 'College Data'
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['course', 'is_used']),
            models.Index(fields=['status']),  # Added for task status queries
        ]