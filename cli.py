from typer import Typer
from clis import auth_cli


cli = Typer()
cli.add_typer(auth_cli, name="auth")

if __name__ == '__main__':
    cli()