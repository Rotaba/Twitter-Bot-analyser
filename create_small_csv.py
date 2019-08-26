import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def vrfy_ds(ds):
    # verifying
    print(ds.head())
    print(ds.shape)
    print(ds.dtypes)
    print("Number of 'is_bot' values:", ds.groupby(["output"]).size())
    print(len(cols), cols)



# load dataset_combined.csv
dscb = pd.read_csv("dataset_combined.csv")

# remove IDs and timediffs from df
dscb.drop(axis=0, columns=["time_difference", "X0", "Unnamed: 0"], inplace=True)
# move target_col in the end of df
target_col = "output"   # output / is_bot
cols = list(dscb)
cols.remove(target_col)
cols.append(target_col)
dscb = dscb.ix[:, cols]

vrfy_ds(dscb)


# select only a sample of 8000 rows
train_amount = 8000
test_amount = int(train_amount / 4)      # number of test samples are one fourth of training samples

ds_train = dscb.iloc[0:train_amount]    # get first train_amount many values
ds_test = dscb.iloc[train_amount:(train_amount + test_amount)]  # get test_amount many values


# verify small shuffled dataset
#print(ds_train.head())
#print("small ds shape:", ds_train.shape)
#print("output values:", ds_train.groupby(["output"]).size())
#print("small ds shape:", ds_test.shape)
#print("output values:", ds_test.groupby(["output"]).size())

# save as .csv file
ds_train.to_csv("8k-0.csv", index=False)
ds_test.to_csv("8k-1.csv", index=False)