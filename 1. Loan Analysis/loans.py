import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
import csv
import urllib.request, json 
with urllib.request.urlopen("https://github.com/cs320-wisc/f22/raw/main/p2/banks.json") as url:
    bank = json.load(url)
    
    
    
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}      
           
class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            try:
                self.race.add(race_lookup[r])
            except (KeyError, AssertionError):
                continue
    def __repr__(self):
        return f"Applicant('{str(self.age)}', {list(self.race)})"
    

    def lower_age(self):
        age = self.age.replace('<','')
        age = age.replace('>','')
        x = age.split('-')
        y = min(x)
        return int(y)
    
    def __lt__(self, other):
        if self.lower_age() < other.lower_age():
            return True
        else:
            return False



class Loan:
    def __init__(self, values):
        if values["loan_amount"] == "NA" or values["loan_amount"] == "Exempt":
            values["loan_amount"] = -1
        if values["property_value"] == "NA" or values["property_value"] == "Exempt":
            values["property_value"] = -1
        if (values["interest_rate"] == "NA") or (values["interest_rate"] == "Exempt"):
            values["interest_rate"] = -1
            # attributes self.xxx
        self.loan_amount = float(values["loan_amount"])
        self.property_value = float(values["property_value"])
        self.interest_rate = float(values["interest_rate"]) 

        ethnicity = (values[x] for x in values if ('applicant_race' in x) and ("co-"not in x) and ("observed" not in x))
        if values["co-applicant_age"] != "9999":
            co_ethnicity = (values[x] for x in values if ('co-applicant_race' in x))
            self.applicants = [Applicant(values["applicant_age"], ethnicity), Applicant(values["co-applicant_age"], co_ethnicity)]
        else:
            self.applicants = [Applicant(values["applicant_age"], ethnicity)]
    
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        amt = self.loan_amount
        rate = self.interest_rate
        assert amt > 0
        assert rate > 0
        while amt > 0:
            yield amt
            amt += ((rate/100) * amt)
            amt -= yearly_payment
   
            
            
class Bank:
    def __init__(self, name):
        for i in bank:
            if name in i["name"]:
                self.lei = i["lei"]
                self.name = i["name"]
                self.count = i["count"]
                self.period = i["period"]
                self.loans = []
        with ZipFile('wi.zip') as zf:
            with zf.open("wi.csv", "r") as f:
                tio = TextIOWrapper(f)
                theta = csv.DictReader(tio)
                for x in theta:
                    if self.lei == x["lei"]:
                        alpha = Loan(x)
                        self.loans.append(alpha)
                     
    def __len__(self):
        return len(self.loans)
    def __getitem__(self, integer):
        return self.loans[integer]            