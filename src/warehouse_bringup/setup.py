from setuptools import setup
import os
from glob import glob

package_name = 'warehouse_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='owl',
    maintainer_email='owl@example.com',
    description='Warehouse bringup launch files',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'warehouse_autonomy = warehouse_bringup.warehouse_autonomy_node:main',
    ],
    },
)
