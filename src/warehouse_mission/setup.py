from setuptools import setup

package_name = 'warehouse_mission'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='owl',
    maintainer_email='owl@todo.todo',
    description='Warehouse mission manager',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'warehouse_autonomy = warehouse_mission.warehouse_mission_manager:main',
        ],
    },
)
