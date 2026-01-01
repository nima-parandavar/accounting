from typing import Annotated
from typer import Typer, Argument
from rich import print as rprint
import asyncio
from auth.models import User, UserRole
from config.db import AsyncSessionLocal

auth_cli = Typer()


@auth_cli.command("create-admin")
def create_admin(
    first_name: Annotated[str, Argument(help="User first name")],
    email: Annotated[str, Argument(help="User email")],
    phone_number: Annotated[str, Argument(help="User phone number")],
    password: Annotated[str, Argument(help="User password")]
):
    print(type(password), password)
    async def run_():
        rprint("[red]Creating admin user[/red]")
        async with AsyncSessionLocal() as session:
            user = User(email=email, phone_number=phone_number, role=UserRole.ADMIN, first_name=first_name,)
            user.set_password(password=password)

            session.add(user)
            await session.commit()
            await session.refresh(user)
        rprint("[green]Admin user created successfully[/green]")

    asyncio.run(run_())
    
