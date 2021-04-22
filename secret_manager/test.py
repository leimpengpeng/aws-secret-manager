import click
from getpass import getpass
# Command Group
@click.group(name='tools')
def cli():
    """Tool related commands"""
    pass

@cli.command(name='create_secret')
def create_secret():
    name=getpass('Secretname: ')
    SecretString=getpass('SecretString: ')
    print('Hello world', name, SecretString)


if __name__ == '__main__':
    cli()