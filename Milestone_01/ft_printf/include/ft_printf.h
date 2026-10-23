/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 10:38:49 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 15:59:34 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <unistd.h>
# include <stdlib.h>
# include "../libft/include/libft.h"

typedef struct s_flags
{
	int	minus;
	int	zero;
	int	hash;
	int	space;
	int	plus;
	int	width;
	int	prec;
	int	has_prec;
}	t_flags;

int		ft_printf(const char *fmt, ...);
int		ft_handle_fmt(char spec, va_list args, t_flags *flags);
t_flags	ft_parse(const char *fmt, int *pos, va_list args);

int		ft_print_char(t_flags *flags, int c);
int		ft_print_str(t_flags *flags, char *s);
int		ft_print_mod(t_flags *flags);
int		ft_print_int(t_flags *flags, long n);
int		ft_print_uint(t_flags *flags, unsigned long n, int base, int upper);
int		ft_print_ptr(t_flags *flags, unsigned long n);

int		ft_pad(char c, int n);
int		ft_putstr_n(char *s, int n);
int		ft_putchar(char c);
int		ft_numprint(t_flags *flags, char *prefix, char *digits);
char	*ft_get_digits(t_flags *flags,
			unsigned long n, int base, int uppercase);
char	*ft_utoa_base(unsigned long n, int base, int upper);

#endif
