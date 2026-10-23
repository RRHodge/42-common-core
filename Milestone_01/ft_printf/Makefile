# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/06 09:13:36 by rarabeto          #+#    #+#              #
#    Updated: 2026/03/18 09:34:21 by rarabeto         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libftprintf.a 

LIBFT_DIR = libft
LIBFT = $(LIBFT_DIR)/build/libft.a

AR = ar rcs
CC =  cc
CFLAGS = -Wall -Wextra -Werror -Iinclude -I$(LIBFT_DIR)/include
RM = rm -rf

SRCS_DIR = srcs
OBJS_DIR = objs

SRCS = mandatory/ft_handle.c \
		mandatory/ft_print_cs.c \
		mandatory/ft_print_nbr.c \
		mandatory/ft_utils.c \
		bonus/ft_numprintf_bonus.c \
		bonus/ft_parse_bonus.c \
		ft_printf.c

OBJS = $(addprefix $(OBJS_DIR)/, $(SRCS:%.c=%.o))

BONUS_SRCS = bonus/ft_numprintf_bonus.c \
				bonus/ft_parse_bonus.c

BONUS_OBJS = $(addprefix $(OBJS_DIR)/, $(BONUS_SRCS:.c=.o))

all: $(NAME)

$(NAME): $(LIBFT) $(OBJS)
		cp ./libft/build/libft.a $(NAME)
		$(AR) $(NAME) $(OBJS)

$(LIBFT):
	make all -C $(LIBFT_DIR)

$(OBJS_DIR)/%.o: $(SRCS_DIR)/%.c
		mkdir -p $(dir $@)
		$(CC) $(CFLAGS) -c $< -o $@
		
bonus: $(LIBFT) $(OBJS) $(BONUS_OBJS)
		cp $(LIBFT) $(NAME)
		$(AR) $(NAME) $(OBJS) $(BONUS_OBJS)

clean:
	make clean -C $(LIBFT_DIR)
	$(RM) $(OBJS_DIR)

fclean: clean
	make fclean -C $(LIBFT_DIR)
	$(RM) $(NAME)
	
re: fclean all

.PHONY: bonus re fclean clean all
