/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rev_rotate.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/15 00:00:00 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	rev_rotate_stack(t_stack *s)
{
	t_list	*prev;
	t_list	*last;

	if (s->size < 2)
		return ;
	prev = s->top;
	last = s->top;
	while (last->next)
	{
		prev = last;
		last = last->next;
	}
	prev->next = NULL;
	last->next = s->top;
	s->top = last;
}

int	rra(t_stack *a)
{
	rev_rotate_stack(a);
	ft_printf("rra\n");
	if (a->bench)
		a->bench->ops[OP_RRA]++;
	return (1);
}

int	rrb(t_stack *b)
{
	rev_rotate_stack(b);
	ft_printf("rrb\n");
	if (b->bench)
		b->bench->ops[OP_RRB]++;
	return (1);
}

int	rrr(t_stack *a, t_stack *b)
{
	rev_rotate_stack(a);
	rev_rotate_stack(b);
	ft_printf("rrr\n");
	if (a->bench)
		a->bench->ops[OP_RRR]++;
	return (1);
}
