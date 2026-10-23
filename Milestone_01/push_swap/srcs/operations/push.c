/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:22:31 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	transfer_node(t_stack *dst, t_stack *src)
{
	t_list	*node;

	if (!src->size)
		return ;
	node = src->top;
	src->top = src->top->next;
	src->size--;
	node->next = dst->top;
	dst->top = node;
	dst->size++;
}

int	pa(t_stack *a, t_stack *b)
{
	transfer_node(a, b);
	ft_printf("pa\n");
	if (a->bench)
		a->bench->ops[OP_PA]++;
	return (1);
}

int	pb(t_stack *a, t_stack *b)
{
	transfer_node(b, a);
	ft_printf("pb\n");
	if (a->bench)
		a->bench->ops[OP_PB]++;
	return (1);
}
