from setuptools import setup, find_packages, Extension
import sys

ext_modules = []
cmdclass = {}

if "--with-cpp" in sys.argv:
    sys.argv.remove("--with-cpp")
    try:
        from pybind11.setup_helpers import Pybind11Extension, build_ext
        ext_modules = [
            Pybind11Extension(
                "execution_cpp",
                ["cpp/execution_module.cpp"],
                cxx_std=11,
            ),
        ]
        cmdclass = {"build_ext": build_ext}
    except ImportError:
        print("Warning: pybind11 not found. Skipping C++ extension.")
        ext_modules = []

setup(
    name="execution_backtester",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "pyarrow>=5.0.0",
        "xgboost>=1.5.0",
        "matplotlib>=3.4.0",
        "jupyter>=1.0.0",
        "pytest>=6.2.0",
        "pybind11>=2.8.0",
    ],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "backtest=backtester.cli:main",
        ],
    },
)
