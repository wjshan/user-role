import typer
import uvicorn

from .config import settings

cli = typer.Typer(name="user_role API")


@cli.command(name="run")
def run(
        port: int = settings.server.port,
        host: str = settings.server.host,
        log_level: str = settings.server.log_level,
        reload: bool = settings.server.reload,
        worker:int = 1
):  # pragma: no cover
    """Run the API server."""
    print(worker)
    uvicorn.run(
        "user_role.app:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        workers=worker,
    )
