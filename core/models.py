import random
import re
import string
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from django.templatetags.static import static
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


POSITION_MS = "MAS"
POSITION_PHD = "PHD"
POSITION_INTEGRATED = "INT"
POSITION_POSTDOC = "POS"
POSITION_VISITING = "VIS"
POSITION_PROFESSOR = "PRO"
position_choices = [
    (POSITION_PROFESSOR, "Professor"),
    (POSITION_POSTDOC, "Postdoctoral Researcher"),
    (POSITION_PHD, "Ph.D. Student"),
    (POSITION_MS, "Master Student"),
    (POSITION_INTEGRATED, "Integrated Ph.D. Student"),
    (POSITION_VISITING, "Visiting Researcher"),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=3, choices=position_choices)
    position_start_date = models.DateField("Join date", null=True,
                                           help_text="If you are a graduate student or alumni, enter your admission date for your current course. Use YYYY-03-01 for Spring admission and YYYY-09-01 for Fall admission.")
    position_end_date = models.DateField("Depart date", blank=True, null=True,
                                         help_text="If you are a graduate alumni, enter your final graduation date. Use YYYY-02-28 for Spring graduation and YYYY-08-31 for Fall graduation.")
    department = models.CharField(max_length=100, default="KAIST AI",
                                  help_text="If you are a graduate student or alumni, enter your department at KAIST. E.g., 'KAIST AI', 'Industrial & Systems Engineering', 'Knowledge Service Engineering'.",
                                  blank=True, null=True)
    visiting_title = models.CharField(max_length=100,
                                      help_text="If you are a visiting reserach, enter a custom title. Please use abbreviations for department names. E.g., 'UG at KAIST CS', 'PhD at SNU CS'.",
                                      blank=True, null=True)
    degree = models.CharField(max_length=100, default="Artificial Intelligence",
                              help_text="If you are a graduate alumni, enter the name of your final degree. E.g., (MS in) 'Artificial Intelligence', (PhD in) 'Artificial Intelligence'. Do not include 'MS in', etc.",
                              blank=True, null=True)

    profile_image = models.ImageField(blank=True, null=True,
                                      help_text="Please upload images with a 1:1 aspect ratio and minimum resolution of 500x500.")
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    scholar = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True, help_text="E.g., '010-0000-0000'")
    secondary_email = models.EmailField(blank=True, null=True)
    research_topics = models.TextField(max_length=500, blank=True, null=True,
                                       help_text="Examples: CV, NLP, Theory, Data Centric, FL, RL, GNN, Few-Shot, LLM, AutoML, SSL.")

    current_position = models.CharField(max_length=100, blank=True, null=True,
                                        help_text="If you are a graduate alumni, enter your current job. Examples: 'Research Scientist, Google', 'Assistant Professor, Seoul National University'")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @staticmethod
    def full_name_exists(full_name: str):
        if full_name in ["Se-Young Yun", "Stephen Cha"]:
            return True

        # Annotate the query with a concatenated field
        users = User.objects.annotate(
            full_name_concat=Concat('first_name', V(' '), 'last_name', output_field=CharField())
        )

        # Process the concatenated field in a similar way as the search string and compare
        matched_users = users.filter(
            full_name_concat__iexact=full_name.lower(),
        )

        # Check if there's a match
        return matched_users.exists()

    @property
    def is_member(self):
        return self.position in [POSITION_MS, POSITION_PHD, POSITION_INTEGRATED, POSITION_POSTDOC]

    course_shorthands = {
        POSITION_MS: "MS",
        POSITION_INTEGRATED: "MS/PhD",
        POSITION_PHD: "PhD",
        POSITION_POSTDOC: "Postdoc",
    }

    @property
    def course_shorthand(self):
        try:
            return self.course_shorthands[self.position]
        except KeyError:
            return "N/A"

    @property
    def graduation_semester(self):
        if self.position_end_date == POSITION_VISITING:
            return None
        if not self.position_end_date or datetime.now().date() < self.position_end_date:
            return None
        if 1 <= self.position_end_date.month <= 5:
            return "Spring {}".format(self.position_end_date.year)
        else:
            return "Fall {}".format(self.position_end_date.year)

    @property
    def entry_semester(self):
        if not self.position_start_date:
            return None
        if 1 <= self.position_start_date.month <= 5:
            return "Spring {}".format(self.position_start_date.year)
        else:
            return "Fall {}".format(self.position_start_date.year)

    @property
    def is_alumni(self):
        return bool(self.graduation_semester)

    @property
    def display_period(self):
        if self.position == POSITION_VISITING:
            if self.position_end_date and self.position_start_date.year < self.position_end_date.year:
                return "Visiting · {} - {}".format(
                    self.position_start_date.year,
                    self.position_end_date.year,
                )
            else:
                return "Visiting · {}".format(
                    self.position_start_date.year,
                )
        else:
            if self.entry_semester:
                if self.graduation_semester:
                    return "{}·{}".format(self.course_shorthand, self.graduation_semester)
                else:
                    return "{}·{}".format(self.course_shorthand, self.entry_semester)

    @property
    def display_research_topics(self):
        if self.research_topics:
            topics = self.research_topics.split(", ")
            if len(topics) > 3:
                topics = topics[:3] + ["..."]
            return topics
        else:
            return []

    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return static("core/images/default_profile.png")

    @property
    def name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return None

    @property
    def is_phd(self):
        return self.position in [POSITION_PHD, POSITION_INTEGRATED, POSITION_POSTDOC]

    @property
    def has_member_permissions(self):
        return self.is_staff or self.position in [POSITION_MS, POSITION_PHD, POSITION_INTEGRATED, POSITION_POSTDOC,
                                                  POSITION_PROFESSOR]

    @property
    def has_phd_permissions(self):
        return self.is_staff or self.position in [POSITION_PHD, POSITION_INTEGRATED, POSITION_POSTDOC,
                                                  POSITION_PROFESSOR]

    @property
    def position_active(self):
        started = self.position_start_date and self.position_start_date < datetime.now().date()
        did_not_end = not self.position_end_date or self.position_end_date >= datetime.now().date()
        return started and did_not_end

    @property
    def position_ended(self):
        return self.position_end_date and self.position_end_date < datetime.now().date()


