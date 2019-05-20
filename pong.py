import pygame
import random
import base64


class Ball:
    def __init__(self, pos_x, pos_y, min_x, max_x, min_y, max_y, width, height, speed, move_x, move_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.width = width
        self.height = height
        self.speed = speed
        self.move_x = move_x
        self.move_y = move_y
        self.move = False

    def start(self):
        self.move = True

    def stop(self):
        self.move = False

    def frame(self):
        if self.move:
            # Collision top or bottom
            if self.get_y_top() <= self.min_y or self.get_y_bottom() >= self.max_y:
                self.move_y = self.move_y * -1

            self.pos_x = self.pos_x + self.speed * self.move_x
            self.pos_y = self.pos_y + self.speed * self.move_y

    def change_direction(self):
        self.move_x = self.move_x * -1

    def get_x_left(self):
        return self.pos_x - self.width / 2

    def get_x_right(self):
        return self.pos_x + self.width / 2

    def get_y_top(self):
        return self.pos_y - self.height / 2

    def get_y_bottom(self):
        return self.pos_y + self.height / 2

    def get_speed(self):
        return self.speed


class Player:
    def __init__(self, pos_x, pos_y, min_y, max_y, width, height, speed):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.min_y = min_y
        self.max_y = max_y
        self.width = width
        self.height = height
        self.speed = speed
        self.score = 0
        self.move_up = False
        self.move_down = False

    def win(self):
        self.score += 1

    def up(self):
        self.move_up = True

    def stopup(self):
        self.move_up = False

    def down(self):
        self.move_down = True

    def stop_down(self):
        self.move_down = False

    def stop_all(self):
        self.move_up = False
        self.move_down = False

    def frame(self):
        if self.move_up:
            if self.min_y <= self.get_y_top() - self.speed:
                self.pos_y = self.pos_y - self.speed
        elif self.move_down:
            if self.max_y >= self.get_y_bottom() + self.speed:
                self.pos_y = self.pos_y + self.speed

    def get_x_left(self):
        return self.pos_x - self.width / 2

    def get_x_right(self):
        return self.pos_x + self.width / 2

    def get_y_top(self):
        return self.pos_y - self.height / 2

    def get_y_bottom(self):
        return self.pos_y + self.height / 2

    def get_score(self):
        return str(self.score)


def main():
    pygame.init()
    pygame.font.init()
    fps_clock = pygame.time.Clock()

    # Font
    FONT_ARIAL = pygame.font.SysFont('System', 36)

    # Color
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GRAY = (150, 150, 150)
    COLOR_RED = (255, 0, 0)
    COLOR_BACKGROUND = (86, 102, 135)
    COLOR_PLAYER = COLOR_BLACK
    COLOR_BALL = COLOR_RED

    # Dimensions
    S_WIDTH: int = 80 * 10
    S_HEIGHT: int = 60 * 10
    BORDER = 25

    # Players
    PLAYER_WIDTH = 10
    PLAYER_HEIGHT = 50
    PLAYER_SPEED = 5 * 1

    p1_pos_x = BORDER + PLAYER_WIDTH / 2
    p2_pos_x = S_WIDTH - BORDER - PLAYER_WIDTH / 2
    p1_pos_y = p2_pos_y = S_HEIGHT / 2
    p1_min_y = p2_min_y = BORDER
    p1_max_y = p2_max_y = S_HEIGHT - BORDER

    p1 = Player(p1_pos_x, p1_pos_y, p1_min_y, p1_max_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED)
    p2 = Player(p2_pos_x, p2_pos_y, p2_min_y, p2_max_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED)

    # Screen
    CAPTION = 'PONG - Matthias Heinlein {}'
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption(CAPTION.format(" - Starting"))

    # Sounds
    s_p1 = pygame.mixer.Sound(base64.b64decode(s_p1_b64))
    s_p2 = pygame.mixer.Sound(base64.b64decode(s_p2_b64))
    s_win = pygame.mixer.Sound(base64.b64decode(s_win_b64))

    fist_run = True
    end = True
    game_active = True

    while game_active:
        # Set and display FPS
        fps_clock.tick(60)
        pygame.display.set_caption(CAPTION.format(" - FPS: " + str(round(fps_clock.get_fps(), 1))))
        if end:
            dir_x: int = random.randint(0, 1)
            if dir_x == 0:
                dir_x = -1
            dir_y: int = random.randint(0, 1)
            if dir_y == 0:
                dir_y = -1
            dir_y = -1
            dir_x = -1
            b = Ball(S_WIDTH / 2, S_HEIGHT / 2, BORDER, S_WIDTH - BORDER, BORDER, S_HEIGHT - BORDER,
                     10, 10, 1 * 5, dir_x, dir_y)
            end = False

        # Catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            elif event.type == pygame.KEYDOWN:
                fist_run = False
                if event.key == pygame.K_w:  # Player 1 UP
                    p1.up()
                elif event.key == pygame.K_s:  # Player 1 DOWN
                    p1.down()
                elif event.key == pygame.K_UP:  # Player 2 UP
                    p2.up()
                elif event.key == pygame.K_DOWN:  # Player 2 DOWN
                    p2.down()
                b.start()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:  # Player 1 UP
                    p1.stopup()
                elif event.key == pygame.K_s:  # Player 1 DOWN
                    p1.stop_down()
                elif event.key == pygame.K_UP:  # Player 2 UP
                    p2.stopup()
                elif event.key == pygame.K_DOWN:  # Player 2 DOWN
                    p2.stop_down()

        # Draw Matchfield
        screen.fill(COLOR_BACKGROUND)
        pygame.draw.rect(screen, COLOR_WHITE,
                         [BORDER, BORDER, S_WIDTH - (BORDER * 2), S_HEIGHT - (BORDER * 2)])
        pygame.draw.rect(screen, COLOR_GRAY, [S_WIDTH / 2 - 1, 0, 2, S_HEIGHT])

        # Draw Scores
        screen.blit(FONT_ARIAL.render(p1.get_score(), True, COLOR_WHITE), ((S_WIDTH / 4) * 1, 0))
        screen.blit(FONT_ARIAL.render(p2.get_score(), True, COLOR_WHITE), ((S_WIDTH / 4) * 3, 0))

        # Draw Players
        p1.frame()
        p2.frame()
        pygame.draw.rect(screen, COLOR_PLAYER, [p1.get_x_left(), p1.get_y_top(), p1.width, p1.height])
        pygame.draw.rect(screen, COLOR_PLAYER, [p2.get_x_left(), p2.get_y_top(), p2.width, p2.height])

        # Draw Ball
        b.frame()
        pygame.draw.rect(screen, COLOR_BALL, [b.get_x_left(), b.get_y_top(), b.width, b.height])

        # Welcome Text
        if fist_run:
            screen.blit(FONT_ARIAL.render("Player 1", True, COLOR_BACKGROUND), (BORDER + 75, S_HEIGHT/2-30))
            screen.blit(FONT_ARIAL.render("W = Up", True, COLOR_BACKGROUND), (BORDER + 75,  S_HEIGHT/2-0))
            screen.blit(FONT_ARIAL.render("S = Down", True, COLOR_BACKGROUND), (BORDER + 75,  S_HEIGHT/2+30))

            screen.blit(FONT_ARIAL.render("Player 2", True, COLOR_BACKGROUND), ((S_WIDTH / 4) * 2 + 75, S_HEIGHT / 2 - 30))
            screen.blit(FONT_ARIAL.render("Keypad Up = Up", True, COLOR_BACKGROUND), ((S_WIDTH / 4) * 2 + 75, S_HEIGHT / 2 - 0))
            screen.blit(FONT_ARIAL.render("Keypad Down = Down", True, COLOR_BACKGROUND), ((S_WIDTH / 4) * 2 + 75, S_HEIGHT / 2 + 30))

        # Bounce
        if b.get_x_left() - b.get_speed() < p1.get_x_right():
            if (p1.get_y_bottom() > b.get_y_bottom() > p1.get_y_top() or
                    p1.get_y_bottom() > b.get_y_top() > p1.get_y_top()):
                s_p1.play()
                pygame.draw.rect(screen, COLOR_RED, [p1.get_x_left(), p1.get_y_top(), p1.width, p1.height])
                b.change_direction()
        elif b.get_x_right() + b.get_speed() > p2.get_x_left():
            if (p2.get_y_bottom() > b.get_y_bottom() > p2.get_y_top() or
                    p2.get_y_bottom() > b.get_y_top() > p2.get_y_top()):
                s_p2.play()
                pygame.draw.rect(screen, COLOR_RED, [p2.get_x_left(), p2.get_y_top(), p2.width, p2.height])
                b.change_direction()

        # WIN
        if b.get_x_left() <= BORDER:
            s_win.play()
            p2.win()
            end = True
        elif b.get_x_right() >= S_WIDTH - BORDER:
            s_win.play()
            p1.win()
            end = True

        pygame.display.flip()


if __name__ == '__main__':
    s_p1_b64 = """UklGRoIWAABXQVZFZm10IBIAAAABAAEARKwAAIhYAQACABAAAABmYWN0BAAAAAAAAABkYXRhDBYA
               'AAYARwA0ACAAFwD3/wMA4/8GAAsABQDz/+//5v/N/9f//////9r/7/8DAB0A/////wYA7v/e/83/
                9//n/83/+P9nAGcASgB7AYIC4ADp/Pn+mRL2ODpdzWJSO9H3V7vInrGh/bBpu+a6Q7TLrhKuN7Gn
                tOK0rLKRsCmxp7P0tNiz4bG1sTmzvLSRtDKzZLJZs7i0ZLWKtF+zfLPCtM+1VbV3tDK0z7TjtSO2
                ZbXbtB21+7Vwtii2lLWXtSi2BLfptqG2WLaVtmS3cLdSt/S2ELd/t7i3x7d7t6O307cluGe4c7g2
                uFG4g7iyuOe49rjLuOu4aLluuV+5QbmOudS567n2ub25BLoDujK6aLphunC6e7qSuuG68LoLuwm7
                HLuDu6e7hLt7u8i797sPvB+8QrxnvF+8lLzMvCa9pr1Dvqm/nsAZwH7B/M708/Qtl2b/fw1wNE1a
                OwVKEWb8b4Bfl0lzR6lZEmmZZHZS+EjmUW1h9GREWdxM5E0XWo9ifF2hUR1NeFTuXW1e/VXYTu5Q
                OVlPXZRYTFFjTwdVs1rUWXZTlk8hUn1Xb1mVVQBRslCUVNRXaVYkUhlQU1KXVRBWXVOPUNJQolNd
                VdhTQlF+UAtSFFQMVLNR8E+kUIRSPVP1US9Q4E83UUBSy1F6UHdP608XUX1Rg1BSTyFP90+yUP1P
                SE/CTgJPoU/STwlPEU5lTv9OIk+JThVOsk3NTUJOSU6yTSpNZE12TRNNqUszSrdJi0rrSTY+XR1T
                5+et84yik/Sz9Mu9xXCryZqJpNy6hcNWthqkhaICspW/uLtsrKqkoqwhulm9QrPWqAyq1bRlvBq4
                G66MquewgrlHui2zFa0ir6S2grqPtiiw7q4OtHS5obihs0uwfrKyt0a5JrY+sjmyCbbtuPe3jbQD
                swW1HbjwuIy2a7TwtFq3A7kvuNi1ULUot824BblltxO2i7ZNuFq5nLhxty+3d7i8uaC5bLjit5m4
                mrniuUG5a7i6uLy5ULo+urK5P7nMuYe65rpiusq5JLq1ui27/Lq4ure6Lru1u9K7vrutu6a8Qb6e
                vyS/Lr6vxUPiqBYRU5Z5bXd8WCo+nUEiW0FtvWXWT4tFElH2YldmM1giSjhMwlrfYyRdoE8pS1tU
                HV8LX/JU8kxRUKdZ710TWHhPK065VA1bp1l8UnZOd1HBV21ZCFX2T8hPX1TiVw9WaFFXT+BRz1Uf
                VqZSt09aUHJTSlWQU2tQT098Ue5ToFMMUUtPIVAvUgFTh1GbTxlPplAyUnlRvE/CTntP21AnUfNP
                tk6/TpZPZFCwT5FOEk52TidPGE9hTqZNmk1OTpdOPE5WTTdNZk3gTd1NH022TO9MQ01STdVMPEw1
                TH1MOUw9S61Jp0i6SO5I2EK7K1z+ecT/lj2NZ6Uww5LJNbVGnlWdybDGwNK7t6k7oOmpIrqhvfCx
                wqUmp9yzp7xGt2urlqc8r0a55rk+sQaqxKxdtcy5ZrXKrXGsQbIpuJC3j7HbrYGwMbZUuHu0ErBE
                sIK03beqtq6y5LA6swi3vLfztJ2yFrMNtuO3sbYmtG+zbLWFt5m3DrZztEe1RLdIuEi3jbVVteW2
                TLgjuPC2Arb+tmy4z7gnuPS2T7c/uDW58Ljwt5e3RrhguQm6cLkmuQC6prqau3e7Nrtfuya8Gr1X
                vRe9IL1lvUC+wL70vlS/BMCKwfTCUsPJwunFatZU/JAxUWAgcSVgsUJLNqdEZVvPYaVSqkA3QG1P
                WFszVhdHB0DfR05U11V2S4tB8kIOTeZSx036Q/xA80ZVThlOl0YZQd9CR0nuS6xHvUG2QOlEzkii
                R+1Csz96QTlFKkb0QmM/ST8aQvRDf0JNP549HT9LQStBwD65PO08bD5IPz8+JzxtO4E8bT0pPUY7
                6zlKOio7gTt8OtY4jDgzOd45dDniNxk3Sje6N5c34jYFNtI1GDYONp01rzQrNAk0RzQeNFUz0TKb
                MrAywzIxMlcxOjElMSQxjTAQMLMvgi9PL70u1y2VLO4r/ys/K6sjlg4/7XvMIL10xdDZt+RH3TvN
                PMdO0MPc896K1f7MKc/r2NDendof0jbQe9aE3aDdZ9cY04bV4Nu63m3boNY/1uXavt4N3hLa/9er
                2n3ek98j3ZLaBNv+3Sjgkt8q3V3cRN6a4DjhoN9Z3kvfQOF74t7hteB64PnhX+OD47HiIuKy4u/j
                reRH5LDj9OPd5OPl/+VS5Trly+W45kfnNefm5iHnDuii6IvoYOhy6N7oO+nd6dLpr+ka6r7q9ur9
                6iDrQOu76ybsZuyO7Kjs+uxg7crts+387TDuke5M71XvaO+j7/nvuvA58SrxSPFT9DL8LwkKF+4e
                PR1xFakP2BCaFiYa5BegEqEQNxPZFvIWlhOhEBkRxxM6FUMTthDBD1IRPROhErYQ6Q6TDx4RXBEl
                EGAOLA75Dq4PNA8JDjgNdQ0UDgQOQw12DCUMWgyhDBoMkgsFC/MKJAv6CmkK1wm0CdQJswlCCdQI
                oQh7CIYICAjfB58HOQccB/cGrgZbBloG4wXBBXcFIwUWBQMF0wSHBEcE4wO5A7ADJgP0AtsC8wIg
                AxkDDwP2AsMCyQIKAwIDKwMGA/kCDgMWAzMDCQMlA9sC+AIEA+4CEAPyAuYC/wLqAtUC5QL9AvUC
                7QLgAr8C1AL8AgED4wLeAuQCvQLJAsEC6wLNAtACtgLAAtACxALIArYC5wK1AscC3wKqAroCpQK5
                At8C0QK8ArQCpAKjAo4CowK4At0C0AK7Ar8CyAKuAsoCywLHAr8CogKmApUCpQKLApACvQK8AtUC
                tAKvAsgCpgKbAsMCpwK7AsoCywLsAukClALcAvECegKxAqgCigKnArwCtAKnArkCnwKGAooCqwKj
                AqICtQJ4Ao0CkAIaAoECnQLSAs8CkAKKAosCigJDAmQCbAJUAnECVAJYAnECbAKBAq4CpgKdAnMC
                UgKVAm4CawJ7ApwCjwKGApQCfwKtAnUCXQJ9AmgCXAJqAnUCbAJCAlICVgJmAicCJwIvAlICQQJh
                AlYCTQJdAjsCSwJ6AnECPwJYAjoCbQIyAioCTwIxAlcCOgJfAkoCIAJOAm8CXwI5Ai8CNAIvAg4C
                LwJVAocCXAJoAkACSAJAAi4CTwJUAjoCSwI6Ah0CXAIQAjQCXgIoAk8CLAI5AkACRgJNAjgCSQJA
                AkkCQAJ2AjMCEgIzAmgCYAJPAm0CDQIqAhECCwIZAu4BBAIQAvoBEwIHAh8CEAK7AfoBJAIkAjgC
                UAIOAv8BFgIKAgYC9AEaAiUCCAIuAjYCCQIZAgECAwL7AfYBHQLWAfsBJQILAvYB0AH5AQIC9QHg
                AQYCLAIfAjMCMwI4AisCCQIdAlACIQI2AgQCAAIJAg0CLgIqAi0CIQL6AfoB5gHhAfYB2AEHAiQC
                BgIXAvoBEwJEAg4CywHcAeUB0gHcAcoBvQEBAvMB/AHxAe8BJQL7AQgC7gHmAQsC5QHzAcUB+wEH
                AvMBAwLlAf0BAQISAiMCBgIEAugBrQHYAQQCJwIuAvkB9AH0Ae8B8wHvAfMB6wHZARUCOgINAuUB
                AwICAq8B7QHhAd0B2AHXAegB5QHlAeAB6AHXAboBxwHLAc8B5wHaAe8B4wEBAuMB1gEEAusB6wHr
                AeEBwAG5AbgB6gH6AcMB5gEHAt0BwwHYAcgBsgHYAZ0BnQGmAboBwgFrAZUBugGdAbYBwQGkAYsB
                vwGtAZ8BtQG5AacBjwG5AawBlwGFAbgB3gGrAbQBuQFfAY4BlgGmAcABxAGRAboBtgGIAbsBywHg
                AaoBmAG2AYgBgAFuAaoBsgGQAdIBkwG6AbUBvQGkAZMB3gGgAZcBtQGXAYsBjwGxAYEBkgHuAZEB
                tAGJAY4BgQFkAXQBngG7AaEBngF9AYUBgQFkAZUBwAF4AaEBhAFjAaoBgwFvAZABmQF2AYMBYwFt
                AXgBfgGVAaQBmAFmAYcBbQGgAZwBmgGXAY8BjwGcAaYBfgFdAVMBpAGeAYIB1QGzAaMBkgGhAa0B
                pgGuAa4BrgHPAZABiwGVAaEBoQGYAagBkAGXAZwBtQGVAZ8BzgHOAccBuQGcAZwBpAGWAY4BuQGf
                AasBowGmAaYBwAGmAZ0BpwHIAbwBuwGdAZYBuwGAAa4BgQGlAXgBfAFzAU4BeAFrAa0BiwGoAZgB
                kwGcAYMBkwFYAZwBnAFoAWABcgGDAVwBPAFsAcQBkgFxAV0BcQF1AS0BSwGFAYQBeQFnAXwBXwFz
                ATkBZwF4AV4BVwFOAWYBfAFeAU4BdgGcAYwBgwGHAaABnAGdAYMBdgGCAWEBMwFIAVgBdgGHAXEB
                SAFLAVUBdQFtAXEBigF5AYkBegGOAV8BXwGVAV8BXAFkAasBdAGVAYEBeAGhAYQBgQGMAYQBiwGY
                AYwBhwFZAVkBTAFAAUkBQAFIAUkBQAFlAUgBYAE3ATMBbAFoAUoBSgFDAUcBUwEuAUoBNQE2AUIB
                PgE6AWABUgGEAWwBRwFFASwBRQFKAVYBbwE9ASwBTgF2AV0BdgFuAWEBWgFhAVkBkwGdAXsBXgFI
                AXIBQAFYAVMBggF2AW4BaAFgAVgBMwFYAWABNgE7AToBKgFHAToBUwFgAWQBXAFtARwBCAE2ASgB
                RQFTAV8BOQFKAUUBbwGRAU4BYwFaAT0BOQE5AW4BZgFRAUQBNAE3AR8BDwE0AUgBOwEjATMBCQEX
                ARYBRAEzAUgBFgEhATsBFQEIAQQBJgEMASAB7wD3AC4B+wAVAUcBNgEuAUoBPgEQARgBLQFDAT4B
                TwFTATUBNQETAQsBHAEfAT0BSQFJAS8BRQEfAQ4BLwH+ACwBDwEPASMBEwE3ARoBRAFQASYBLwFr
                AUABFgH6ADQBTAEmASEBIQEtAQEBQwE7AUIBRwEdARUB8AD8APQA8wAqAR0BCQELAToBKgEAAQsB
                IAE9AT4BAwEcAQAB+wAdASgBIAFRAS0BKAFRAQ8BAgH5AAsBEwH6APUAFwEcAQoBAgEOASQBLgH5
                AOwAJgE7AREB5wAFAREB6AD1AOQAGgEPARoB7wDKABEBDgHvAPQA9wAAAQMB2gD3AOcA/AD7AOkA
                6wDeAOcAEAEQAfsACwHzAMkA3gD2AAgBGAEMASQB6wDRAOEAGAEHATIBLAETAQ8B4AATAe0A7QAY
                AQoB4ADdADUB9QAPAQUBJwEvAfkADgEeAfAA/QD0AOQAEgH5AN8AygDKAMcAygD0ANwAwgDfANMA
                tQDFAMoAtADPANoA4QDrANIA7gDSAPcAxADZAOEA1gDOALwA+wDEANIA3gDrALkAuQDAANYA+gDm
                AOEA0QCzALQAtADZAPUAxACfALYAuwCiAMQA6QDQAKcAyADVAPkA9gCzAN0A6QD5ANcA1wD9AMwA
                2ADcAMsAnQDKAOcAwwDcAM8AuwC+AO0A4ADLAMIAygCtAJAAwgDCALwA1wDnAPwA2gDSAO8A/AAB
                AdoA1gAEAeYA8wDaAOIA8wADAesA4QD7APsACAHzAAAB+wDMAMwA+gDuAOIA6wC3ANkAwwDAAKcA
                uQD+AMwA8gDhAMsArwDEANMA3ADgANAAswDEAMQAwACiANgAywDVAOUAAgHQAMcAvgCuANAAzwDf
                AAoB0ADPAM8A3wAKAe8AsADaAPQAygDCAK0AxwDFAJUApwCyANoA4gC5ALwAtQCAALkA5wDFAOIA
                0gDOALkApQDJAOIA3QC5AM4AsACvANkAvADhAO4AzgC3ANEA0QC3APUAwADVALsAtwCOALQApwCS
                AJoAiQCdALQAtwDAAN0AyAC2ALQArgCeAMgA5QCmANgAkQDLAO0AwADwANcAywCpAJUA3ADPANcA
                vgC7AKgAtQDXAOsA7ADHAN8A9AD8AAkBBAHnACsB5wDaALUAggDBALkAnwCbALAAvQC5AMEA9ADJ
                AJsAnwCkAMkAtAC5AK8AigCiAMEApwCvAMAAmwCnALwAsACPAJoAigCaALMAnwCsAIIAigCfAMAA
                0QCaAK8ApwCkANYAqwCmAJkAuwCXAI4ArwCfAI4AkgChAIkAyADHANAAoQCJAOAAmgCZAHwAeQCp
                AJ4AvgCeAJYAeQCuAMcAuwCuAJkAfABvAG8AlQCpAJgAgwCgAKYAlQCgAJUAvQDoANcAqQCyAJgA
                0wC6AKUAqACuAL0AqADTAK0AtACDAHYAbgBrAK0ApQCsAKAAbwB7AHIAUQBMAGsATACLAJAAUQB2
                AHYAoABEADQAkwBmAGEAaQA8ADwAZgBpAHIATQBhAFAAjwBlAGEAaQBJAIMAdgBiAGkAYQB3AH4A
                sgCdAJIAdgCbAJgAbQCLAIwAYQCVAL0AnQBUAFAAWABRAIcAkwCwAF4AhwCCAIIAkwDJAKQAiAB+
                AIcArACyAHsAkgB9AGAAegCbAJgAggCXAH4AlwB+AHAAQwBYAJIAkgD0AIoAegBwAI8AaABlAHoA
                WABhAJEAfQCFAJIAcAByAIIAogC8AHUAigCaAHkAjwCsAKwAZABsAK8AmgCrAI4AnwBwAHoAkQCE
                AI4AeQCBAHQAgQCJAGQAZQBwAEUAdACOAJYAngCJAJEAuwDTANgAuwCRAIAAdwCEAHMAhABrAFYA
                ZwCBAHkAZwCOAKEAdABvAHsAdwCTAG8AZwCuALsAoQChAKkAmQBmAJUAmQC2AMcAmAC9ANIAvQCY
                AMUAsgC5AK0AdgCkAH4AmACQAIMAgwCIAJgAVACPAKAAlwCPAIIAcwCQAKcAtACaAKgAxADWAL0A
                pADeALQApACXAG0ArwC3ALQAdQBkAHIAiwB+AEsAUwBQAGQAbQBdAHUAegBoAGUAcABfAG0AaABn
                AH0AgQCaAJYAhQCFAKIAjwCBAGQAaAAgACkAQgBbAIkAVwB1AIEAVwBLAFMAdQB0AGgAYABPAEoA
                UwBPADkAbQCBAFMAXwBwAFcAbACJAGQAUgBSADAAXwB5AIIAoQCaAIEAdwCeALIAgACEAIgAiQCW
                AIQAlQCBAJ0AhABzAK0AgwCdADQAYgCtAJUArQBvAH4AbgCLAIsAjAC1AJMAiwCyAHYAcwCPAJsA
                lwBzAJsAeQBtAFQAXQCTAJsAdQB2AJ8APACCAIIAbQB7AGEAaACHAJ8AhQCKAGUAQABAAGAAbQBd
                AIUASwCKAG0AfgCBAHkAkgB8AJkAmgCOAJYArACSAIwAogCvAJ8AswCKAJoApgCeAIkAhACiAHcA
                iQCRAIEArgCmAGcAXwBbAHQAcwBrAIAAlQCRAJEAoQBSAB8AZwB5AG4AawCYAFYAjACeAHcAngCB
                AHcAWQB8AJAAZgBiAEEAbwB7AKEA5AC2AKEAawB7AIMAkwClAG4AcgBIAFkAdgCYAIcApACYAHoA
                qABzAGYAWQB6AGYAbgCkAHoAWQBYAG0AfgCHAIcAegB9AHYAfgByADYANwByAIoAdQCHAHUAggCA
                AGAAkAB6AF8AWgB1AJoAgABhAE8AcwBZAG8AhwCMAGcARABUAFEASQAfABYAMAAMAPX/9f/6/+H/
                1P9zbXBsPAAAAAAAAAAAAAAAk1gAADwAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAA
                AAYLAAAAAAAAAAAAAA=="""
    s_p2_b64 = """UklGRmQTAABXQVZFZm10IBIAAAABAAEARKwAAIhYAQACABAAAABmYWN0BAAAAAAAAABkYXRh7hIA
                ADAA6v/Q/+X/DgAcAA0ABAD4/yEAGwATABsAOwBEACUA3v9EAIoAjwBGAZICigLa/nL8YQc9KONT
                d2w8WC0Z2c93oEyXaaUNtEi3jbHzqhKphKtvrnWv3q0crD2s8a1Hr82ui63lrAiue695r4Kuwa05
                rhqvCrCvr9Wu266Ir3ewg7Cwr3Sv+q+UsCWxkbA/sD2w2LBYsSGxErHcsDaxwbHQsZax/bGLsiK0
                0bUotg61OrfjyCf0wDKsav9/CWwZSaY6zktUZ/ZuOl1lSERIzVoDabNigFAiSH9SPmJeZJBXpkv4
                TaxaJGIAXFNQ3EyaVPhd0F3eVBJOClF8WdNcp1d1UB1P6FR2WstYiFIOT/1ReFe1WGJUPFAYUAhU
                vFZxVFlPVEy3TjdSnUvCLf/2prc+jROLvqhcxSLF9axYmLqcQ7JSv/61PqOknWSqhblxuZKrQKEx
                ppGzuLkXsmim7qSMrlS3dbUgrJymL6sbtMq2pbCzqTiqIrEbttqzp63VqoiuVbQRtaawj6zTrYCy
                +LTjsiSvz67EsnG337dqtNWzAMJy6SEmrWHMfi1y/k7mOc9FcGILcJRhdkomRQBWnGdgZYZTqkcX
                T25f8mRuWqFMqkuWV1hhy13PUetLEVJsXFteSFY4TiFPgFeoXL1Y/FBnTkxTnlmUWcpT+U60UF1W
                51hvVXZQmU8qU4dW3VS9Tw1MC05HUvdNJjXpAtrD/5Juh3Gfgb8tyN+zZZuhmBms471YupanYZxX
                paq2mLvCryKi6qLJr4+5W7XKqJCj/qr8tXm3v67cpuWo1rHptuey06rxqNGuUbUDtdWug6rorJ6y
                dbUtsi+tx6wtsQO17bP8rxuuJbF2tnG4yrTZsbi8qOCsGw1ZsXuPdXRVuD10Q9dcTW2VZCZPYEZv
                UtBjt2VPV2NKcU3cW7FjbFxeT/5L8lQxX3VeFFS+TIFQ8VnYXd1XbE+TTnVVX1uQWV5Si04RUstX
                TlmmVKFPPVDWVPZX6lVtUYRPLlKeVUZV41CNTNBMWVG5UFg9ew4UzqKXvIWKm+28qcistjedwZe3
                qX28HLsyqfec+6PLtF67E7EiowCiQK7NuLO14amZo9ipnrQNtzyvCKcGqHmwVrYAs1eriai3rXO0
                9rQar3GqY6wesgW1GLIhrVese7BetM6zLrBMrnuwQ7Xqt3y1XbIKuXjWKA54Tol5jHonW4A9Iz5Q
                WK9tBGgzUTVEp05WYvBn01nlSYJKSVlNZKFeH1D5SbZSs14GYMxVjUz0TttYel5IWdtPY00cVERb
                lFogU+5NvVBOVylallWyTyRPCFRbWL1WrVETT5JRnFWsVX5R/0x1TF1Qi1BHQSQZA90vozqHfJNr
                tGLIib3rojSWC6OUuN29Y67+nXSfNbB0uwi1JaaHoGiqLLceuBqt3KMFpzayA7h1suqoxabVrai1
                v7QMrSyoeavHsr61F7ESq/CqTLCetGazia7wq/GujLNitCexCa5rr1u01Lf/tRqyj7ZQ0CcDvkEj
                cbx6nmIJRPY8Q1FLaBZqFlesRsVKBl3aZs5dnE1uSSxVwmGNYOBTE0viT1Zb4V9oWGdOZk23VRpd
                wFoBUjVNFFEyWJRZwFOjTcxNQ1PjVjpUZE4mTEJPZlNbU+9OL0sDTH9PlVBZTZxIwkaeSfJLw0EY
                IVnrhbOAk3mY5LQ+y0vH6LDkoRipRrwoxSu7CKyfqQ+2VcK8wHm0Nq0/s7m+b8IMu2SyvLKiu2PC
                wL8+uNa01LnUwC3CPb2DuO65w792w9/AUrxpuyO/k8N+wyrAsr1OvzXDIcWDw+nARMHixFbIbMiG
                xWbGNNX294UnsU9bXfZNPzX8Kxg4L0qRThBCKzRuNKBAf0nXRKM4jjMTOktDVkQYPGI06TXKPcRB
                Zj3/NQQ0gTjyPWE9cjd1M001+zmlOzY4lTO7Mh425jivN/4zczEDMy42eDbiMwYxCjEzMyM0hDKC
                L64tgy5uMKwsfBte+3nWQL01vFfORN9a3xjRMsUkyEfV89xz19DMEcrC0XXaidrm0m/NfNCF2Ofb
                ideE0TXRsta025/at9VG0wzW19pz3FzZStaV1k7abt0/3H3ZRNiN2sfdMd4o3H7audsv3nHfp97A
                3Nnc994Q4X/hQOAt4L/mdveHEI4onzNSLhggmxf8G58mtCsjJv4crBqaIMEmDCaCHwIbXR2yIrQk
                oiBwGxQb8B4pIpkgCBwXGt4b1R5UH54cfhmlGVUcnB1YHMsZjRjXGV4bFBtDGX8XtxfsGCgZNRiw
                FlQWEheQFxoXbRVCFKkUghX9E6sNJwH88e7mjeTH6jHyHfTO733qSOqt7qryIfJm7m/sk+4N8kfz
                LfEK71jv0/HP8xnzefGo8DXyQPSE9IfzcPJL88z05PVr9UD0ZvSM9aL2pvYd9tL1k/ZC98j3qvdi
                99P3gvgn+UP5Evkg+WT5TPq0+q/6p/re+8P+GwM3B0YJgghJBpcEtwTfBbAG8QWZBPkDJASDBEAE
                qwMLA/0C9AL9ArkCIALsAeMB1wE+AUcBYgE0AUsBDQFCAVMBPQFrAW8BXAFcAScBQQFPAUYBQQFG
                AZABdgFuAXYBTQFSAV8BSgFnATwBKAGIAUMBNwFaATcBOwFHAVIBXwE7AT4BcgEyAVEBIwEVATYB
                PgGFAZgBWgFVAWEBIwESAWUBQgFlAU8BNAFGAUEBSwFCAWoBYQFbAR4BPAFLAW4BRQFNAUEBKQFA
                ATcBcQGPAUgBQAGNAUABMQE+AV0BLAEsATsBXQFMATsBQgFwAVABHwE7AQkBPQFlAWEBTAEsAUMB
                EAEsAS8BRwF8AUcBaQE9AT0BOAE4AYQBewFPATIBNwFKAU0BWwFIAS8BQAGGAYYBYgFnAXEBSAEj
                AVYBawFAAS0BSAFVAUwBQgE2AU0BUwEjASQBGgESARUBCAHbAOkADQEjAfYA5AD7AA0BGgEeARIB
                KwEdARUB9QD5AOgA9QAHARkBHQH+AC4BPAHfAOgA2gDHANYAAgEHAeMA9AD5ABgBGAEdAUABNgE7
                ASkBGgHmAAUBMgETAQoB2QAtASEB5gDGAL0A5gC1AMIA5QDpAMoA0gD2AMYA/wDfAMEA8wDcANcA
                7gD6ABIBJwEtARUBEAHUANsA9QDsABABHgEQAfEA9QBuASkBDAEdAfAA7ADEAOMA6QD/AN8A0QCh
                AKkAqADHABMBvwDNALsArQD9AOEAsQDQAOsA4QDoAOMAywDAAPMA1QCWAOYA0ADhANQAywDPAMsA
                CQHhABcB7wDLAO4A1AASARcB8QDbABcB5QCsAM0A4AC1AL0ABwHcAO4A0gC8AJ4AzwChAIcAjACM
                AMoAzQDpANYAnQCdANsA+gDKAOQA7ADEALwAqQC7ANIA2wC/AL8AzQCOALIAzQCtALIApQClAJMA
                xwClAH0AtgCtALEAxwCjAKUA1QC7AIgAkwDJAMQA0ADRAMsA4QDqAMcAsQAOAcsAmQDlAOsADgHK
                AMIAowDKALUAxgCwALgAxgDhAOUA6gAeAcEA2wDoAL0AzwDJAN8AqwDSALcAzwDoAMkArgCpAKkA
                1gCgAKAA0gCyAMkAswDNAOQAoQDQANoA6wDEAMkAxADMAN4A6wC6ALsAuwCbANAA6gDEAMsA0AC/
                ALIAywDHALEAtQCyAMIA4QCjAIwAmwC1AL0AlACsAKcAxgDUAKsAzwDLALwAvwBtAH4AwQCRAIwA
                fwCZAJ4ApwCWAHoAzwCZAGgApwCRAMUAwQDpALwAzQCuALIAvADpAMUAvwDJAKkAwQDMAJwA6QCd
                AJwA5AC/AK0ArgCyALcA2gD1ANkAuwAKAfUA0QDMAKAAlwCgAK0ArQCxALUAuwC2ALYAxgCnAIgA
                mwCnAMIA0ACoAJkArQC1ALEAlgCSAKwAlgDHAKMAlgCgAKwAsACsALEAmQCeANwArACDALgA1wDW
                AJQAogCzAKwApgChAMsAlACiALwAnQCZAIgAxQDNANIAyQDGAOUAtwDFABAB9gDxAPUA0gCuANsA
                0gDNANYAxQDaAPUA0QDEANsA1gCsAMkA2gDJAPAAsgC/ALsAuwCxAIkAvAC2AIQAoACXAJwAoACX
                AKgAvwCGAJsAfwCbAMQAnACNAIkAiQC6AMcAzACeAMQA3AC/AKwAqACbAJ4AsQCWAKAAeACWAJ4A
                owC9AKsAzwCNANQAkQCjALgAtgDjALEA0ACwAKwAxgC6AJQAcgCMAKgAtQCiAJkAngCWAKcAvQCz
                ALMAkQCrAKsAxgDKAMoA1AC8AM0A+gDgAKsApgC9ANwA5ADuAOAA1wD/AP8AzwDaANIAvACmAKkA
                oADNALwA3wDpAMkA9QDJAMAAqQCYAMQAwADVAKUAtwCtAMwA8ADUALIAnADRAJsAuwDQAMsAsgC6
                AKcAgQCgAKwAowCsAMIAkgB6ALUA1QCIAKMAsQCRAKcAvQCiALUAxgC4ALoAwgCwAI8A1ACZAIgA
                sACRAJEAdQCPAKcAuACZALgAxQDKAO4AjADBANcAzwAIAYoAcACYAFYAqwDFAMoAzQCzAJMAkwCK
                AJgAqQDPAMUArQChAFQArgC3AIoAmACKAIIAkwCGAIIAvwCBAIQAzQCYAKAAmwCGAKAAJwCYAMwA
                gQCSAKMAlgCOAL8AkwClAKAAmwDHAJsAxACoAKMAowC7ANQArACXAIMApwCjAJsAfwB8AHIAugCw
                AIgAzwCZAIMArACIAJEAngCdAJQAogC8AIgAogC1AKIAfwDKAMoAwQC4AKYAvADRALgAswC3AMAA
                wADFAMwAvADJAKEAgQB8AK0AxQCHAKEAzQDRAK0AtgCbAK0AtgC2AN4AvwCTAI0AsQDCANEAlwBy
                AMcAxADMANAAuwDZALoAfwCSAKMAhgDPAMsAsAC6AKIAvQCoAH8AgwCbAKMAxgDjANQAvQC9AKgA
                iQCUAJ0AmQC1ALgAngCmAKIAugCzALgApwB6AKsAvACdAJ0AmACdAIoArgCuAMEAnQCpAKsAUQCg
                AMEAswC3AJgAqQB5AKEAnACPAMkAuwDVAIkAjgCOAH8AoQCBAIYAmwCBAK0ArgCXAJcAwAC9AI4A
                oADMAIoAkwDMANUArQC6ANcA0QDcAMIAiABuALUAsACMAL0ApwDLAJEAggDBAJ0AmQB1AG0AfgCN
                AJQAvQCmAMUAxQDFAMAA7ADbAKIAGQHAALcAnQBrAKkAqQDRALsAyQCpALYAkwCSALYArQClAIkA
                iQB8AI4ApQCcALsApQCIAIYAoQDcALUAxwDLAJ4AiACSAIQAqACeAG0AwgC6AMsAjQCbAM8ApgDH
                AHkAtQCzAJYApgCUAJ4AqwCUAIIAhwCrAJwAoQCZAJMAmAB+AKAAmACmAI8AdQChAKEAmADAAKkA
                pQDjAN4ApgCcAMIArQDHAMAAxACoAJcAqACGAI4AjQCSAMcAuwDGAJYAlwCJAF0AmQCjANkAxgDH
                ANQAuAC6AKwAegCeANQAsACnAKIAlAC1AM0AlAB1AHkAfgCUALMAaABjAHAAjwCGAIoAjwBjAJMA
                fgBMAF4AkwCOAIEAlwB0AHgAggB9AGYAbgCGALcAuwCgAJcAlwCXAKkAjQCgAI0AowCJAIkAvwCW
                AKgAmQByAMsAxADcAAQBqACWAIMAbQCwAI0AowC9AHoAogB/AJYAswDNALgAlACeAM8AtQCdAIoA
                fgChAKkApgDAALIAqQDAAIoAuwChAIYAoQCGAJgApQCcAHMAfQBvAJcAqACbAJcAjgCEAFQAZgCI
                AKwAcwBzAKMAjgBqAGAAPgBYAG8AWQBtAG4AoABlAGkAkQCbAHwAZACMAG0AagB/AJEAhwCDAGkA
                cgBOAFUAmABkAJEAnQCHAJQAVgCIAHkAmAB9AHIAZABaAHUAXwBwAJkAfQB1AFoAaABmAHoAeQCH
                AHAAVQBrAI4AhwCBAHQAYgCPAHQAWgClAKEAWQBvAIQAqACjAGoAmwB8AF0AiQCGAGoApQDZALUA
                xwCyAJsAogCxALYAvQCeAJEAogCzAHIAdwBpAJ4A4QC3AKIAZACzAI0AnQBkAGQAswCCAIoAmADA
                AKEAqQCMAF4AfQCKAJMAggCOAN8AoACcAKEAdACCAK0AnACGAIkAagB9AI4ApQCoAIIAZQBVAGAA
                aQCSAIEAgQClAJIAcgBKAGoAugCNAH8AoABzAHIAaQCDAG4AYABOAE4ARQBgAE4ANABgAJYAZABw
                AHoAmQBtAHIAWABdAH8AXwBMAEkAXwBWAHUAlABbAFYAcAAqAGMAbwBwAH4AYwBWAC0AMgAxACUA
                TABOABwAMQBMAFoARAAyADsAOwAoABYALAAoAFUAUQBRAH0AYgBVADYAdAB+ADEAWABrAJMAQwBU
                AKEARABgAG8AdACBAFQAPgAoADYAbwBGAFQANQBmACcAFgBgAEYAQwBYAEsAYABgAEcA6P8XANH/
                yf9zbXBsPAAAAAAAAAAAAAAAk1gAADwAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAA
                AHcJAAAAAAAAAAAAAA=="""
    s_win_b64 = """UklGRvYsAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YdIsAAAAAJcqlypTR1NHt023
                TbZNtk20TbRNs02zTbJNsk0kOiQ6xOjE6AS/BL9UslSyVbJVslayVrJYsliyWbJZslqyWrJbsluy
                ecF5wQz7DPtlPmU+oU2hTaBNoE2eTZ5NnU2dTZxNnE2bTZtN4EbgRtMn0ycgziDOObQ5tGyybLJu
                sm6yb7JvsnCycLJxsnGyc7JzsrW7tbtN3U3dgDWANYpNik2ITYhNh02HTYZNhk2FTYVNg02DTYJN
                gk3lPuU+ExITEu3E7cSEsoSyhbKFsoayhrKHsoeyibKJsoqyirKLsouyj8CPwH3rfes9OT05cU1x
                TXBNcE1vTW9NbU1tTWxNbE1rTWtNak1qTdxB3EHwHfAd2MnYye6y7rKdsp2yn7KfsqCyoLKhsqGy
                orKisqSypLLXuNe4mtSa1L4rvivJRslGV01XTVZNVk1VTVVNVE1UTVJNUk1RTVFNUE1QTQI4Ajju
                5u7mE8ETwbaytrK3sreyuLK4srqyurK7sruyvLK8sr2yvbKmu6a7wNnA2csuyy4WSBZIPk0+TTxN
                PE07TTtNOk06TTlNOU03TTdNNk02TUw7TDsPCg8Kt8W3xdCy0LLRstGy0rLSstOy07LVstWy1rLW
                stey17JttG20LMosygMbAxvyPfI9JE0kTSJNIk0hTSFNIE0gTR9NH00eTR5NHE0cTRtKG0rmMuYy
                2+Db4AfAB8Drsuuy7LLssu2y7bLvsu+y8LLwsvGy8bLysvKyLbUttY3KjcrNGc0Z1TzVPAlNCU0H
                TQdNBk0GTQVNBU0ETQRNAk0CTQFNAU0ATQBNvzq/OvYO9g5PyE/IHrQetAezB7MIswizCrMKswuz
                C7MMswyzDbMNsw+zD7OYvZi9L9gv2CcrJyu1RLVE7EzsTOtM60zqTOpM6UzpTOdM50zmTOZM5Uzl
                TBlLGUvLNss2WO9Y7yjGKMZNs02zJLMksyWzJbMmsyazJ7MnsymzKbMqsyqzK7Mrs2a6ZrqC0YLR
                /SL9Ihg/GD/QTNBMz0zPTM1MzUzMTMxMy0zLTMpMykzITMhMx0zHTLFCsULmKOYotte21+697r1A
                s0CzQbNBs0OzQ7NEs0SzRbNFs0azRrNHs0ezSbNJsym9Kb3s1OzURCVEJWdAZ0CyTLJMsUyxTLBM
                sEyuTK5MrUytTKxMrEyrTKtMqUypTKRFpEV8LnwuLOAs4I7CjsJes16zX7Nfs2CzYLNhs2GzY7Nj
                s2SzZLNls2WzZrNms2i1aLUYxxjH7uvu64kyiTLLRstGk0yTTJJMkkyRTJFMj0yPTI5MjkyNTI1M
                jEyMTIpMiky/Q79DVy1XLczfzN9Mw0zDfbN9s36zfrN/s3+zgbOBs4KzgrODs4OzhLOEs4azhrOH
                s4ezkMCQwLnZudm+Jr4meT95P3RMdExzTHNMckxyTHBMcExvTG9MbkxuTG1MbUxrTGtMakxqTA8+
                Dz4YJBgktta21ou/i7+ds52znrOes6CzoLOhs6GzorOis6Ozo7Ols6WzprOms6ezp7Ppvum++tT6
                1EIgQiBFO0U7gkuCS1JMUkxRTFFMUExQTE9MT0xNTE1MTExMTEtMS0xKTEpMrEasRl80XzRGA0YD
                SMxIzNi52Lm/s7+zwLPAs8GzwbPDs8OzxLPEs8WzxbPGs8azyLPIs8mzybP6v/q/MdUx1a0frR/o
                Oeg5zUnNSTFMMUwvTC9MLkwuTC1MLUwsTCxMKkwqTClMKUwoTChM3EvcS+g86DyoJKgkENoQ2pPC
                k8IutC604rPis+Oz47Pks+Sz5rPms+ez57Pos+iz6bPps+uz67Pss+yz6cHpwa3XrdfLIMsg9Tn1
                OQtJC0kOTA5MDEwMTAtMC0wKTApMCUwJTAdMB0wGTAZMBUwFTARMBEzVQtVCJTAlMKDvoO/iy+LL
                E7sTuwW0BbQGtAa0B7QHtAm0CbQKtAq0C7QLtAy0DLQOtA60D7QPtCG2IbYvxC/E/9r/2o8ijyLI
                Ocg5W0hbSOlL6UvoS+hL50vnS+ZL5kvkS+RL40vjS+JL4kvhS+FL30vfS8lHyUeTOJM4aB9oH83X
                zdcUwxTDm7WbtSq0KrQstCy0LbQttC60LrQwtDC0MbQxtDK0MrQztDO0NbQ1tIy3jLdmxWbFzNvM
                2+sh6yGvOK84BEcER8RLxEvCS8JLwUvBS8BLwEu/S79LvUu9S7xLvEu7S7tLuku6S7hLuEtVQFVA
                Vy5XLiHwIfAHzgfOvL28vVC0ULRRtFG0U7RTtFS0VLRVtFW0V7RXtFi0WLRZtFm0WrRatFy0XLSg
                t6C3vMS8xGzYbNiSHJIcjjWONUJEQkSdS51Lm0ubS5pLmkuZS5lLmEuYS5ZLlkuVS5VLlEuUS5NL
                k0uRS5FL20fbR3I6cjrSJdIlOeE54XXJdclBu0G7ebR5tHq0erR7tHu0fLR8tH60frR/tH+0gLSA
                tIG0gbSDtIO0hLSEtK61rrWDwYPBGNIY0kgDSANKLkouez57PklKSUpzS3NLcktyS3BLcEtvS29L
                bktuS21LbUtrS2tLaktqS2lLaUtoS2hLDkYORsM4wzh3JHckOeE54XjKeMqVvJW8orSitKS0pLSl
                tKW0prSmtKe0p7SptKm0qrSqtKu0q7SstKy0rrSutK+0r7Tnuue6ysfKx2HbYdtfHF8cdTN1M41B
                jUFJS0lLSEtIS0dLR0tFS0VLREtES0NLQ0tCS0JLQEtASz9LP0s+Sz5LPUs9S/1H/Uc2PDY8bytv
                K47xjvGI0YjRD8IPwva29rbPtM+00LTQtNG00bTStNK01LTUtNW01bTWtNa02LTYtNm02bTatNq0
                27TbtPS79LsbyBvIH9of2g4ZDhkHMQcx+j76PlxJXEkcSxxLGksaSxlLGUsYSxhLFksWSxVLFUsU
                SxRLE0sTSxFLEUsQSxBLD0sPS+JE4kTVONU4VCdUJ9bp1ukg0CDQzsHOwVO3U7f8tPy0/rT+tP+0
                /7QAtQC1AbUBtQO1A7UEtQS1BbUFtQe1B7UItQi1CbUJtTi3OLcVwRXBo86jzmTkZORJIkkiEDUQ
                NTJBMkGySrJK7ErsSutK60rqSupK6UrpSudK50rmSuZK5UrlSuRK5EriSuJK4UrhSuBK4Eq3R7dH
                Yj1iPV8vXy/VFtUWltqW2nXJdcm9vb29LLUstS21LbUutS61L7UvtTG1MbUytTK1M7UztTS1NLU2
                tTa1N7U3tTi1OLU6tTq1NbY1ti+/L7+7yrvKBNwE3PQW9BYpLiku0zvTO6VFpUW8SrxKu0q7SrlK
                uUq4SrhKt0q3SrZKtkq0SrRKs0qzSrJKskqwSrBKr0qvSq5KrkouSC5Iuz67Pi8yLzL+Hv4ejeKN
                4sjOyM4owijC07jTuF+1X7VgtWC1YbVhtWO1Y7VktWS1ZbVltWa1ZrVotWi1abVptWq1arVrtWu1
                bbVttWm2abbCvsK+UMlQyWjYaNg9CT0JsyizKB03HTejQaNBHEocSodKh0qGSoZKhUqFSoRKhEqC
                SoJKgUqBSoBKgEp+Sn5KfUp9SnxKfEp7SntKeUp5SslHyUfzPvM+kTORM/si+yIT6hPqOdM50yLG
                IsaQvJC8k7WTtZW1lbWWtZa1l7WXtZi1mLWatZq1m7WbtZy1nLWetZ61n7WftaC1oLWhtaG1o7Wj
                taq2qrZUvlS+CsgKyOHU4dT86/zrsiKyIjEyMTIYPRg9pUWlRVFKUUpQSlBKT0pPSk5KTkpMSkxK
                S0pLSkpKSkpISkhKR0pHSkZKRkpFSkVKQ0pDSkJKQkqISIhIoUChQKA2oDYgKSApbA9sD0PbQ9tg
                zGDM9sH2wdK50rnMtcy1zbXNtc61zrXQtdC10bXRtdK10rXUtdS11bXVtda11rXXtde12bXZtdq1
                2rXbtdu13bXdtd673rs+xD7E1M7Uzq7drt06EToRnCicKDY1NjWJPok+NkY2RhdKF0oWShZKFUoV
                ShRKFEoSShJKEUoRShBKEEoOSg5KDUoNSgxKDEoLSgtKCUoJSghKCEoHSgdKFUUVRQ09DT3yMvIy
                /ST9JCv3K/fK2crZZsxmzK7CrsLnuue6B7YHtgm2CbYKtgq2C7YLtgy2DLYOtg62D7YPthC2ELYS
                thK2E7YTthS2FLYWtha2F7YXthi2GLa8try2F70Xvc/Ez8R4znjOItwi3McHxwe1JLUkrzGvMSM7
                IzudQp1CGUkZSdlJ2UnYSdhJ10nXSdVJ1UnUSdRJ00nTSdJJ0knQSdBJz0nPSc5JzknMScxJy0nL
                ScpJyknISchJYUZhRmg/aD/YNtg2oyujK48ajxqt5a3lqNSo1KLJoskzwTPBbbptuke2R7ZItki2
                SbZJtku2S7ZMtky2TbZNtk+2T7ZQtlC2UbZRtlO2U7ZUtlS2VbZVtla2VrZYtli2WbZZtiq5Krlb
                v1u/0cbRxhzQHNC73LvcAvkC+UwiTCIgLyAvkjiSOOo/6j/tRe1FmEmYSZdJl0mWSZZJlEmUSZNJ
                k0mSSZJJkUmRSY9Jj0mOSY5JjUmNSYtJi0mKSYpJiUmJSYdJh0mGSYZJjEeMR3ZBdkEqOio6JjEm
                MRslGyXNDs0Ow9/D3zzSPNKjyKPIE8ETweW65bqLtou2jLaMto22jbaOto62kLaQtpG2kbaStpK2
                lLaUtpW2lbaWtpa2mLaYtpm2mbaatpq2nLactp22nbaetp62GLoYusS/xL+CxoLGvM68zm3Zbdl9
                6n3qxxrHGlgpWCkzMzMz5DrkOjFBMUFxRnFGUklSSVFJUUlPSU9JTklOSU1JTUlLSUtJSklKSUlJ
                SUlHSUdJRklGSUVJRUlDSUNJQklCSUFJQUlASUBJPkk+SXBFcEWxP7E/2zjbOH0wfTCLJYslZhNm
                E9Dj0OPc1dzVTsxOzLzEvMSHvoe+WrlaudS21LbVttW21rbWtti22LbZttm22rbatty23Lbdtt22
                3rbetuC24LbhtuG24rbituS25LbltuW25rbmtue257YQuBC4t7y3vCnCKcKWyJbIYNBg0GTaZNqn
                6afpEBgQGKMmoyZNME0wjDeMN6k9qT3pQulClEeURwZJBkkESQRJA0kDSQJJAkkBSQFJ/0j/SP5I
                /kj9SP1I+0j7SPpI+kj5SPlI90j3SPZI9kj1SPVI80jzSPJI8kiUR5RH3kLeQmM9Yz3oNug2Cy8L
                LwMlAyUvFS8VGOcY5/zY/Nh/z3/PIsgiyAHCAcLZvNm8l7iXuCO3I7cktyS3Jbcltye3J7cotyi3
                Kbcptyu3K7cstyy3Lbctty+3L7cwtzC3MbcxtzK3Mrc0tzS3Nbc1tza3Nrc4tzi3G7obumm+ab5m
                w2bDPsk+ySbQJtDZ2NnYtOS05BYOFg6ZIJkg6SrpKpEykTLxOPE4Ez4TPpVClUKLRotGtEi0SLNI
                s0ixSLFIsEiwSK9Ir0itSK1IrEisSKtIq0iqSKpIqEioSKdIp0imSKZIpEikSKNIo0iiSKJIoEig
                SJ9In0g7RztHIEMgQ2Y+Zj7qOOo4gTKBMqoqqipEIEQgkg2SDXXkdeTA2MDYU9BT0JfJl8nqw+rD
                ML8wvxa7FruRt5G3ebd5t3q3erd7t3u3fbd9t363frd/t3+3gbeBt4K3greDt4O3hbeFt4a3hreH
                t4e3iLeIt4q3ireLt4u3jLeMt463jrfCuMK4RrxGvEXARcDaxNrECsoKyirQKtCY15jXMuEy4VTy
                VPLFGcUZBSUFJeUs5SxYM1gzwjjCOEo9Sj1TQVNB60TrRPFH8UdaSFpIWUhZSFdIV0hWSFZIVUhV
                SFNIU0hSSFJIUUhRSE9IT0hOSE5ITUhNSEtIS0hKSEpISUhJSEdIR0hGSEZIRUhFSLhHuEdQRFBE
                c0BzQAs8Czz+Nv42JDEkMRUqFSoKIQohAhMCE+/p7+lO3U7d3NTc1CXOJc6NyI3I0sPSw62/rb8T
                vBO8/7j/uNa31rfXt9e32LfYt9q32rfbt9u33Lfct9633rfft9+34Lfgt+K34rfjt+O35Lfkt+a3
                5rfnt+e36Lfot+q36rfrt+u37Lfst+a45rjQu9C7GL8Yv8TCxMLvxu/GrcutyxnRGdGf15/Xo9+j
                39rr2uuWEpYSSB9IH6cnpyfyLfItazNrMxs4GzgXPBc8sD+wP6xCrEJ3RXdF6EfoR/dH90f2R/ZH
                9Uf1R/NH80fyR/JH8UfxR+9H70fuR+5H7UftR+tH60fqR+pH6UfpR+dH50fmR+ZH5UflR+NH40fi
                R+JH4UfhR8NFw0W6QrpCUj9SP347fjspNyk3OjI6MnQsdCyKJYolYBxgHC4MLgzs5+zndN103QXW
                BdYI0AjQ+8r7ypzGnMbKwsrCbL9sv3e8d7zWuda5Pbg9uD64Prg/uD+4QbhBuEK4QrhDuEO4RbhF
                uEa4RrhHuEe4SbhJuEq4SrhLuEu4TbhNuE64TrhPuE+4UbhRuFK4UrhTuFO4VbhVuMG5wbkuvC68
                4b7hvt3B3cE0xTTF48jjyBTNFM3F0cXRR9dH1/Dd8N3U5tTmM/kz+dYX1hcJIQkhzCfMJ0gtSC3E
                McQx8zXzNXU5dTnAPMA8hD+EPxFCEUJTRFNEUEZQRotHi0eJR4lHiEeIR4dHh0eFR4VHhEeER4JH
                gkeBR4FHgEeAR35Hfkd9R31HfEd8R3pHekd5R3lHeEd4R3ZHdkd1R3VHdEd0R3JHckc/RT9FxULF
                QgRABED2PPY8jzmPOcU1xTV/MX8xnSydLO8m7ybWH9YfDRYNFjr0OvSH5YflUN1Q3fXW9da50bnR
                UM1QzVXJVcnkxeTFysLKwgbABsCjvaO9c7tzu4a5hrmwuLC4sriyuLO4s7i1uLW4tri2uLe4t7i5
                uLm4uri6uLu4u7i9uL24vri+uL+4v7jBuMG4wrjCuMO4w7jFuMW4xrjGuMe4x7jJuMm4arpqula8
                VrxxvnG+wcDBwEzDTMMSxhLGKMkoyYjMiMxC0ELQj9SP1GzZbNkn3yffs+az5ivzK/PoEugSexx7
                HCAjICNDKEMonyyfLKwwrDAXNBc0EzcTN+w57Dl7PHs8pT6lPpdAl0B8QnxCKkQqRKdFp0UPRw9H
                DkcORw1HDUcLRwtHCkcKRwlHCUcHRwdHBkcGRwVHBUcDRwNHAkcCRwFHAUf/Rv9G/kb+RvxG/Eb7
                RvtG+kb6RvhG+EaeRp5G5kTmRP5C/kLkQORAlT6VPgs8CzxDOUM5NDY0Ns4yzjIJLwkvyyrLKugl
                6CUQIBAgWxhbGBILEgsg7CDsLeMt48/cz9yN143XK9Mr02DPYM8DzAPM/8j/yDfGN8a0w7TDgcGB
                wYa/hr/AvcC9K7wrvLW6tbpnuWe5NLk0uTa5Nrk3uTe5OLk4uTq5Ork7uTu5PLk8uT65Prk/uT+5
                QLlAuUK5QrlDuUO5RblFuUa5RrlHuUe5SblJuUq5Srn5ufm5QbtBu6W8pbwtvi2+4b/hv7rBusG7
                w7vD58XnxUDIQMjMyszKkc2RzZjQmNAB1AHUxNfE1wXcBdwE4QThQedB527wbvDHDccNrxevFw4e
                Dh4NIw0jPic+JwwrDCtnLmcuRjFGMeEz4TM/Nj82aThpOGM6YzoyPDI81z3XPVY/Vj+wQLBA5kHm
                QRpDGkN6RHpEw0XDRYJGgkaARoBGf0Z/Rn1GfUZ8RnxGe0Z7RnlGeUZ4RnhGd0Z3RnVGdUZ0RnRG
                ckZyRnFGcUZwRnBGbkZuRm1GbUbwRfBFwETARG5DbkP5QflBYEBgQKI+oj69PL08rjquOnQ4dDgK
                Ngo2aTNpM4swizBkLWQt5inmKfcl9yVtIW0h9Bv0G7kUuRQlBiUGreyt7BflF+WH34ff/dr92hnX
                Gdet063Tn9Cf0N3N3c1cy1zLE8kTyQzHDMcxxTHFcMNww9jB2MFmwGbAGL8Yv+297b3kvOS89rv2
                uyC7ILtkumS6zLnMuc65zrnPuc+50bnRudK50rnTudO51bnVuda51rnXude52bnZudq52rncudy5
                3bnduXa6dropuym79Lv0u9i82Lzcvdy9+L74viPAI8BowWjBx8LHwkLEQsTZxdnFkseSx2XJZcla
                y1rLc81zzbbPts8n0ifSw9TD1KPXo9fV2tXabd5t3pTilOJ453jn9u327Yn9if3MEcwRbBhsGCsd
                Kx0XIRchmSSZJLInsid5Knkq3CzcLA4vDi8xMTExKTMpM/s0+zR4Nng2/zf/N3M5cznKOso61TvV
                O+887zz7Pfs97T7tPqk/qT9uQG5Ag0GDQYVChUJpQ2lDMUQxRNxE3ERrRWtF2UXZRdhF2EXXRddF
                1UXVRdRF1EXSRdJF0UXRRdBF0EXDRcNFUUVRRcRExEQfRB9EZUNlQ5JCkkKkQaRBoUChQIU/hT9O
                Pk4+/zz/PJc7lzsROhE6cDhwOLE2sTbRNNE0zzLPMqYwpjBULlQu0CvQKxApECkRJhEmtCK0Itwe
                3B5hGmEapRSlFMwLzAsu8i7yPuo+6vfk9+St4K3gB90H3evZ69kT1xPXitSK1DnSOdIM0AzQIM4g
                zknMScyeyp7KEskSyZfHl8dPxk/GD8UPxfPD88Puwu7C9MH0wSjBKMFhwGHAwL/Avx+/H7+Wvpa+
                Hr4evrW9tb1dvV29Cb0Jvdu827ytvK28obyhvJS8lLyhvKG8vry+vOu867wpvSm9dr12vdS91L1B
                vkG+v76/vky/TL/pv+m/lcCVwFLBUsEVwhXC+ML4wujD6MPmxObE9MX0xRPHE8dEyETIiMmIyd7K
                3spIzEjMyM3IzV7PXs8M0QzR1tLW0rvUu9TE1sTW7tju2EzbTNvW3dbdpOCk4NHj0eN9533n/Ov8
                6xTyFPKNB40HkRCREMEVwRXJGckZIR0hHQkgCSCMIowi9ST1JAUnBSfxKPEoxCrEKmUsZSwMLgwu
                dC90L8wwzDAZMhkyPzM/M1k0WTRrNWs1WjZaNlo3WjcnOCc46zjrOKo5qjlJOkk64TrhOnQ7dDvo
                O+g7iDyIPGI9Yj0vPi8+5T7lPoY/hj8SQBJAiUCJQO1A7UA7QTtBd0F3QaBBoEG2QbZBuUG5QalB
                qUGKQYpBWEFYQRVBFUHCQMJAXUBdQOg/6D9iP2I/zT7NPic+Jz5xPXE9qzyrPNQ71DvrOus69Dn0
                Oew47DjRN9E3pDakNmY1ZjUVNBU0sDKwMjUxNTGkL6Qv+i36LTYsNixVKlUqUihSKComKibTI9Mj
                RyFHIXcedx5IG0gblxeXF/4S/hJwDHAMufa59sXuxe7h6eHpEeYR5tLi0uIG4Abgit2K3UXbRds3
                2TfZU9dT14fVh9Xi0+LTXtJe0vLQ8tCYz5jPWs5azjHNMc0OzA7MBssGyxPKE8oxyTHJXsheyJTH
                lMfhxuHGPMY8xqbFpsURxRHFk8STxCfEJ8THw8fDcMNwwyLDIsPdwt3Cm8KbwmrCasJEwkTCJ8In
                whXCFcIMwgzCDsIOwhrCGsIkwiTCQcJBwmzCbMKgwqDC38LfwijDKMN6w3rD1sPWwzvEO8SqxKrE
                I8UjxabFpsUyxjLGx8bHxmfHZ8cQyBDIw8jDyH/Jf8lGykbKF8sXy/LL8svXzNfMyM3IzcPOw87P
                z8/P49Dj0ALSAtIt0y3TZ9Rn1LDVsNUI1wjXcthy2PDZ8NmC24LbLd0t3fPe897a4Nrg6eLp4h/l
                H+WZ55nnb+pv6svty+0h8iHyjfmN+RQLFAs+ED4Q6BPoE8MWwxZHGUcZiBuIG5AdkB1bH1sfESER
                IacipyIKJAokZSVlJbQmtCbvJ+8nCykLKSUqJSoZKxkrDywPLAAtAC3XLdctsS6xLn8vfy8rMCsw
                3DDcMIwxjDEkMiQyqjKqMjYzNjPCM8IzNzQ3NLM0szQONQ41cDVwNcU1xTUhNiE2XTZdNqA2oDbW
                NtY2KjcqN9M30zd7OHs4ETkROZc5lzkWOBY4QTRBNNwv3C+7KrsqjSSNJJMckxzJD8kPAAA=="""
    main()
