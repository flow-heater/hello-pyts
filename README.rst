About
=====
Just a hello world scribble.


Synopsis
========
::

    # Setup.
    python -m venv .venv
    source .venv/bin/activate
    pip install wasmer==1.0.0-beta1 wasmer_compiler_cranelift==1.0.0-beta1

    # Invoke core with inline wat code.
    python kernel/core.py inline

    # Build userspace modules.
    make userspace

    # Invoke core with wat code from TypeScript/AssemblyScript.
    python kernel/core.py typescript


Credits
=======
Standing on the shoulders of giants.

- https://github.com/python/cpython
- https://github.com/microsoft/typescript
- https://github.com/AssemblyScript/assemblyscript
- https://github.com/wasmerio/wasmer
- https://github.com/wasmerio/wasmer-python
