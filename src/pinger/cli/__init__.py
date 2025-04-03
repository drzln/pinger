import typer
from pinger.app import app


this_cli = typer.Typer(no_args_is_help=True)


@this_cli.command("status")
def status():
    """get a status"""
    print("asaok")


@this_cli.command("run")
def run():
    """run app from cli"""
    app().run()


this_cli()
