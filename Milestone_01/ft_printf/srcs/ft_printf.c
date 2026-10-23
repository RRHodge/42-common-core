/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 10:38:21 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:01:21 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_printf(const char *fmt, ...)
{
	va_list	args;
	t_flags	flags;
	int		total;
	int		pos;

	va_start(args, fmt);
	total = 0;
	pos = 0;
	if (!fmt)
		return (-1);
	while (fmt[pos])
	{
		if (fmt[pos] == '%')
		{
			pos++;
			flags = ft_parse(fmt, &pos, args);
			total += ft_handle_fmt(fmt[pos], args, &flags);
		}
		else
			total += ft_putchar(fmt[pos]);
		pos++;
	}
	va_end(args);
	return (total);
}
