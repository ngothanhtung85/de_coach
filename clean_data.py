import re
import pandas as pd
import sqlalchemy

#df = pd.read_csv("data.csv")

def parse_salary(salary):
    salary = str(salary).lower().strip()
    # Thoả thuận
    if "thoả thuận" in salary:
        return None, None, "VND"
    
    if salary.startswith("trên") or salary.startswith("từ"):
    #    num = re.search(r"(\d+)", salary)
        pattern = r"\d[\d,]*"
        num = re.findall(pattern, salary)
        if num:
            if "triệu" in salary:
                return int(num[0].replace(",", "")), None, "VND"            
            return int(num[0].replace(",", "")), None, "USD"

    # Tới X triệu
    if "tới" in salary:
        pattern = r"\d[\d,]*"
        num = re.findall(pattern, salary)
        if num:
            if "triệu" in salary:
                return int(num[0].replace(",", "")), None, "VND"            
            return int(num[0].replace(",", "")), None, "USD"

    # X - Y triệu
    pattern = r"\d[\d,]*"
    range_match = re.findall(pattern, salary)
    if range_match:
        if "triệu" in salary:
            return int(range_match[0].replace(",", "")), int(range_match[1].replace(",", "")), "VND"
        return int(range_match[0].replace(",", "")), int(range_match[1].replace(",", "")), "USD"
    
    # X triệu 
    pattern = r"\d[\d,]*"
    single_match = re.findall(pattern, salary)
    if single_match:
        val = int(range_match[0].replace(",", ""))
        if "triệu" in salary:
            return val, val, "VND"
        return val, val, "USD"
    
    return None, None, "VND"

def parse_address(address):
    parts = address.split(':')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return address, None

mapping = {
    "developer": "Software Engineer",
    "programer": "Software Engineer",
    "engineer": "Software Engineer",
    "lập trình": "Software Engineer",
    "analyst": "BA",
    "manager": "Project Manager",
    "tester": "Tester"
}

def standardize_job_tittle(title):
    for k, v in mapping.items():
        if k.lower() in title.lower():
            return v
        return title
    
def extract(path="data/data.csv"):
    return pd.read_csv(path)

def transform(df):
    #parse job title 
    df['Group']= df['job_title'].apply(standardize_job_tittle)
    #parse salary
    df[['min_salary', 'max_salary', 'salary_unit']] = df['salary'].apply(lambda x: pd.Series(parse_salary(x)))
    #parse address
    df[['city', 'district']] = df['address'].apply(lambda x: pd.Series(parse_address(x)))
    return df

def load(df):
    #connect MySQL DB
    conn = sqlalchemy.create_engine("mysql+pymysql://system:abc#123@localhost/mysql")
    df.to_sql("job_demand", con=conn, if_exists="append", index=False)

def etl_flow():
    df = extract()
    df = transform(df)
    df.to_csv("clean_data.csv", index=False)
    load(df)
    
if __name__ == "__main__":
    etl_flow()