/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:22:24 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	rotate_stack(t_stack *s)
{
	t_list	*node;
	t_list	*last;

	if (s->size < 2)
		return ;
	node = s->top;
	s->top = s->top->next;
	node->next = NULL;
	last = s->top;
	while (last->next)
		last = last->next;
	last->next = node;
}

int	ra(t_stack *a)
{
	rotate_stack(a);
	ft_printf("ra\n");
	if (a->bench)
		a->bench->ops[OP_RA]++;
	return (1);
}

int	rb(t_stack *b)
{
	rotate_stack(b);
	ft_printf("rb\n");
	if (b->bench)
		b->bench->ops[OP_RB]++;
	return (1);
}

int	rr(t_stack *a, t_stack *b)
{
	rotate_stack(a);
	rotate_stack(b);
	ft_printf("rr\n");
	if (a->bench)
		a->bench->ops[OP_RR]++;
	return (1);
}
