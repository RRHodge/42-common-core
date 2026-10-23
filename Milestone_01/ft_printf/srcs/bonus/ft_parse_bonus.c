/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_parse_bonus.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/06 10:44:11 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:00:14 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	is_flag(char c)
{
	return (c == '-' || c == '0' || c == '#' || c == ' ' || c == '+');
}

static void	set_flag(t_flags *flags, char c)
{
	if (c == '-')
		flags->minus = 1;
	else if (c == '0')
		flags->zero = 1;
	else if (c == '#')
		flags->hash = 1;
	else if (c == ' ')
		flags->space = 1;
	else if (c == '+')
		flags->plus = 1;
}

static int	parse_num(const char *fmt, int *pos, va_list args)
{
	int	n;

	n = 0;
	if (fmt[*pos] == '*')
	{
		n = va_arg(args, int);
		(*pos)++;
		return (n);
	}
	while (fmt[*pos] >= '0' && fmt[*pos] <= '9')
		n = n * 10 + (fmt[(*pos)++] - '0');
	return (n);
}

t_flags	ft_parse(const char *fmt, int *pos, va_list args)
{
	t_flags	flags;

	flags.minus = 0;
	flags.zero = 0;
	flags.hash = 0;
	flags.space = 0;
	flags.plus = 0;
	flags.width = 0;
	flags.prec = 0;
	flags.has_prec = 0;
	while (is_flag(fmt[*pos]))
	{
		set_flag(&flags, fmt[*pos]);
		(*pos)++;
	}
	flags.width = parse_num(fmt, pos, args);
	if (fmt[*pos] == '.')
	{
		(*pos)++;
		flags.has_prec = 1;
		flags.prec = parse_num(fmt, pos, args);
	}
	return (flags);
}
