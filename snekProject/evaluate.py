import pygame
import random
import numpy as np
import cv2

def evaluate_snek(model, *args):

    pygame.init()
    snek = (29, 191, 94)
    apple = (255, 255, 255)
    background = (60, 60, 60)

    dis_width = 512
    dis_height = 512

    dis = pygame.display.set_mode((dis_width, dis_height))

    snake_block = 32

    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, snek, [x[0], x[1], snake_block, snake_block])


    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = np.random.randint(0, (dis_width - snake_block)//snake_block)*snake_block
    foody = np.random.randint(0, (dis_height - snake_block)//snake_block)*snake_block

    steps = 0
    steps_since_improvement = 0
    max_steps_since_improvement = 200
    while not game_close:

        steps+=1
        steps_since_improvement+=1

        frame = np.array(dis.get_view('3'))[::8, ::8][np.newaxis]
        prediction = model.predict(frame/255)
        move = np.argmax(prediction)

        # if move == 0 (nothing) nothing changes to the movement of the snake

        if move == 1:  # LEFT
            x1_change = -snake_block
            y1_change = 0
        elif move == 2:  # RIGHT
            x1_change = snake_block
            y1_change = 0
        elif move == 3:  # UP
            y1_change = -snake_block
            x1_change = 0
        elif move == 4: # DOWN
            y1_change = snake_block
            x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(background)
        pygame.draw.rect(dis, apple, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = np.random.randint(0, (dis_width - snake_block)//snake_block)*snake_block
            foody = np.random.randint(0, (dis_height - snake_block)//snake_block)*snake_block
            Length_of_snake += 1
            steps_since_improvement = 0

        if steps_since_improvement > max_steps_since_improvement:
            # no bonus for extra long time
            print(f"Max steps since improvement reached Length: {Length_of_snake} total score: {20*(Length_of_snake-1)}")
            return 20*(Length_of_snake-1)

    pygame.quit()

    print(f"Length: {Length_of_snake}, time: {steps}, total score: {20*(Length_of_snake-1) + steps-9}")
    return 20*(Length_of_snake-1) + steps-9


def evaluate_positional_snek(model, *args):

    pygame.init()
    snek = (29, 191, 94)
    apple = (255, 255, 255)
    background = (60, 60, 60)

    dis_width = 512
    dis_height = 512

    dis = pygame.display.set_mode((dis_width, dis_height))

    snake_block = 32

    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, snek, [x[0], x[1], snake_block, snake_block])


    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = np.random.randint(0, (dis_width - snake_block)//snake_block)*snake_block
    foody = np.random.randint(0, (dis_height - snake_block)//snake_block)*snake_block

    steps = 0
    steps_since_improvement = 0
    max_steps_since_improvement = 200

    x1_last = x1
    y1_last = y1

    while not game_close:

        steps+=1
        steps_since_improvement+=1

        frame = np.array([x1, y1, x1_last, y1_last, foodx, foody])[np.newaxis]
        prediction = model.predict(frame)
        move = np.argmax(prediction)

        # if move == 0 (nothing) nothing changes to the movement of the snake

        if move == 1:  # LEFT
            x1_change = -snake_block
            y1_change = 0
        elif move == 2:  # RIGHT
            x1_change = snake_block
            y1_change = 0
        elif move == 3:  # UP
            y1_change = -snake_block
            x1_change = 0
        elif move == 4: # DOWN
            y1_change = snake_block
            x1_change = 0

        x1_last = x1
        y1_last = y1

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(background)
        pygame.draw.rect(dis, apple, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = np.random.randint(0, (dis_width - snake_block)//snake_block)*snake_block
            foody = np.random.randint(0, (dis_height - snake_block)//snake_block)*snake_block
            Length_of_snake += 1
            steps_since_improvement = 0

        if steps_since_improvement > max_steps_since_improvement:
            # no bonus for extra long time
            print(f"Max steps since improvement reached Length: {Length_of_snake} total score: {20*(Length_of_snake-1)}")
            return 20*(Length_of_snake-1)

    pygame.quit()

    print(f"Length: {Length_of_snake}, time: {steps}, total score: {20*(Length_of_snake-1) + steps-9}")
    return 20*(Length_of_snake-1) + steps-9


def evaluate_positional_snek_dis_disable(model, *args):

    dis_width = 512
    dis_height = 512
    snake_block = 32
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = np.random.randint(0, (dis_width - snake_block)//snake_block)*snake_block
    foody = np.random.randint(0, (dis_height - snake_block)//snake_block)*snake_block

    steps = 0
    steps_since_improvement = 0
    max_steps_since_improvement = 200

    x1_last = x1
    y1_last = y1

    while not game_close:

        steps+=1
        steps_since_improvement+=1

        frame = np.array([x1, y1, x1_last, y1_last, foodx, foody])[np.newaxis]
        prediction = model.predict(frame)
        move = np.argmax(prediction)

        # if move == 0 (nothing) nothing changes to the movement of the snake

        if move == 1:  # LEFT
            x1_change = -snake_block
            y1_change = 0
        elif move == 2:  # RIGHT
            x1_change = snake_block
            y1_change = 0
        elif move == 3:  # UP
            y1_change = -snake_block
            x1_change = 0
        elif move == 4: # DOWN
            y1_change = snake_block
            x1_change = 0

        x1_last = x1
        y1_last = y1

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True


        if x1 == foodx and y1 == foody:
            foodx = np.random.randint(0, (dis_width - snake_block)//snake_block)*snake_block
            foody = np.random.randint(0, (dis_height - snake_block)//snake_block)*snake_block
            Length_of_snake += 1
            steps_since_improvement = 0

        if steps_since_improvement > max_steps_since_improvement:
            # no bonus for extra long time
            print(f"Max steps since improvement reached Length: {Length_of_snake} total score: {20*(Length_of_snake-1)}")
            return 20*(Length_of_snake-1)

    print(f"Length: {Length_of_snake}, time: {steps}, total score: {20*(Length_of_snake-1) + steps-9}")
    return 20*(Length_of_snake-1) + steps-9

