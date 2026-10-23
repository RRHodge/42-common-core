/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_cs.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 10:37:41 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:00:40 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putchar(char c)
{
	ft_putchar_fd(c, 1);
	return (1);
}

int	ft_print_char(t_flags *flags, int c)
{
	int	total;

	total = 0;
	if (!flags->minus)
		total += ft_pad(' ', flags->width - 1);
	total += ft_putchar((char)c);
	if (flags->minus)
		total += ft_pad(' ', flags->width - 1);
	return (total);
}

int	ft_print_str(t_flags *flags, char *s)
{
	int	len;
	int	total;

	if (!s)
		s = "(null)";
	len = ft_strlen(s);
	if (flags->has_prec && flags->prec < len)
		len = flags->prec;
	total = 0;
	if (!flags->minus)
		total += ft_pad(' ', flags->width - len);
	total += ft_putstr_n(s, len);
	if (flags->minus)
		total += ft_pad(' ', flags->width - len);
	return (total);
}

int	ft_print_mod(t_flags *flags)
{
	int	total;

	total = 0;
	if (!flags->minus)
		total += ft_pad(' ', flags->width - 1);
	total += ft_putchar('%');
	if (flags->minus)
		total += ft_pad(' ', flags->width - 1);
	return (total);
}
