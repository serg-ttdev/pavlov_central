from setuptools import setup, find_packages


with open('requirements.txt') as requirements:
    install_requires = []
    dependency_links = []
    for line in requirements:
        if line.startswith('-e git+') or line.startswith('git+'):
            dependency_links.append(line)
        elif line.startswith('--'):
            pass
        else:
            install_requires.append(line)

setup(
    name='pavlov_central',
    version='0.1.0',
    author='RoseNimbus',
    author_email='s.yermolaev@gmail.com',
    description='Pavlov Game portal',
    packages=find_packages(exclude=['example', 'test']),
    install_requires=install_requires,
    package_data={
        '': ['*.json'],
        'pavlov_central.api': ['openapi/*.yaml'],
        'pavlov_central.storage': ['migrations/*'],
    },
    dependency_links=dependency_links
)
