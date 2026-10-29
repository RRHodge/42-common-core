/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/22 16:54:16 by rarabeto          #+#    #+#             */
/*   Updated: 2026/01/31 10:33:47 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	src_length;

	src_length = ft_strlen(src);
	if (src_length >= size)
	{
		if (size > 0)
		{
			ft_memcpy(dst, src, size);
			dst[size - 1] = '\0';
		}
	}
	else
		ft_memcpy(dst, src, src_length + 1);
	return (src_length);
}
