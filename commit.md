Improve error handling.

- Change all HttpResponseBadRequest
  to SuspiciousOperation so bad API usage
  alerts the admin from the firewall side too.
- Update tests to check admin email subject.
- Remove OperationalError from ipset/apps.py
