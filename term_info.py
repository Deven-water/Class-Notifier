import requests

TERMS_URL = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?offset=1&max=10&searchTerm="

courseTerms = requests.get(TERMS_URL, timeout=5)
print(courseTerms.json())
