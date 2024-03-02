from setuptools import setup, find_packages

setup(
    name='APWikipedia',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-restful",
        "nltk",
        "flask_cors"
    ],
    entry_points={
        'console_scripts': [
            # 如果你有一个可以从命令行运行的脚本，可以在这里设置
            'apwikipedia=web_backend.app:main',
        ],
    },
)
