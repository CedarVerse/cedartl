# CedarTL
A minimally-intrusive templating language thought for interactive use in LLM chats

CedarTL is a recursive, minimally-intrusive templating language tailored to interactive use, like in an LLM chat session.
It's got a straightforward syntax that's easy to grasp.

## Key Features:
1. **Minimal syntax overhead**: The syntax is designed to blend naturally with the target text, minimizing typing overhead
2. **Recursive**: It can process templates within templates, allowing for nested template structures
3. **Hierarchical** key access and function calls
4. **Directory-based** templating through `FolderDict` (accessing local directories, tar/zip files, and remote servers via WebDAV, HTTP, FTP, etc)
5. **Direct shell** command integration
6. **LLM integration**

You provide the `CedarTL` runtime a _root context_: a `dict`, a `list`, an object, or a `FolderDict`
(a path to a directory where its contained files are the keys, and the file contents are the values)

## Syntax
To escape to `CedarTL` syntax, you type a backslash and then a symbol. Examples:

### Basic syntax:
`\name`: Key lookup.
`\path/to/key`: Nested Key lookup
`\!(shell commands)`: Shell escape hatch

### LLM Control
`\*chat(some text)`: LLM chat (starts a separate LLM session)
`\*temp(<float>)`: LLM temperature control

... more to come