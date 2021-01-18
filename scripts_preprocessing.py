from astropy.io import fits
import pandas as pd
import numpy as np

def main(
        datafile='http://gal-03.sai.msu.ru/~vtoptun/photometry/rcsed_v2_8.fits'):
    
    data = fits.open(datafile)
    
    # converting to dataframe
    data_pd = pd.DataFrame(np.array(data[1].data).byteswap().newbyteorder())
    
    cols = data_pd.columns.to_list()
    
    #drop ID columns
    ID_cols = [s for s in cols if "ID" in s]
    ID_cols.append('recno_uzc')
    ID_cols.append('ind')
    
    data_pd.drop(ID_cols, axis = 1, inplace=True)
    
    #select onnly munerical columnns
    data_pd = data_pd.select_dtypes(include='number')
    
    #delete columns with anomaly and nan values
    data_pd.replace([-2147483648, -9223372036854775808,-32768,255, -999999488.0,
     99.0,
     -99.0,
     9999.0,
     -999.0,
     float('inf'),
     -9999.0], np.nan, inplace=True)
    
    for_del = []

    for c in data_pd.columns:
        if (data_pd[c].isna().sum()/data_pd.shape[0] > 0.5):
            for_del.append(c)
            
    data_pd.drop(for_del, axis=1, inplace=True)
    print('dataframe shape: ', data_pd.shape)

    data_pd.to_csv('../datasets/cleaned_data.csv')

if __name__ == '__main__':
    main()
    
