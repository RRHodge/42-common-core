/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   adaptive.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 12:23:42 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	mark_bench_used(t_bench *bench, double d)
{
	if (!bench)
		return ;
	if (d < 0.2)
		bench->used = 's';
	else if (d < 0.5)
		bench->used = 'm';
	else
		bench->used = 'c';
}

static void	run_by_disorder(t_stack *a, t_stack *b, double d)
{
	mark_bench_used(a->bench, d);
	if (d < 0.2)
		simple(a, b);
	else if (d < 0.5)
		sort_range(a, b, a->size);
	else
		sort_range_bit(a, b, a->size);
}

void	adaptive(t_stack *a, t_stack *b)
{
	double	d;

	if (a->size <= 3)
	{
		if (a->bench)
			a->bench->used = 's';
		simple(a, b);
		return ;
	}
	if (a->bench)
		d = a->bench->disorder;
	else
		d = compute_disorder(a);
	run_by_disorder(a, b, d);
}
