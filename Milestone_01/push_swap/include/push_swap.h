/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/31 13:02:40 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "../lib/libft/include/libft.h"
# include "../lib/ft_printf/include/ft_printf.h"
# include <stdlib.h>
# include <limits.h>

# define OP_SA  0
# define OP_SB  1
# define OP_SS  2
# define OP_PA  3
# define OP_PB  4
# define OP_RA  5
# define OP_RB  6
# define OP_RR  7
# define OP_RRA 8
# define OP_RRB 9
# define OP_RRR 10
# define OP_NB  11

typedef struct s_bench
{
	int		ops[OP_NB];
	char	strategy;
	char	used;
	double	disorder;
}	t_bench;

typedef enum e_mode
{
	MODE_ADAPTIVE,
	MODE_SIMPLE,
	MODE_MEDIUM,
	MODE_COMPLEX
}	t_mode;

typedef enum s_bool
{
	false,
	true
}		t_bool;

typedef struct s_stack
{
	t_list	*top;
	int		size;
	t_bench	*bench;
}	t_stack;

typedef struct s_chunk
{
	int	low;
	int	high;
	int	mid;
}	t_chunk;

typedef struct s_bit_ctx
{
	int	*bit_a;
	int	*bit_b;
	int	*b_circ;
	int	*pos_of_rank;
	int	b_top;
	int	b_size;
	int	n;
	int	nb_chunks;
	int	chunk_size;
}	t_bit_ctx;

int			pa(t_stack *a, t_stack *b);
int			pb(t_stack *a, t_stack *b);
int			sa(t_stack *a);
int			sb(t_stack *b);
int			ss(t_stack *a, t_stack *b);
int			ra(t_stack *a);
int			rb(t_stack *b);
int			rr(t_stack *a, t_stack *b);
int			rra(t_stack *a);
int			rrb(t_stack *b);
int			rrr(t_stack *a, t_stack *b);

int			find_min_pos(t_stack *s);
int			find_max_pos(t_stack *s);
void		simple(t_stack *a, t_stack *b);

void		normalize_ranks(t_stack *a, int n);
void		bring_back_max(t_stack *a, t_stack *b);
void		sort_range(t_stack *a, t_stack *b, int size);

void		bit_update(int *bit, int n, int rank, int delta);
int			bit_query(int *bit, int rank);
int			bit_range(int *bit, int low, int high);
int			bit_find_max(int *bit, int n, int count);
void		bit_init(int *bit, int n);

int			get_nb_chunks(int n);
int			get_rank(t_list *node);
t_bit_ctx	*ctx_new(int n, int nb_chunks);
void		ctx_free(t_bit_ctx *ctx);

void		op_pb(t_stack *a, t_stack *b, t_bit_ctx *ctx);
void		op_rb(t_stack *b, t_bit_ctx *ctx);
void		op_rrb(t_stack *b, t_bit_ctx *ctx);
void		op_pa(t_stack *a, t_stack *b, t_bit_ctx *ctx);
void		op_rr_ctx(t_stack *a, t_stack *b, t_bit_ctx *ctx);
void		op_rrr_ctx(t_stack *a, t_stack *b, t_bit_ctx *ctx);

void		push_chunks_to_b(t_stack *a, t_stack *b, t_bit_ctx *ctx);
void		sort_range_bit(t_stack *a, t_stack *b, int n);

void		sort_3(t_stack *a);
void		sort_5(t_stack *a, t_stack *b);
void		bring_min_top(t_stack *a);
void		push_swap_dispatcher(t_stack *a, t_stack *b);

double		compute_disorder(t_stack *a);
void		adaptive(t_stack *a, t_stack *b);

char		parse_strategy(int argc, char **argv);
int			parse_bench(int argc, char **argv);
int			parse_start(int argc, char **argv);
int			parse_args(t_stack *a, int argc, char **argv, int start);

int			stack_push_int(t_stack *s, int val);
void		stack_free(t_stack *s);
int			has_duplicate(t_stack *a);
int			is_sorted(t_stack *a);

void		bench_init(t_stack *a, t_stack *b, t_bench *bench, char strategy);
void		bench_print(t_bench *bench);

void		stack_add_back(t_stack *a, void *value);
void		run_sort(t_stack *a, t_stack *b, char strategy);
void		init_stacks(t_stack *a, t_stack *b);

#endif
