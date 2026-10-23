/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_pointer.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/10 15:35:19 by tny-onin          #+#    #+#             */
/*   Updated: 2026/02/12 14:25:51 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_pointer(void *ptr)
{
	uintptr_t	address;
	int			len;
	int			tmp;

	if (!ptr)
		return (print_str("(nil)"));
	len = print_str("0x");
	if (len == -1)
		return (-1);
	address = (uintptr_t)ptr;
	tmp = print_hex(address, 'x');
	if (tmp == -1)
		return (-1);
	return (len + tmp);
}
