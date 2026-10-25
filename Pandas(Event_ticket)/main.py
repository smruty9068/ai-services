import pandas as pd
def load_ticket_sales(file_path):
    ticket__s=pd.read_csv(file_path)
    ticket__s=ticket__s.drop(columns=['sale_date'])
    return ticket__s
def clean_ticket_sales(df):
    df=df.dropna(subset=['buyer_email'])
    df=df.drop_duplicates(subset=['sale_id'],keep='first')
    return df
def merge_with_events(df, ref_file_path):
    events_d=pd.read_csv(ref_file_path)
    df=pd.merge(df,events_d,on='event_id',how='inner')
    return df
def add_net_ticket_value(df):
    df['net_ticket_value']=(df['tickets']*df['ticket_price']*(1-df['discount_pct']/100)).round(2)
    return df
def aggregate_by_category(df):
    df=(df.groupby(['category']).agg(avg_net_ticket_value=('net_ticket_value','mean'), total_net_ticket_revenue=('net_ticket_value','sum'), valid_sale_count=('net_ticket_value','count')).reset_index())
    return df
def finalize_summary(df):
    df['avg_net_ticket_value']= df['avg_net_ticket_value'].round(2)
    df['total_net_ticket_revenue']=df['total_net_ticket_revenue'].round(2)
    df['valid_sale_count']=df['valid_sale_count']
    df=df.sort_values(by='category',ascending=True).reset_index()
    return df
if __name__ == "__main__":
    file_path="data/ticket_sales.csv"
    ref_file_path="data/events.csv"
    d=load_ticket_sales(file_path)
    d1=clean_ticket_sales(d)
    d2=merge_with_events(d1,ref_file_path)
    d3=add_net_ticket_value(d2)
    d4=aggregate_by_category(d3)
    d5=finalize_summary(d4)
    print(d5)
    #C:\\Users\\10880923\\Desktop\\Pandas(Event_ticket)