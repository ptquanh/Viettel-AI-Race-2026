from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

setup(
    name='lfm_custom_ops',
    ext_modules=[
        CUDAExtension(
            name='lfm_custom_ops',
            sources=['lfm_fused_kernels.cu'],
            extra_compile_args={'cxx': ['-O3'], 'nvcc': ['-O3', '--use_fast_math']}
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
