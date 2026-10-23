/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ops.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 09:41:47 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 12:35:53 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	op_pb(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	int	rank;

	rank = get_rank(a->top);
	pb(a, b);
	bit_update(ctx->bit_a, ctx->n, rank, -1);
	bit_update(ctx->bit_b, ctx->n, rank, 1);
	ctx->b_top = (ctx->b_top - 1 + ctx->n) % ctx->n;
	ctx->b_circ[ctx->b_top] = rank;
	ctx->pos_of_rank[rank] = ctx->b_top;
	ctx->b_size++;
}

void	op_rb(t_stack *b, t_bit_ctx *ctx)
{
	int	r;
	int	new_bot;

	if (ctx->b_size < 2)
		return ;
	r = ctx->b_circ[ctx->b_top];
	new_bot = (ctx->b_top + ctx->b_size) % ctx->n;
	ctx->b_circ[new_bot] = r;
	ctx->pos_of_rank[r] = new_bot;
	rb(b);
	ctx->b_top = (ctx->b_top + 1) % ctx->n;
}

void	op_rrb(t_stack *b, t_bit_ctx *ctx)
{
	int	old_bot;
	int	r;
	int	new_top;

	if (ctx->b_size < 2)
		return ;
	old_bot = (ctx->b_top + ctx->b_size - 1) % ctx->n;
	r = ctx->b_circ[old_bot];
	new_top = (ctx->b_top - 1 + ctx->n) % ctx->n;
	ctx->b_circ[new_top] = r;
	ctx->pos_of_rank[r] = new_top;
	rrb(b);
	ctx->b_top = new_top;
}

void	op_pa(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	int	rank;

	rank = ctx->b_circ[ctx->b_top];
	pa(a, b);
	bit_update(ctx->bit_b, ctx->n, rank, -1);
	ctx->b_top = (ctx->b_top + 1) % ctx->n;
	ctx->b_size--;
}
