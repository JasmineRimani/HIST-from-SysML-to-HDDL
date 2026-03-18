# HIST: SysML to HDDL Translation

HIST translates Papyrus MBSE models into HDDL planning artifacts. In this repository, the focus is on rover operations and mission descriptions modeled in Papyrus and exported as UML/XMI files.

The codebase started as a research prototype and is now being cleaned up into a more standard Python project layout so it is easier to test, extend, and maintain.

## Reference

If you use this repository or the underlying workflow, please cite the reference paper:

```bibtex
@article{rimani2023simulating,
  title   = {Simulating Operational Concepts for Autonomous Robotic Space Exploration Systems: A Framework for Early Design Validation},
  author  = {Rimani, Jasmine and Viola, Nicole and Lizy-Destrez, Stephanie},
  journal = {Aerospace},
  volume  = {10},
  number  = {5},
  pages   = {408},
  year    = {2023},
  doi     = {10.3390/aerospace10050408}
}
```

Paper link: https://www.mdpi.com/2226-4310/10/5/408

## Project Layout

- `src/hist/`: Python source package.
- `config/`: default YAML configuration.
- `examples/inputs/`: sample Papyrus UML inputs.
- `examples/outputs/`: example generated HDDL and feedback artifacts kept for reference.
- `outputs/`: runtime output directory for newly generated files.
- `tests/`: baseline regression tests for configuration parsing and XML extraction.

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Run with the default sample configuration:

```bash
python3 -m hist
```

Or use the legacy entry point:

```bash
python3 src/main.py
```

You can also override the default paths:

```bash
python3 -m hist --config config/configuration.yaml --input-dir examples/inputs --output-dir outputs
```

## Status

- Domain generation is the most mature part of the prototype.
- Problem generation is partial and still contains prototype-era assumptions.
- Detailed feedback generation remains incomplete in this branch.

## License

This work is distributed under the MIT License. See `LICENSE.md`.
