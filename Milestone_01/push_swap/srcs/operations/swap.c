/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:22:26 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	swap_top(t_stack *s)
{
	void	*tmp;

	if (s->size < 2)
		return ;
	tmp = s->top->content;
	s->top->content = s->top->next->content;
	s->top->next->content = tmp;
}

int	sa(t_stack *a)
{
	swap_top(a);
	ft_printf("sa\n");
	if (a->bench)
		a->bench->ops[OP_SA]++;
	return (1);
}

int	sb(t_stack *b)
{
	swap_top(b);
	ft_printf("sb\n");
	if (b->bench)
		b->bench->ops[OP_SB]++;
	return (1);
}

int	ss(t_stack *a, t_stack *b)
{
	swap_top(a);
	swap_top(b);
	ft_printf("ss\n");
	if (a->bench)
		a->bench->ops[OP_SS]++;
	return (1);
}
