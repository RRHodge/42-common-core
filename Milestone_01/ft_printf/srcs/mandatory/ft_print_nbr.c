/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_nbr.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 10:38:01 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:00:50 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_int(t_flags *flags, long n)
{
	unsigned long	abs_val;
	char			*prefix;
	char			*digits;
	int				total;

	if (n < 0)
		prefix = "-";
	else if (flags->plus)
		prefix = "+";
	else if (flags->space)
		prefix = " ";
	else
		prefix = "";
	if (n < 0)
		abs_val = (unsigned long)-n;
	else
		abs_val = (unsigned long)n;
	digits = ft_get_digits(flags, abs_val, 10, -1);
	if (!digits)
		return (0);
	total = ft_numprint(flags, prefix, digits);
	free(digits);
	return (total);
}

int	ft_print_uint(t_flags *flags, unsigned long n, int base, int upper)
{
	char	*prefix;
	char	*digits;
	int		total;

	prefix = "";
	if (flags->hash && n != 0)
	{
		if (base == 16 && !upper)
			prefix = "0x";
		else if (base == 16)
			prefix = "0X";
	}
	digits = ft_get_digits(flags, n, base, upper);
	if (!digits)
		return (0);
	total = ft_numprint(flags, prefix, digits);
	free(digits);
	return (total);
}

int	ft_print_ptr(t_flags *flags, unsigned long n)
{
	char	*digits;
	int		ptr_len;
	int		total;

	if (!n)
		return (ft_print_str(flags, "(nil)"));
	digits = ft_utoa_base(n, 16, 0);
	if (!digits)
		return (0);
	ptr_len = 2 + ft_strlen(digits);
	total = 0;
	if (!flags->minus)
		total += ft_pad(' ', flags->width - ptr_len);
	total += ft_putstr_n("0x", 2);
	total += ft_putstr_n(digits, ft_strlen(digits));
	if (flags->minus)
		total += ft_pad(' ', flags->width - ptr_len);
	free(digits);
	return (total);
}
