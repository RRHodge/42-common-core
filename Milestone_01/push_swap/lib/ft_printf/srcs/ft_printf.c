/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/10 11:30:09 by tny-onin          #+#    #+#             */
/*   Updated: 2026/02/12 14:18:11 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	check_format(va_list args, const char *input);

int	ft_printf(const char *input, ...)
{
	va_list	args;
	int		i;

	i = 0;
	va_start(args, input);
	while (*input != '\0')
	{
		if (*input == '%')
		{
			input++;
			if (*input == '%')
				i += print_char('%');
			else
				i += check_format(args, input);
		}
		else
			i += print_char(*input);
		input++;
	}
	va_end(args);
	return (i);
}

static int	check_format(va_list args, const char *input)
{
	if (*input == 'c')
		return (print_char(va_arg(args, int)));
	else if (*input == 's')
		return (print_str((char *)va_arg(args, char *)));
	else if (*input == 'd' || *input == 'i')
		return (print_nbr(va_arg(args, int)));
	else if (*input == 'u')
		return (print_unsigned(va_arg(args, unsigned int)));
	else if (*input == 'x' || *input == 'X')
		return (print_hex(va_arg(args, unsigned int), *input));
	else if (*input == 'p')
		return (print_pointer(va_arg(args, void *)));
	return (0);
}
