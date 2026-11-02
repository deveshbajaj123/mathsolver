# Add Newclid locally on Windows

The current machine has Python 3.12.4. Newclid 3.0.1 and `py-yuclid` 3.0.0 are installed and verified in this project's `.venv`. The shared `C:\Python312` installation has a damaged Scripts state and should not be used for this project. The upstream Newclid package declares Python `>=3.11` and lists Windows as a supported platform.

The virtual environment is already present here. To reproduce it from scratch, run these PowerShell commands from the workspace root:

```powershell
py -3.12 -m venv .\math_solution_pipeline\.venv
.\math_solution_pipeline\.venv\Scripts\python.exe -m pip install --upgrade pip
.\math_solution_pipeline\.venv\Scripts\python.exe -m pip install -r .\math_solution_pipeline\requirements-geometry.txt
.\math_solution_pipeline\.venv\Scripts\python.exe -c "import newclid; print(newclid.__file__)"
.\math_solution_pipeline\.venv\Scripts\newclid.exe --help
```

Using the virtual environment keeps Newclid and its dependencies separate from the shared Python. Newclid's package installation on this machine omitted `PyYAML`, which it imports at runtime; `requirements-geometry.txt` lists it explicitly. If installing the `yuclid` extra fails while building its C++ extension, try the pure Python package first:

```powershell
.\math_solution_pipeline\.venv\Scripts\python.exe -m pip install newclid
```

The upstream `py-yuclid` build uses CMake, pybind11 and scikit-build-core; its Windows build configuration names a vcpkg toolchain file. A source build may therefore need Visual Studio C++ Build Tools, CMake and vcpkg. Prefer a compatible prebuilt wheel when one is available. Check the actual pip error before installing a toolchain.

After installation, rerun the pipeline with the virtual environment's Python. Its `newclid_available` metric should become `true`. This means only that Python finds the module.

**Windows runtime repair (25 October 2026):** The `py-yuclid` Windows wheel omitted five Boost 1.88 runtime DLLs, causing exit `0xC0000135`. Run `\.venv\Scripts\python.exe repair_yuclid_windows.py` from `math_solution_pipeline`. The script downloads conda-forge's Windows `libboost` 1.88 package, verifies its pinned SHA-256, retains the original executable, patches its five import names to the package's generic Boost DLL names, installs the DLLs into the virtual environment, and smoke tests `yuclid.exe --help`. The installed repair has been run successfully here. Re-run it after recreating the virtual environment.

`\.venv\Scripts\python.exe newclid_probe.py` now returns a Newclid proof for PD-MATH-VII-002. The encoded source figure, assumptions, engine goal, and an independent exact symbolic midpoint identity are checked before the result is accepted. The main pipeline counts that single geometry answer as `SOLVED_AND_TRACE_CHECKED`; the other geometry questions remain unsupported. The generated school proof still awaits teacher presentation review and board-method approval.

Sources: [Newclid README](https://github.com/Newclid/Newclid/blob/main/README.rst), [Newclid package metadata](https://github.com/Newclid/Newclid/blob/main/newclid/pyproject.toml), [Yuclid package metadata](https://github.com/Newclid/Newclid/blob/main/yuclid/pyproject.toml).
