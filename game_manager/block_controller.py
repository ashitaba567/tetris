#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random
import copy
import time
import pandas as pd
import numpy as np

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0
    
    

    # GetNextMove is main function.
    # input
    #    nextMove : nextMove structure which is empty.
    #    GameStatus : block/field/judge/debug information. 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : nextMove structure which includes next shape position and the other.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # ここからシステムパラメーター的なもの------------------------------------------------------
        # 何列左を開けて平積みしていくか？
        self.openCol = 1
        # 何列積んでいたら消すか？（1なら床から一列積んでいたら消す、2なら二列積んでいたら消す）
        self.deleteRow = 4
        # ここまで------------------------------------------------------

        # get data from GameStatus
        # current shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        # next shape info
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        self.Nexthape_index = GameStatus["block_info"]["nextShape"]["index"]
        # hold shape info
        HoldShapeDirectionRange = GameStatus["block_info"]["holdShape"]["direction_range"]
        self.HoldShape_class = GameStatus["block_info"]["holdShape"]["class"]
        self.HoldShape_index = GameStatus["block_info"]["holdShape"]["index"]
        
        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]
        self.CurrentMinoNum = GameStatus["judge_info"]["block_index"]
        
        self.deleteMode =  GameStatus["board_info"]["delete_mode"]
        self.skip =  GameStatus["board_info"]["skip"]
        self.delete = 0
        self.replace = 0
        self.insertSpace = 0
         
        strategy = None
        LastGround = 9999
        LastAdjacent = 0
        LastRow = 0
        Ground = 9999
        DeleteLineNum = 0
        Adjacent = 0
        UnderAdjacent = 0
        LastUnderAdjacent = 0
        Row = 0
        LastRowAllLine = 0
        FirstGround = 9999
        LastFirstGround = 9999
        MaxHeight = 0
        LastMaxHeight = 0
        count = 0
        ClosedWall = 0
        CurrentMinoNum = GameStatus["block_info"]["currentShape"]["index"]
        self.CalcDataList = np.empty((0,11), int)
        
        # directionMaxSize: ブロックを回転させたときに地面に接する最大数
        self.shapeData = {"shape_info": 
                        {
                          "shapeNone": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeI": {
                             "directionMaxSizeX": {
                                 "d0" : 1,
                                 "d1" : 4,
                                 "d2" : 1,
                                 "d3" : 4,
                             },
                             "directionMaxSizeY": {
                                 "d0" : 4,
                                 "d1" : 1,
                                 "d2" : 4,
                                 "d3" : 1,
                             },
                             "index" : "none",
                          },
                          "shapeL": {
                              "directionMaxSizeX": {
                                 "d0" : 2,
                                 "d1" : 3,
                                 "d2" : 2,
                                 "d3" : 3,
                             },
                              "directionMaxSizeY": {
                                 "d0" : 3,
                                 "d1" : 2,
                                 "d2" : 3,
                                 "d3" : 2,
                             },
                             "index" : "none",
                          },
                          "shapeJ": {
                              "directionMaxSizeX": {
                                 "d0" : 2,
                                 "d1" : 3,
                                 "d2" : 2,
                                 "d3" : 3,
                             },
                              "directionMaxSizeY": {
                                 "d0" : 3,
                                 "d1" : 2,
                                 "d2" : 3,
                                 "d3" : 2,
                             },
                             "index" : "none",
                          },
                          "shapeT": {
                              "directionMaxSizeX": {
                                 "d0" : 2,
                                 "d1" : 3,
                                 "d2" : 2,
                                 "d3" : 3,
                             },
                              "directionMaxSizeY": {
                                 "d0" : 3,
                                 "d1" : 2,
                                 "d2" : 3,
                                 "d3" : 2,
                             },
                             "index" : "none",
                          },
                          "shapeO": {
                              "directionMaxSizeX": {
                                 "d0" : 2,
                                 "d1" : 2,
                                 "d2" : 2,
                                 "d3" : 2,
                             },
                              "directionMaxSizeY": {
                                 "d0" : 2,
                                 "d1" : 2,
                                 "d2" : 2,
                                 "d3" : 2,
                             },
                             "index" : "none",
                          },
                          "shapeS": {
                              "directionMaxSizeX": {
                                 "d0" : 2,
                                 "d1" : 2,
                                 "d2" : 2,
                                 "d3" : 2,
                             },
                              "directionMaxSizeY": {
                                 "d0" : 2,
                                 "d1" : 3,
                                 "d2" : 2,
                                 "d3" : 3,
                             },
                             "index" : "none",
                          },
                          "shapeZ": {
                              "directionMaxSizeX": {
                                 "d0" : 2,
                                 "d1" : 2,
                                 "d2" : 2,
                                 "d3" : 2,
                             },
                              "directionMaxSizeY": {
                                 "d0" : 2,
                                 "d1" : 3,
                                 "d2" : 2,
                                 "d3" : 3,
                             },
                             "index" : "none",
                          },
                        },
                  }
    
               
        # random sample
        # nextMove["strategy"]["direction"] = random.randint(0,4)
        # nextMove["strategy"]["x"] = random.randint(1,9)
        # nextMove["strategy"]["y_operation"] = 1
        # nextMove["strategy"]["y_moveblocknum"] = random.randint(1,8)
        
        # 作戦（基本は平積みして、テトリス狙い）
         #　平積みの評価としてはボードを全部なめて、開いている箇所の形に対し最も適した配置をする
         #　平積みの作戦として、左一列以外の９列に対して、Y列との接地面が一番多い場所へ置くような評価をする
         
         
         #    2  
         #  222    
         # 0000000000 床
         #　接地面が3で最大のため配置する
              
         #      3
         #    233 
         #  2223    
         # 0000000000 床
         #　この場合は接地面が1
         
         #    3
         #   33 
         #   32 
         #  222   
         # 0000000000 床
         #　この場合は接地面が2となり最大なので配置する
         
         # こんな感じで接地面が最大となる場所を探して配置する
         # 注意事項。最大の接地面が同じ場合は、下に空白が全くないものを優先する
         

         #    
         #    233 
         #  222 33 
         # 0000000000 床
         #　この場合は接地面が2たが、空白ができてしまうため、上と比較した場合にこちらは評価しない
         
         # なので、評価ポイントとしては以下の2点
         # 1:下にあるブロックまたは床との接地面が一番多いものを評価
         # 2:接地面が同じ場合は、下に空白がない置き方を評価
         #   自分の持っているミノの各ブロックの一つしたつまり配列的に[+10]が空白つまり0であるかつ自分のミノ番号以外であるものが最大何個あるかを探す。これで評価する
        '''
        LastRowAllLine, LastGround, LastAdjacent, LastFirstGround, LastMaxHeight  = self.calcContactArea(self.board_backboard)
        print(str(self.board_backboard))
        print("これは現状の盤面を取得した場合です。以下結果についてーーーーーーーーーーーーーーーー")  
        print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
        print("今回の結果についてーーーーーーーーーーーーーーーー")  
        print("残り床数についてーーーーーーーーーーーーーーーー")  
        print("現在残り床数" + str(LastGround))
        print("ひとつ上の残り床数についてーーーーーーーーーーーーーーーー")  
        print("現在ひとつ上の残り床数" +  str(LastFirstGround))
        print("壁の隣接数についてーーーーーーーーーーーーーーーー")  
        print("現在壁の隣接数" + str(LastAdjacent))
        print("埋まっている列数についてーーーーーーーーーーーーーーーー")  
        print("現在埋まっている列数" + str(LastRowAllLine))
        print("ブロックの最大積み上げ列についてーーーーーーーーーーーーーーーー")  
        print("現在ブロックの最大積み上げ列" + str(LastMaxHeight)) 
        print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★") 
        '''
        #print(str(editBoard))

        # 積みパターンで、空白ができてしまった場合は、消せるミノを使って積極的に列を消しに行くパターンに移行する
        # その際に、周囲がブロックで囲まれた空白があれば、それは特殊壁として判定する必要がある
        
        # !!!!!!　ブロックの形でうまく埋まるような配置があれば、それを優先するようにする !!!!!!!!!!!!!!!!!
        # これをするためには、下、左、右の接地面がブロックの縦、横の最大数と一致するか判定する必要がある
        
        # 事前準備現状の盤面を取得し、すでに置いてあるミノは特殊壁とみなす
        # さらに空白が周囲の壁で埋まっていたら特殊壁とみなす
        editBoard = self.replaceBlankSpace(self.editBoard(self.board_backboard), self.openCol)
        
        # 空白を埋めた場合は積極的に消しに行く(最低限消せる列があったら消しに行くようにする)
        if (self.replace == 1):
            #self.deleteRow = 1
            print("隙間が埋められてしまったので、積極的に消しに行くようにします。" + str(self.deleteRow) + "列揃っていれば消しにきます。")
                
        # 空白を埋めた場合は、埋めた最大高さを保持して、それよりも上のラインで消せるラインがあればそれを優先する
                
        # 3列以上溝ができていれば、縦棒を差し込む
        setX = self.shapeIsetCheck(editBoard, self.openCol)
        delFl = self.checkDeleteLine(self.board_backboard, self.openCol, self.deleteRow)
        
        if (setX > 0 and not delFl):
            if (GameStatus["block_info"]["currentShape"]["index"] == 1):
                nextMove["strategy"]["direction"] = 0
                nextMove["strategy"]["x"] = setX
                nextMove["strategy"]["y_operation"] = 1
                nextMove["strategy"]["y_moveblocknum"] = 1
                return nextMove
                
            if (GameStatus["block_info"]["holdShape"]["index"] == 1):
                nextMove["strategy"]["use_hold_function"] = "y"
                nextMove["strategy"]["direction"] = 0
                nextMove["strategy"]["x"] = setX
                nextMove["strategy"]["y_operation"] = 1
                nextMove["strategy"]["y_moveblocknum"] = 1
                return nextMove
        
        # 現在の最大盤面取得
        maxFullLine = self.maxFullLine(editBoard, self.openCol)
        print ("現在の埋まっている盤面の最大列数:" + str(maxFullLine))
        
        if (self.CurrentMinoNum > 1 and maxFullLine >= 2):
            # 2列消しかつL字で消せるなら最優先で消す
            width = self.board_data_width
            height = self.board_data_height
            dFl = 0
            for l in range(1, width,  1):
                #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                #print("y座標チェック" + str(y) + "インデックス" + str((y) * width + x))
                if (l == 1 and editBoard[(height - 1 - maxFullLine) * width + l] != 0):
                    dFl = 1
                    break
                
                if (l > 1 and editBoard[(height - 1 - maxFullLine) * width + l]) == 0:
                    dFl = 1
                    break
            
            if (dFl != 1):
                if (GameStatus["block_info"]["currentShape"]["index"] == 3):
                    nextMove["strategy"]["direction"] = 2
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    return nextMove
                    
                if (GameStatus["block_info"]["holdShape"]["index"] == 3):
                    nextMove["strategy"]["use_hold_function"] = "y"
                    nextMove["strategy"]["direction"] = 2
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    return nextMove    
        
        
        # 二列埋まっていて、四角を差し込めるなら優先的に差し込む
        if (self.CurrentMinoNum > 1 and maxFullLine >= 2):
            # 2列消しかつL字で消せるなら最優先で消す
            width = self.board_data_width
            height = self.board_data_height
            dFl = 0
            for l in range(1, width,  1):
                #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                #print("y座標チェック" + str(y) + "インデックス" + str((y) * width + x))
                if ((l == 1 or l == 2) and editBoard[(height - 1 - maxFullLine + 2) * (width - 1) + l] != 0 or (l == 1 or l == 2) and editBoard[(height - 1 - maxFullLine + 1) * (width - 1) + l] != 0):
                    dFl = 1
                    break
                
                if (l > 2 and editBoard[(height - 1 - maxFullLine ) * width + l]) == 0:
                    dFl = 1
                    break
            
            if (dFl != 1):
                if (GameStatus["block_info"]["currentShape"]["index"] == 5):
                    nextMove["strategy"]["direction"] = 2
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    return nextMove
                    
                if (GameStatus["block_info"]["holdShape"]["index"] == 5):
                    nextMove["strategy"]["use_hold_function"] = "y"
                    nextMove["strategy"]["direction"] = 2
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    return nextMove
        
                                                                    
        # もし一番左列以外の列が全てxx列埋まっていたら、問答無用でHOLD解除して、縦棒を差し込む
        # 一番左以外の下xxx列が埋まっている
        if (delFl):
            print("チェック通過")
            if (self.board_backboard[210] != 0 and self.board_backboard[200] != 0 and self.board_backboard[190] != 0 and self.board_backboard[180] != 0):
                # 縦棒で消せる列以上になったら二列開けるようにする
                self.openCol = 2
            
            if(GameStatus["block_info"]["currentShape"]["index"] == 1 or GameStatus["block_info"]["holdShape"]["index"] == 1):
                self.delete = 1
                #self.openCol = 0
                
                    
            if (self.replace == 1 or (self.replace == 0 and self.deleteRow >= 3)):
                #ShapeI
                if(GameStatus["block_info"]["currentShape"]["index"] == 1):
                    # 現在が縦棒だったら左端にセットする
                    nextMove["strategy"]["direction"] = 0
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    
                    print("以下結果についてーーーーーーーーーーーーーーーー")  
                    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
                    print("今回の結果についてーーーーーーーーーーーーーーーー")  
                    print("現在は" + str(self.CurrentMinoNum) + "番目のブロックです")
                    print("列を消すためにセットされたミノは" + self.convertShapeNumToName(CurrentMinoNum) + "です。")
                    print(str(self.debugBoard(self.getBoard(self.board_backboard, self.CurrentShape_class, 0, 0))))
                    return nextMove
                               
                elif(GameStatus["block_info"]["holdShape"]["index"] == 1):
                    # 縦棒だったらホールドしているので入れ替えて左端にセットする
                    nextMove["strategy"]["use_hold_function"] = "y"
                    nextMove["strategy"]["direction"] = 0
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    
                    print("以下結果についてーーーーーーーーーーーーーーーー")  
                    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
                    print("今回の結果についてーーーーーーーーーーーーーーーー")  
                    print("現在は" + str(self.CurrentMinoNum) + "番目のブロックです")
                    print("列を消すためにセットされたミノは" + self.convertShapeNumToName(CurrentMinoNum) + "です。")
                    print(str(self.debugBoard(self.getBoard(self.board_backboard, self.CurrentShape_class, 0, 0))))
                    return nextMove
            
            if (self.deleteRow == 2):
                if (GameStatus["block_info"]["holdShape"]["index"] == 6 and editBoard[210] != 0):
                # 縦棒だったらホールドしているので入れ替えて左端にセットする
                    nextMove["strategy"]["use_hold_function"] = "y"
                    nextMove["strategy"]["direction"] = 1
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    
                    print("以下結果についてーーーーーーーーーーーーーーーー")  
                    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
                    print("今回の結果についてーーーーーーーーーーーーーーーー")  
                    print("現在は" + str(self.CurrentMinoNum) + "番目のブロックです")
                    print("列を消すためにセットされたミノは" + self.convertShapeNumToName(CurrentMinoNum) + "です。")
                    print(str(self.debugBoard(self.getBoard(self.board_backboard, self.CurrentShape_class, 0, 0))))
                    return nextMove
                
                if (GameStatus["block_info"]["holdShape"]["index"] == 7 and editBoard[211] != 0):
                # 縦棒だったらホールドしているので入れ替えて左端にセットする
                    nextMove["strategy"]["use_hold_function"] = "y"
                    nextMove["strategy"]["direction"] = 1
                    nextMove["strategy"]["x"] = 0
                    nextMove["strategy"]["y_operation"] = 1
                    nextMove["strategy"]["y_moveblocknum"] = 1
                    
                    print("以下結果についてーーーーーーーーーーーーーーーー")  
                    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
                    print("今回の結果についてーーーーーーーーーーーーーーーー")  
                    print("現在は" + str(self.CurrentMinoNum) + "番目のブロックです")
                    print("列を消すためにセットされたミノは" + self.convertShapeNumToName(CurrentMinoNum) + "です。")
                    print(str(self.debugBoard(self.getBoard(self.board_backboard, self.CurrentShape_class, 0, 0))))
                    return nextMove
        
        # holdの条件チェックを行います。条件に合致していれば、holdを実施する 
        # 縦棒で、holdしているものが縦棒でない場合（４列消し狙うため）
        # 一番目のブロックで、S字かZ字の場合（初手で来られたらほぼ確実に平積みできなくなるため）      
        if ((self.CurrentMinoNum == 1 and (GameStatus["block_info"]["currentShape"]["index"] == 6 or GameStatus["block_info"]["currentShape"]["index"] == 7)) or
             (GameStatus["block_info"]["currentShape"]["index"] == 1 and GameStatus["block_info"]["holdShape"]["index"] != 1)) :
            nextMove["strategy"]["use_hold_function"] = "y"
            print("以下結果についてーーーーーーーーーーーーーーーー")  
            print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
            print("今回の結果についてーーーーーーーーーーーーーーーー")  
            print("現在は" + str(self.CurrentMinoNum) + "番目のブロックです")
            print("ホールドされたミノは" + self.convertShapeNumToName(CurrentMinoNum) + "です。")
            print(str(self.debugBoard(self.board_backboard)))
            
            if ((GameStatus["block_info"]["holdShape"]["index"] is None) or (GameStatus["block_info"]["holdShape"]["index"] == 1)):
                return nextMove
            else:
                #入れ替えた場合は、ホールドしているブロックの情報と入れ替えた縦棒の情報を入れ替えないといけない
                self.CurrentShape_class = GameStatus["block_info"]["holdShape"]["class"]
                GameStatus["block_info"]["currentShape"]["index"] = GameStatus["block_info"]["holdShape"]["index"]
                CurrentShapeDirectionRange = GameStatus["block_info"]["holdShape"]["direction_range"]
        else:
            nextMove["strategy"]["use_hold_function"] = "n"
                  
        # search best nextMove -->
        '''
        if (self.skip == "skip"):
            self.skip = "none"
            strategy = (GameStatus["board_info"]["nextDirection"], GameStatus["board_info"]["nextXpos"], 1, 1)
            nextMove["strategy"]["direction"] = strategy[0]
            nextMove["strategy"]["x"] = strategy[1]
            nextMove["strategy"]["y_operation"] = strategy[2]
            nextMove["strategy"]["y_moveblocknum"] = strategy[3]
            return nextMove
        
        
        # 盤面に歪な組み方があるかチェックし、消し方を変更する
        if (self.checkBoard(self.board_backboard)):
            #print("条件合致")
            self.deleteMode = "delete"
        else:
            self.deleteMode = "normal"   
        '''    
        
        # search with current block Shape
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ここからミノが降ってくる開始ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー")
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー")  
         
        # 評価計算 
        print("現在のミノの評価です")      
        CalcDataList = self.calcBlockSet(CurrentShapeDirectionRange, self.CurrentShape_class, editBoard, GameStatus, "current", self.CurrentShape_index)
        _df = self.judgeEvaluate(CalcDataList, CurrentShapeDirectionRange, self.CurrentShape_class, editBoard, GameStatus)
        
        # 評価計算（ホールド）
        print("ホールドされたのミノの評価です")  
        CalcDataListHold = self.calcBlockSet(HoldShapeDirectionRange, self.HoldShape_class, editBoard, GameStatus, "hold", self.HoldShape_index)
        _dfh = self.judgeEvaluate(CalcDataListHold, HoldShapeDirectionRange, self.HoldShape_class, editBoard, GameStatus)
        
        #print("ホールド側の評価" + str(_dfh))
                
        # なかった場合(配置後に空白ができてしまう場合はホールドしているミノも評価対象にする
        # and (GameStatus["block_info"]["currentShape"]["index"] != 1)
        if ((_df['UnderSpace'].min() == 1) ):
            
            # 縦棒をホールドしてしまっていたら、一度入れ替え直す
            if (nextMove["strategy"]["use_hold_function"] == "y"):
                nextMove["strategy"]["use_hold_function"] == "n"
                self.HoldShape_class = GameStatus["block_info"]["currentShape"]["class"]
                GameStatus["block_info"]["holdShape"]["index"] = GameStatus["block_info"]["currentShape"]["index"]
                HoldShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
            
            print("盤面に置けないのでホールドしてそれを評価する")
            #print(str(HoldShapeDirectionRange))
            #print(str(self.HoldShape_class))
            strategyH = (_dfh['Direction'].min(), _dfh['xPos'].min(), 1, 1)
            
            # ホールド側のブロックも評価に値しなければ諦める
            if (_dfh['UnderSpace'].min() == 1):
                nextMove["strategy"]["use_hold_function"] = "y"
                nextMove["strategy"]["direction"] = strategy[0]
                nextMove["strategy"]["x"] = strategy[1]
                nextMove["strategy"]["y_operation"] = strategy[2]
                nextMove["strategy"]["y_moveblocknum"] = strategy[3]
                print(nextMove)
            
            print("諦めて配置した時のもの")
        
            nextMove["strategy"]["use_hold_function"] = "y"
            nextMove["strategy"]["direction"] = strategyH[0]
            nextMove["strategy"]["x"] = strategyH[1]
            nextMove["strategy"]["y_operation"] = strategyH[2]
            nextMove["strategy"]["y_moveblocknum"] = strategyH[3]
            print(nextMove)
            ## 置いた後に最適華道家の確認のためにwaitを挟む（デバッグ用）
            ## 大会やスコア計測時はコメントアウト市内と影響する
            #time.sleep(3)
        
            return nextMove
        else: 
            #print("条件分岐入ってる")
            strategy = (_df['Direction'].min(), _df['xPos'].min(), 1, 1)       
            # 縦棒以外でホールドしているブロックが対象
            print ("現在ブロック" + str(GameStatus["block_info"]["currentShape"]["index"]))
            print ("ホールドしているブロック" + str(GameStatus["block_info"]["holdShape"]["index"]))
            if (GameStatus["block_info"]["holdShape"]["index"] is not None and GameStatus["block_info"]["holdShape"]["index"] != 1):
                
                if (_df['FullAdjustSide'].min() is None):
                    fullAd = 0
                else:
                    fullAd = _df['FullAdjustSide'].min()
                    
                if (_dfh['FullAdjustSide'].min() is None):
                    fullAdHold = 0
                else:
                    fullAdHold = _dfh['FullAdjustSide'].min()
        
                # ホールドしているブロックのほうが接地面多かったらそっちを採用する
                print("今のミノの接地数" + str(fullAd) + "-----------------------ホールドされているミノの接地数" + str(fullAdHold))
                if ((fullAdHold > fullAd)):
                    strategy = (_dfh['Direction'].min(), _dfh['xPos'].min(), 1, 1)
                    nextMove["strategy"]["use_hold_function"] = "y"
                    print("ホールドしているブロックのほうが評価が高いため入れ替えます")
                            
        # S字とZ字は一番いらないブロックなので早めに消していく
        
        if (self.delete == 1):
            print("現在のモードは削除モードです")
        else: 
            print("現在のモードは通常モードです")
         
        print("\n")
        print("\n")
        print("以下結果についてーーーーーーーーーーーーーーーー")  
        print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")  
        print("今回の結果についてーーーーーーーーーーーーーーーー") 
        print("現在は" + str(self.CurrentMinoNum) + "番目のブロックです")
        print("配置されたミノは" + self.convertShapeNumToName(CurrentMinoNum) + "です。")
        print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")         
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ここでミノの評価が完了して配置されたーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー")    
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー") 
        print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー")
        
        #time.sleep(10)
        
        #print(df)
                ###test
                ###for direction1 in NextShapeDirectionRange:
                ###  x1Min, x1Max = self.getSearchXRange(self.NextShape_class, direction1)
                ###  for x1 in range(x1Min, x1Max):
                ###        board2 = self.getBoard(board, self.NextShape_class, direction1, x1)
                ###        EvalValue = self.calcEvaluationValueSample(board2)
                ###        if EvalValue > LatestEvalValue:
                ###            strategy = (direction0, x0, 1, 1)
                ###            LatestEvalValue = EvalValue
        # search best nextMove <--
        
        
        print("===", datetime.now() - t1)
        
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        print(nextMove)
        print("###### SAMPLE CODE ######")
        
        ## 置いた後に最適華道家の確認のためにwaitを挟む（デバッグ用）
        ## 大会やスコア計測時はコメントアウト市内と影響する
        #time.sleep(3)
        
        return nextMove
    
    def judgeEvaluate(self, CalcDataList, ShapeDirectionRange,Shape_class, editBoard, GameStatus):
    
        # ここからが評価計算した値から最適解を算出する    
        # 最終的な評価をpandasを利用して実施する
        strategy = None
        col=["UnderWall", "SideWall", "BlankGroundSpace", "MaxBlockHeight", "closedWall", "Direction", "xPos", "DeleteLineNum", "FullAdjust", "FullAdjustSide", "UnderSpace"]
        pd.set_option('display.max_columns', 900)
        df = pd.DataFrame(data=CalcDataList, columns=col).astype('int')
        print(df)
        print("\n")
        
        # 
        # その後に盤面に対して壁で空白が埋まっているかどうかを確認して、埋まっていたらそれは特殊壁として扱うように刷る処理を追加する
        
        # 今の回転数に対して、最大接地面と同じ下の設置数がない場合は壁が埋まってしまっている場合も考慮する(縛りをゆるくする)
        # もし埋めた場合は、埋めたフラグを立てる
        clFl = 0
        dff = df.query('FullAdjust == 1')
        
        if (dff.empty):
            clFl = 1
        
        # 左壁がミノで埋まってたら別の消し方に変える(消したときにミノが残るパターンすべて想定して条件分岐させる)
        preBoard = self.board_backboard
        if (preBoard[210] != 0 and preBoard[200] != 0 and preBoard[190] != 0 and preBoard[180] != 0):
            self.insertSpace = 1
                    
        if (self.insertSpace == 1):
            dfsp = df.query('FullAdjustSide == 1')
        
            if (not dfsp.empty):
                minBlockHeight = dfsp['MaxBlockHeight'].min()
                dfsp2 = dfsp.query('MaxBlockHeight == @minBlockHeight').head(1)
                strategy = (dfsp2['Direction'].max(), dfsp2['xPos'].max(), 1, 1)
                return strategy 
               
        # 削除モードのときは残り床が0のものを優先的に採用する
        if (self.delete == 1):
            maxDeleteLineNum = df['DeleteLineNum'].max()
            
            # 削除列数が1ライン以上のものを週出
            dfs = df.query('DeleteLineNum > 0 & closedWall != 1').head(1)
            
            if (dfs.empty):
                
                # 削除モードで削除できないブロックだったら、通常モードとして再評価
                print("列を削除できないので通常モードで再評価します")
                self.delete = 0
                ReCalcDataList = self.calcBlockSet(ShapeDirectionRange,Shape_class, editBoard, GameStatus)
                df = pd.DataFrame(data=ReCalcDataList, columns=col).astype('int')
                  
                if (clFl == 0):
                    df2 = df.query('closedWall == 0')
                    print(df2)
                    print("\n")
                else:
                    df2 = df
            
                print("床に対して残りマスが少ないものを評価")                
                minBlankGroundSpace = df2['BlankGroundSpace'].min()
                df3 = df2.query('BlankGroundSpace == @minBlankGroundSpace')
                print(df3)
                print("\n")
            
                print("下壁に最も接しているものを評価")
                maxUnderWall = df3['UnderWall'].max()
                df4 = df3.query('UnderWall == @maxUnderWall')
                print(df4)
                print("\n")
            
                print("左壁に最も接しているものを評価")
                maxSideWall = df4['SideWall'].max()
                df5 = df4.query('SideWall == @maxSideWall')
                print(df5)
                print("\n")
            
                print("ブロックの最大高さが低いものを評価")
                minBlockHeight = df5['MaxBlockHeight'].min()
                df6 = df5.query('MaxBlockHeight == @minBlockHeight')
                print(df6)
                print("\n")
            
                print("最終的に採用したもの")
                if (df6.empty):
                    _df5 = df5.head(1)
                    strategy = (_df5['Direction'].min(), _df5['xPos'].min(), 1, 1)
                    print(df5)
                    return df5
            
                #最終的に評価した回転数とx座標をセットする
                _df6 = df6.head(1)
                strategy = (_df6['Direction'].min(), _df6['xPos'].min(), 1, 1)
                print(df6)
                return df6
                
            else:
                df2 = df.query('DeleteLineNum == @maxDeleteLineNum & closedWall != 1').head(1)
                print(str(df2['Direction'].max()) + str(df2['xPos'].max()))
                strategy = (df2['Direction'].max(), df2['xPos'].max(), 1, 1)
                print(df2)
                print("\n")
        #通常モード
        else:
            
            if (clFl == 0):
                df2 = df.query('closedWall == 0')
                print(df2)
                print("\n")
            else:
                df2 = df
                
            print("設置した後に空白がないものを優先的に評価")                       
            dfss = df2.query('UnderSpace != 1')
            print(dfss)
            print("\n") 
     
            print("床に対して残りマスが少ないものを評価")                       
            minBlankGroundSpace = dfss['BlankGroundSpace'].min()
            df3 = dfss.query('BlankGroundSpace == @minBlankGroundSpace')
            print(df3)
            print("\n")
            
            print("下壁に最も接しているものを評価")
            maxUnderWall = df3['UnderWall'].max()
            df4 = df3.query('UnderWall == @maxUnderWall')
            print(df4)
            print("\n")
        
            print("左壁に最も接しているものを評価")
            maxSideWall = df4['SideWall'].max()
            df5 = df4.query('SideWall == @maxSideWall')
            print(df5)
            print("\n")
                
            print("ブロックの最大高さが低いものを評価")
            minBlockHeight = df5['MaxBlockHeight'].min()
            df6 = df5.query('MaxBlockHeight == @minBlockHeight')
            print(df6)
            print("\n")
        
            print("最終的に採用したもの")
            if (df6.empty):
                _df5 = df5.head(1)
                strategy = (_df5['Direction'].min(), _df5['xPos'].min(), 1, 1)
                print(df5)
                return _df5
        
            #最終的に評価した回転数とx座標をセットする
            _df6 = df6.head(1)
            strategy = (_df6['Direction'].min(), _df6['xPos'].min(), 1, 1)
            print(df6)
            return df6
        
        return df 
    
        
    
    def calcBlockSet(self, ShapeDirectionRange, ShapeClass, editBoard, GameStatus, mode, minoIndex):
        
        CalcDataList = np.empty((0,11), int)
        count = 0
        
        shapeType = "currentShape"
        
        if (mode == "hold"):
            shapeType = "holdShape"
                   
        for direction0 in ShapeDirectionRange:
          
            # search with x range
            x0Min, x0Max = self.getSearchXRange(ShapeClass, direction0)
            #print("最小値:" + str(x0Min + 1) + "最大値:" + str(x0Max))
            #削除モードの場合は盤面全般を評価するようにする
            if (self.delete == 1):
                x1Min = x0Min
            else:
                x1Min = x0Min + self.openCol    
                
            for x0 in range(x1Min, x0Max):
                count = count + 1
                fullAdjust = 0
                fullAdjustSide = 0
                # get board data, as if dropdown block
                board = self.getBoard(editBoard, ShapeClass, direction0, x0)                
                print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")                
                print("評価番号" + str(count - 1) + "について")
                if (mode == "current"):
                    print("今のミノは" + self.convertShapeNumToName(GameStatus["block_info"][shapeType]["index"]) + "で回転数は" + str(direction0 + 1) + "で今のx座標の位置" + str(x0))
                else:
                    print("ホールドされたミノは" + self.convertShapeNumToName(GameStatus["block_info"][shapeType]["index"]) + "で回転数は" + str(direction0 + 1) + "で今のx座標の位置" + str(x0))
                print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
                print("\n")
                
                # 次の一手に対して評価する
                
                #self.nextBoardCalc(board, GameStatus, direction0, x0)
                                
                Ground, Adjacent, UnderAdjacent, MaxHeight, ClosedWall, DeleteLineNum, UnderSpace = self.calcContactArea2(board, minoIndex)
                               
                # 床と下接地最大面を比較する
                if (self.checkMinoContactArea(GameStatus["block_info"][shapeType]["index"], direction0, UnderAdjacent)):
                    fullAdjust = 1
                    
                # 床と下と左接地最大面を比較する
                if (self.checkMinoContactSideArea(GameStatus["block_info"][shapeType]["index"], direction0, UnderAdjacent, Adjacent)):
                    fullAdjustSide = 1
                                    
                # 対象データをデータリストに退避（後で評価として利用する）
                arr = np.array([])
                arr = np.append(arr, np.array(UnderAdjacent))
                arr = np.append(arr, np.array(Adjacent))
                arr = np.append(arr, np.array(Ground))
                arr = np.append(arr, np.array(MaxHeight))
                arr = np.append(arr, np.array(ClosedWall))
                arr = np.append(arr, np.array(direction0))
                arr = np.append(arr, np.array(x0))
                arr = np.append(arr, np.array(DeleteLineNum))
                arr = np.append(arr, np.array(fullAdjust))
                arr = np.append(arr, np.array(fullAdjustSide))
                arr = np.append(arr, np.array(UnderSpace))                
                CalcDataList = np.append(CalcDataList, np.array([arr]), axis=0)
                print(str(self.CalcDataList))
        
        return CalcDataList

    # ミノの番号からミノの名前に変換します（デバッグ用）
    def convertShapeNumToName(self, MinoNo):
        # ないとは思うが万が一該当しない場合はなしとして返却
        MinoName = "該当しないミノ"
        
        if (MinoNo == 1):
            MinoName = "shapeI(縦棒)"
            return MinoName
        
        if (MinoNo == 2):
            MinoName = "shapeL(L字)"
            return MinoName
        
        if (MinoNo == 3):
            MinoName = "shapeJ(逆L字)"
            return MinoName
        
        if (MinoNo == 4):
            MinoName = "shapeT(T字)"
            return MinoName
        
        if (MinoNo == 5):
            MinoName = "shapeO(四角)"
            return MinoName
        
        if (MinoNo == 6):
            MinoName = "shapeS(S字)"
            return MinoName
        
        if (MinoNo == 7):
            MinoName = "shapeZ(Z字)"
            return MinoName    
        
        return MinoName
    
    # おける床の範囲とミノの最大接地面を比較します
    def checkMinoContactArea(self, MinoNo, directionx, underAdjacent):
        # ないとは思うが万が一該当しない場合はなしとして返却
        
        directionxx = "d" + str(directionx)
        #print(self.shapeData["shape_info"]["shapeL"]["directionMaxSizeX"][directionxx])
        
        if (MinoNo == 1):
            if (self.shapeData["shape_info"]["shapeI"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        if (MinoNo == 2):
            if (self.shapeData["shape_info"]["shapeL"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        if (MinoNo == 3):
            if (self.shapeData["shape_info"]["shapeJ"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        if (MinoNo == 4):
            if (self.shapeData["shape_info"]["shapeT"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        if (MinoNo == 5):
            if (self.shapeData["shape_info"]["shapeO"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        if (MinoNo == 6):
            if (self.shapeData["shape_info"]["shapeS"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        if (MinoNo == 7):
            if (self.shapeData["shape_info"]["shapeZ"]["directionMaxSizeX"][directionxx] == underAdjacent):
                return True
        
        return False
    
    # おける床と左壁範囲とミノの最大接地面を比較します
    def checkMinoContactSideArea(self, MinoNo, directionx, underAdjacent, sideAdjacent):
        # ないとは思うが万が一該当しない場合はなしとして返却
        
        directionxx = "d" + str(directionx)
        #print(str(underAdjacent))
        #print(str(sideAdjacent))
        #print(self.shapeData["shape_info"]["shapeL"]["directionMaxSizeX"][directionxx])
        
        if (MinoNo == 1):
            if (self.shapeData["shape_info"]["shapeI"]["directionMaxSizeX"][directionxx] == underAdjacent and self.shapeData["shape_info"]["shapeI"]["directionMaxSizeY"][directionxx] == sideAdjacent):
                return True
        
        if (MinoNo == 2):
            if (self.shapeData["shape_info"]["shapeL"]["directionMaxSizeX"][directionxx] == underAdjacent and self.shapeData["shape_info"]["shapeL"]["directionMaxSizeY"][directionxx] == sideAdjacent):
                return True
        
        if (MinoNo == 3):
            #print("下壁数:" + str(underAdjacent) + "左壁数:" + str(sideAdjacent))
            if (self.shapeData["shape_info"]["shapeJ"]["directionMaxSizeX"][directionxx] == underAdjacent and self.shapeData["shape_info"]["shapeJ"]["directionMaxSizeY"][directionxx] == sideAdjacent):
                
                return True
        
        if (MinoNo == 4):
            if (self.shapeData["shape_info"]["shapeT"]["directionMaxSizeX"][directionxx] == underAdjacent and self.shapeData["shape_info"]["shapeT"]["directionMaxSizeY"][directionxx] == sideAdjacent):
                return True
        
        if (MinoNo == 5):
            if (self.shapeData["shape_info"]["shapeO"]["directionMaxSizeX"][directionxx] == underAdjacent and self.shapeData["shape_info"]["shapeO"]["directionMaxSizeY"][directionxx] == sideAdjacent):
                return True
        
        if (MinoNo == 6):
            if (self.shapeData["shape_info"]["shapeS"]["directionMaxSizeX"][directionxx] == underAdjacent and self.shapeData["shape_info"]["shapeS"]["directionMaxSizeY"][directionxx] == sideAdjacent):
                return True
        
        if (MinoNo == 7):
            if (self.shapeData["shape_info"]["shapeZ"]["directionMaxSizeX"][directionxx] <= underAdjacent and (self.shapeData["shape_info"]["shapeZ"]["directionMaxSizeY"][directionxx] == sideAdjacent)):
                return True
        
        return False

    # ミノと回転数から詳細なミノの回転情報に変換します（デバッグ用）
    def convertShapeDirectionToName(self, MinoNo, direction):
        # ないとは思うが万が一該当しない場合はなしとして返却
        directionDetail = "回転なし"
        
        # ShapeI,ShapeS,ShapeZは2回転で一周
        if (MinoNo == 1 or MinoNo == 6 or MinoNo == 7):
            if (direction == 1):
                directionDetail = "右に一回回転"
                return directionDetail
        
            if (direction == 2):
                directionDetail = "回転なし"
                return directionDetail
        
        # ShapeL,ShapeJ,ShapeTは4回転で一周
        if (MinoNo == 2 or MinoNo == 3 or MinoNo == 4):
            if (direction == 1):
                directionDetail = "右に一回回転"
                return directionDetail
        
            if (direction == 2):
                directionDetail = "回転なし"
                return directionDetail
        
        # ShapeTは何回転しても一周（最初に例外的にない場合を書いている都合上一応条件分岐として書いておく）
        if (MinoNo == 4):
            if (direction == 1):
                directionDetail = "右に一回回転"
                return directionDetail
        
            if (direction == 2):
                directionDetail = "右に二回回転"
                return directionDetail
            
            if (direction == 3):
                directionDetail = "右に三回回転"
                return directionDetail
        
            if (direction == 4):
                directionDetail = "回転なし"
                return directionDetail
    
        return directionDetail

    def nextBoardCalc(self, board, GameStatus, preDirection, preX):
        
        editBoard = self.editBoard(board)
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        count = 0
        
        for direction0 in NextShapeDirectionRange:
                        
            # search with x range
            x0Min, x0Max = self.getSearchXRange(self.NextShape_class, direction0)
            #print("最小値:" + str(x0Min + 1) + "最大値:" + str(x0Max))
            for x0 in range(x0Min + 1, x0Max):
                count = count + 1
                # get board data, as if dropdown block
                board = self.getBoard(editBoard, self.NextShape_class, direction0, x0)                
                print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")                
                print("評価番号" + str(count - 1) + "について")
                print("次のミノは" + self.convertShapeNumToName(GameStatus["block_info"]["nextShape"]["index"]) + "で回転数は" + str(direction0 + 1) + "で今のx座標の位置" + str(x0))
                print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
                print("\n")
                                
                Ground, Adjacent, UnderAdjacent, MaxHeight, ClosedWall = self.calcContactArea2(board)
                
                # 対象データをデータリストに退避（後で評価として利用する）
                arr = np.array([])
                arr = np.append(arr, np.array(UnderAdjacent))
                arr = np.append(arr, np.array(Adjacent))
                arr = np.append(arr, np.array(Ground))
                arr = np.append(arr, np.array(MaxHeight))
                arr = np.append(arr, np.array(ClosedWall))
                arr = np.append(arr, np.array(preDirection))
                arr = np.append(arr, np.array(preX)) 
                arr = np.append(arr, np.array(direction0))
                arr = np.append(arr, np.array(x0))               
                self.CalcDataList = np.append(self.CalcDataList, np.array([arr]), axis=0)
                #print(CalcDataList)
        
        return 

    # 現在の盤面をデバッグ向けとして表示します（デバッグ用）
    def debugBoard(self, board):
        
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
             
        widthInfo = ""
            
        for y in range(0, height, 1):            
            for x in range(0, width, 1):
                widthInfo = widthInfo + " " + str(board[y * self.board_data_width + x])
            widthInfo = widthInfo + "\r\n"
        
        #print(str(widthInfo))       
        return widthInfo
    
    # 現在の盤面から周囲のブロックで空白ができているか確認する
    def checkBoard(self, board): 
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
            
        for y in range(0, height, 1): 
            # 一番左列は壁扱いとする           
            for x in range(1, width - 1, 1):
                if (x == 1):
                    # 二列目のみ右と上をチェック
                    if (board[(y) * self.board_data_width + x + 1 ] == 0 and board[(y + 1) * self.board_data_width + x ] == 0):
                        return True
                if (x == width - 1):
                    # 一番右列のみ左と上をチェック
                    if (board[(y) * self.board_data_width + x - 1 ] == 0 and board[(y + 1) * self.board_data_width + x ] == 0):
                        return True
                else:
                    # 右、左、上をチェック
                    if (board[(y) * self.board_data_width + x - 1 ] == 0 and board[(y) * self.board_data_width + x + 1 ] == 0 and board[(y + 1) * self.board_data_width + x ] == 0):
                        return True
        return False
    
    # 空白が3つ以上あるかどうか確認する
    def shapeIsetCheck(self, board, openCol): 
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
        #print("width" + str())
        xx = 0
        
        # 複数候補があったらなるべく右側の方に配置する（左は段で積みたいため）
                    
        for y in range(height - 1, 0 , -1): 
            # 一番左列は壁扱いとする           
            for x in range(openCol, width, 1):
                '''
                print("左上1:" + str((y) * self.board_data_width + x - 1 )  + "値:" +  str(board[(y) * self.board_data_width + x - 1]))
                print("左上2:" + str((y - 1) * self.board_data_width + x - 1 )  + "値:" + str( board[(y - 1) * self.board_data_width + x - 1]))
                print("左上3:" + str((y - 2) * self.board_data_width + x - 1 )  + "値:" + str( board[(y - 2) * self.board_data_width + x - 1]))
                
                print("空白1:" + str((y) * self.board_data_width + x )  + "値:" + str( board[(y) * self.board_data_width + x]))
                print("空白2:" + str((y - 1) * self.board_data_width + x )  + "値:" + str( board[(y - 1) * self.board_data_width + x]))
                print("空白3:" + str((y - 2) * self.board_data_width + x )  + "値:" + str( board[(y - 2)  * self.board_data_width + x]))
                
                print("右上1:" + str((y) * self.board_data_width + x + 1 )  + "値:" + str( board[(y) * self.board_data_width + x + 1 ]))
                print("右上2:" + str((y - 1) * self.board_data_width + x + 1 )  + "値:" + str( board[(y - 1) * self.board_data_width + x + 1 ]))
                print("右上3:" + str((y - 2) * self.board_data_width + x + 1 )  + "値:" + str( board[(y - 2) * self.board_data_width + x + 1 ]))
                '''
                #print("xの値:" + str(x))
                if (x == openCol):
                    # 二列目のみ右と上をチェック
                    if ((board[(y) * self.board_data_width + x + 1 ] != 0 and board[(y - 1) * self.board_data_width + x + 1 ] != 0 and board[(y - 2) * self.board_data_width + x + 1 ] != 0) and (board[(y) * self.board_data_width + x] == 0 and board[(y - 1) * self.board_data_width + x] == 0 and board[(y - 2) * self.board_data_width + x ] == 0)):
                        xx = x
                if (x == width - 1):
                    # 一番右列のみ左と上をチェック
                    if ((board[(y) * self.board_data_width + x - 1 ] != 0 and board[(y - 1) * self.board_data_width + x - 1 ] != 0 and board[(y - 2) * self.board_data_width + x - 1 ] != 0) and (board[(y) * self.board_data_width + x] == 0 and board[(y - 1) * self.board_data_width + x] == 0 and board[(y - 2) * self.board_data_width + x ] == 0)):
                        xx = x
                else:
                    # 右、左、上をチェック
                    if ((board[(y) * self.board_data_width + x + 1 ] != 0 and board[(y - 1) * self.board_data_width + x + 1 ] != 0 and board[(y - 2) * self.board_data_width + x + 1 ] != 0)  and (board[(y) * self.board_data_width + x - 1 ] != 0 and board[(y - 1) * self.board_data_width + x - 1 ] != 0 and board[(y - 2) * self.board_data_width + x - 1 ] != 0) and (board[(y) * self.board_data_width + x] == 0 and board[(y - 1) * self.board_data_width + x] == 0 and board[(y - 2) * self.board_data_width + x ] == 0)):
                        xx = x
        return xx
    
    # 現在の盤面で空白が周囲の壁で埋まっているかチェックする
    def replaceBlankSpace(self, board, openCol): 
        
        print("置き換え盤面チェック")
        print("置き換え前")
        print(self.debugBoard(board))
        
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
        repBoard = board
        replaceFl = 0
        arr = []
        
        # 指定した消せる列をチェック   
        for y in range(height - 1, 0 , -1): 
            #print("y座標チェック" + str(y + 1))
            for x in range(openCol, width, 1):
                #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                
                if ((y == height - 1)  or (((y < height - 1) and board[(y) * width + x]) != 0)):
                    #print("条件分岐入っている")
                    
                    if ((y - 1) * width + x < 0):
                        break
                    
                    # 一個上が壁なら見る必要はないので無視
                    if ((y < height - 1) and board[(y - 1) * width + x]) != 0:
                        continue
                    else:
                        #床が空白だったら自分も含める
                        yy = y
                        yyy = yy - 1
                        if board[(y) * width + x] != 0:
                            #print("y座標チェック" + str(y + 1))
                            #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                            #print("床が空白ではない")
                            yy -= 1   
                            yyy -= 1
                        arr.append((yy) * width + x)
                        #一個上が壁でない場合は、さらに上を見ていって壁があれば空白が壁で埋まっていると判断
                        for y0 in range(yyy, 0 , -1):
                            #print("yyy座標チェック" + str(x) + "インデックス" + str((y0) * width + x))
                            if (board[(y0) * width + x]) != 0:
                                
                                
                                for i in range(0, len(arr), 1):
                                    # 壁を埋めて初期化する
                                    #print(str(arr[0]))
                                    #print(str(arr[1]))
                                    #print("添字" + str(i))
                                    #print(str(board[1]))
                                    #print(str(repBoard))
                                    #testNum = int(arr2[i])
                                    #print(testNum)
                                    #print(str(arr))
                                    #print(str(arr))
                                    if (repBoard[arr[i]] == 9):
                                        continue
                                    replaceFl = 1
                                    repBoard[arr[i]] = 9
                            else:
                                # 埋める候補のインデックス番号を追加する
                                arr.append((y0) * width + x)
                                # 置き換えた場合は削除モードにして積極的に消しに行く
                                #self.delete = 1
                        #初期化
                        
                        arr = []
                                            
        print("置き換え後")
        print(self.debugBoard(repBoard))
                                                
        if (replaceFl == 1):
            self.replace = 1
            return repBoard
                        
        return board
         
    # 現在の盤面から列消しできるか判定する
    def checkDeleteLine(self, board, openCol, checkLineNum): 
        
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
        
        print("デリート前チェック")
        print(str(self.debugBoard(board)))
         
        # 指定した消せる列をチェック   
        for y in range(height - 1, height - 1 - checkLineNum , -1):     
            for x in range(openCol, width, 1):
                #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                #print("y座標チェック" + str(y) + "インデックス" + str((y) * width + x))
                if (board[(y) * width + x]) == 0:
                    
                    return False
        return True
    
    
    # 盤面の最大埋まっている列数を取得
    def maxFullLine(self, board, openCol): 
        
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
        rowCount = 0
        rowFl = 0
        
        print("デリート前チェック")
        print(str(self.debugBoard(board)))
         
        # 指定した消せる列をチェック   
        for y in range(height - 1, 0, -1): 
            rowFl = 0   
            for x in range(openCol, width, 1):
                #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                #print("y座標チェック" + str(y) + "インデックス" + str((y) * width + x))
                if (board[(y) * width + x]) == 0:
                    rowFl = 1
                    break
            
            if (rowFl == 0):
                rowCount += 1
                       
        return rowCount
    
    # 現在の盤面から何列消せるかを判定する
    def checkDeleteLineNum(self, board): 
        
        deleteLineNum = 0
        deleteLineFl = 0
        nowMinoFl = 0
        
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
         
        # 全部埋まっていたら消せると判断する
        for y in range(0,height, 1): 
            #print("yループ" + str(y))    
            for x in range(0, width, 1):
                #print("x座標チェック" + str(x) + "インデックス" + str((y) * width + x))
                #print("y座標チェック" + str(y) + "インデックス" + str((y) * width + x))
                if (board[(y) * width + x]) == 0:
                    #print("終了ーーーー" + str(board[(y) * width + x]))
                    deleteLineFl = 1
                    #print("フラグ" + str(deleteLineFl))
                    break
                
                if (board[(y) * width + x]) != 9 and  (board[(y) * width + x]) != 0:
                    nowMinoFl = 1
            # ライン消し可能かつ壁とミノの両方が含まれる場合で判断する    
            if (deleteLineFl != 1 and nowMinoFl == 1):
                    deleteLineNum += 1
                    #print("削除ライン数" + str(deleteLineNum))
            deleteLineFl = 0
            nowMinoFl = 0            
        return deleteLineNum

    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = self.board_data_width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board
    
    #差し込みアリのパターン
    def dropDown2(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        dy0 = self.board_data_height
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        print("回転後のミノの形を表す座標" + str(list((self.getShapeCoordArray(Shape_class, direction, x, 0)))))
        # update dy
        #↓このfor文にて配置するy座標の値を決めているっぽい
        count = 0
        
        # ↓について判定方法がよくないので、改修する        
        _yy = 0
       
        for y in range(0 , dy0, 1):
            count += 1
            wallFl = 0
            #print("列数は" + str(count) + "列目")
            for r in range (0, len(list(self.getShapeCoordArray(Shape_class, direction, x, 0))), 1):
                _x = list(list(self.getShapeCoordArray(Shape_class, direction, x, 0))[r])[0]
                _y = list(list(self.getShapeCoordArray(Shape_class, direction, x, 0))[r])[1]
                #print("ーーーーーーーーーーーーーーーーーー")
                #print(str(y) + "tttt" + str(r))
                #print(y * self.board_data_width + _x + 1)
                #print("ーーーーーーーーーーーーーーーーーー")
                # 盤面内の場合のみ判定対象とする
                #print("評価するブロック座標" + str(list(self.getShapeCoordArray(Shape_class, direction, x, 0))[r]) +"で判定対象インデックス番号" + str((y + _y) * self.board_data_width + _x ))
                
                # 盤面が降ってくる上の場合は盤面内ということにして一旦無視する(たぶんそんな状態の場合はゲームオーバーなので…)
                if ((y + _y) * self.board_data_width + _x + 1 < 0):
                    continue
                
                if (len(board) >= (y + _y) * self.board_data_width + _x + 1):
                    #print("ーーーーーーーーーー盤面内のみ判定")
                    if (board[((y + _y)) * self.board_data_width + _x] != self.ShapeNone_index):
                        #壁があったらアウト
                        wallFl += 1
                        #print("盤面内判定結果" + str(wallFl))
                        break
                else:
                    #盤面外は壁扱い
                    #print("ーーーーーーーーーー判定対象外")
                    wallFl += 1
                    #print("判定結果" + str(wallFl))
                    break
            
            #print("最終的な判定結果" + str(wallFl))
            # ミノに対しすべて空白であればそこは配置できるとしてy座標を設定する
            if wallFl < 1:
                _yy = y
                
            #print("現在の列" + str(_yy + 1))
        
        # もし床より上に配置できる場合は、その列として配置する
        if _yy < dy:
            dy = _yy        
                
        '''
        for _x, _y in coordArray:
            print("ループ回数は" + str(count) + "回目で" + "xの値は" + str(_x)  + "でyの値は" + str(_y))
            count = count + 1
            _yy = 0
            # ここで配置できるy座標を決めている（この条件をいじって差込できるようにする）
            # whileだとブロックの下にあった場合の想定がされていない
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                print("_yyは" + str(_yy))
                _yy += 1
            print("ここまで")
            _yy -= 1
            # もし床より上に配置できる場合は、その列として配置する
            if _yy < dy:
                dy = _yy
        '''
        
        # get new board
        #print("dropDown側の座標取得処理終了")
        #print("配置するy座標の値" + str(dy))
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        #print("ミノの座標を取得")
        #print(list(self.getShapeCoordArray(Shape_class, direction, x, 0)))
        #print("-----------------------------------------------")
        count = 0
        for _x, _y in coordArray:
            count = count + 1
            #ここではすでに取得した落ちる場所を配置しているだけ
            #print("配置するインデックス番号" + str((_y + dy) * self.board_data_width + _x))
            #print("ループ回数" + str(count) + "回目:" + "xは" + str(_x) + "でyは" + str(_y) + "で列数は" + str(dy))
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board
     
    def editBoard(self, board):
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
        
        # 盤面の最大高さを求める
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] != 0:
                    # すでに盤面にミノがあれば特殊壁に加工する
                    board[y * self.board_data_width + x] = 9
                        
        return board   
    
    
    def insertWall(self, board, openCol): 
        
        width = self.board_data_width
        height = self.board_data_height
        
        for y in range(0, height, 1):           
            for x in range(0, openCol, 1):
                board[y * width + x] = 9
        
        return board 

    
    #以下、評価に必要な情報を取得する
    # 床に対して空白が何個あるか？
    # 下面に対して壁が何個あるか？
    # 左面に対して壁が何個あるか？
    # ベースは左側に平積みしていくように組み込む。その際に、一度置いたブロックはすべて壁とみなして
    # 床の残り空白数、下面の壁に面する数、左面の壁に面する数を抽出し、それを評価軸にしていく   
    def calcContactArea2(self, board0, minoIndex):   
        
        #print("ボードーーーーーーーーーーーーーー" + str(board))       
        #print(str(board))
        
        # 縦横の数を抽出
        width = self.board_data_width
        height = self.board_data_height
        xNum = self.openCol
            
        tmnpGround = 100
        tmpAdjacent = 100
        tmpRow = 0
         #print(board)
        groundChkFl = 0
        ground = 0
        secGround = 0
        adjacent = 0
        underAdjacent = 0
        
        groundXFl = 1 
        rowAllLine = 0
        firstGround = 0
        closedWall = 0
        deleteLineNum = 0
        underSpace = 0
        
        #最大高さ
        maxHeight = 0
        
        #print("削除モードか確認する" + str(self.delete))
        
        # 左端は壁扱いにする 
        if (self.delete == 0 and self.openCol > 0):
            board = self.insertWall(board0, self.openCol)
        else:
            # 削除モードの場合は左端含めて評価
            xNum = 0
            board = board0
            
        #print(self.debugBoard(board0))  
               
        # 盤面の最大高さを求める
        for y0 in range(height - 1, 0, -1):
            #print("隣接数テスト" + str(width))
            # each x line
            #print("隣接数テスト" + str(y))
            #print(str(y) + "列")
            maxHeightFl = 0
            
            for x in range(xNum, width, 1):
                # 何かしらのブロックがあったらそれを最大高さとして評価する
                #print (str(y * self.board_data_width + x) + "について高さーーーーーーーーーーーーーーーーーーーーーーーー") 
                if board[y0 * self.board_data_width + x ] != 0:
                    #print("値ーーーーーーーーーーーーーーーーーーーーー" + str(board[y0 * self.board_data_width + x ]))
                    #print("はいってるよーーーーーーーーーーーーーーーーーーーーーーーー")
                    if (maxHeightFl == 0): 
                        maxHeight = maxHeight + 1
                        maxHeightFl == 1
                        break
        
        
        #print("最大高さ" + str(maxHeight) + "------------------------------------------------------------------------------------------------------------")            
        # 盤面最大高さが求まる
        
        searchY = height - maxHeight
        count = 0
        
        if (self.delete == 1):
            #削除モードの場合は削除可能列数を検索
            deleteLineNum = self.checkDeleteLineNum(board)
        
        # 探索実施
        #print("探索実施しますーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー")      
        for y in range(height - 1, searchY - 1, -1):
            
            #print("探索開始" + str(height - 1) + "ここまで" + str(maxHeight) +"探索数" + str(height - y) + "回目------------------------------------------------------------------------------------------------------------")
            #rint (str(height) + "について高さーーーーーーーーーーーーーーーーーーーーーーーー") 
            maxHeightFl = 0
            groundFl = 1
            groundWallFl = 0
            # 床が全部ブロックで埋まっていたら、その列は評価せず次の列へ
            for x in range(xNum, width, 1):
                if (board[y * self.board_data_width + x ] != 9 and board[y * self.board_data_width + x ] != 0):
                    groundWallFl = 1
                #print (str(y * self.board_data_width + x) + "について高さーーーーーーーーーーーーーーーーーーーーーーーー") 
                if board[y * self.board_data_width + x ] == 0:
                    #print("評価しないー")
                    groundFl = 0
                    break
                          
            if (groundFl == 1 and groundWallFl == 0):
                continue
            
            for x0 in range(xNum, width, 1):
                # 残り床数をカウントする(床の接地面の列のみ)
              if board[y * self.board_data_width + x0 ] == 0:
                  #print ("色々と値出してみる" + str(x0) + "aaaa" + str(xNum) + str(ground) + "残り床数ーーーーーーーーーーーーーーーーーーーーーーーー")        
                  if (count < 1):
                       ground = ground + 1
                   
              if (self.delete == 0):                              
                # 自身の左側に特殊壁があるかどうかを確認する
                #print (str(y * self.board_data_width + x + 1) + "について壁ーーーーーーーーーーーーーーーーーーーーーーーー" )        
                if len(board) >= y * self.board_data_width + x0 + 1:
                    
                    # 自分が空白で両サイドが壁なら即アウト
                    # if (x0 > 2 and board[y * self.board_data_width + x0 - 1]  == 0 and board[y * self.board_data_width + x0] != 0 and board[y * self.board_data_width + x0 -2] != 0):
                    #     break
                    
                    if ((board[y * self.board_data_width + x0]  != 9 and board[y * self.board_data_width + x0]  != 0) and board[y * self.board_data_width + x0 - 1] == 9):
                        adjacent = adjacent + 1
                        #print ("壁ーーーーーーーーーーーーーーーーーーーーーーーー" + str(adjacent)) 

                # 自身の下側に特殊壁があるかどうかを確認する（これは床との接地面について判定を行うために必要）
                if (board[(y) * self.board_data_width + x0 ] == minoIndex):         
                    if len(board) > (y + 1) * self.board_data_width + x0:     
                            if ((board[y * self.board_data_width + x0]  != 9 and board[y * self.board_data_width + x0]  != 0) and board[(y + 1) * self.board_data_width + x0 ] == 9):
                                underAdjacent = underAdjacent + 1 
                    else:
                            # 盤面外なら下壁として扱う
                            if ((board[y * self.board_data_width + x0]  != 9 and board[y * self.board_data_width + x0]  != 0)):
                                underAdjacent = underAdjacent + 1 
                    
                    # ブロックを置いたときに自分の下に隙間があるかどうかを確認する          
                    if len(board) > (y + 1) * self.board_data_width + x0:     
                            if (board[(y + 1) * self.board_data_width + x0 ] != minoIndex and board[(y + 1) * self.board_data_width + x0 ] != 9 and board[(y + 1) * self.board_data_width + x0 ] == 0):
                                print("チェックするーーーーーーーー")
                                underSpace = 1 
                    else:
                            # 盤面外なら下壁として扱う
                            if ((board[y * self.board_data_width + x0]  != minoIndex and board[y * self.board_data_width + x0]  != 9 and board[y * self.board_data_width + x0]  != 0)):
                                print("チェックするーーーーーーーー盤面外")
                                underSpace = 1 
                                
                # 隙間があるか確認（自身を空白として、左、右、真上があれば塞がっていると判断。その瞬間、評価の対象外にする）
                #print(y * self.board_data_width + x0 + 1)
                #print("左端" + str(xNum) + "現在のループ" + str(x0))
                # ループのはじめ（左端）、ループ中（真ん中）、ループの終わり（右端）で処理を分岐
                
                if (x0 == xNum):
                    # 左端の場合
                    if ((board[y * self.board_data_width + x0] == 0 and board[y * self.board_data_width + x0 + 1]  != 0 and board[(y - 1) * self.board_data_width + x0 ]  != 0)):
                        closedWall = 1    
                elif (x0 == width - 1):
                    # 右端の場合
                    if ((board[y * self.board_data_width + x0] == 0 and board[y * self.board_data_width + x0 - 1]  != 0 and board[(y - 1) * self.board_data_width + x0 ]  != 0)):
                        closedWall = 1
                else:
                    if ((board[y * self.board_data_width + x0] == 0 and board[y * self.board_data_width + x0 + 1]  != 0 and board[y * self.board_data_width + x0 - 1]  != 0 and board[(y - 1) * self.board_data_width + x0 ]  != 0)):
                        closedWall = 1              
                                                   
            count = count + 1
        
        
        # 床と現在の回転のミノの床接地最大数を比較する
        
                    
        print ("最大高さーーーーーーーーーーーーーーーーーーーーーーーー" + str(maxHeight))            
        print ("残り床数ーーーーーーーーーーーーーーーーーーーーーーーー" + str(ground))
        print ("接地壁数(左)ーーーーーーーーーーーーーーーーーーーーーーーー" + str(adjacent) )
        print ("接地壁数(下)ーーーーーーーーーーーーーーーーーーーーーーーー" + str(underAdjacent) ) 
        print ("壁が埋まっているかどうかーーーーーーーーーーーーーーーーーーーーーーーー" + str(closedWall) )  
        print ("削除モードの場合に何列消せるかーーーーーーーーーーーーーーーーーーーーーーーー" + str(deleteLineNum) )  
        print("\n")
        
        #盤面情報
        print(self.debugBoard(board))  
               
        return ground, adjacent, underAdjacent, maxHeight, closedWall, deleteLineNum, underSpace

    def calcEvaluationValueSample(self, board):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height
        
        #print("隣接数テスト" + str(width))

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## number of holes or blocks in the line.
        nHoles, nIsolatedBlocks = 0, 0
        ## absolute differencial value of MaxY
        absDy = 0
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width

        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                #print("隣接数テスト" + str(x))
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    hasHole = True
                    holeCandidates[x] += 1  # just candidates in each column..
                else:
                    # block
                    hasBlock = True
                    BlockMaxY[x] = height - y                # update blockMaxY
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column..
                        holeCandidates[x] = 0                # reset
                    if holeConfirm[x] > 0:
                        nIsolatedBlocks += 1                 # update number of isolated blocks

            if hasBlock == True and hasHole == False:
                # filled with block
                fullLines += 1
            elif hasBlock == True and hasHole == True:
                # do nothing
                pass
            elif hasBlock == False:
                # no block line (and ofcourse no hole)
                pass

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            absDy += abs(x)

        #### maxDy
        #maxDy = max(BlockMaxY) - min(BlockMaxY)
        #### maxHeight
        #maxHeight = max(BlockMaxY) - fullLines

        ## statistical data
        #### stdY
        #if len(BlockMaxY) <= 0:
        #    stdY = 0
        #else:
        #    stdY = math.sqrt(sum([y ** 2 for y in BlockMaxY]) / len(BlockMaxY) - (sum(BlockMaxY) / len(BlockMaxY)) ** 2)
        #### stdDY
        #if len(BlockMaxDy) <= 0:
        #    stdDY = 0
        #else:
        #    stdDY = math.sqrt(sum([y ** 2 for y in BlockMaxDy]) / len(BlockMaxDy) - (sum(BlockMaxDy) / len(BlockMaxDy)) ** 2)


        # calc Evaluation Value
        score = 0
        score = score + fullLines * 10.0           # try to delete line 
        score = score - nHoles * 1.0               # try not to make hole
        score = score - nIsolatedBlocks * 1.0      # try not to make isolated block
        score = score - absDy * 1.0                # try to put block smoothly
        #score = score - maxDy * 0.3                # maxDy
        #score = score - maxHeight * 5              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        # print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, stdY, stdDY, absDy, BlockMaxY)
        return score


BLOCK_CONTROLLER = Block_Controller()
