from .api import LessPassClient
from .boolean import BooleanOptionalAction
from netrc import netrc
from argparse import ArgumentParser
from lesspass.password import generate_password

def main():
	parser = ArgumentParser(
			prog="lesspass-client",
			description="Get passwords from your LessPass account.",
			epilog="This project requires the use of a .netrc file (lesspass for API, lesspass_gen for master password). For more info, see this project's README."
		)

	subparsers = parser.add_subparsers(help='Sub-command help', dest='command', required=True)

	parser_ls = subparsers.add_parser("ls", help="View your collection of passwords.")

	parser_show = subparsers.add_parser("show", help="Show a password.")

	lookup = parser_show.add_mutually_exclusive_group(required=True)
	lookup.add_argument("-s", "--site", help="The site a password belongs to.")
	lookup.add_argument("-i", "--id", help="The UUID a password belongs to.")

	parser_show.add_argument(
		"-f",
		"--format",
		help="Format this command's output using Python's format string syntax (https://docs.python.org/3/library/string.html#formatstrings); useful for command line parsing."
	)

	parser_add = subparsers.add_parser("add", help="Add a password profile.")

	parser_add.add_argument("site", help="Site of the password.")
	parser_add.add_argument("login", help="Login to the site (email, username).")
	parser_add.add_argument("--lowercase", action=BooleanOptionalAction, help="Have the password contain lowercase letters.", default=True)
	parser_add.add_argument("--uppercase", action=BooleanOptionalAction, help="Have the password contain uppercase letters.", default=True)
	parser_add.add_argument("--symbols", action=BooleanOptionalAction, help="Have the password contain symbols.", default=True)
	parser_add.add_argument("--numbers", action=BooleanOptionalAction, help="Have the password contain numbers.", default=True)
	parser_add.add_argument("-c", "--counter", type=int, help="The counter of the passowrd.", default=1)
	parser_add.add_argument("-l", "--length", type=int, help="The length of the passowrd.", default=16)

	args = parser.parse_args()

	rc = netrc()
	login, _, password = rc.authenticators("lesspass")
	_, _, master_password = rc.authenticators("lesspass_gen")
	client = LessPassClient(login, password)

	if args.command == "add":
		client.create_password(args.site, args.login, lowercase=args.lowercase,  uppercase=args.uppercase, numbers=args.numbers, symbols=args.symbols, counter=args.length, length=args.length)
		return

	passwords = client.passwords()

	HEADER_STRING="{site} [id: {id}]"

	if args.command == "ls":
		for password_info in passwords:
			string = HEADER_STRING.format(**password_info)
			print(string)
	elif args.command == "show":
		if args.site:
			password_info = [password_info for password_info in passwords if password_info["site"] == args.site][0]
		elif args.id:
			password_info = [password_info for password_info in passwords if password_info["id"] == args.id][0]

		# Lesspass's JSON response returns "numbers" instead of "digits",
		# so we'll need to fix that.

		if "numbers" in password_info and "digits" not in password_info:
			numbers = password_info["numbers"]
			password_info.update({"digits": numbers})

		password = generate_password(password_info, master_password)
		password_info.update({"password": password})

		if args.format:
			print(args.format.format(**password_info))
		else:
			print(HEADER_STRING.format(**password_info))
			print("Site:", password_info["site"])
			print("Login:", password_info["login"])
			print("Password:", password_info["password"])
