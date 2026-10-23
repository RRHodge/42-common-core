/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_unsigned.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/12 09:40:47 by tny-onin          #+#    #+#             */
/*   Updated: 2026/02/12 10:13:39 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	nbr_digit(unsigned int n);
static char	*ft_uitoa(unsigned int n);

int	print_unsigned(unsigned int n)
{
	char	*num_str;
	int		len;

	num_str = ft_uitoa(n);
	if (!num_str)
		return (0);
	ft_putstr_fd(num_str, 1);
	len = ft_strlen(num_str);
	free(num_str);
	return (len);
}

static char	*ft_uitoa(unsigned int n)
{
	char	*str;
	int		len;

	len = nbr_digit(n);
	str = malloc((len + 1) * sizeof(char));
	if (!str)
		return (NULL);
	str[len] = '\0';
	if (n == 0)
		str[0] = '0';
	while (n != 0)
	{
		str[--len] = (n % 10) + 48;
		n /= 10;
	}
	return (str);
}

static int	nbr_digit(unsigned int n)
{
	int	count;

	if (n == 0)
		return (1);
	count = 0;
	while (n != 0)
	{
		n /= 10;
		count++;
	}
	return (count);
}
