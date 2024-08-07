from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import sys

# Module name
module_name = "pynpmi"

# Module extension configuration
ext_modules = [
    Pybind11Extension(
        module_name,
        ["pynpmi.cpp"],  # Name of your C++ source file
        extra_compile_args=[
            "-O3",  # Use maximum optimization level O3
            "-march=native",  # Enable code generation that leverages the most advanced instructions on the local machine
            "-ffast-math",  # Allow the compiler to use faster, less precise math calculations
        ],
        language="c++",
    ),
]

setup(
    name=module_name,
    version="0.1.0",
    description="A module to calculate NPMI using pybind11 and C++",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
