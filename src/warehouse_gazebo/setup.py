from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'warehouse_gazebo'

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

model_files = package_files('models')

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    (os.path.join('share', package_name, 'models'), model_files),
]

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='owl',
    maintainer_email='zesmaeili85@gmail.com',
    description='Warehouse Gazebo launch files',
    license='MIT',
    tests_require=['pytest'],
    entry_points={'console_scripts': []},
)