def generate_invitation_code(n=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(n))


def generate_admin_token(n=40, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(n))


def generate_password_reset_token(n=40, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(n))


class InvitationCode(models.Model):
    code = models.CharField(max_length=20, default=generate_invitation_code)
    position = models.CharField(max_length=3, choices=position_choices)
    uses_remaining = models.IntegerField(default=1)

    def __str__(self):
        return "[{}] {} ({} uses remaining)".format(self.get_position_display(), self.code, self.uses_remaining)


class PublicationTag(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name="publication_tags_created")
    last_modified_by = models.ForeignKey(User, models.SET_NULL, null=True)

    name = models.TextField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class PasswordResetToken(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, models.CASCADE)
    token = models.CharField(max_length=40, default=generate_password_reset_token)

    def __str__(self):
        return self.user.name


class Publication(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name="publications_created")
    last_modified_by = models.ForeignKey(User, models.SET_NULL, null=True)

    title = models.TextField()
    published_date = models.DateField(
        help_text="Date of publication, used for year grouping. Enter the conference start date for conferences.")
    accepted_date = models.DateField(help_text="Date of acceptance, used for sorting.")
    authors = models.TextField(help_text="E.g., 'Yoshua Bengio, Yann LeCun and Geoffrey Hinton'")
    venue = models.TextField(
        help_text="Use abbreviations for top-tier AI conferences. Add parentheses around the publication year for journal articles. E.g., 'NeurIPS (Oral) 2020', 'NeurIPS Workshop: \"Competition Track on Black-Box Optimization Challenge\" 2020', 'Nature (2020)', 'IEEE Transactions on Wireless Communications (2020)'")
    image = models.ImageField(blank=True, null=True)

    TYPE_INTERNATIONAL_CONFERENCE = "CON"
    TYPE_INTERNATIONAL_CONFERENCE_WORKSHOP = "WOR"
    TYPE_INTERNATIONAL_JOURNAL = "JRN"
    TYPE_DOMESTIC_CONFERENCE = "KCO"
    TYPE_DOMESTIC_JOURNAL = "KJR"
    type_choices = [
        (TYPE_INTERNATIONAL_CONFERENCE, "International Conference"),
        (TYPE_INTERNATIONAL_CONFERENCE_WORKSHOP, "International Conference (Workshop)"),
        (TYPE_INTERNATIONAL_JOURNAL, "International Journal"),
        (TYPE_DOMESTIC_JOURNAL, "Domestic Journal"),
        (TYPE_DOMESTIC_CONFERENCE, "Domestic Conference"),
    ]
    type = models.CharField(max_length=3, choices=type_choices)

    tags = models.ManyToManyField(PublicationTag, "Tags", blank=True)

    pdf_link = models.URLField(null=True, blank=True)
    code_link = models.URLField(null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)

    public = models.BooleanField(default=False)

    @property
    def display_author_list(self):
        def trim_non_alpha(s):
            # Remove non-alphabetic characters from the start and end of the string
            return re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', s)

        authors = self.authors.replace(" and ", ",").split(",")
        authors = list(filter(lambda a: a.strip(), authors))
        # TODO: optimize this
        authors = [
            {
                "name": author,
                "member": User.full_name_exists(trim_non_alpha(author)),
                "first": author.find("*") != -1,
            } for author in authors
        ]
        return authors

    def __str__(self):
        return '({}) {} et al., {}'.format(self.published_date.year, self.authors.split(",")[0], self.title)

    type_tags = {
        "CON": "Conference",
        "JRN": "Journal",
        "WOR": "Workshop",
        "KCO": "Domestic Conference",
        "KJR": "Domestic Journal",
    }

    @property
    def type_tag(self):
        try:
            return self.type_tags[self.type]
        except KeyError:
            return None


