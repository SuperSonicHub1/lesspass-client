from requests import Session

API_BASE = 'https://api.lesspass.com'
class LessPassClient:
	"""
	A very simple implementation of the LessPasss API.
	It can only authenticate and get all of a user's passwords.
	Would be nice if it could add, update, and remove passwords,
	but that's for another time.
	"""

	def __init__(self, email: str, password: str, session: Session = Session()):
		self.email = email
		self.password = password
		self.session = session
		self.authenticate(self.email, self.password)

	def authenticate(self, email: str, password: str):
		res = self.session.post(f'{API_BASE}/auth/jwt/create/', json={'email': email, 'password': password})
		res.raise_for_status()

		self.token = res.json()["access"]

	def passwords(self):
		res = self.session.get(f'{API_BASE}/passwords/', headers={'Authorization': f'JWT {self.token}'})
		res.raise_for_status()
		return res.json()["results"]

if __name__ == "__main__":
	from netrc import netrc
	from pprint import pprint as print

	rc = netrc()
	login, _, password = rc.authenticators("lesspass")
	client = LessPassClient(login, password)

	passwords = client.passwords()
	print(passwords)
