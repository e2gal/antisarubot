antisarubot handlers
-----

(still in development, expect changes)

Each handler should be in one module, with a `run` function.
`run` takes a file-like object as its parameter, and returns:

- `(rating, character, copyright, general)` tuple on success; or
- `None` on failure.

See [noop.py](noop.py) for example.
