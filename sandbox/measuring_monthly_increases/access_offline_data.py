import pandas as pd

_DATA_DIR = './offline_data/'

def access(ticker, date):

    dict_from_csv = pd.read_csv(f'{_DATA_DIR}/{ticker}.txt', header=None, index_col=0, squeeze=True).to_dict()

    return dict_from_csv[date]

def access_range(ticker, start_date, end_date, return_list=False, download=False):

    dict_from_csv = pd.read_csv(f'{_DATA_DIR}/{ticker}.txt', header=None, index_col=0, squeeze=True).to_dict()

    range_dict = {}
    record = False
    closings = []

    if list(dict_from_csv.keys())[0] > start_date: 
        return range_dict

    for key in list(dict_from_csv.keys()):
        if key < start_date and record is False: 
            continue
        elif key >= start_date:
            record = True
        if key >= end_date:
            break
        if record:
            range_dict[key] = dict_from_csv[key]
            closings.append(dict_from_csv[key])

    if return_list:
        return closings
    return(range_dict)



def main():

    print("Unit tests.")
    print(access('AUY', '2020-01-17'))
    print(access_range('AUY', '2020-04-20', '2020-10-17', return_list=False))


if __name__ == '__main__':
    main()