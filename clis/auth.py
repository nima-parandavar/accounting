from typing import Annotated
from typer import Typer, Argument, Exit
from rich import print as rprint
import asyncio
from auth.models import User, UserRole
from config.db import AsyncSessionLocal
from core.utils import normalize_phone_number

auth_cli = Typer()


@auth_cli.command("create-admin")
def create_admin(
    first_name: Annotated[str, Argument(help="User first name")],
    email: Annotated[str, Argument(help="User email")],
    phone_number: Annotated[str, Argument(help="User phone number")],
    password: Annotated[str, Argument(help="User password")],
):

    async def run_():
        rprint("[red]Creating admin user[/red]")
        n_phone_number = normalize_phone_number(phone_number)
        async with AsyncSessionLocal() as session:
            user = User(
                email=email,
                phone_number=n_phone_number,
                role=UserRole.ADMIN,
                first_name=first_name,
            )
            user.set_password(password=password)

            session.add(user)
            await session.commit()
            await session.refresh(user)
        rprint("[green]Admin user created successfully[/green]")
        Exit()

    asyncio.run(run_())
    
