import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-streamfield",
    version="1.2.2",
    author="Yury Lapshinov",
    author_email="y.raagin@gmail.com",
    description="StreamField for native Django Admin or with Grappelli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raagin/django-streamfield",
    packages=setuptools.find_packages(exclude=['test_project']),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
    ],
)