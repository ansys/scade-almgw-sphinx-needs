# Traceability Resources
The directory `Resources` contains scripts and configuration files you can use 'as is' or customize regarding your project needs.

## `Traceability.aty`
This file defines the annotation type `DesignElement` with a cardinality 1-1 for SCADE Suite LLRs:
* Equation sets
* Textual diagrams
* States
* Transitions
* Net diagrams

This note type has two fields:
* `Nature`: Either `Low Level Requirement` (default), `Architecture` or `Derived Low Level Requirement`. This property is tagged to be part of the LLRs exported by ALMGW.
* `Description`: Free text.

**Note**: This file conflicts with the file `DefaultAty.aty` delivered with SCADE. We advise to remove references to `DefaultAty.aty` to not depend on the installed SCADE releases and add to your project the other file present in this directory: `Design.aty`.

## `Traceability.tot`
This file defines a few styles for equation sets: `EQS1`, `EQS2`...

## `Readability.tot`
Additional options for larger fonts, more readable colors, common IDE settings. Feel free to edit the file before using it for a project.

## `Suite.json`
This file is a configuration schema for exporting SCADE Suite LLRs with the connector sphinx-needs or with other connectors supporting the customization script `llrs.py`.

Refer to [Traceable Elements Export Schema](https://pyalmgw.scade.docs.pyansys.com/) for details.

## `Test.json`
This file is a configuration schema for exporting SCADE Test elements with the connector sphinx-needs or with other connectors supporting the customization script `llrs.py`.
It exports only the records, with the structure of procedures and folders. It contains at the end of the file templates to export either all the scenarios or exclude the initialization or preamble scenarios: This is not recommended since the scenarios are not necessarily unique: The exported elements must be unique.
* Aliases, init or preamble scenarios are usually shared among records of the same procedure.
* Regular scenarios may be share by procedures testing different instantiations of polymorphic operators.

Refer to [Traceable Elements Export Schema](https://pyalmgw.scade.docs.pyansys.com/) for details.
