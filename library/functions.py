def rank_course(mark_exam, total_mark_course, countRankXS=0, countRankG=0, countRankKha=0,
     countRankTBK=0, countRankTB=0,  countRankY=0 ):
    list_rank = dict()
    rank = ""
    if mark_exam>=5:
        if total_mark_course>=9:
            rank = " XS"
            countRankXS =countRankXS+1
        elif (total_mark_course< 9) and (total_mark_course>=8):
            rank = " Giỏi"
            countRankG =countRankG+1
        elif (total_mark_course< 8) and (total_mark_course>=7):
            rank = " Khá"
            countRankKha =countRankKha+1
        elif (total_mark_course< 7) and (total_mark_course>=6):
            rank = " TB-Khá"
            countRankG =countRankG+1
        elif (total_mark_course< 6) and (total_mark_course>=5):
            rank = " TB"
            countRankG =countRankG+1
        elif (total_mark_course< 5) and (total_mark_course>=0):
            rank = "Yếu"
            countRankG =countRankG+1

    list_rank['rank'] = rank
    list_rank['countRankXS'] = countRankXS
    list_rank['countRankG'] = countRankG
    list_rank['countRankKha'] = countRankKha
    list_rank['countRankTBK'] = countRankTBK
    list_rank['countRankTB'] = countRankTB
    list_rank['countRankY'] = countRankY
    return list_rank
def rank_mark(mark):
    rank = ""
   
    if mark>=9:
        rank = " XS"
            
    elif (mark< 9) and (mark>=8):
        rank = " Giỏi"
          
    elif (mark< 8) and (mark>=7):
        rank = " Khá"
            
    elif (mark< 7) and (mark>=6):
        rank = " TB-Khá"
            
    elif (mark< 6) and (mark>=5):
        rank = " TB"
            
    elif (mark< 5) and (mark>=0):
        rank = "Yếu"
           
    return rank