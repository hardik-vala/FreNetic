from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='FreNetic',
      version='0.1',
      description='The funniest joke in the world',
      long_description=readme(),
      classifiers=[],
      keywords='wordnet wolf sense synonymy lexicon words nlp',
      url='https://github.com/hardik-vala/FreNetic',
      author='Hardik Vala',
      # author_email='flyingcircus@example.com',
      license='MIT',
      packages=['frenetic'],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
