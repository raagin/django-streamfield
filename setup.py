import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-streamfield",
    version="2.4.0",
    author="Yury Lapshinov",
    author_email="y.raagin@gmail.com",
    description="StreamField for native Django Admin or with Grappelli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raagin/django-streamfield",
    packages=setuptools.find_packages(exclude=['test_project', 'frontend']),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2"
    ],
)