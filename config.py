import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_BASE_URL = "https://test.elements.gwu.edu:8092/"


@dataclass(frozen=True)
class ElementsSettings:
    username: str | None
    password: str | None
    base_url: str = DEFAULT_BASE_URL


def get_settings() -> ElementsSettings:
    """Load Elements connection settings from the environment."""
    load_dotenv()
    return ElementsSettings(
        username=os.getenv("ELEMENTS_USER"),
        password=os.getenv("ELEMENTS_PASSWORD"),
        base_url=os.getenv("ELEMENTS_BASE_URL", DEFAULT_BASE_URL),
    )