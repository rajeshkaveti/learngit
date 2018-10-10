import pytest
import pandas as pd


def test_student_data():
    #sortedDistance.str[0].to_csv("/Users/adcxdpf/Downloads/pset_03/sd.csv")
    df_2 = pd.read_csv("/Users/adcxdpf/Downloads/pset_03/sd.csv", header = None , usecols=[1])

    df_2_top = df_2[:5]
    actual_top_list = df_2_top[1].tolist()
    print("actual_top_list : ", actual_top_list)

    expected_top_list = [0.0, 0.036405674848454805, 0.037279251584316997, 0.039576056208744936, 0.040040851763060721]


    print(all([a == b for a, b in zip(actual_top_list, expected_top_list)]))
    
