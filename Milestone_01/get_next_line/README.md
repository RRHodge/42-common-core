*Project completed as part of the 42 curriculum by rarabeto.*

## Description

The **get_next_line** project consists of implementing a C function capable of reading a file **line by line** from a **file descriptor (`fd`)**.

The `get_next_line` function returns **one complete line per call**, until the end of the file is reached.

### Key Points

* **Static variable**: keeps the remaining data between two function calls.
* **Configurable BUFFER_SIZE**: the buffer size is defined at compilation time.
* **Strict memory management**: no memory leaks.

---

# Compilation

Compile with the required 42 flags and define `BUFFER_SIZE`:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c
````

The function must work with different buffer sizes:

```
BUFFER_SIZE=1
BUFFER_SIZE=42
BUFFER_SIZE=9999
```

---

# Usage

Include the header:

```c
#include "get_next_line.h"
```

Then call the function:

```c
char *line;

line = get_next_line(fd);
```

---

# Creating Test Files

To test the program:

### Standard file

```bash
echo -e "First line\nSecond line\nThird line" > test.txt
```

### Empty file

```bash
touch empty.txt
```

### Single line without newline

```bash
echo -n "Single text" > short.txt
```

### File with long lines

```bash
yes "very long line to test buffer behavior" | head -n 5 > long.txt
```

---

# Example `main.c` (Mandatory)

This `main` opens a file, reads each line using `get_next_line`, prints it, and then frees the memory.

```c
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "get_next_line.h"

int	main(void)
{
	int		fd;
	char	*line;

	fd = open("test.txt", O_RDONLY);
	if (fd < 0)
	{
		printf("File opening error\n");
		return (1);
	}

	line = get_next_line(fd);
	while (line)
	{
		printf("%s", line);
		free(line);
		line = get_next_line(fd);
	}

	close(fd);
	return (0);
}
```

Compilation with the `main`:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c
```

---

# Algorithm Principle

The algorithm uses a **static string called "stash"** that stores characters read but not yet returned.

### Steps

1. **Reading**

`read()` reads `BUFFER_SIZE` characters and appends them to the stash.

2. **Extraction**

The function extracts the line up to the first `\n`.

3. **Cleanup**

The remaining text after `\n` is kept in the static variable for the next call.

---

# Bonus Approach (Multiple File Descriptors)

The bonus allows reading **multiple files simultaneously**.

The solution used: **linked list**

Each node contains:

* an `fd`
* a **stash specific to that file**

---

# 1. Structure `t_buffer`

```c
typedef struct s_buffer
{
	char				*content;
	struct s_buffer		*next;
}				t_buffer;
```

### Description

The `t_buffer` structure represents **an element of a linked list containing data**.

### Fields

* **`char *content`**

  * Pointer to a character string.
  * Contains a portion of data read (for example from `read()`).

* **`struct s_buffer *next`**

  * Pointer to the **next element** in the linked list.
  * Allows chaining multiple buffers together.

### Diagram

```
+-------------------+
| content           | --> "Hello "
| next              | ----+
+-------------------+     |
                          v
                   +-------------------+
                   | content           | --> "World"
                   | next              | --> NULL
                   +-------------------+
```

Each node contains a piece of text and a link to the next one.

---

# 2. Structure `t_fd_node`

```c
typedef struct s_fd_node
{
	int					fd;
	t_buffer			*head;
	t_buffer			*last;
	struct s_fd_node	*next;
}				t_fd_node;
```

### Description

The `t_fd_node` structure represents **a file descriptor and the buffers associated with it**.

It allows managing **multiple open files simultaneously**, each with its own buffer list.

### Fields

* **`int fd`**

  * The **file descriptor** (identifier of the opened file).
  * Example: result of `open()` or parameter of `read()`.

* **`t_buffer *head`**

  * Pointer to **the first buffer** in the list.
  * Used to iterate through all buffers.

* **`t_buffer *last`**

  * Pointer to **the last buffer**.
  * Useful for quickly adding a new buffer at the end.

* **`struct s_fd_node *next`**

  * Pointer to the **next file descriptor node** in the list.
  * Allows managing multiple `fd`.

---

# 3. Global Organization

`t_fd_node` elements form a **linked list of files**, and each file has its own **linked list of buffers**.

### Global Diagram

```
t_fd_node (fd = 3)
│
├── head --> [buffer1] -> [buffer2] -> [buffer3]
│
├── last --> [buffer3]
│
└── next
      |
      v
   t_fd_node (fd = 4)
   │
   ├── head --> [buffer1] -> [buffer2]
   ├── last --> [buffer2]
   └── next --> NULL
```

---

# 4. Summary

| Structure        | Role                                  |
| ---------------- | ------------------------------------- |
| `t_buffer`       | Stores a piece of text                |
| `t_fd_node`      | Associates an `fd` with a buffer list |
| `t_buffer` list  | Contains the read data                |
| `t_fd_node` list | Allows handling multiple files        |

---

This allows operations such as:

```
get_next_line(fd1)
get_next_line(fd2)
get_next_line(fd1)
```

without losing the reading position.

---

# Resources

Useful documentation:

```
man 2 read
man 3 malloc
man 3 free
```

Important concepts:

* static variables
* memory management
* string manipulation
* structures and linked lists (bonus)

---

✔ AI was used only to:

* structure the documentation
* explain certain concepts (linked lists)

All algorithmic logic was manually verified.

---

If you want, I can also create an **"excellent level 42 README" version** that includes:

* visual algorithm diagrams
* project structure
* stash flow diagram
* `read()` execution flow example

This is the type of README that **immediately adds credibility to the project.**