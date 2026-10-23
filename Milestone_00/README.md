_This project has been created as part of the 42 curriculum by rarabeto._

# Description

Libft is the first project in the 42 curriculum. The goal is to recode a number of functions from the standard C library (libc), as well as additional utility functions that will be useful throughout our studies. 

This project helps to deeply understand memory management, pointers, and the manipulation of basic data structures in C.

### Check and manipulate characters:
| Function | Description |
| :- | :- |
| `ft_isalpha` | Alphabetic character test. |
| `ft_isdigit` | Decimal-digit character test. |
| `ft_isalnum` | Alphanumeric character test. |
| `ft_isascii` | Test for ASCII character. |
| `ft_isprint` | Check if a character is printable. |
| `ft_toupper` | Lower case to upper case letter conversion. |
| `ft_tolower` | Upper case to lower case letter conversion. |

### Manipulate strings:
| Function | Description |
| :- | :- |
| `ft_strlen`   | Find the length of the string. |
| `ft_strlcpy`  | Size-bounded string copying. |
| `ft_strlcat`  | Size-bounded string concatenation. |
| `ft_strchr`   | Locate the character in the string (first occurrence). |
| `ft_strrchr`  | Locate the character in the string (last occurrence). |
| `ft_strncmp`  | Compare strings (size-bounded). |
| `ft_strnstr`  | Locate a substring in a string (size-bounded) |
| `ft_substr`   | Extract substring from a string. |
| `ft_strjoin`  | Concatenate two strings into a new string (with malloc). |
| `ft_strtrim`  | Trim the beginning and end of the string with the specified characters. |
| `ft_split`    | Split string, with specified character as delimiter, into an array of strings. |
| `ft_strmapi`  | Create a new string by modifying the string with a specified function. |
| `ft_striteri` | Iterates through a string, enabling character and index manipulation. |

### Manipulate memory:
| Function | Description |
| :- | :- |
| `ft_memset`  | Write a byte to a byte string. |
| `ft_bzero`   | Write zeroes to a byte string. |
| `ft_memcpy`  | Copy memory area. |
| `ft_memmove` | Copy byte string. |
| `ft_memchr`  | Locate byte in byte string. |
| `ft_memcmp`  | Compare byte string. |
| `ft_calloc`  | Memory allocation. |
| `ft_strdup`  | Save a copy of a string (with malloc). |

### Manipulate numbers:
| Function | Description |
| :- | :- |
| `ft_atoi` | Convert the ASCII string to an integer. |
| `ft_itoa` | Convert integer to ASCII string. |

### Write to a file descriptor:
| Function | Description |
| :- | :- |
| `ft_putchar_fd` | Output a character to the given file. |
| `ft_putstr_fd`  | Output string to the given file. |
| `ft_putendl_fd` | Output string to given file with newline. |
| `ft_putnbr_fd`  | Output integer to the given file. |

### Manipulate list:
```c
typedef struct s_list
{
    void            *content;
    struct s_list   *next;
}                   t_list;
```

| Function | Description |
| :- | :- |
| `ft_lstnew`       | Create new list. |
| `ft_lstadd_front` | Add a new element at the beginning of the list. |
| `ft_lstadd_back`  | Add a new element at the end of the list. |
| `ft_lstsize`      | Count elements of a list. |
| `ft_lstlast`      | Find the last element of the list. |
| `ft_lstdelone`    | Delete element from the list. |
| `ft_lstclear`     | Delete the sequence of elements of the list from a starting point. |
| `ft_lstiter`      | Apply function to the content of all list elements. |
| `ft_lstmap`       | Apply function to the content of all list elements into a new list. |

# Instructions

### Makefile rules

- make & make all - Compile libft files.

- make clean - Delete all .o (object files) files.

- make fclean - Delete all .o (object file) and .a (executable) files.

- make re - Use rules fclean + all.

### Norminette
At 42 School, it is expected that almost every project is written following the Norm, which is the coding standard of the school.


- No for, do...while, switch, case, goto, ternary operators, or variable-length arrays allowed;
- Each function must be a maximum of 25 lines, not counting the function's curly brackets;
- Each line must be at most 80 columns wide, with comments included;
- A function can take 4 named parameters maximum;
- No assigns and declarations in the same line (unless static);
- You can't declare more than 5 variables per function;
- ...

# Resources
### References Used
- UNIX Manual (man pages) for libc specifications.
- C documentation on pointers and memory management.

### AI Usage Report
- Tools used: Gemini

- Usage: AI was used to clarify complex concepts like function pointers (ex: ft_striteri) and to help understand the logic of linked list manipulation.

- Validation: Every li ne of code generated or suggested by AI was analyzed, tested, and rewritten to comply with the 42 Norm and ensure its reliability. No code was copied without a full understanding of its operation.