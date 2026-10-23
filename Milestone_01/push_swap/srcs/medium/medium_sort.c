/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   medium_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 14:14:29 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 12:43:59 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	count_in_range(t_stack *a, int low, int high)
{
	t_list	*cur;
	int		count;
	int		rank;

	cur = a->top;
	count = 0;
	while (cur)
	{
		rank = *(int *)cur->content;
		if (rank >= low && rank <= high)
			count++;
		cur = cur->next;
	}
	return (count);
}

static void	handle_in_chunk(t_stack *a, t_stack *b, int mid)
{
	pb(a, b);
	if (b->size > 1 && *(int *)b->top->content >= mid)
		rb(b);
}

static void	push_chunk(t_stack *a, t_stack *b, int low, int high)
{
	int	mid;
	int	rank;

	mid = (low + high) / 2;
	while (count_in_range(a, low, high) > 0)
	{
		rank = *(int *)a->top->content;
		if (rank >= low && rank <= high)
			handle_in_chunk(a, b, mid);
		else
			ra(a);
	}
}

static void	push_by_chunks(t_stack *a, t_stack *b, int size)
{
	int	nb_chunks;
	int	chunk_size;
	int	chunk;
	int	low;

	nb_chunks = get_nb_chunks(size);
	chunk_size = size / nb_chunks;
	chunk = 0;
	low = 0;
	while (chunk < nb_chunks)
	{
		if (chunk == nb_chunks - 1)
			push_chunk(a, b, low, size - 1);
		else
			push_chunk(a, b, low, low + chunk_size - 1);
		low += chunk_size;
		chunk++;
	}
}

void	sort_range(t_stack *a, t_stack *b, int size)
{
	normalize_ranks(a, size);
	push_by_chunks(a, b, size);
	while (b->size > 0)
		bring_back_max(a, b);
}
