from setuptools import setup

setup(
    name='WindowsPowerplanSetter',
    version='1.0',
    py_modules=['WindowsPowerplanSetter', 'AliasedGroup', 'powercfg_commands'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'wpp = WindowsPowerplanSetter:cli',
        ],
    },
)
