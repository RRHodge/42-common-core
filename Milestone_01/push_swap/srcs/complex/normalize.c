/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   normalize.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:40:13 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/15 00:00:00 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	sort_array(int *arr, int n)
{
	int	i;
	int	j;
	int	tmp;

	i = 0;
	while (i < n)
	{
		j = i + 1;
		while (j < n)
		{
			if (arr[j] < arr[i])
			{
				tmp = arr[i];
				arr[i] = arr[j];
				arr[j] = tmp;
			}
			j++;
		}
		i++;
	}
}

static void	copy_values(t_stack *a, int *sorted, int n)
{
	t_list	*tmp;
	int		i;

	tmp = a->top;
	i = 0;
	while (i < n)
	{
		sorted[i++] = *(int *)tmp->content;
		tmp = tmp->next;
	}
}

static void	assign_ranks(t_stack *a, int *sorted, int n)
{
	t_list	*tmp;
	int		j;

	tmp = a->top;
	while (tmp)
	{
		j = 0;
		while (j < n && sorted[j] != *(int *)tmp->content)
			j++;
		*(int *)tmp->content = j;
		tmp = tmp->next;
	}
}

void	normalize_ranks(t_stack *a, int n)
{
	int	*sorted;

	sorted = malloc(n * sizeof(int));
	if (!sorted)
		exit(1);
	copy_values(a, sorted, n);
	sort_array(sorted, n);
	assign_ranks(a, sorted, n);
	free(sorted);
}
