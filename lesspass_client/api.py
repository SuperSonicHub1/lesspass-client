from typing import List
from requests import Session

DEFAULT_API_DOMAIN = 'api.lesspass.com'
class LessPassClient:
	"""
	A very simple implementation of the LessPasss API.
	It can only authenticate and get all of a user's passwords.
	Would be nice if it could add, update, and remove passwords,
	but that's for another time.
	"""

	def __init__(self, email: str, password: str, api_domain: str = DEFAULT_API_DOMAIN, session: Session = Session()) -> None:
		self.email = email
		self.password = password
		self.session = session
		self.api_domain = api_domain
		self.authenticate(self.email, self.password)

	def authenticate(self, email: str, password: str) -> None:
		res = self.session.post(f'https://{self.api_domain}/auth/jwt/create/', json={'email': email, 'password': password})
		res.raise_for_status()

		self.token = res.json()["access"]

	def passwords(self) -> List[dict]:
		res = self.session.get(f'https://{self.api_domain}/passwords/', headers={'Authorization': f'JWT {self.token}'})
		res.raise_for_status()
		return res.json()["results"]

	def create_password(self, site: str, login: str, lowercase: bool = True,  uppercase: bool = True, numbers: bool = True, symbols: bool = True, counter: int = 1, length: int = 16) -> dict:
		password = {
			"site": site,
			"login": login,
			"lowercase": lowercase,
			"uppercase": uppercase,
			"number": numbers,
			"symbol": symbols,
			"counter": counter,
			"length": length,
        	}
		res = self.session.post(f'https://{self.api_domain}/passwords/', headers={'Authorization': f'JWT {self.token}'}, json=password)
		res.raise_for_status()
		return res.json()

if __name__ == "__main__":
	from netrc import netrc
	from pprint import pprint as print
	from sys import argv

	rc = netrc()
	login, _, password = rc.authenticators("lesspass")
	client = LessPassClient(login, password)

	if len(argv) > 1:
		if argv[1] == "create":
			info = client.create_password("example.org", "example@example.org")
			print(info)

	passwords = client.passwords()
	print(passwords)
