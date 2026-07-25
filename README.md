![Python](https://img.shields.io/badge/Python-3.13.12-blue?style=flat-square)
![Clopen](https://img.shields.io/badge/version-0.1.4-orange?style=flat-square)

# Clopen
programming language

it is very simple by design


## Features

- // and # comments
- creating and deleting variables with `let` and `del`
- modifying variables using `update` and `set`
- conditionals like `if` `elif` and `else`
- loops like `for` and `while`
- functions with `fn` + returning from said functions
- printing and getting inputs using `log` and `get`
- importing other clopen files with `"with"` + `from` or `as`

## Installation

1. clone the repo to a C:\Clopen folder
2. add C:\Clopen to **PATH**
3. Install python and add it to **PATH**

## File Extension and running

1. extension: `.clo`
2. to run a file use 
```bash 
clopen filename.clo
```
in the folder containing the file

## Clopen commands

```bash
clopen --help <optional command>
clopen -h <optional command>

clopen --version <optional topic>
clopen -v <optional topic>
```

## Example code

```clo
let var 0 int
log var
log "var"

get var "integer: "
log $var
```
**OUTPUT:**

```
0
var

integer: [typed value]
[typed value]
```

## Variable types:   ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

| type  | value |
|-------|-------|
| int   | 10    |
| float | 10.0  |
| bool  | true  |
| str   | "hi"  |

## Commands:

- `let`
- `get`
- `log`
- `update`
- `set`
- `halt`
- `shalt`
- `del`

## conditionals: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `if` 
- `elif`
- `else`

## loops: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `while`
- `for`

## Miscellaneous: ![works](https://img.shields.io/badge/status-beta-yellow?style=flat-square)

- `with` module imports (supports `from` and `as`)

# Made by:
- [pasztet211](https://github.com/pasztet211) ![pasztet](https://img.shields.io/badge/creator-orange?style=flat-square)
