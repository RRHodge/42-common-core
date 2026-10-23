# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/01/01 00:00:00 by student           #+#    #+#              #
#    Updated: 2026/03/17 11:13:27 by tny-onin         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

BUILD       = libftprintf.a
CC          = cc
CFLAGS      = -Wall -Wextra -Werror
AR          = ar rcs
RM          = rm -rf

# ── Libft ────────────────────────────────────────────────────────────────── #

NAME        = $(BUILD_DIR)/$(BUILD)
LIBFT_DIR   = ../libft
LIBFT       = $(LIBFT_DIR)/build/libft.a

# ── Répertoires ──────────────────────────────────────────────────────────── #

INC_DIR     = include
SRCS_DIR    = srcs
OBJS_DIR    = objs
BUILD_DIR   = build


# ── Sources ─────────────────────────────────────────────────────── #

SRCS        = ft_printf.c \
               print_char.c \
               print_hex.c \
               print_nbr.c \
               print_pointer.c \
			   print_str.c \
			   print_unsigned.c

OBJS        = $(addprefix $(OBJS_DIR)/, $(SRCS:.c=.o))

# ── Flags d'inclusion ────────────────────────────────────────────────────── #

INCLUDES    = -I$(INC_DIR) -I$(LIBFT_DIR)/include

# ============================================================================ #
#  Règles                                                                       #
# ============================================================================ #

#
# Règle par défaut : compile uniquement la partie mandatory.
# make → libftprintf.a avec les sources de srcs/ uniquement.
#

all: $(NAME)

$(NAME): $(LIBFT) $(OBJS)
	mkdir -p $(BUILD_DIR)
	cp $(LIBFT) $(NAME)
	$(AR) $(NAME) $(OBJS)
	@echo "$(NAME)  prêt."

#
# all : compile mandatory + bonus dans le même archive.
# make all → libftprintf.a avec srcs/ + srcs_bonus/.
#

# ── Libft ────────────────────────────────────────────────────────────────── #

$(LIBFT):
	$(MAKE) -C $(LIBFT_DIR)

# ── Compilation des objets  ─────────────────────────────────────── #

$(OBJS_DIR)/%.o: $(SRCS_DIR)/%.c
	@mkdir -p $(OBJS_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# ── Nettoyage ────────────────────────────────────────────────────────────── #

clean:
	$(RM) -r $(OBJS_DIR)
	$(MAKE) -C $(LIBFT_DIR) clean

fclean: clean
	$(RM) $(BUILD_DIR)
	$(MAKE) -C $(LIBFT_DIR) fclean

re: fclean all

.PHONY: all clean fclean re bonus
