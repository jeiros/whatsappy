from setuptools import setup, find_packages

setup(
    name='whatsappy',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    author='Juan Eiros',
    author_email='jeiroz@gmail.com',
    package_data={
        'whatsappy': ['README.md', 'requirements.txt']
    },
    include_package_data=True
)
