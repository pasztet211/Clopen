![Python](https://img.shields.io/badge/Python-3.14+-blue?style=flat-square)
![Clopen](https://img.shields.io/badge/version-0.1.7-orange?style=flat-square)

# Clopen
programming language

it is very simple by design

Read the full documentation: [Clopen Documentation](https://pasztet211.github.io/Clopen/)

## Quick Start

Create a file called `hello.clo`:

```clo
log "Hello, World!"
```

Run it:
```bash
clopen hello.clo
```

Output:
```text
Hello, World!
```

Not installed yet? See the [Installation Guide](https://pasztet211.github.io/Clopen/installation.html).

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

## Clopen commands[^first]
```bash
clopen --help <optional command>
clopen -h <optional command>

clopen --version <optional topic>
clopen -v <optional topic>

clopen --debug <optional mode>
clopen -d <optional mode>
```

## Example code

```clo
let var [0,1] int
log var
log "var"
log var[0]

get var "integer: "
log $var
```
**OUTPUT:**

```text
[0,1]
var
0

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
| list  | [1,2] |  

**Note:** Lists are currently a beta feature. Some edge cases may cause unexpected behavior.

## Commands: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

### Variables: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `let` eg. `let var 10 int`
- `update` eg `update var += 8`
- `set` eg. `set var 0 int`
- `del` eg. `del var`

### User content: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)
 
- `get` eg. `get guess "guess: "`
- `log` eg. `log "\n"`

### Stopping: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `halt` eg. `halt`
- `shalt` eg. `shalt`

### Lists: ![works](https://img.shields.io/badge/status-beta-yellow?style=flat-square)

- `add` eg. `add 6 int to end-of values`

## conditionals: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `if` eg. `if (var > 8) {}`
- `elif` eg. `elif (var < 8) {}`
- `else` eg. `else {}`

## loops: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `while` eg. `while (guess != 8) {}`
- `for` eg. `for (i 0 int;i < 7;i += 1) {}`

## Miscellaneous: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

### Functions: ![works](https://img.shields.io/badge/status-stable-green?style=flat-square)

- `fn` eg. `fn name (args) {}`
- `return` eg. `return "value"`

### Miscellanier: ![works](https://img.shields.io/badge/status-beta-yellow?style=flat-square)

- `with` module imports (supports `from` and `as`) eg. `with math as m`[^second]

# Made by:
- [pasztet211](https://github.com/pasztet211) ![pasztet](https://img.shields.io/badge/creator-orange?style=flat-square)

# License

Clopen is licensed under the GNU General Public License v3.0.
See [LICENSE.md](LICENSE.md) for details.

[^first]: Replace **<optional command/topic/mode>** with the name of a command, topic or mode. Examples: `let`, `fn`, `status` or `--basic`.
[^second]: [Additional Extension Creation Guide](https://github.com/pasztet211/Clopen/blob/main/docs/ADDITIONAL_extensions.md), [Standard Python Extension Guide](https://github.com/pasztet211/Clopen/blob/main/docs/ADDITIONAL_.pyextensions.md)