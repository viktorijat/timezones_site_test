from timezones_site.settings import *

# Test runner with no database creation
TEST_RUNNER = 'timezones_site.scripts.testrunner.NoDbTestRunner'

# Use an alternative database as a safeguard against accidents
DATABASES['default']['NAME'] = '_test_mysite_db'