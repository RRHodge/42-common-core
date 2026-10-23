*This project has been created as part of the 42 curriculum by rarabeto.*

## Description

`ft_printf` is a custom reimplementation of the C standard library `printf()` function, compiled as a static library `libftprintf.a`. The project introduces **variadic functions** in C — functions that accept a variable number of arguments via `va_list`, `va_start`, `va_arg`, and `va_end`.

The library handles formatted output to stdout for the mandatory conversion specifiers (`c`, `s`, `p`, `d`, `i`, `u`, `x`, `X`, `%`) and the full set of bonus formatting flags (`-`, `0`, `.`, field width, `#`, ` `, `+`).

## Project Structure

```
ft_printf_125/
├── include/
│   └── ft_printf.h          # Header : types et prototypes
├── srcs/
│   ├── ft_printf.c          # Point d'entrée principal
│   ├── mandatory/
│   │   ├── ft_handle.c      # Dispatch par spécificateur
│   │   ├── ft_print_cs.c    # Impression de %c, %s, %%
│   │   ├── ft_print_nbr.c   # Impression de %d/%i, %u, %x/%X, %p
│   │   └── ft_utils.c       # ft_utoa_base, ft_putstr_n
│   └── bonus/
│       ├── ft_parse_bonus.c     # Parsing des flags, largeur, précision
│       └── ft_numprintf_bonus.c # ft_numprint, ft_get_digits, ft_pad
├── libft/                   # Bibliothèque de base (ft_strlen, ft_putchar_fd…)
├── Makefile
└── README.md
```

## Instructions

### Compilation

```bash
make          # build libftprintf.a (mandatory)
make bonus    # build with bonus flag support (same binary, fully integrated)
make clean    # remove object files
make fclean   # remove object files and libftprintf.a
make re       # full rebuild
```

### Integration

```c
#include "ft_printf.h"

int main(void)
{
    ft_printf("%-10s | %+d | %#010x\n", "hello", 42, 255);
    return (0);
}
```

Compile and link:

```bash
cc -Wall -Wextra -Werror main.c -L. -lftprintf -o program
```

## Supported Conversions

| Spécificateur | Description |
|---------------|-------------|
| `%c` | Caractère unique |
| `%s` | Chaîne (NULL → `"(null)"`) |
| `%p` | Pointeur en hexadécimal (NULL → `"(nil)"`) |
| `%d` / `%i` | Entier signé en décimal |
| `%u` | Entier non signé en décimal |
| `%x` | Hexadécimal — minuscules |
| `%X` | Hexadécimal — majuscules |
| `%%` | Signe pourcentage littéral |

## Bonus Flags

| Flag | Description |
|------|-------------|
| `-` | Aligner à gauche dans la largeur de champ (annule `0`) |
| `0` | Zéro-padder les nombres (ignoré si une précision est définie) |
| `.n` | Précision : nombre min de chiffres pour les nombres, max de chars pour les chaînes |
| `*` | Prendre la largeur ou la précision depuis le prochain `va_arg` |
| `#` | Forme alternative : préfixe `0x`/`0X` pour les hex non nuls |
| ` ` | Espace avant les nombres positifs (ignoré si `+` est présent) |
| `+` | Toujours afficher le signe pour les entiers signés |

## Algorithme et Structure de données

### Structure `t_flags`

Toutes les informations de formatage pour une conversion sont stockées dans une structure `t_flags` légère :

```c
typedef struct s_flags
{
    int minus;      // '-' : aligner à gauche
    int zero;       // '0' : zéro-padder
    int hash;       // '#' : forme alternative
    int space;      // ' ' : espace avant les positifs
    int plus;       // '+' : forcer le signe
    int width;      // largeur minimale de champ
    int prec;       // valeur de la précision
    int has_prec;   // indique si '.' était présent
} t_flags;
```

Cette structure est passée par pointeur à chaque handler, ce qui rend l'API uniforme pour tous les types de conversion.

### Parsing (`ft_parse`)

`ft_printf` parcourt la chaîne de format octet par octet. À chaque `%`, `ft_parse()` effectue un scan en trois phases :

1. **Scan des flags** — consomme toute combinaison de `-`, `0`, `#`, ` `, `+` dans n'importe quel ordre.
2. **Scan de la largeur** — lit un entier optionnel ou `*` (lu depuis `va_list`).
3. **Scan de la précision** — si `.` est trouvé, lit un entier optionnel ou `*`.

Après le parsing, le caractère de type (`c`, `s`, `d`, …) est dispatché via `ft_handle_fmt()`.

### Impression des nombres (`ft_numprint`)

Toutes les conversions numériques (`%d`, `%i`, `%u`, `%x`, `%X`) partagent le helper unifié `ft_numprint(flags, prefix, digits)` :

```
total_len = len(prefix) + max(len(digits), precision)

si !minus && !zero_pad :  espace-pad à gauche  → total_len atteint width
afficher prefix
si zero_pad :             zero-pad au milieu   → total_len atteint width
précision-pad avec des zéros devant
afficher digits
si minus :                espace-pad à droite  → total_len atteint width
```

La séparation entre *prefix* (signe / `0x`) et *digits* garantit l'interaction correcte entre les flags `0`, `.`, `+`, ` ` et `-` pour tous les cas limites.

### Conversion en base (`ft_utoa_base`)

`ft_utoa_base(n, base, upper)` convertit un entier non signé en chaîne dans la base demandée :

- `upper == 1` → majuscules (`0123456789ABCDEF`)
- `upper == 0` → minuscules (`0123456789abcdef`)
- `upper == -1` → décimal (`0123456789`)

Le nombre de chiffres est calculé avant l'allocation pour éviter tout realloc. Le cas `n == 0` est traité séparément pour garantir la sortie `"0"`.

### Gestion de la précision zéro (`ft_get_digits`)

Quand la précision est explicitement `0` et que la valeur est `0` (`%.0d` avec `n=0`), `ft_get_digits` retourne une chaîne vide — conformément au comportement de `printf` standard qui n'affiche rien dans ce cas.

## Cas limites notables

| Cas | Comportement |
|-----|--------------|
| `%s` avec `NULL` | Affiche `(null)` |
| `%p` avec `NULL` | Affiche `(nil)` |
| `%-5d` (moins + largeur) | Aligne à gauche, ignore `0` |
| `%.0d` avec `n = 0` | N'affiche rien (précision zéro) |
| `%#x` avec `n = 0` | Pas de préfixe `0x` (standard C) |
| `%+d` avec positif | Affiche le `+` explicitement |
| `% d` avec positif | Affiche un espace à la place du signe |

## Resources

- **Documentation & References:** 
 
 [`printf(3)` — Linux man page](https://man7.org/linux/man-pages/man3/printf.3.html)
 
 [Variadic functions — cppreference](https://en.cppreference.com/w/c/variadic)
 
 [42 Norm v3 — norminette](https://github.com/42School/norminette)
 
 [printf format string — Wikipedia](https://en.wikipedia.org/wiki/Printf_format_string)

- **AI Usage:** An AI coding assistant (LLM) was utilized exclusively to help structure and format documentation in strict accordance with the 42 curriculum standards, and to clearly outline the explanation of the implemented algorithm. No AI tools were used to implement the actual C code or the core project logic.
