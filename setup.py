from setuptools import setup

setup(
    name='pgtune',
    version='0.1.0',    
    description='A python module that helps you tune your postgres db',
    url='',
    author='Satyajit Sarangi',
    author_email='satyajit@zerodha.com',
    license='BSD 2-clause',
    packages=['pgtune'],
    install_requires=['psycopg2',                     
                      ],
entry_points={
        'console_scripts': [
            'pgtune=pgtune.tuner:run'
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)