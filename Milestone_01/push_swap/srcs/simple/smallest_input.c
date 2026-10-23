/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   smallest_input.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/31 12:24:26 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/31 13:18:20 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_3(t_stack *a)
{
	int	first;
	int	second;
	int	third;

	first = *(int *)a->top->content;
	second = *(int *)a->top->next->content;
	third = *(int *)a->top->next->next->content;
	if (first > second && second < third && third > first)
		sa(a);
	else if (first > second && second > third && third < first)
	{
		sa(a);
		rra(a);
	}
	else if (first > second && second < third && third < first)
		ra(a);
	else if (first < second && second > third && third > first)
	{
		sa(a);
		ra(a);
	}
	else if (first < second && second > third && third < first)
		rra(a);
}

void	sort_5(t_stack *a, t_stack *b)
{
	bring_min_top(a);
	pb(a, b);
	bring_min_top(a);
	pb(a, b);
	sort_3(a);
	pa(a, b);
	pa(a, b);
}

void	sort_dispatcher(t_stack *a, t_stack *b)
{
	if (a->size == 2)
		sa(a);
	else if (a->size == 3)
		sort_3(a);
	else if (a->size == 4 || a->size == 5)
		sort_5(a, b);
}
