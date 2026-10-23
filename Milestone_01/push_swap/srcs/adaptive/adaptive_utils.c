/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   adaptive_utils.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 12:19:36 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/17 12:23:51 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	copy_to_array(t_stack *a, int *arr)
{
	t_list	*cur;
	int		i;

	cur = a->top;
	i = 0;
	while (cur)
	{
		arr[i++] = *(int *)cur->content;
		cur = cur->next;
	}
}

static long	count_inversions(int *arr, int n)
{
	long	inv;
	int		i;
	int		j;

	inv = 0;
	i = 0;
	while (i < n)
	{
		j = i + 1;
		while (j < n)
		{
			if (arr[i] > arr[j])
				inv++;
			j++;
		}
		i++;
	}
	return (inv);
}

double	compute_disorder(t_stack *a)
{
	int		*arr;
	long	inv;
	long	max_inv;
	int		n;

	n = a->size;
	if (n <= 1)
		return (0.0);
	arr = malloc(n * sizeof(int));
	if (!arr)
		return (0.5);
	copy_to_array(a, arr);
	inv = count_inversions(arr, n);
	free(arr);
	max_inv = (long)n * (n - 1) / 2;
	return ((double)inv / (double)max_inv);
}
