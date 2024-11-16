# CedarTL

[![PyPI version](https://badge.fury.io/py/cedartl.svg)](https://pypi.org/project/cedartl/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cedartl.svg)](https://pypi.org/project/cedartl/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimally-intrusive templating language thought for interactive use in LLM chats

CedarTL is a recursive, minimally-intrusive templating language tailored to interactive use, like in an LLM chat session.
It's got a straightforward syntax that's easy to grasp.

## Table of Contents
- [Why should I use it?](#why-should-i-use-it)
- [Key Features](#key-features)
- [Syntax](#syntax)
    - [Basic syntax](#basic-syntax)
    - [LLM Control](#llm-control)
- [FolderDict](#folderdict)
- [Quick Start](#quick-start)
- [Concrete Example](#concrete-example)
    - [Context](#context)
    - [Chat Session](#chat-session-in-cedarml-format)

## Why should I use it?
It can save you time when writing your prompts.

Frequently-used pieces of text can be stored in named _variables_ or _templates_.
Then, instead of typing the same text over and over, you just put a reference to the named template.

See the [concrete example](#concrete-example).

## Key Features:
1. **Minimal syntax overhead**: The syntax is designed to blend naturally with the target text, minimizing typing overhead
2. **Recursive**: It can process templates within templates, allowing for nested template structures
3. **Hierarchical** key access and function calls
4. **Directory-based** templating through `FolderDict` (accessing local directories, tar/zip files, and remote servers 
via WebDAV, HTTP, FTP, etc)
5. **Direct shell** command integration
6. **LLM integration**

You provide the `CedarTL` runtime a _root context_: a `dict`, a `list`, an object, or a [`FolderDict`](#folderdict)
(a path to a directory where its contained files are the keys, and the file contents are the values)

## Syntax
To escape to `CedarTL` syntax, you type a backslash and then a symbol. Examples:

### Basic syntax:
- `\name`: Key lookup.
- `\path/to/key`: Nested Key lookup
- `\!(shell commands)`: Shell escape hatch

### LLM Control
- `\*chat(some text)`: LLM chat (starts a separate LLM session)
- `\*temp(<float>)`: LLM temperature control

... more to come

## FolderDict
A `FolderDict` is simply a way to view a folder as if it were a `dict` (that is, a mapping between keys and values).
In `Python`, it's compatible with type `dict[str, str]`.

Example: Inside a `resources` folder, we've added a folder named `templates`. We want to view this folder as a `dict`,
so we point a `FolderDict` to that `templates` folder:

```text
resources/
└── templates/
    └── main/
        ├── fsninja.txt
        ├── l0.txt
        ├── rar.txt
        └── sbs.txt
```

In the case above, the keys are:
1. `fsninja` (a full-stack ninja)
2. `l0` (for _**L**evel_ zero)
3. `rar` (for _Rephrase And Respond_)
4. `sbs` (for thinking _step-by-step_)

Notice that key names should represent the concept contained in the files.
However, all names above are arbitrary: `FolderDict` will work regardless of the names involved.

And where are the values for the keys?
Yes, the file _contents_ are the values for their corresponding keys.

## Quick Start

```bash
pip install cedartl
```

```python
from cedartl import CedarTLProcessor
from importlib.resources import files

# [...]
class ExistingClass:
    def __init__(self):
      self.template_processor = CedarTLProcessor(files('resources.templates.main'))
    def process_user_input(self, input: str):
        # ...
        processed_input: str = self.template_processor.process(input)
        # ...
```

## Concrete Example
Real chat session using `CedarTL` with `qwen-2.5-72b-instruct` and Aider:

### Context
In this example, we're using a patched version of Aider that adds support for `CedarTL` inside chat sessions.
(Check the [FolderDict section](#folderdict) to see the names of the templates we're using here)

Aider delegates template processing to the `CedarTL` engine, which returns the final rendition of the text to be sent
to the LLM.

### Chat session in `CedarML` format:

(see [CedarML](https://github.com/CedarVerse/cedarml?tab=readme-ov-file#readme) for more info)

```xml
<cedarml:tool-in.aider>
/add aider/coders/base_coder.py
</cedarml:tool-in.aider>

<cedarml:tool-out.aider>
Added /GitHub/aider/aider/coders/base_coder.py to the chat
─────────
aider/coders/base_coder.py
</cedarml:tool-out.aider>

<cedarml:tool-in.aider>
what does this file do? \l0
</cedarml:tool-in.aider>

<cedarml:tool-out.cedartl>
\l0: \rar\sbs
\rar: Rephrase my request, then respond.
\sbs: Do so by thinking step by step.
</cedarml:tool-out.cedartl>

<cedarml:role.user>
what does this file do? Rephrase my request, then respond.
Do so by thinking step by step.
</cedarml:role.user>

<cedarml:role.assistant>
Sure, let's break down your request and then respond step by step.

Rephrased Request:
"Can you explain the purpose and main functionalities of the aider/coders/base_coder.py file?"

Step-by-Step Response:

1. File Overview:
• The aider/coders/base_coder.py file is a Python module that defines the Coder class and related functionalities.
• This class is a core component of the Aider application, which is designed to assist users in coding tasks using AI.
</cedarml:role.assistant>
```

<details>
<summary>Actual screenshot</summary>

![img.png](img.png)
</details>
