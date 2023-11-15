import click
import os
from rich import print, pretty
import json

from codintxt.language import build_model, model_2_codin

pretty.install()

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command('validate', help='Model Validation')
@click.pass_context
@click.argument('model_path')
def validate(ctx, model_path):
    model = build_model(model_path)
    print('[*] Model validation success!!')


@cli.command('gen', help='M2T/M2M transformations')
@click.pass_context
@click.argument('model_path')
@click.argument('generator')
def generate(ctx, model_path, generator):
    if generator == 'codin':
        model = build_model(model_path)
        _model = model_2_codin(model)
        filepath = f'codin-{model.metadata.name}.json'
        with open(filepath, 'w') as fp:
            json.dump(_model, fp)


def main():
    cli(prog_name='codintxt')
