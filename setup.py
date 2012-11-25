from distutils.core import setup, Extension
import subprocess


def pkg_config(*packages, **kw):
    
    flag_map = {
        '-I': 'include_dirs',
        '-L': 'library_dirs',
        '-l': 'libraries',
    }
    proc = subprocess.Popen(['pkg-config', '--libs', '--cflags'] + list(packages), stdout=subprocess.PIPE)
    out, err = proc.communicate()
    
    for token in out.strip().split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    
    return kw


setup(

    name='av',
    version='0.1',
    description='Pythonic bindings for libav.',
    
    author="Mike Boers",
    author_email="pyav@mikeboers.com",
    
    url="https://github.com/mikeboers/PyAV",
    
    ext_modules=[
        Extension(
            name,
            sources=['build/%s.c' % name.replace('.', '/')],
            **pkg_config('libavformat', 'libavcodec', 'libswscale', 'libavutil')
        )
        for name in
        (
            'av.codec',
            'av.format',
            'av.tutorial',
            'av.utils',
        )
    ],
)