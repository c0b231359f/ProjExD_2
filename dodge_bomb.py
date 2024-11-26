import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or  HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)

    #移動の辞書
    delta = {
            pg.K_UP:(0, -5),
            pg.K_DOWN:(0, 5),
            pg.K_LEFT:(-5, 0),
            pg.K_RIGHT:(5, 0)
            }

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    #爆弾の表示
    bb_x = int(random.randint(0, WIDTH))
    bb_y = int(random.randint(0, HEIGHT))
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = bb_x, bb_y
    bb_img.set_colorkey((0,0,0))

    v_x, v_y = +5, +5

    clock = pg.time.Clock()

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        screen.blit(bb_img, bb_rct)

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, tpl in delta.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            v_x *= -1
        if not tate:
            v_y *= -1

        bb_rct.move_ip(v_x, v_y)

        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
