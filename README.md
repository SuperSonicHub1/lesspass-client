 # LessPass Client

> A [LessPass][lesspass] client written in Python heavily 
inspired by [lastpass-cli][lastpass-cli].

## Installation

### Git
```
git clone https://github.com/supersonichub1/lesspass-client
cd lesspass-client
poetry install
```

## Help
Run `lesspass-client --help` for the most up-to-date information.

### .netrc

Use of a [`.netrc` file][netrc] for supplying your LessPass login and master
password is **required**. There is currently no way to supply either using
command line arguments or environment variables; both of these methods are
[insecure][secrets-command-line], anyways. Use the host `lesspass` for sharing
your username and password, and the host `lesspass_gen` for storing your master
password.

### `show --format`
The `show` subcommand allows for the customization of the command's output
through the `--format` option, a la `lpass show --format`. 
Instead of using `printf`-like formatting, `lesspass-client` instead uses 
[Python's format string syntax][format-string], which I believe is much
more intuitive and user friendly.

The format string supplies the following values:
* site
* login
* password
* created
* modified
* id
* version
* counter
* length
* uppercase
* lowercase
* numbers

For example, if you wanted to append your [Freesound][freesound] login to your
.netrc file:
```bash
lesspass-client show --site freesound.org \
--format "machine freesound login {login} password {password}" \
>> ~/.netrc
```

## What This Tool Isn't
* a complete replacement for [LessPass's exisiting CLI][lesspass-cli].
* a complete way to manage your LessPass passwords
* a 1-to-1 drop-in replacement for `lpass`

## Caveots
* doesn't support password encryption
* doesn't support LessPass servers outside of `api.lesspass.com`
* doesn't allow for the addition, updating, or removal of passwords

## TODO
* error handling
* more password operations
* configuration (encryprion, other servers, alternate `.netrc` locations)

[lesspass]: https://www.lesspass.com/
[lastpass-cli]: https://github.com/lastpass/lastpass-cli
[netrc]: https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html
[format-string]: https://docs.python.org/3/library/string.html#format-string-syntax
[freesound]: https://freesound.org/
[secrets-command-line]: https://smallstep.com/blog/command-line-secrets/
[lesspass-cli]: https://github.com/lesspass/lesspass#cli
