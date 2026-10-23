/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   phase2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 09:45:41 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:21:53 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	relative_pos(t_bit_ctx *ctx, int rank)
{
	int	pos;
	int	rel;

	pos = ctx->pos_of_rank[rank];
	rel = (pos - ctx->b_top + ctx->n) % ctx->n;
	return (rel);
}

static void	align_to_top(t_stack *b, t_bit_ctx *ctx, int rel)
{
	int	count;

	if (rel <= ctx->b_size / 2)
	{
		count = rel;
		while (count > 0)
		{
			op_rb(b, ctx);
			count--;
		}
	}
	else
	{
		count = ctx->b_size - rel;
		while (count > 0)
		{
			op_rrb(b, ctx);
			count--;
		}
	}
}

static void	extract_max(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	int	max_rank;
	int	rel;

	max_rank = bit_find_max(ctx->bit_b, ctx->n, ctx->b_size);
	rel = relative_pos(ctx, max_rank);
	align_to_top(b, ctx, rel);
	op_pa(a, b, ctx);
}

static void	rebuild_a(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	while (ctx->b_size > 0)
		extract_max(a, b, ctx);
}

void	sort_range_bit(t_stack *a, t_stack *b, int n)
{
	t_bit_ctx	*ctx;
	int			nb_chunks;

	normalize_ranks(a, n);
	nb_chunks = get_nb_chunks(n);
	ctx = ctx_new(n, nb_chunks);
	bit_init(ctx->bit_a, n);
	push_chunks_to_b(a, b, ctx);
	rebuild_a(a, b, ctx);
	ctx_free(ctx);
}
