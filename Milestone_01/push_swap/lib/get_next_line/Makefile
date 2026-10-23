NAME    := build/libgnl.a
CC      := cc
CFLAGS  := -Wall -Wextra -Werror
AR      := ar rcs
RM      := rm -rf

SRCS    := srcs/get_next_line.c \
		srcs/get_next_line_utils.c
		
OBJS    := $(SRCS:.c=.o)

INCLUDES := -Iinclude

all: $(NAME)

$(NAME): $(OBJS)
	@mkdir -p build
	$(AR) $(NAME) $(OBJS)
	@echo "[libgnl] compilée"

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) build

re: fclean all

.PHONY: all clean fclean re
