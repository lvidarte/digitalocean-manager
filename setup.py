# Copyright 2025 Cloutfit.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

from digitalocean_manager.__version__ import __version__


setup(
    name='digitalocean-manager',
    version=__version__,
    description='Digital Ocean manager with CLI functionality',
    long_description=open('README.md').read(),  # Use a README for long description
    long_description_content_type='text/markdown',  # README is markdown
    author='The Cloutfit Team',
    author_email='dev@cloutfit.com',
    url='https://github.com/cloutfit/digitalocean-manager',
    packages=find_packages(),  # Automatically finds the packages in your project
    install_requires=[  # List any dependencies here
        'click==8.1.8',  # CLI interface
        'pydo==0.7.0',  # Digital Ocean API wrapper
        'PyYAML==6.0.2', # For settings main file and cloud init files
        'paramiko==3.5.0', # SSH
    ],
    entry_points={  # For CLI commands
        'console_scripts': [
            'dom = digitalocean_manager.main:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)