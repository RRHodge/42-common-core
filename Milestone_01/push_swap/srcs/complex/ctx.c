/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ctx.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 09:40:13 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 16:32:04 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	get_rank(t_list *node)
{
	return (*(int *)node->content);
}

static int	*alloc_array(int size)
{
	int	*arr;
	int	i;

	arr = malloc(size * sizeof(int));
	if (!arr)
		exit(1);
	i = 0;
	while (i < size)
		arr[i++] = 0;
	return (arr);
}

int	get_nb_chunks(int n)
{
	int	chunks;
	int	tmp;

	if (n <= 10)
		return (1);
	if (n <= 100)
		return (5);
	if (n <= 500)
		return (9);
	chunks = 0;
	tmp = n;
	while (tmp > 1)
	{
		tmp >>= 1;
		chunks++;
	}
	return (chunks);
}

t_bit_ctx	*ctx_new(int n, int nb_chunks)
{
	t_bit_ctx	*ctx;

	ctx = malloc(sizeof(t_bit_ctx));
	if (!ctx)
		exit(1);
	ctx->bit_a = alloc_array(n + 1);
	ctx->bit_b = alloc_array(n + 1);
	ctx->b_circ = alloc_array(n);
	ctx->pos_of_rank = alloc_array(n);
	ctx->b_top = 0;
	ctx->b_size = 0;
	ctx->n = n;
	ctx->nb_chunks = nb_chunks;
	ctx->chunk_size = n / nb_chunks;
	return (ctx);
}

void	ctx_free(t_bit_ctx *ctx)
{
	free(ctx->bit_a);
	free(ctx->bit_b);
	free(ctx->b_circ);
	free(ctx->pos_of_rank);
	free(ctx);
}
