/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_utils.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 10:39:05 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/24 16:01:02 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putstr_n(char *s, int n)
{
	write(1, s, n);
	return (n);
}

static int	ft_num_len(unsigned long n, int base)
{
	int	len;

	len = 0;
	while (n > 0)
	{
		len++;
		n /= base;
	}
	return (len);
}

static void	ft_fill_buf(char *buf, unsigned long n, char *charset, int len)
{
	int	base;

	base = ft_strlen(charset);
	while (n > 0)
	{
		buf[--len] = charset[n % (unsigned long)base];
		n /= (unsigned long)base;
	}
}

char	*ft_utoa_base(unsigned long n, int base, int upper)
{
	char	*buf;
	char	*charset;
	int		len;

	if (upper == 1)
		charset = "0123456789ABCDEF";
	else if (upper == 0)
		charset = "0123456789abcdef";
	else
		charset = "0123456789";
	if (n == 0)
		len = 1;
	else
		len = ft_num_len(n, base);
	buf = malloc(len + 1);
	if (!buf)
		return (NULL);
	buf[len] = '\0';
	if (n == 0)
		buf[0] = '0';
	else
		ft_fill_buf(buf, n, charset, len);
	return (buf);
}
