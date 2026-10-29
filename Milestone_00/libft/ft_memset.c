/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/22 16:43:34 by rarabeto          #+#    #+#             */
/*   Updated: 2026/01/31 10:30:44 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *dst, int c, size_t len)
{
	unsigned char	*dstp;

	dstp = (unsigned char *)dst;
	while (len > 0)
	{
		dstp[len - 1] = c;
		len--;
	}
	return (dst);
}
