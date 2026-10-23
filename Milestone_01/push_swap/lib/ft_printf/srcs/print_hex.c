/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_hex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/10 14:56:29 by tny-onin          #+#    #+#             */
/*   Updated: 2026/02/12 14:23:36 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_hex(uintptr_t n, char format)
{
	char	*hex;
	int		len;

	len = 0;
	if (format == 'x')
		hex = "0123456789abcdef";
	else if (format == 'X')
		hex = "0123456789ABCDEF";
	if (n < 16)
		ft_putchar_fd(hex[n], 1);
	else
	{
		len += print_hex(n / 16, format);
		ft_putchar_fd(hex[n % 16], 1);
	}
	return (len + 1);
}
