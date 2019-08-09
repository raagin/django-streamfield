import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-streamfield",
    version="1.0.6",
    author="Yury Lapshinov",
    author_email="y.raagin@gmail.com",
    description="StreamField for native Django Admin or with Grappelli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raagin/django-streamfield",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
    ],
)