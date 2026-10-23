# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/06 21:58:50 by rarabeto          #+#    #+#              #
#    Updated: 2026/03/31 13:01:03 by tny-onin         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        := push_swap
BONUS_NAME  := checker

CC          := cc
CFLAGS      := -Wall -Wextra -Werror -g
RM          := rm -rf



INC_DIR     := include
OBJS_DIR    := objs


LIBFT_DIR   := lib/libft
LIBFT       := $(LIBFT_DIR)/build/libft.a

PRINTF_DIR  := lib/ft_printf
PRINTF      := $(PRINTF_DIR)/build/libftprintf.a

GNL_DIR     := lib/get_next_line
GNL         := $(GNL_DIR)/build/libgnl.a

INCLUDES    := -I$(INC_DIR) \
               -I$(LIBFT_DIR)/include \
               -I$(PRINTF_DIR)/include \
               -I$(GNL_DIR)/include


SRCS_OPS    := srcs/operations/push.c       \
               srcs/operations/swap.c       \
               srcs/operations/rotate.c     \
               srcs/operations/rev_rotate.c


SRCS_SIMPLE := srcs/simple/simple_sort.c \
			   srcs/simple/find_min_max.c \
			   srcs/simple/smallest_input.c


SRCS_MEDIUM := srcs/medium/medium_sort.c \
			   srcs/medium/bring_max.c


SRCS_COMPLEX := srcs/complex/bit.c         \
                srcs/complex/ctx.c         \
                srcs/complex/normalize.c   \
                srcs/complex/ops.c         \
                srcs/complex/phase1.c      \
                srcs/complex/phase2.c


SRCS_ADAPTIVE := srcs/adaptive/adaptive.c \
				 srcs/adaptive/adaptive_utils.c


SRCS_UTILS  := srcs/utils/parse.c          \
			   srcs/utils/parse_strategy.c \
               srcs/utils/stack_utils.c    \
               srcs/utils/bench_utils.c    \
			   srcs/utils/parse_bench_utils.c


SRCS_ROOT   := push_swap.c


SRCS        := $(SRCS_OPS)      \
               $(SRCS_SIMPLE)   \
               $(SRCS_MEDIUM)   \
               $(SRCS_COMPLEX)  \
               $(SRCS_ADAPTIVE) \
               $(SRCS_UTILS)    \
               $(SRCS_ROOT)

OBJS        := $(addprefix $(OBJS_DIR)/, $(SRCS:.c=.o))


SRCS_BONUS  := srcs/bonus/checker_bonus.c       \
               srcs/bonus/checker_parse_bonus.c  \
               srcs/bonus/checker_ops_bonus.c    \
               srcs/bonus/checker_exec_bonus.c \
			   srcs/bonus/checker_exec_bonus_utils.c

OBJS_BONUS  := $(addprefix $(OBJS_DIR)/, $(SRCS_BONUS:.c=.o))

all: $(NAME)

$(NAME): $(LIBFT) $(PRINTF) $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) \
		-L$(LIBFT_DIR)/build -lft \
		-L$(PRINTF_DIR)/build -lftprintf \
		-o $(NAME)
	@echo "[push_swap] compilé → $(NAME)"

bonus: $(LIBFT) $(PRINTF) $(GNL) $(OBJS_BONUS)
	$(CC) $(CFLAGS) $(OBJS_BONUS) \
		-L$(LIBFT_DIR)/build -lft \
		-L$(PRINTF_DIR)/build -lftprintf \
		-L$(GNL_DIR)/build -lgnl \
		-o $(BONUS_NAME)
	@echo "[checker] compilé → $(BONUS_NAME)"


$(LIBFT):
	$(MAKE) -C $(LIBFT_DIR)

$(PRINTF): $(LIBFT)
	$(MAKE) -C $(PRINTF_DIR)

$(GNL):
	$(MAKE) -C $(GNL_DIR)


$(OBJS_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@


$(OBJS): $(INC_DIR)/push_swap.h
$(OBJS_BONUS): $(INC_DIR)/checker.h $(INC_DIR)/push_swap.h

clean:
	$(RM) $(OBJS_DIR)
	$(MAKE) -C $(LIBFT_DIR) clean
	$(MAKE) -C $(PRINTF_DIR) clean
	$(MAKE) -C $(GNL_DIR) clean

fclean: clean
	$(RM) $(NAME) $(BONUS_NAME)
	$(MAKE) -C $(LIBFT_DIR) fclean
	$(MAKE) -C $(PRINTF_DIR) fclean
	$(MAKE) -C $(GNL_DIR) fclean

re: fclean all

.PHONY: all clean fclean re bonus
