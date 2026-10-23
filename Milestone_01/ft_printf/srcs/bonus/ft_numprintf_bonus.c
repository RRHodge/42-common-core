/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_numprintf_bonus.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/06 10:44:11 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:00:09 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_pad(char c, int n)
{
	int	total;

	total = 0;
	while (n-- > 0)
		total += ft_putchar(c);
	return (total);
}

int	ft_numprint(t_flags *flags, char *prefix, char *digits)
{
	int	prefix_len;
	int	digits_len;
	int	prec_pad;
	int	total_len;
	int	total;

	prefix_len = ft_strlen(prefix);
	digits_len = ft_strlen(digits);
	prec_pad = 0;
	if (flags->has_prec && flags->prec > digits_len)
		prec_pad = flags->prec - digits_len;
	total_len = prefix_len + prec_pad + digits_len;
	total = 0;
	if (!flags->minus && !(flags->zero && !flags->has_prec))
		total += ft_pad(' ', flags->width - total_len);
	total += ft_putstr_n(prefix, prefix_len);
	if (flags->zero && !flags->minus && !flags->has_prec)
		total += ft_pad('0', flags->width - total_len);
	total += ft_pad('0', prec_pad);
	total += ft_putstr_n(digits, digits_len);
	if (flags->minus)
		total += ft_pad(' ', flags->width - total_len);
	return (total);
}

char	*ft_get_digits(t_flags *flags, unsigned long n, int base, int uppercase)
{
	char	*digits;

	if (flags->has_prec && flags->prec == 0 && n == 0)
	{
		digits = malloc(1);
		if (!digits)
			return (NULL);
		digits[0] = '\0';
		return (digits);
	}
	return (ft_utoa_base(n, base, uppercase));
}
