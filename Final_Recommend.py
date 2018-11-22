import numpy as np
import sys

def main(i) :
    DownSum = []
    UpSum = []
    
    with open('Feature/Feature_Up_' + str(i + 1) + '.txt', 'r') as r :
        up_lines = r.readlines()
        for up_line in up_lines :
            UP = up_line.replace("\n", "").split(",")
            del UP[-1]
            UpSum.append(UP)

        r.close()

    with open('datas/data_' + str(i + 1) + '.txt', 'r') as r :
        data = r.read().split(",")
        del data[-1]

    for data_to_int in range(len(data)) :
        data[data_to_int] = int(data[data_to_int])

    with open('Feature/Feature_Down_' + str(i + 1) + '.txt', 'r') as r :
        down_lines = r.readlines()
        for down_line in down_lines :
            DOWN = down_line.replace("\n", "").split(",")
            del DOWN[-1]
            DownSum.append(DOWN)
        r.close()

    for Char_to_int_1 in range(len(DownSum)) :
        for Char_to_int_2 in range(len(DownSum[Char_to_int_1])) :
            DownSum[Char_to_int_1][Char_to_int_2] = int(DownSum[Char_to_int_1][Char_to_int_2])

    for Char_to_int_1 in range(len(UpSum)) :
        for Char_to_int_2 in range(len(UpSum[Char_to_int_1])) :
            UpSum[Char_to_int_1][Char_to_int_2] = int(UpSum[Char_to_int_1][Char_to_int_2])

    DataSumMean = sum(data) / len(data)
    DownSum = np.array(DownSum)
    UpSum = np.array(UpSum)

    print(UpSum)
    print(DownSum)

    DownUpSumMean = int(np.sum(UpSum)) / UpSum.size + int(np.sum(DownSum)) / DownSum.size

    return int(np.sum(DownSum)), int(np.sum(UpSum)), DownUpSumMean, DataSumMean
            
if __name__ == '__main__' :
    Final_Recommend = []
    Data_Means = []
    Up_Down_Means = []
    Final = []
    Final_Val = []
    Final_Val_Bak = []

    Music_dict = {0: "Classic",
                  1: "Blues, Jazz",
                  2: "Church_Music",
                  3: "Pop"}
    
    print("=======================")
    
    for iteration in range(5) :
        Down, Up, DownUpSumMean, DataSumMean = main(iteration)
        
        print("<"+ str(iteration  +1) + ">" )
        print("Down : " + str(Down))
        print("Up : " + str(Up))
        print("")
        print("Data_Mean : " + str(DataSumMean))
        print("Change_Mean : " + str(DownUpSumMean))
        print("=======================")

        Final_Recommend.append([DataSumMean, DownUpSumMean])

    print("<First>")
    print("Data_Mean : " + str(Final_Recommend[0][0]))
    print("Change_Mean : " + str(Final_Recommend[0][1]))
    print("")
    First_Data_Mean = Final_Recommend[0][0]
    First_Change_Mean =  Final_Recommend[0][1]
    del Final_Recommend[0]
    
    for Recommend in range(len(Final_Recommend)) :
        try :
            print("=======================")
            print("<" + Music_dict[Recommend] + ">")
    
        except :     
            print("=======================")
            print("Some Error")
            sys.exit()

        Data_Mean_Change = Final_Recommend[Recommend][0] - First_Data_Mean
        Change_Mean_Change = Final_Recommend[Recommend][1] - First_Change_Mean
        
        print("Data_Mean_Change : " + str(Data_Mean_Change))
        print("Change_Mean_Change : " + str(Change_Mean_Change))
        print("Final_Score : " + str(Data_Mean_Change + Change_Mean_Change))
        Final_Val.append(Data_Mean_Change + Change_Mean_Change)
        
        print("")
        
    for Bak in range(len(Final_Val)) : Final_Val_Bak.append(Final_Val[Bak])
    for Maxs in range(2) :
        print("Recommend_" + str(Maxs + 1) + " : " + Music_dict[Final_Val_Bak.index(max(Final_Val))])
        Final_Val.remove(max(Final_Val))
        

        
                    
                    
