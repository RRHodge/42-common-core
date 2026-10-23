/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   phase1.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 09:43:56 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:21:45 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static t_chunk	compute_chunk(t_bit_ctx *ctx, int i)
{
	t_chunk	ck;

	ck.low = i * ctx->chunk_size;
	ck.high = ck.low + ctx->chunk_size - 1;
	if (i == ctx->nb_chunks - 1)
		ck.high = ctx->n - 1;
	ck.mid = (ck.low + ck.high) / 2;
	return (ck);
}

static void	process_top(t_stack *a, t_stack *b, t_bit_ctx *ctx, t_chunk ck)
{
	int	rank;

	rank = get_rank(a->top);
	if (rank >= ck.low && rank <= ck.high)
	{
		op_pb(a, b, ctx);
		if (get_rank(b->top) >= ck.mid)
			op_rb(b, ctx);
	}
	else
		ra(a);
}

static void	push_chunk_to_b(t_stack *a, t_stack *b, t_bit_ctx *ctx, int i)
{
	t_chunk	ck;

	ck = compute_chunk(ctx, i);
	while (bit_range(ctx->bit_a, ck.low, ck.high) > 0)
		process_top(a, b, ctx, ck);
}

void	push_chunks_to_b(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	int	i;

	i = 0;
	while (i < ctx->nb_chunks)
	{
		push_chunk_to_b(a, b, ctx, i);
		i++;
	}
}
