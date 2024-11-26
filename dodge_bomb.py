import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#衝突判定
def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    衝突の判定を行う
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or  HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen:pg.Surface) -> None:
    """
    ブラックアウトを行う関数
    """
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(200)
    bl_rct = black.get_rect()
    screen.blit(black, bl_rct)

    #game over表示
    text = "game over"
    font = pg.font.Font(None, 100)
    text_color = (255, 255, 255)
    text_surface = font.render(text, True, text_color)
    x = WIDTH//2 - text_surface.get_width() // 2 
    y = HEIGHT//2 -text_surface.get_height() // 2
    screen.blit(text_surface, [x, y])

    #泣いているこうかとんの位置
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_rct_right = cry_img.get_rect()
    cry_rct_right.center = x + 400, y+20
    cry_rct_left = cry_img.get_rect()
    cry_rct_left.center = x - 50, y+20
    screen.blit(cry_img, cry_rct_left)
    screen.blit(cry_img, cry_rct_right)

    pg.display.update()
    time.sleep(2)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    #速度, 大きさの変更
    """
    円の速度と大きさの変更を行う関数
    """
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs, accs

def get_kk_img(sum_mv: tuple[int, int])-> pg.Surface:
    """
    こうかとんの向きを変更する関数
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    # r_kk_img = py.transform.flip(kk_img, True, False)
    kk_dct = {
        (+5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9),
        (-5, +0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
        (+0, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9),
        (+5, -5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9), True, False),
        (+5, 0):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9), True, False),
        (+5, +5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9), True, False),
        (+0, +5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9), True, False),
    }
    return kk_dct[sum_mv]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    # kk_img = get_kk_img((0,5))

    #移動の辞書
    delta = {
            pg.K_UP:(0, -5),
            pg.K_DOWN:(0, 5),
            pg.K_LEFT:(-5, 0),
            pg.K_RIGHT:(5, 0)
            }

    #こうかとんの表示
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
    v_x, v_y = +5, +5 #速度の初期値

    #タイマーの設定
    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = init_bb_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        #画像の描画
        screen.blit(bg_img, [0, 0]) 
        screen.blit(bb_img, bb_rct)
        screen.blit(kk_img, kk_rct)

        #円、こうかとんの移動の設定
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

        avx = v_x * bb_accs[min(tmr//500, 9)]
        avy = v_y * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)

        kk_rct.move_ip(sum_mv)

        #ゲームオーバー処理
        if kk_rct.colliderect(bb_rct):
            print("game over")
            gameover(screen)
            return 

        #画面の更新
        # kk_img = get_kk_img(sum_mv)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
