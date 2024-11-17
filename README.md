# CedarTL
A lightweight, intuitive templating language designed for interactive use in LLM chat sessions.

[![PyPI version](https://badge.fury.io/py/cedartl.svg)](https://pypi.org/project/cedartl/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cedartl.svg)](https://pypi.org/project/cedartl/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)



## Overview

CedarTL is a non-intrusive, recursive templating language that seamlessly integrates with LLM chat sessions.
Its simple syntax minimizes cognitive overhead while maximizing speed,
making it perfect for interactive development sessions.

## Table of Contents
- [Why should I use it?](#why-should-i-use-it)
    - [For LLM Users](#for-llm-users)
    - [For AI Code Assistant / IDE Developers](#for-ai-code-assistant--ide-developers)
- [Key Features](#key-features)
- [Syntax](#syntax)
    - [Basic syntax](#basic-syntax)
    - [FolderDict context folder control](#folderdict-context-folder-control)
    - [Template management](#template-management)
    - [LLM Control](#llm-control)
- [FolderDict](#folderdict)
- [Quick Start](#quick-start)
- [Concrete Example](#concrete-example)
    - [Context](#context)
    - [Chat Session](#chat-session-in-cedarml-format)
- [What's Next?](#whats-next)
- [Contributing](#contributing)

## Why should I use it?
It can save you time when writing your prompts.

Frequently-used pieces of text can be stored in named _templates_.
Then, instead of typing the same text over and over, you just put a reference to the named template.

- [**Templating via folders**](#folderdict): Frequently used prompts are stored as text files _grouped in a `context folder`_
- **Intuitive References**: Access templates using simple `\name` syntax

### For LLM Users:
See the [concrete example](#concrete-example) to see how easy the syntax is.

### For AI Code Assistant / IDE Developers:
See the [quick start](#quick-start) section if you want to support `CedarTL` in your product

## Key Features:
1. 🚀 Minimal Syntax: Clean, intuitive syntax that feels natural
   - Designed to blend naturally with the target text, minimizing typing overhead
2. 🤖 **LLM-Optimized**: Built specifically for LLM interactions
3. 🔄 **Recursive Processing**: It can process templates within templates, allowing for nested template structures
4. 🔗 **Hierarchical** key access and function calls
5. 📁 Smart Folder-based templating through `FolderDict`
    - Structure your templates logically in different `context folders` (accessing local directories, tar/zip files, and remote servers via WebDAV, HTTP, FTP, etc)
    - Easy to switch between different contexts (See `\%cd`)
    - Multiple contexts can be layered (using _most-recent-wins_ strategy)
6. 🖥️ Shell command Integration

You provide the `CedarTL` runtime a _root context_: a `dict`, a `list`, an object, or a [`FolderDict`](#folderdict)
(a path to a directory where its contained files are the keys, and the file contents are the values)

## Syntax
To escape to `CedarTL` syntax, you type a backslash and then a symbol. Examples:

### Basic syntax:
- `\name`: Key lookup.
- `\path/to/key`: Nested Key lookup

### FolderDict context folder control:
- `\..`: Move up one level in the context hierarchy
- `\%cd(<path-spec-1> <path-spec-2>...)`: Change the current `context folder` from where template keys and values are read
- `\%pwd`: Print current working context folder
- `\%ls`: List contents of current working context folder

### Template management:
- `\%set(key="value")`: Set volatile template value
- `\%get(key)`: Get the value associated with a key
- `\%saveas(<target-path>)`: Save the current template to a folder
- `\%load(<path>)`: Load template into volatile area

### LLM Control
- `\*chat(some text)`: LLM chat (starts a separate LLM session)
- `\*temp(<float>)`: LLM temperature control

... more to come

## FolderDict
A `FolderDict` is simply a way to view a folder (the `context folder`) as if it were a `dict` (that is, a mapping between keys and values).
In `Python`, it's compatible with type `dict[str, str]`.

Example: Inside a `resources` folder, we've added a folder named `templates` to hold different context folders. We want to view the `main` context folder as a `dict`,
so we point a `FolderDict` to that `main` folder:

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

By storing templates in a `FolderDict`, we get some advantages:
- Each folder can have specialized prompts for a specific type of task
- It's easier to share your template folder with the community (just zip it)
- It's easier to version-control a template folder

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

<cedarml:tool-in.cedartl>
what does this file do? \l0
</cedarml:tool-in.cedartl>

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
<summary>Actual chat session screenshot</summary>

![img.png](img.png)
</details>

## What's Next?

Here's what's on the horizon for `CedarTL`:

- **Browser Extension**
    - Cross-platform extension for seamless template access in any web text input
    - Support for popular platforms:
        - LLM web interfaces ([Kagi Assistant](https://kagi.com/assistant), ChatGPT, Claude, OpenRouter, etc.)
        - Messaging apps (WhatsApp Web, Google Chat)
        - Online text editors
        - Social media platforms like Facebook, Instagram
    - Features:
        - Local template storage and management
        - Secure sync across devices
        - Template preview on hover
        - Context-aware template auto-complete
        - Integration with browser's autofill system
        - Smart template generation from frequently typed text

- **Core Enhancements**
    - Template sharing ecosystem
    - More backend storage options (databases, cloud storage)
    - Better template versioning

- **Integration APIs**
    - SDK for easy integration into other applications


## Contributing
Want to contribute? Check out our [GitHub issues](https://github.com/YourRepo/CedarTL/issues) or propose new features!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
