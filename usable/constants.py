
LANGUAGE = (
    ("English", "English"),
    ("Nepali", "Nepali"),
)

LEVEL = (
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advanced", "Advanced"),
)


TEACHER_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Published", "Published"),
)

PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Processing", "Processing"),
    ("Failed", "Failed"),
)


CLASS_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('private', 'Private'),
    ]

DURATION_FORMAT_CHOICES = [
        ('hours', 'Hours'),
        ('days', 'Days'),
    ]




CATEGORY = (
        ('CoffeeShopMenuCategory', 'CoffeeShopMenuCategory'),
        ('PhysicalCourseCategory', 'PhysicalCourseCategory'),
    )



GENDER_OPTIONS = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )

STATE_CHOICES = (
    ("koshi", "Koshi"),
    ("madhesh", "Madhesh"),
    ("bagmati", "Bagmati"),
    ("gandaki", "Gandaki"),
    ("lumbini", "Lumbini"),
    ("karnali", "Karnali"),
    ("sudurpaschim", "Sudurpaschim"),
)