class Project(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name="projected_created")
    last_modified_by = models.ForeignKey(User, models.SET_NULL, null=True)

    title = models.TextField()
    organization = models.TextField()
    members = models.TextField(help_text="E.g., 'Yoshua Bengio, Yann LeCun and Geoffrey Hinton'")
    previous_members = models.TextField(help_text="E.g., 'Yoshua Bengio, Yann LeCun and Geoffrey Hinton'", blank=True,
                                        null=True)
    image = models.ImageField()
    summary = models.TextField(max_length=800)

    start_date = models.DateField()
    end_date = models.DateField()

    priority = models.IntegerField(default=0, help_text="Higher comes first")

    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Award(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name="awards_created")
    last_modified_by = models.ForeignKey(User, models.SET_NULL, null=True)

    name = models.CharField("Award name", max_length=100)
    awardees = models.TextField(help_text="E.g., 'Yoshua Bengio, Yann LeCun and Geoffrey Hinton'")
    awarded_date = models.DateField()
    venue = models.TextField(blank=True, null=True)
    paper = models.TextField("Paper title", blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    public = models.BooleanField(default=False)

    pdf_link = models.URLField(null=True, blank=True)
    code_link = models.URLField(null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name="photos_created")
    last_modified_by = models.ForeignKey(User, models.SET_NULL, null=True)

    image = models.ImageField()
    taken_date = models.DateField()
    description = models.TextField(max_length=200)
    public = models.BooleanField(default=False)

    starred = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Post(models.Model):
    """
    News post
    """
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.SET_NULL, null=True, related_name="news_created")
    last_modified_by = models.ForeignKey(User, models.SET_NULL, null=True)

    published_date = models.DateField(default=now)
    title = models.TextField()
    body = models.TextField(help_text="This will be displayed on the website as raw HTML.", null=True, blank=True)


class AdminToken(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    token = models.CharField(max_length=40, default=generate_admin_token)

    def __str__(self):
        return self.token


class GPUStatus(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    server_name = models.TextField(max_length=100)
    status = models.TextField()

    def __str__(self):
        return "[{}] {}".format(self.server_name, self.created_date.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        verbose_name_plural = "GPU status"
