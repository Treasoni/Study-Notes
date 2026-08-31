---
url: "https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html"
title: "sha2 utilities (GNU Coreutils 9.11)"
scraped_at: 2026-08-31T15:11:02+00:00
---

Previous: [`sha1sum`: Print or check SHA-1 digests](https://www.gnu.org/software/coreutils/manual/html_node/sha1sum-invocation.html), Up: [Summarizing files](https://www.gnu.org/software/coreutils/manual/html_node/Summarizing-files.html) [[Contents](https://www.gnu.org/software/coreutils/manual/html_node/index.html#SEC_Contents "Table of contents")][[Index](https://www.gnu.org/software/coreutils/manual/html_node/Concept-index.html "Index")]
### 6.7 sha2 utilities: Print or check SHA-2 digests[ ¶](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html#sha2-utilities_003a-Print-or-check-SHA_002d2-digests)
This is a legacy interface to the more modern `cksum` utility. See [`cksum`: Print and verify file checksums](https://www.gnu.org/software/coreutils/manual/html_node/cksum-invocation.html). 
The commands `sha224sum`, `sha256sum`, `sha384sum` and `sha512sum` compute checksums of various lengths (respectively 224, 256, 384 and 512 bits), collectively known as the SHA-2 hashes. 
If a file is specified as ‘-’ or if no files are given `sha???sum` computes the checksum for the standard input. `sha???sum` can also determine whether a file and checksum are consistent. Synopsis: 

```
sha???sum [option]... [file]...

```

`sha???sum` uses the ‘Untagged output format’ for each specified file, as described at [cksum output modes](https://www.gnu.org/software/coreutils/manual/html_node/cksum-output-modes.html). 
The program accepts [cksum common options](https://www.gnu.org/software/coreutils/manual/html_node/cksum-common-options.html). Also see [Common options](https://www.gnu.org/software/coreutils/manual/html_node/Common-options.html). 
