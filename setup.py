import os
import zipfile

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

PACKAGE_NAME = "myanmar-location"


class my_build_py(build_py):
    """Custom build step to unzip packaged parquets."""

    def run(self) -> None:
        src_dir = os.path.abspath(os.path.join("src", PACKAGE_NAME))
        zip_path = os.path.join(src_dir, "mimu_geo.zip")

        if not os.path.exists(zip_path):
            error_msg = f"Missing '{zip_path}. Ensure package was built correctly."
            raise FileNotFoundError(error_msg)

        extract_to = os.path.join(src_dir, "data")
        if not os.path.exists(extract_to):
            raise FileNotFoundError(
                f"Directory {extract_to} not found. Ensure package was built correctly."
            )

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        os.remove(zip_path)

        super().run()


_ = setup(
    name=PACKAGE_NAME,
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=("test*", "testing*", "tests*")),
    cmdclass={"build_py": my_build_py},
    include_package_data=True,
    package_data={PACKAGE_NAME: ["mimu_geo.zip"]},
)
