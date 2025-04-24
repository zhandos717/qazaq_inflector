from setuptools import setup, find_packages

# Читаем README для long_description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="qazaq_inflector",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,

    description="Склонение казахских имен по падежам",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Zhandos Zhandarbekov",
    author_email="zhandos.zhandarbekov@gmail.com",
    url="https://github.com/zhandos717/qazaq_inflector",
    license="MIT",

    keywords=["kazakh", "language", "grammar", "inflection"],
    python_requires=">=3.6",

    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
        ]
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],

    # Тесты в папке tests/, pytest автоматически их найдёт
)
