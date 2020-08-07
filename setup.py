from setuptools import find_packages, setup


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="django-filepreview",
    version="0.1",
    description="file preview for django files",
    long_description=readme(),
    url="https://basx.dev",
    author="basx Software Development Co., Ltd.",
    author_email="info@basx.dev",
    license="Private",
    install_requires=["preview-generator", "django"],
    setup_requires=["setuptools_scm"],
    use_scm_version={"write_to": "filepreview/version.py"},
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
)
