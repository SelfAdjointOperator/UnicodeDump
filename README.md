# UnicodeDump

Like hexdump but for Unicode codepoints. Pass strings on the command line, or read from stdin. The script converts UTF-8 (or your system's default encoding?) to formatted codepoints.

## Example

`./src/unicode-dump.py Hello, שלום עליכם`
```
H U+0048   e U+0065   l U+006C   l U+006C   o U+006F   , U+002C     U+0020   ש U+05E9
ל U+05DC   ו U+05D5   ם U+05DD     U+0020   ע U+05E2   ל U+05DC   י U+05D9   כ U+05DB
ם U+05DD
```
