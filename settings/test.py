TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--verbosity=1',
    '--nologcapture',  # prevent sql log capturing (dont want to be flooded)
    '--with-id',  # it is always handy to be able to run test by it's number
    '--with-timer',  # to enable execution time reporting
    '--timer-ok=100ms',  # good tests should run faster than 100ms
    '--timer-warning=1s',  # but  it is a problem if it takes more than 1s
    '--timer-top-n=10',  # show only top ten slowest tests, do not flood output
]

# To speedup tests
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

FEATURE_AUTO_SYNC_USER_POSITION_GROUP = False
