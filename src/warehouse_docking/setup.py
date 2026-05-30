from setuptools import setup

package_name = 'warehouse_docking'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='owl',
    maintainer_email='owl@todo.todo',
    description='Vision-guided docking controller',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vision_docking_controller = warehouse_docking.vision_docking_controller:main',
        ],
    },
)
