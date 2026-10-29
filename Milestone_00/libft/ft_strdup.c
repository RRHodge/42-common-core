/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 15:44:10 by rarabeto          #+#    #+#             */
/*   Updated: 2026/02/05 13:51:34 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s)
{
	int		count;
	char	*dest;

	if (!s)
		return (NULL);
	count = ft_strlen(s);
	dest = (char *)malloc(sizeof(*s) * (count + 1));
	if (!dest)
		return ((void *)0);
	ft_memcpy(dest, s, count);
	dest[count] = '\0';
	return (dest);
}
