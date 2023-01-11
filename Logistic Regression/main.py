from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.model_selection import cross_val_score



class UserPredictor:
    
    def __init__(self):
        self.model = None
       
    #train
    def fit(self, train_users, train_logs, train_y):
        #cleaning data
        sum_seconds = train_logs.groupby("user_id").sum("seconds").to_dict()["seconds"]
        for i in train_users["user_id"]:
            if i not in sum_seconds:
                sum_seconds[i] = 0
        sum_seconds = dict(sorted(sum_seconds.items()))
        newdf = train_users
        newdf["CountSeconds"] = sum_seconds.values()  
        
        
        count_entries = train_logs.groupby("user_id")["user_id"].count().to_dict()
        for i in train_users["user_id"]:
            if i not in count_entries:
                count_entries[i] = 0
        count_entries = dict(sorted(count_entries.items()))
        newdf["CountIDs"] = count_entries.values()
        
         # setup transform, convert badge to code
        trans = make_column_transformer(
        (OneHotEncoder(), ["badge"]),
        (PolynomialFeatures(1, include_bias = False), ["past_purchase_amt", "age", "CountSeconds", "CountIDs"]),
        ) 
        
        model = Pipeline([
        ("trans", trans),
        ("logistic", LogisticRegression(max_iter = 500))]
        )
        
        self.model = model
        self.xcol = ["badge", "past_purchase_amt", "age", "CountSeconds", "CountIDs"] 
        self.model.fit(newdf[self.xcol], train_y["y"])
        
        scores = cross_val_score(self.model, newdf[self.xcol], train_y["y"])
        print(f"AVG: {scores.mean()}, STD: {scores.std()}\n")
        
    #test    
    def predict(self, test_users, test_logs):
        sum_seconds = test_logs.groupby("user_id").sum("seconds").to_dict()["seconds"]
        for i in test_users["user_id"]:
            if i not in sum_seconds:
                sum_seconds[i] = 0
        sum_seconds = dict(sorted(sum_seconds.items()))
        new_df2 = test_users
        new_df2["CountSeconds"] = sum_seconds.values()
        
        
        count_entries = test_logs.groupby("user_id")["user_id"].count().to_dict()
        for i in test_users["user_id"]:
            if i not in count_entries:
                count_entries[i] = 0
        count_entries = dict(sorted(count_entries.items()))
        test_users["CountIDs"] = count_entries.values()
        
        return self.model.predict(new_df2[self.xcol])