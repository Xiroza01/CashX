import sys
from flask.sessions import SecureCookieSessionInterface
from app import create_app

app = create_app()
si = SecureCookieSessionInterface()
s = si.get_signing_serializer(app)
print(s.loads(sys.argv[1]))
