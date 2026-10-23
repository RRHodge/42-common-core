/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/31 13:00:24 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	init_stacks(t_stack *a, t_stack *b)
{
	a->top = NULL;
	a->size = 0;
	a->bench = NULL;
	b->top = NULL;
	b->size = 0;
	b->bench = NULL;
}

void	run_sort(t_stack *a, t_stack *b, char strategy)
{
	if (strategy == 's')
		simple(a, b);
	else if (strategy == 'm')
		sort_range(a, b, a->size);
	else if (strategy == 'c')
		sort_range_bit(a, b, a->size);
	else
		adaptive(a, b);
}

static void	sort_bench(t_stack *a, t_stack *b, char strategy)
{
	if (!is_sorted(a))
		run_sort(a, b, strategy);
}

static void	print_bench(t_bench *bench, int bench_on)
{
	if (bench_on)
		bench_print(bench);
}

int	main(int argc, char **argv)
{
	t_stack	a;
	t_stack	b;
	t_bench	bench;
	char	strategy;
	int		bench_on;

	if (argc < 2)
		return (0);
	strategy = parse_strategy(argc, argv);
	bench_on = parse_bench(argc, argv);
	init_stacks(&a, &b);
	if (!parse_args(&a, argc, argv, parse_start(argc, argv)))
	{
		stack_free(&a);
		return (1);
	}
	if (bench_on)
		bench_init(&a, &b, &bench, strategy);
	push_swap_dispatcher(&a, &b);
	sort_bench(&a, &b, strategy);
	print_bench(&bench, bench_on);
	stack_free(&a);
	stack_free(&b);
	return (0);
}
