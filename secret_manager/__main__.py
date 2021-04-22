


import boto3
from . import get_common_config
import yaml
import click
from getpass import getpass
import re

@click.group()
def cli():
    pass

def secret_tags():
    config=get_common_config()
    return [
        dict(Key='ProjectCode', Value=config['ProjectCode']),
        dict(Key='Contact', Value=config['contact']),
        dict(Key='CostCenter', Value=config['cost_center']),
        dict(Key='DeploymentName', Value='testning'),
    ]

def parse_namespace(name):
    prefix_search = re.search("/", name)
    if not prefix_search:
        raise ValueError(f'Invalid format for the secret name: {name!r}, prefix is required')

    prefix = name.rsplit('/', 1)[0]

    # Prefix format: {reg}-{projectCode}-{ci|stg|prd}-{devname}  or {reg}-{projectCode}-{dev}-{devname}
    pattern = r'^(?P<reg>[a-z0-9]+)-(?P<projectCode>[idprot]+)-(?P<stage>dev|ci|stg|prd)(-?)(?P<devName>[a-z0-9-]+)*$'
    match = re.match(pattern, prefix)
    print(match)
    if not match:
        raise ValueError(f'Invalid prefix format: {prefix!r}')
    
    reg = match.group('reg')
    projectCode = match.group('projectCode')
    stage = match.group('stage')
    devName = match.group('devName')
    if devName:
        return f'{reg}-{projectCode}-{stage}-{devName}'

    return f'{reg}-{projectCode}-{stage}'

@cli.command(name='create')
@click.argument('name')
def create_secret(name):
    '''
    Create a secret
    '''
    secretValue = getpass('secretValue:')
    deploymentGroup = parse_namespace(name)
    tags = secret_tags()
    print(tags)
    tags.append(dict(Key='DeploymentGroup', Value=deploymentGroup))
    print(tags)
    # aws.create_secret(Name=secretName, SecretString=secretValue, Tags=secret_tags())


@cli.command(name='list')
def list_secrets():
    '''
    Print secret names
    '''
    config=get_common_config()
    kwargs = dict(Filters=[
            dict(Key='tag-key', Values=['ProjectCode']),
            dict(Key='tag-value', Values=[config['ProjectCode']]),
        ])

    resp = aws.list_secrets(**kwargs)
    # for secret in resp['SecretList']:
    #     print('\n\n\n\n\nPP1', secret.get('Name'))
    print('\n\n\n\nresp.g:', resp.get('NextToken'))
    return resp['SecretList'], resp.get('NextToken')


@cli.command(name='get')
@click.argument('name')
def get_secret_value(name):
    '''
    Get the value (SecretString) of the secret
    '''

    secret = aws.get_secret_value(SecretId=name)
    print('secret', secret['SecretString'])


@cli.command(name='update')
@click.argument('name')
def update_secret(name):
    '''
    Update the value (SecretString) of a secret
    '''
    value = getpass('SecretString: ')
    aws.put_secret_value(SecretId=name, SecretString=value)
    print('Secret updated')

@cli.command(name='delete')
@click.argument('name')
def delete_secret(name):
    '''
    delete a secret
    '''
    value = getpass('SecretString: ')
    aws.delete_secret(SecretId=name)
    print('Secret Deleted')


aws=boto3.client('secretsmanager')
config=get_common_config()
cli(prog_name='bin/idp_secretmanager')
