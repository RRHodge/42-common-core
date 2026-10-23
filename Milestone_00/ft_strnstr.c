/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 18:05:41 by rarabeto          #+#    #+#             */
/*   Updated: 2026/01/31 11:19:08 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *s, const char *find, size_t len)
{
	size_t	j;
	size_t	i;

	if ((!*s && *find == '\0') || !*find)
		return ((char *)s);
	i = 0;
	while (s[i] != '\0')
	{
		j = 0;
		while (find[j] != '\0' && s[i + j] == find[j] && i + j < len)
		{
			j++;
			if (find[j] == '\0')
				return ((char *)&s[i]);
		}
		i++;
	}
	return (0);
}
