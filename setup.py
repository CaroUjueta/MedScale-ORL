from setuptools import setup, find_packages

setup(
    name="MedScale-ORL",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.2.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
    ],
    author="",
    description="Aplicación de escalas clínicas ORL",
)
