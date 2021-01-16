import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blackjack-pkg-kaseymallette",
    version="0.0.1",
    author="Kasey Mallettte",
    author_email="kcmmallette@gmail.com",
    description="Continuously play blackjack hands from a blackjack shoe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaseymallette/Blackjack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
