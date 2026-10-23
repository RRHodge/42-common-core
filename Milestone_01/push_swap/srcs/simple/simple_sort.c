/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simple_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 14:13:36 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/31 13:02:10 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	optimal_rotate(t_stack *s, int pos,
				int (*rot)(t_stack *), int (*rot_inv)(t_stack *))
{
	int	nb_rot;

	if (pos <= s->size / 2)
	{
		while (pos--)
			rot(s);
	}
	else
	{
		nb_rot = s->size - pos;
		while (nb_rot--)
			rot_inv(s);
	}
}

void	bring_min_top(t_stack *a)
{
	optimal_rotate(a, find_min_pos(a), ra, rra);
}

static void	bring_max_top(t_stack *b)
{
	optimal_rotate(b, find_max_pos(b), rb, rrb);
}

void	simple(t_stack *a, t_stack *b)
{
	while (a->size > 0)
	{
		bring_min_top(a);
		pb(a, b);
	}
	while (b->size > 0)
	{
		bring_max_top(b);
		pa(a, b);
	}
}
