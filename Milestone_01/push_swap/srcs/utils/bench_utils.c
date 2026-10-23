/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/13 00:00:00 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/15 00:00:00 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static char	*strategy_name(t_bench *bench)
{
	if (bench->strategy == 's')
		return ((char *)"Simple / O(n^2)");
	if (bench->strategy == 'm')
		return ((char *)"Medium / O(n*sqrt(n))");
	if (bench->strategy == 'c')
		return ((char *)"Complex / O(n log n)");
	if (bench->used == 's')
		return ((char *)"Adaptive / O(n^2)");
	if (bench->used == 'm')
		return ((char *)"Adaptive / O(n*sqrt(n))");
	return ((char *)"Adaptive / O(n log n)");
}

static void	print_ops_line1(int *o)
{
	ft_putstr_fd("[bench] sa: ", 2);
	ft_putnbr_fd(o[OP_SA], 2);
	ft_putstr_fd(" sb: ", 2);
	ft_putnbr_fd(o[OP_SB], 2);
	ft_putstr_fd(" ss: ", 2);
	ft_putnbr_fd(o[OP_SS], 2);
	ft_putstr_fd(" pa: ", 2);
	ft_putnbr_fd(o[OP_PA], 2);
	ft_putstr_fd(" pb: ", 2);
	ft_putnbr_fd(o[OP_PB], 2);
	ft_putstr_fd("\n", 2);
}

static void	print_ops_line2(int *o)
{
	ft_putstr_fd("[bench] ra: ", 2);
	ft_putnbr_fd(o[OP_RA], 2);
	ft_putstr_fd(" rb: ", 2);
	ft_putnbr_fd(o[OP_RB], 2);
	ft_putstr_fd(" rr: ", 2);
	ft_putnbr_fd(o[OP_RR], 2);
	ft_putstr_fd(" rra: ", 2);
	ft_putnbr_fd(o[OP_RRA], 2);
	ft_putstr_fd(" rrb: ", 2);
	ft_putnbr_fd(o[OP_RRB], 2);
	ft_putstr_fd(" rrr: ", 2);
	ft_putnbr_fd(o[OP_RRR], 2);
	ft_putstr_fd("\n", 2);
}

void	bench_init(t_stack *a, t_stack *b, t_bench *bench, char strategy)
{
	int	i;

	i = 0;
	while (i < OP_NB)
		bench->ops[i++] = 0;
	bench->strategy = strategy;
	bench->used = strategy;
	bench->disorder = compute_disorder(a);
	a->bench = bench;
	b->bench = bench;
}

void	bench_print(t_bench *bench)
{
	int	*o;
	int	total;
	int	pct;
	int	frac;

	o = bench->ops;
	total = o[0] + o[1] + o[2] + o[3] + o[4] + o[5]
		+ o[6] + o[7] + o[8] + o[9] + o[10];
	pct = (int)(bench->disorder * 100);
	frac = (int)(bench->disorder * 10000) % 100;
	ft_putstr_fd("[bench] desordre: ", 2);
	ft_putnbr_fd(pct, 2);
	ft_putchar_fd('.', 2);
	if (frac < 10)
		ft_putchar_fd('0', 2);
	ft_putnbr_fd(frac, 2);
	ft_putstr_fd("%\n[bench] strategie: ", 2);
	ft_putstr_fd(strategy_name(bench), 2);
	ft_putstr_fd("\n[bench] total_ops: ", 2);
	ft_putnbr_fd(total, 2);
	ft_putstr_fd("\n", 2);
	print_ops_line1(o);
	print_ops_line2(o);
}
