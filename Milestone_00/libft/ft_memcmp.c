/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/25 15:55:52 by rarabeto          #+#    #+#             */
/*   Updated: 2026/01/31 11:39:54 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	size_t			index;
	unsigned char	*dst;
	unsigned char	*src;

	index = 0;
	dst = (unsigned char *)s1;
	src = (unsigned char *)s2;
	while (index < n)
	{
		if (dst[index] != src[index])
			return (dst[index] - src[index]);
		index++;
	}
	return (0);
}
