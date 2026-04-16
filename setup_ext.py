from setuptools import setup, Extension
import sys

# Windows (MSVC) uses /O2, Linux/Mac (GCC/Clang) uses -O3
compile_args = ['/O2'] if sys.platform == 'win32' else ['-O3']

fast_matcher_module = Extension(
    'error_translator.fast_matcher',
    sources=['src/error_translator/ext/fast_matcher.c'],
    extra_compile_args=compile_args
)

setup(
    name='error_translator_ext',
    version='1.0',
    description='C extensions for Error Translator',
    package_dir={'': 'src'},
    ext_modules=[fast_matcher_module]
)
