/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_handle.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 10:37:11 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:00:27 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_handle_fmt(char spec, va_list args, t_flags *flags)
{
	if (spec == 'c')
		return (ft_print_char(flags, va_arg(args, int)));
	if (spec == 's')
		return (ft_print_str(flags, va_arg(args, char *)));
	if (spec == 'p')
		return (ft_print_ptr(flags, (unsigned long)va_arg(args, void *)));
	if (spec == 'd' || spec == 'i')
		return (ft_print_int(flags, (long)va_arg(args, int)));
	if (spec == 'u')
		return (ft_print_uint(flags,
				(unsigned long)va_arg(args, unsigned int), 10, -1));
	if (spec == 'x')
		return (ft_print_uint(flags,
				(unsigned long)va_arg(args, unsigned int), 16, 0));
	if (spec == 'X')
		return (ft_print_uint(flags,
				(unsigned long)va_arg(args, unsigned int), 16, 1));
	if (spec == '%')
		return (ft_print_mod(flags));
	if (spec != '\0')
		return (ft_putchar('%') + ft_putchar(spec));
	return (0);
}
