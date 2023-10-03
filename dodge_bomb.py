import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  #練習3: 移動量の辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def check_bound(obj_rct: pg.Rect):
    """
    引数: Rect
    戻り値: タプル(横の判定, 縦の判定)
    画面内: True, 画面外: False
    
    """
    hori, vert = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:#練習4: 横
        hori = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:#練習4: 横
        vert = False
    return hori, vert

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img2 = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)  # 練習３：こうかとんの初期座標を設定する
    direction = {  #追加機能1: 辞書
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
        (0, -5): pg.transform.rotozoom(kk_img2, 90, 1.0),
        (+5, -5): pg.transform.rotozoom(kk_img2, -45, 1.0),
        (+5, 0): pg.transform.rotozoom(kk_img2, 0, 1.0),
        (+5, +5): pg.transform.rotozoom(kk_img2, 45, 1.0),
        (0, +5): pg.transform.rotozoom(kk_img2, -90, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        }

    """ばくだん"""
    bd_img = pg.Surface((20, 20))  # 練習１：爆弾Surfaceを作成する
    bd_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  # 練習１：SurfaceからRectを抽出する
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)  # 練習１：Rectにランダムな座標を設定する
    vx, vy = +5, +5  # 練習２：爆弾の速度を設定

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bd_rct):  #ぶつかる
            print("ゲームオーバー")
            return
        
        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        direct = (-5, 0)
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #練習3: 横
                sum_mv[1] += mv[1]  #練習3: 縦
                direct = (mv[0], mv[1])  #追加機能1: 向き
        kk_rct.move_ip(sum_mv[0], sum_mv[1])  #Rectで移動
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #練習4: こうかとんがはみ出た時の処理
        
        screen.blit(direction[direct], kk_rct)  # 練習３, 追加機能1：移動後の座標に表示させる
        

        """ばくだん"""
        bd_rct.move_ip(vx, vy)  # 練習２：爆弾を移動
        holi, vert = check_bound(bd_rct)
        if not holi:
            vx *= -1
        if not vert:
            vy *= -1
        screen.blit(bd_img, bd_rct)  #練習1: blit
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()