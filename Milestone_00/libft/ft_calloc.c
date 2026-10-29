/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 15:59:28 by rarabeto          #+#    #+#             */
/*   Updated: 2026/01/31 10:03:48 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	void	*ptr;

	if (nmemb != 0 && (size_t)-1 / nmemb < size)
		return ((void *)0);
	ptr = (void *)malloc(nmemb * size);
	if (!ptr)
		return ((void *)0);
	ft_bzero(ptr, (nmemb * size));
	return (ptr);
}
