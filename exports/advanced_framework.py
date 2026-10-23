"""
Framework Python Avancé

Ce module illustre :
1. Les métaclasses pour le contrôle de structure et la validation de configuration.
2. La programmation asynchrone (asyncio) et les générateurs asynchrones.
3. Le typage avancé, les protocoles et les gestionnaires de contexte asynchrones.
"""

import asyncio
import logging
import time
from typing import Any, AsyncIterator, Dict, Generic, List, Type, TypeVar

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AdvancedFramework")

T = TypeVar("T")


class ConfigMeta(type):
    """Métaclasse garantissant que toute classe de configuration possède
    les attributs requis et un schéma valide.
    """
    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        required = attrs.get("_REQUIRED_FIELDS_", [])
        for field in required:
            if field not in attrs:
                raise TypeError(f"Champ requis manquant dans la configuration {name}: {field}")
        return super().__new__(mcs, name, bases, attrs)


class BaseConfig(metaclass=ConfigMeta):
    _REQUIRED_FIELDS_: List[str] = []


class AppConfig(BaseConfig):
    _REQUIRED_FIELDS_ = ["host", "port", "timeout"]
    
    host: str = "localhost"
    port: int = 8080
    timeout: float = 5.0


class AsyncPipeline(Generic[T]):
    """Pipeline de traitement asynchrone générique avec gestion de contexte."""
    def __init__(self, items: List[T]):
        self.items = items

    async def __aenter__(self) -> "AsyncPipeline[T]":
        logger.info("Initialisation du pipeline asynchrone...")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        logger.info("Fermeture et nettoyage du pipeline.")
        await asyncio.sleep(0.1)

    async def process_stream(self) -> AsyncIterator[Dict[str, Any]]:
        for index, item in enumerate(self.items):
            # Simulation d'une E/S asynchrone
            await asyncio.sleep(0.2)
            yield {
                "index": index,
                "data": item,
                "timestamp": time.time(),
                "status": "processed"
            }


async def main() -> None:
    # Validation de la configuration par métaclasse
    config = AppConfig()
    logger.info(f"Configuration validée : hôte={config.host}, port={config.port}")

    raw_data = ["alpha", "beta", "gamma", "delta", "omega"]
    
    # Utilisation du pipeline asynchrone
    async with AsyncPipeline(raw_data) as pipeline:
        async for result in pipeline.process_stream():
            logger.info(f"Élément traité : {result}")


if __name__ == "__main__":
    asyncio.run(main())
