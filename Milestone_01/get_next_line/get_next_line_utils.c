/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/12 10:12:35 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/04 11:02:48 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(const char *s)
{
	size_t	length;

	length = 0;
	if (!s)
		return (0);
	while (*s)
	{
		length++;
		s++;
	}
	return (length);
}

char	*ft_strchr(const char *s, int c)
{
	if (!s)
		return (NULL);
	while (*s != '\0')
	{
		if (*s == (char)c)
			return ((char *)s);
		s++;
	}
	if ((char)c == '\0')
		return ((char *)s);
	return (0);
}

void	*ft_memcpy(void *dest, const void *src, size_t len)
{
	size_t	i;

	if (!src && !dest)
		return (NULL);
	i = 0;
	while (i < len)
	{
		((unsigned char *)dest)[i] = ((unsigned char *)src)[i];
		i++;
	}
	return (dest);
}

char	*ft_strjoin(char *storage, char *buffer)
{
	char	*new_str;
	size_t	len_s;
	size_t	len_b;

	if (!storage)
	{
		storage = (char *)malloc(sizeof(char) * 1);
		if (!storage)
			return (NULL);
		storage[0] = '\0';
	}
	if (!buffer)
		return (NULL);
	len_s = ft_strlen(storage);
	len_b = ft_strlen(buffer);
	new_str = (char *)malloc(sizeof(char) * (len_s + len_b + 1));
	if (!new_str)
	{
		free(storage);
		return (NULL);
	}
	ft_memcpy(new_str, storage, len_s);
	ft_memcpy(new_str + len_s, buffer, len_b + 1);
	free(storage);
	return (new_str);
}
