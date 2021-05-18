import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-streamfield",
    version="1.3.9",
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
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)