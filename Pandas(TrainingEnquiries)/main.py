import pandas as pd
def load_student_enquiries(file_path):
    train_enq=pd.read_csv(file_path)
    train_enq=train_enq.drop(columns=['enquiry_date'])
    return train_enq
def clean_enquiry_data(df):
    df=df.dropna(subset=['email'])
    df=df.drop_duplicates(subset=['enquiry_id'],keep='first')
    return df
def merge_with_courses(train_enq,ref_file_path):
    train_cou=pd.read_csv(ref_file_path)
    mer=pd.merge(train_enq,train_cou,on='course_id',how='inner')
    return mer
def add_net_quoted_fee(df):
    df['net_quoted_fee']=df['quoted_fee']*(1-df['discount_pct']/100).round(2)
    return df
def aggregate_by_course(df):
    df=(df.groupby(['course_id','course_name']).agg(avg_net_quoted_fee=('net_quoted_fee','mean'),enquiry_count=('enquiry_id','count')))
    return df
def finalize_summary(df):
    df['avg_net_quoted_fee']=df['avg_net_quoted_fee'].round(2)
    df=df[['avg_net_quoted_fee','enquiry_count']]
    df=(df.sort_values(by='course_name',ascending=True).reset_index())
    return df


if __name__=='__main__':
    file_path='C:\\Users\\10880923\\Desktop\\Pandas(TrainingEnquiries)\\data\\training_enquiries.csv'
    ref_file_path="C:\\Users\\10880923\\Desktop\\Pandas(TrainingEnquiries)\\data\\training_courses.csv"
    df1=load_student_enquiries(file_path) 
    df2=clean_enquiry_data(df1)
    df3=merge_with_courses(df2,ref_file_path)
    df4=add_net_quoted_fee(df3)
    df5=aggregate_by_course(df4)
    df6=finalize_summary(df5)
    print(df6)