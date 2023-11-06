import setuptools

with open('README.md','r', encoding='utf-8') as f:
    long_description = f.read()
    
setuptools.setup(
    name='fluids',
    version='0.0.1',
    author='Wolfgang Meiners',
    author_email='wolfgangmeiners@googlemail.com',
    #packages=['fluids'],
    description='Use Properties of Fluids in Jupyter Notebooks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wolfgang_302/fluids',
    project_urls={
        'Bug Tracker': 'https://github.com/wolfgang_302/fluids/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'':'.'},
    packages=setuptools.find_packages(where='.'),
    python_requires='>=3.8',
    install_requires=[
        'CoolProp',
        'numpy',
        'pandas',
        'matplotlib',
        'pint',
    ]
    
)
